import os, tempfile
from pathlib import Path
from fastapi.testclient import TestClient

def test_banking_workflows():
 with tempfile.TemporaryDirectory() as root:
  os.environ['AWS_BANK_DATA_DIR']=root+'/data'
  os.environ['AWS_BANK_ARTIFACT_DIR']=root+'/artifacts'
  os.environ['AWS_BANK_BOOTSTRAP_PASSWORD']='local-test-password-123'
  import app.main as main
  main.DATA=Path(root)/"data";main.DATA.mkdir()
  main.ART=Path(root)/"artifacts";main.ART.mkdir()
  main.DB=main.DATA/"bank.sqlite3"
  app=main.app
  with TestClient(app) as client:
   assert client.get('/api/health').status_code==200
   assert client.get('/api/ready').status_code==200
   assert client.post('/api/credit/assess',json={'income':100,'debt':5,'credit_utilization':.2,'delinquencies':0,'employment_years':4}).status_code==401
   assert client.post('/api/login',json={'username':'admin','password':'local-test-password-123'}).status_code==200
   cloud=client.get('/api/admin/cloud-readiness')
   assert cloud.status_code==200 and cloud.json()['cloud_validated'] is False and len(cloud.json()['blockers'])>=3
   assert client.post('/api/admin/users',json={'username':'analyst','password':'analyst-password-123','role':'user'}).status_code==200
   assert client.put('/api/admin/users/analyst/status',json={'active':False}).json()['active'] is False
   assert client.post('/api/login',json={'username':'analyst','password':'analyst-password-123'}).status_code==401
   assert client.put('/api/admin/users/analyst/status',json={'active':True}).status_code==200
   assert client.post('/api/credit/assess',json={'income':100,'debt':5,'credit_utilization':.2,'delinquencies':0,'employment_years':4}).status_code==200
   assert client.post('/api/aml/screen',json={'amount':12000,'velocity':9,'cross_border':False,'high_risk_country':False,'customer_age_days':10}).json()['alert']
   assert client.post('/api/llm/query',json={'question':'What does MLflow track?'}).json()['provider']=='offline'
   llm_settings=client.get('/api/admin/llm-settings')
   assert llm_settings.status_code==200 and llm_settings.json()['external_adapters']=='disabled'
   updated=client.put('/api/admin/llm-settings',json={'provider':'offline','model_identifier':'curated-rule-v2','temperature':0.1,'max_output_tokens':256,'timeout_seconds':5,'max_retries':0,'token_budget':256,'cost_ceiling':0,'prompt_version':'test-v1','tracing':True,'safety_mode':True})
   assert updated.status_code==200 and updated.json()['prompt_version']=='test-v1'
   assert client.put('/api/admin/llm-settings',json={'provider':'bedrock','model_identifier':'external','temperature':0,'max_output_tokens':256,'timeout_seconds':5,'max_retries':0,'token_budget':256,'cost_ceiling':0,'prompt_version':'test-v1','tracing':True,'safety_mode':True}).status_code==422
   genai=client.get('/api/admin/genai-settings')
   assert genai.status_code==200 and genai.json()['human_approval_required'] is True
   assert client.put('/api/admin/genai-settings',json={'guardrails_enabled':True,'structured_output':True,'tool_allowlist':[],'human_approval_required':True,'policy_version':'test-policy-v1'}).status_code==200
   assert client.put('/api/admin/genai-settings',json={'guardrails_enabled':True,'structured_output':True,'tool_allowlist':['transfer_funds'],'human_approval_required':True,'policy_version':'test-policy-v1'}).status_code==422
   assert client.put('/api/admin/genai-settings',json={'guardrails_enabled':True,'structured_output':True,'tool_allowlist':[],'human_approval_required':False,'policy_version':'test-policy-v1'}).status_code==422
   first_eval=client.post('/api/admin/evals/run')
   assert first_eval.status_code==200
   first_payload=first_eval.json()
   assert first_payload['agent_eval']['hitl_compliance']==1.0
   assert first_payload['rag_eval']['recall_at_3']>=0
   assert first_payload['ml_model_eval']['status']=='not_run'
   assert first_payload['dataset_manifest']['total_executed_cases']>=13
   second_eval=client.post('/api/admin/evals/run')
   assert second_eval.status_code==200
   regression=client.get('/api/admin/evals/regression')
   assert regression.status_code==200 and regression.json()['status']=='completed'
   report=client.get('/api/admin/evals/'+str(client.get('/api/evals').json()[0]['id'])+'/report')
   assert report.status_code==200 and report.json()['report_version']=='evaluation-report-v1'
   assert client.get('/api/cases').status_code==200
   assert client.post('/api/admin/providers',json={'name':'bedrock','kind':'bedrock','model':'anthropic.claude','enabled':True}).status_code==422
