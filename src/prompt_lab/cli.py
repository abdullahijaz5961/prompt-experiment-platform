import argparse,random
from .core import PromptLab

def main():
 p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True); v=s.add_parser('serve'); v.add_argument('--host',default='127.0.0.1'); v.add_argument('--port',type=int,default=8609); s.add_parser('seed')
 a=p.parse_args()
 if a.cmd=='serve': import uvicorn; uvicorn.run('prompt_lab.api:app',host=a.host,port=a.port)
 else:
  l=PromptLab(); pid=l.create_prompt('support-summary','Summarise this ticket for {{user_name}}: {{context}}'); v2=l.new_version(pid,'Create a concise support summary for {{user_name}}: {{context}}','{}','clearer instruction'); eid=l.experiment('concise-summary',pid,[1,v2],[50,50])
  for i in range(300):
   v=l.assign(eid,str(i)); l.record(eid,v,str(i),1 if random.random() < (.72 if v==1 else .82) else 0)
  print({'prompt_id':pid,'experiment_id':eid,**l.results(eid)})
