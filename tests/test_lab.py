from prompt_lab.core import PromptLab

def test_versions_and_assignment(tmp_path):
 l=PromptLab(tmp_path/'p.db'); pid=l.create_prompt('x','Hello {{name}}'); v=l.new_version(pid,'Hi {{name}}'); eid=l.experiment('e',pid,[1,v],[50,50]); assert l.assign(eid,'same')==l.assign(eid,'same'); assert 'Hi' in l.render(pid,v,{'name':'A'})

def test_significance(tmp_path):
 l=PromptLab(tmp_path/'p.db'); pid=l.create_prompt('x','x'); v=l.new_version(pid,'y'); eid=l.experiment('e',pid,[1,v],[50,50])
 for i in range(200): l.record(eid,1,f'a{i}',0)
 for i in range(200): l.record(eid,v,f'b{i}',1)
 assert l.results(eid)['winner']==v
