from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from .core import PromptLab,health_summary
app=FastAPI(title='Prompt Experiment Platform'); lab=PromptLab()
class PromptCreate(BaseModel): name:str; template:str; params:dict={}
class VersionCreate(BaseModel): template:str; params:dict={}; message:str='update'
class ExperimentCreate(BaseModel): name:str; prompt_id:int; variants:list[int]; splits:list[float]; metric:str='quality'
class Complete(BaseModel): prompt_id:int; user_id:str; variables:dict; experiment_id:int|None=None
class Metric(BaseModel): user_id:str; variant:int; value:float; error:bool=False
@app.get('/health')
def health():return health_summary()
@app.post('/prompts')
def create(x:PromptCreate):return {'id':lab.create_prompt(x.name,x.template,x.params)}
@app.post('/prompts/{pid}/versions')
def version(pid:int,x:VersionCreate):return {'version':lab.new_version(pid,x.template,x.params,x.message)}
@app.get('/prompts/{pid}/versions')
def versions(pid:int):return lab.versions(pid)
@app.get('/prompts/{pid}/diff')
def diff(pid:int,a:int,b:int):return {'diff':lab.diff(pid,a,b)}
@app.post('/experiments')
def experiment(x:ExperimentCreate):return {'id':lab.experiment(x.name,x.prompt_id,x.variants,x.splits,x.metric)}
@app.post('/v1/completions')
def completion(x:Complete):
 version=lab.assign(x.experiment_id,x.user_id) if x.experiment_id else lab.db.execute('select active_version from prompts where id=?',(x.prompt_id,)).fetchone()[0]
 prompt=lab.render(x.prompt_id,version,x.variables); return {'variant':version,'prompt':prompt,'output':f'Demo response for: {prompt}'}
@app.post('/experiments/{eid}/metrics')
def metric(eid:int,x:Metric):lab.record(eid,x.variant,x.user_id,x.value,x.error);return {'ok':True}
@app.get('/experiments/{eid}/results')
def results(eid:int):return lab.results(eid)

@app.post('/experiments/{eid}/promote')
def promote(eid:int,actor:str='admin'):return lab.promote_winner(eid,actor)
