from __future__ import annotations
import hashlib,json,math,sqlite3,time
from pathlib import Path
from string import Template

class PromptLab:
 def __init__(self,path='runtime/prompts.db'):
  Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path,check_same_thread=False); self.db.row_factory=sqlite3.Row; self.init()
 def init(self):
  self.db.executescript('''create table if not exists prompts(id integer primary key,name text unique,active_version integer); create table if not exists versions(id integer primary key,prompt_id integer,version integer,template text,params text,message text,created real); create table if not exists experiments(id integer primary key,name text,prompt_id integer,variants text,splits text,metric text,status text,created real); create table if not exists events(id integer primary key,experiment_id integer,variant integer,user_id text,value real,error integer,created real); create table if not exists audit(id integer primary key,action text,details text,created real);'''); self.db.commit()
 def create_prompt(self,name,template,params=None,message='initial version'):
  cur=self.db.execute('insert into prompts(name,active_version) values(?,1)',(name,)); pid=cur.lastrowid; self.db.execute('insert into versions(prompt_id,version,template,params,message,created) values(?,?,?,?,?,?)',(pid,1,template,json.dumps(params or {}),message,time.time())); self.db.commit(); return pid
 def new_version(self,pid,template,params=None,message='update'):
  v=self.db.execute('select coalesce(max(version),0)+1 from versions where prompt_id=?',(pid,)).fetchone()[0]; self.db.execute('insert into versions(prompt_id,version,template,params,message,created) values(?,?,?,?,?,?)',(pid,v,template,json.dumps(params or {}),message,time.time())); self.db.commit(); return v
 def activate(self,pid,version,actor='admin',reason='manual activation'):
  self.db.execute('update prompts set active_version=? where id=?',(version,pid)); self.db.execute('insert into audit(action,details,created) values(?,?,?)',('activate',json.dumps({'prompt_id':pid,'version':version,'actor':actor,'reason':reason}),time.time())); self.db.commit()
 def versions(self,pid): return [dict(r) for r in self.db.execute('select * from versions where prompt_id=? order by version',(pid,))]
 def diff(self,pid,a,b):
  va=self.db.execute('select template from versions where prompt_id=? and version=?',(pid,a)).fetchone()[0]; vb=self.db.execute('select template from versions where prompt_id=? and version=?',(pid,b)).fetchone()[0]
  import difflib; return ''.join(difflib.unified_diff(va.splitlines(True),vb.splitlines(True),fromfile=str(a),tofile=str(b)))
 def experiment(self,name,pid,variants,splits,metric='quality'):
  if abs(sum(splits)-100)>0.01: raise ValueError('Traffic splits must sum to 100')
  cur=self.db.execute('insert into experiments(name,prompt_id,variants,splits,metric,status,created) values(?,?,?,?,?,?,?)',(name,pid,json.dumps(variants),json.dumps(splits),metric,'running',time.time())); self.db.commit(); return cur.lastrowid
 def assign(self,eid,user_id):
  e=self.db.execute('select variants,splits from experiments where id=?',(eid,)).fetchone(); variants=json.loads(e[0]); splits=json.loads(e[1]); bucket=int(hashlib.sha256(f'{eid}:{user_id}'.encode()).hexdigest(),16)%10000/100
  total=0
  for v,s in zip(variants,splits): total+=s; 
  # deterministic selection
  total=0
  for v,s in zip(variants,splits):
   total+=s
   if bucket<total:return v
  return variants[-1]
 def render(self,pid,version,variables):
  row=self.db.execute('select template from versions where prompt_id=? and version=?',(pid,version)).fetchone();
  if not row: raise KeyError('Version not found')
  return Template(row[0].replace('{{','$').replace('}}','')).substitute(variables)
 def record(self,eid,variant,user_id,value,error=False): self.db.execute('insert into events(experiment_id,variant,user_id,value,error,created) values(?,?,?,?,?,?)',(eid,variant,user_id,value,int(error),time.time())); self.db.commit()
 def results(self,eid):
  rows=self.db.execute('select variant,count(*) n,avg(value) mean,avg(error) error_rate from events where experiment_id=? group by variant',(eid,)).fetchall(); data=[dict(r) for r in rows]
  if len(data)<2:return {'variants':data,'winner':None,'significant':False}
  if any((x['error_rate'] or 0)>.20 for x in data):
   self.db.execute('update experiments set status=\'cancelled\' where id=?',(eid,)); self.db.commit()
   return {'variants':data,'winner':None,'significant':False,'auto_stopped':True,'reason':'error rate exceeded 20%'}
  a,b=data[0],data[1]; se=math.sqrt((a['mean']*(1-a['mean'])/max(1,a['n']))+(b['mean']*(1-b['mean'])/max(1,b['n']))) if 0<=a['mean']<=1 and 0<=b['mean']<=1 else math.sqrt(1/max(1,a['n'])+1/max(1,b['n']))
  z=(float('inf') if se==0 and a['mean']!=b['mean'] else abs(a['mean']-b['mean'])/(se or 1)); significant=z>=1.96; winner=max(data,key=lambda x:x['mean'])['variant'] if significant else None
  return {'variants':data,'z_score':round(z,3),'significant':significant,'winner':winner}

 def promote_winner(self,eid,actor='admin'):
  result=self.results(eid)
  if not result.get('winner'): raise ValueError('No statistically significant winner')
  row=self.db.execute('select prompt_id from experiments where id=?',(eid,)).fetchone();self.activate(row[0],result['winner'],actor,'experiment winner');self.db.execute('update experiments set status=\'completed\' where id=?',(eid,));self.db.commit();return result

def health_summary(): return {'status':'ok','project':'Prompt Experiment Platform'}
