import os, sqlite3, json, secrets, hashlib, hmac, time, io, csv, threading
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, Depends, Request, Response, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score, confusion_matrix
from sklearn.model_selection import train_test_split
from .artifacts import ArtifactStore

DATA = Path(os.getenv('AWS_BANK_DATA_DIR','data')); DATA.mkdir(parents=True,exist_ok=True)
ART = Path(os.getenv('AWS_BANK_ARTIFACT_DIR','artifacts')); ART.mkdir(parents=True,exist_ok=True)
DB=DATA/'bank.sqlite3'
FEATURES=['amount','hour','velocity','merchant_risk','geo_distance']
lock=threading.Lock()
login_attempts={}
app=FastAPI(title='AWS_BANK',version='0.1.0')

def now(): return datetime.now(timezone.utc).isoformat()
@contextmanager
def db():
 c=sqlite3.connect(DB,timeout=15);c.row_factory=sqlite3.Row
 try: yield c;c.commit()
 finally:c.close()
def audit(actor,action,detail):
 with db() as c:c.execute('INSERT INTO audit(ts,actor,action,detail) VALUES(?,?,?,?)',(now(),actor,action,json.dumps(detail)))
def password_hash(password,salt=None):
 salt=salt or secrets.token_hex(16)
 return salt+':'+hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),310000).hex()
def verify(password,stored):
 try:salt,_=stored.split(':');return hmac.compare_digest(password_hash(password,salt),stored)
 except Exception:return False
def login_allowed(key):
 current=time.time();window=[x for x in login_attempts.get(key,[]) if current-x<60]
 if len(window)>=5:login_attempts[key]=window;return False
 login_attempts[key]=window;return True
def record_login_failure(key):login_attempts.setdefault(key,[]).append(time.time())

def init():
 with db() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT NOT NULL,role TEXT NOT NULL,active INTEGER NOT NULL DEFAULT 1);
  CREATE TABLE IF NOT EXISTS sessions(token_hash TEXT PRIMARY KEY,username TEXT NOT NULL,expires INTEGER NOT NULL);
  CREATE TABLE IF NOT EXISTS password_reset_tokens(token_hash TEXT PRIMARY KEY,username TEXT NOT NULL,expires INTEGER NOT NULL,used INTEGER NOT NULL DEFAULT 0,created_by TEXT NOT NULL,created TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS models(version INTEGER PRIMARY KEY,created TEXT NOT NULL,metrics TEXT NOT NULL,status TEXT NOT NULL,source TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS predictions(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT NOT NULL,version INTEGER NOT NULL,features TEXT NOT NULL,score REAL NOT NULL);
  CREATE TABLE IF NOT EXISTS drift(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT NOT NULL,psi REAL NOT NULL,flag INTEGER NOT NULL,details TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT NOT NULL,actor TEXT NOT NULL,action TEXT NOT NULL,detail TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS lessons(slug TEXT PRIMARY KEY,title TEXT NOT NULL,content TEXT NOT NULL,updated TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS learning_progress(username TEXT NOT NULL,slug TEXT NOT NULL,completed INTEGER NOT NULL DEFAULT 0,last_visited TEXT NOT NULL,exercise_status TEXT NOT NULL DEFAULT 'not_started',updated TEXT NOT NULL,PRIMARY KEY(username,slug));''')
  if not c.execute('SELECT 1 FROM users').fetchone():
   pwd=os.getenv('AWS_BANK_BOOTSTRAP_PASSWORD')
   if not pwd or len(pwd)<12:raise RuntimeError('Set AWS_BANK_BOOTSTRAP_PASSWORD with at least 12 characters')
   c.execute('INSERT INTO users VALUES(?,?,?,1)',(os.getenv('AWS_BANK_BOOTSTRAP_ADMIN','admin'),password_hash(pwd),'admin'))
  for slug,title,content in LESSONS:
   c.execute('INSERT OR IGNORE INTO lessons VALUES(?,?,?,?)',(slug,title,content,now()))
  c.execute("INSERT OR IGNORE INTO settings VALUES('drift_threshold','0.2')")

LESSONS=[
 ('lifecycle','Classic MLOps lifecycle', '''Goal: maintain reliable fraud decisions as transaction behavior changes. Flow: ingest → validate → train → evaluate → register candidate → human approval → serve → monitor → retrain → rollback. In this application the model is Logistic Regression, chosen for CPU efficiency, explainability and reproducible baseline. It is NOT a bank-grade fraud system. In production add feature store, streaming ingestion, secure labeling, independent test sets, data lineage, and regulatory review. Code: app/main.py train(), score(), drift_check(). Architecture: browser → FastAPI → SQLite + model artifact. MLflow tracking is optional; production registry is a separate service.'''),
 ('metrics','Fraud metrics and threshold selection', '''Fraud is imbalanced: accuracy can be misleading. Precision measures the share of flagged transactions that are fraud; recall measures detected fraud share; PR-AUC summarizes ranking quality. False negatives cost fraud losses; false positives create customer friction. Select a decision threshold using a cost matrix and validation data, then test on untouched data. Here 0.5 is a teaching default, not an approved banking threshold. Code: train() and score().'''),
 ('drift','PSI and Evidently', '''Population Stability Index (PSI) compares binned reference and current feature distributions: sum((current% - reference%) × ln(current% / reference%)). This app computes PSI for transaction amount using fixed reference bins. A value above 0.2 is an illustrative alert threshold, not a universal statistical law. Drift does not prove model accuracy degraded: performance drift requires labels. Evidently is a future optional reporting integration; built-in PSI is functional today. Code: psi() and drift_check().'''),
 ('registry','Model registry, approvals, rollback', '''Training creates a candidate model. An administrator reviews metrics and explicitly promotes it to active. Only one version can be active. Rollback promotes an earlier stored version after review; preserve artifacts and audit events. Local SQLite models table is a lightweight registry. MLflow logging can be enabled with the optional dependency; an external managed MLflow registry is recommended for multi-instance production. Code: train(), promote().'''),
 ('aws','AWS architecture and Bedrock boundaries', '''Local: one FastAPI container on localhost:7005, SQLite volume, joblib artifacts. AWS target: ECS Fargate service behind ALB, ECR images, Secrets Manager, CloudWatch, S3 model artifacts, RDS PostgreSQL for multi-instance, IAM least privilege, VPC endpoints, WAF and HTTPS. Bedrock provides foundation-model inference for optional analyst explanations; it does NOT host FastAPI or the fraud classifier. Do not send sensitive banking data to an LLM without approved governance. Local resource cap 1 GB; cloud production sizing must be benchmarked.'''),
 ('governance','Model risk, human approval and operations', '''Separate roles: user can score and read lessons; admin can provision users, edit lessons, train and promote models. Every sensitive action is audited. In regulated banking, use maker-checker approval by distinct identities, immutable logs, evidence packages, independent validation, access reviews and incident response. Current app has one admin approval step and is a learning foundation, not regulatory compliance.'''),
 ('credit_risk','Credit risk design','Credit models estimate probability of default (PD), loss given default (LGD), and exposure at default (EAD). This build implements a transparent risk index only, not a calibrated PD. Explain why labels, observation windows, rejected applicants, fairness, calibration, and out-of-time validation matter. Trace POST /api/credit/assess to app/domains.py credit(). In production: governed feature pipeline, independent validation, calibration, adverse-action explanations, periodic monitoring, and documented policy thresholds.'),
 ('aml','AML alert lifecycle','AML screening here uses simple transparent rules: large transfers, velocity, geography and customer tenure. Real AML requires customer due diligence, watchlists, sanctions controls, transaction monitoring, typology coverage, analyst casework, evidence preservation, and suspicious activity reporting governed by jurisdiction. POST /api/aml/screen creates a case; GET /api/cases lists; POST /api/cases/{id}/review requires a different admin identity from the requester. Compare deterministic rules to anomaly detection and supervised detection, and discuss alert fatigue and false positives.'),
 ('llmops','LLMOps gateway, grounding and evaluation','The gateway uses curated offline responses: POST /api/llm/query. It is NOT an LLM and does not call Bedrock. POST /api/admin/evals/run checks fixed keyword coverage; this is NOT an LLM-as-judge evaluation. Real gateway architecture includes IAM auth, model selection, token accounting, budgets, input/output filtering, prompt/version registry, prompt injection defenses, PII handling, grounding citations, safety checks, retries and telemetry. Bedrock is model inference; ECS hosts the API. Add external adapters only after approval and integration testing.'),
 ('agentic','Agentic workflow and human-in-the-loop','A real LangGraph-style workflow has explicit state, nodes, edges, checkpoint persistence, retry policy, and human interrupts. This application implements a simple persistent maker-checker case review, not a LangGraph agent. Study POST /api/cases/{id}/review and the separate requester/reviewer guard. Production agents must use allowlisted tools, scoped credentials, idempotency keys, durable checkpoints, expiry, escalation and rollback; high-risk external actions must not execute until approved.'),
 ('mlflow','MLflow experiment lifecycle','Training happens in app/main.py train(). It fits a scaled logistic regression baseline, calculates precision, recall, F1 and PR-AUC and stores a joblib artifact. Optional mlflow_log records run parameters and metrics to local MLflow tracking. The SQLite models table is a separate lightweight registry, NOT the MLflow Model Registry. To migrate: deploy a dedicated MLflow tracking server with artifact store and registry backend, register versions, attach validation evidence, and map approval events to aliases. Test candidate/active/rollback consistency before enabling automated promotion.'),
 ('operations','Bank-grade deployment and risk controls','Separate educational controls from production claims. Current local app uses SQLite, session cookies, one-process CPU inference, local model artifacts, and a 1 GB memory cap. Production requires managed relational storage, object storage, strong IAM and SSO, CSRF protection, network isolation, secrets rotation, immutable audit, supply chain scanning, incident playbooks, backups, HA, regulatory review, encryption, capacity testing and a real CI/CD release gate. Never deploy the local starter as an internet-facing regulated bank service.'),
 ('llmops','LLMOps Gateway and agentic HITL (planned)', '''Proposed optional module: route prompts through a provider-neutral gateway, manage Bedrock credentials with IAM, track latency and spend, enforce PII redaction and rate limits. Evaluate groundedness, answer relevance, policy violations and task success on curated datasets. Agentic workflows require checkpointing and human approval before external actions. These are design lessons only: not implemented in the current MVP. Prefer separate services when memory permits.''')]

@app.on_event('startup')
def startup():
 init()
 from .domains import setup
 setup()
 from .banking import setup as setup_banking
 setup_banking()
class Credentials(BaseModel):username:str;password:str
class NewUser(BaseModel):username:str=Field(min_length=3,max_length=40,pattern=r'^[A-Za-z0-9_.-]+$');password:str=Field(min_length=12);role:str='user'
class PasswordChange(BaseModel):password:str=Field(min_length=12)
class SelfPasswordChange(BaseModel):current_password:str=Field(min_length=1);new_password:str=Field(min_length=12)
class PasswordResetRequest(BaseModel):token:str=Field(min_length=20,max_length=200);new_password:str=Field(min_length=12)
class UserStatus(BaseModel):active:bool
class RoleUpdate(BaseModel):role:str
class Tx(BaseModel):amount:float=Field(ge=0,le=10000000);hour:int=Field(ge=0,le=23);velocity:float=Field(ge=0,le=1000);merchant_risk:float=Field(ge=0,le=1);geo_distance:float=Field(ge=0,le=20000)
class LessonEdit(BaseModel):title:str=Field(min_length=3,max_length=150);content:str=Field(min_length=20,max_length=30000)
class Setting(BaseModel):value:float=Field(gt=0,le=5)
class LearningProgress(BaseModel):completed:bool=False;exercise_status:str=Field(default='not_started',pattern=r'^(not_started|in_progress|passed|needs_review)$')

def principal(request:Request):
 token=request.cookies.get('aws_bank_session','');th=hashlib.sha256(token.encode()).hexdigest()
 with db() as c:
  r=c.execute('SELECT u.username,u.role FROM sessions s JOIN users u ON u.username=s.username WHERE s.token_hash=? AND s.expires>? AND u.active=1',(th,int(time.time()))).fetchone()
 if not r:raise HTTPException(401,'Please log in')
 return dict(r)
def admin(u=Depends(principal)):
 if u['role'] not in ('admin','bank_admin','super_admin'):raise HTTPException(403,'Administrator role required')
 return u
@app.post('/api/login')
def login(x:Credentials,request:Request,response:Response):
 key=(request.client.host if request.client else 'unknown')+'|'+x.username.lower()
 if not login_allowed(key):raise HTTPException(429,'Too many login attempts; retry after 60 seconds',headers={'Retry-After':'60'})
 with db() as c:r=c.execute('SELECT * FROM users WHERE username=? AND active=1',(x.username,)).fetchone()
 if not r or not verify(x.password,r['password']):
  record_login_failure(key);time.sleep(0.3);raise HTTPException(401,'Invalid credentials')
 login_attempts.pop(key,None)
 token=secrets.token_urlsafe(32)
 with db() as c:c.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),r['username'],int(time.time())+8*3600))
 response.set_cookie('aws_bank_session',token,httponly=True,samesite='strict',secure=os.getenv('AWS_BANK_SECURE_COOKIE','false').lower()=='true',max_age=8*3600,path='/')
 audit(r['username'],'login',{})
 return {'username':r['username'],'role':r['role']}
@app.post('/api/logout')
def logout(request:Request,response:Response,u=Depends(principal)):
 with db() as c:c.execute('DELETE FROM sessions WHERE token_hash=?',(hashlib.sha256(request.cookies.get('aws_bank_session','').encode()).hexdigest(),))
 response.delete_cookie('aws_bank_session');return {'ok':True}
@app.get('/api/me')
def me(u=Depends(principal)):return u
@app.put('/api/me/password')
def change_my_password(x:SelfPasswordChange,request:Request,response:Response,u=Depends(principal)):
 with db() as c:r=c.execute('SELECT password FROM users WHERE username=? AND active=1',(u['username'],)).fetchone()
 if not r or not verify(x.current_password,r['password']):raise HTTPException(400,'Current password is incorrect')
 with db() as c:
  c.execute('UPDATE users SET password=? WHERE username=?',(password_hash(x.new_password),u['username']))
  c.execute('DELETE FROM sessions WHERE username=?',(u['username'],))
 audit(u['username'],'password.change',{})
 response.delete_cookie('aws_bank_session')
 return {'ok':True,'relogin_required':True}
@app.get('/api/health')
def health():return {'status':'ok','service':'AWS_BANK'}
@app.get('/api/ready')
def readiness():
 checks={'data_directory':DATA.exists(),'artifact_directory':ART.exists(),'database':DB.exists()}
 ready=all(checks.values())
 if not ready:raise HTTPException(status_code=503,detail={'status':'not_ready','checks':checks})
 return {'status':'ready','service':'AWS_BANK','checks':checks}
@app.get('/api/admin/cloud-readiness')
def cloud_readiness(u=Depends(admin)):
 checks={'health_endpoint':True,'readiness_endpoint':True,'data_directory':DATA.exists(),'artifact_directory':ART.exists(),'database':DB.exists(),'bootstrap_secret_injected':bool(os.getenv('AWS_BANK_BOOTSTRAP_PASSWORD')),'session_secret_injected':bool(os.getenv('AWS_BANK_SESSION_SECRET')),'local_container_ready':True}
 blockers=['SQLite requires managed PostgreSQL for multi-instance cloud deployment','Local artifact backend requires approved S3 or Azure Blob adapter','Production TLS, SSO/MFA, CSRF, WAF, backups and vulnerability scanning remain required','No authorized AWS or Azure deployment has been executed']
 return {'status':'documented-local-ready','checks':checks,'cloud_validated':False,'blockers':blockers,'runbooks':['docs/21_AWS_DEPLOYMENT_RUNBOOK.md','docs/22_AZURE_DEPLOYMENT_RUNBOOK.md'],'policy_boundary':'No cloud resources or paid providers were provisioned'}
@app.get('/api/admin/users')
def users(u=Depends(admin)):
 with db() as c:return [dict(x) for x in c.execute('SELECT username,role,active FROM users ORDER BY username')]
@app.post('/api/admin/users')
def create_user(x:NewUser,u=Depends(admin)):
 if x.role not in ('user','admin','customer','bank_officer','risk_analyst','mlops_operator','governance_officer','bank_admin','super_admin'):raise HTTPException(400,'Invalid role')
 try:
  with db() as c:c.execute('INSERT INTO users VALUES(?,?,?,1)',(x.username,password_hash(x.password),x.role))
 except sqlite3.IntegrityError:raise HTTPException(409,'Username exists')
 audit(u['username'],'user.create',{'username':x.username,'role':x.role});return {'ok':True}
@app.put('/api/admin/users/{username}/password')
def reset_password(username:str,x:PasswordChange,u=Depends(admin)):
 with db() as c:
  r=c.execute('UPDATE users SET password=? WHERE username=?',(password_hash(x.password),username))
  if not r.rowcount:raise HTTPException(404,'Unknown user')
  c.execute('DELETE FROM sessions WHERE username=?',(username,))
 audit(u['username'],'user.reset_password',{'username':username});return {'ok':True}
@app.post('/api/admin/users/{username}/reset-token')
def issue_reset_token(username:str,u=Depends(admin)):
 token=secrets.token_urlsafe(32);expires=int(time.time())+15*60
 with db() as c:
  if not c.execute('SELECT 1 FROM users WHERE username=? AND active=1',(username,)).fetchone():raise HTTPException(404,'Unknown or inactive user')
  c.execute('INSERT INTO password_reset_tokens(token_hash,username,expires,used,created_by,created) VALUES(?,?,?,?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),username,expires,0,u['username'],now()))
 audit(u['username'],'user.reset_token.issue',{'username':username,'expires':expires});return {'token':token,'expires_at':expires,'single_use':True,'expires_in_seconds':900}
@app.post('/api/password-reset')
def consume_reset_token(x:PasswordResetRequest,response:Response):
 token_hash=hashlib.sha256(x.token.encode()).hexdigest()
 with db() as c:
  row=c.execute('SELECT username FROM password_reset_tokens WHERE token_hash=? AND used=0 AND expires>?',(token_hash,int(time.time()))).fetchone()
  if not row:raise HTTPException(400,'Reset token is invalid, expired, or already used')
  c.execute('UPDATE users SET password=? WHERE username=? AND active=1',(password_hash(x.new_password),row['username']))
  c.execute('UPDATE password_reset_tokens SET used=1 WHERE token_hash=?',(token_hash,))
  c.execute('DELETE FROM sessions WHERE username=?',(row['username'],))
 audit('password-reset','user.reset_token.consume',{'username':row['username']});response.delete_cookie('aws_bank_session');return {'ok':True,'relogin_required':True}
@app.put('/api/admin/users/{username}/status')
def set_user_status(username:str,x:UserStatus,u=Depends(admin)):
 if username==u['username'] and not x.active:raise HTTPException(400,'Cannot deactivate the current admin session')
 with db() as c:
  r=c.execute('UPDATE users SET active=? WHERE username=?',(int(x.active),username))
  if not r.rowcount:raise HTTPException(404,'Unknown user')
  if not x.active:c.execute('DELETE FROM sessions WHERE username=?',(username,))
 audit(u['username'],'user.status',{'username':username,'active':x.active})
 return {'username':username,'active':x.active}
@app.put('/api/admin/users/{username}/role')
def set_user_role(username:str,x:RoleUpdate,u=Depends(admin)):
 roles=('user','admin','customer','bank_officer','risk_analyst','mlops_operator','governance_officer','bank_admin','super_admin')
 if x.role not in roles:raise HTTPException(400,'Invalid role')
 if username==u['username']:raise HTTPException(400,'Cannot change the current administrator role')
 with db() as c:
  r=c.execute('UPDATE users SET role=? WHERE username=?',(x.role,username))
  if not r.rowcount:raise HTTPException(404,'Unknown user')
  c.execute('DELETE FROM sessions WHERE username=?',(username,))
 audit(u['username'],'user.role.update',{'username':username,'role':x.role});return {'username':username,'role':x.role,'relogin_required':True}
@app.get('/api/lessons')
def lessons(u=Depends(principal)):
 with db() as c:return [dict(x) for x in c.execute('SELECT slug,title,content,updated FROM lessons ORDER BY slug')]
@app.get('/api/learning/progress')
def learning_progress(u=Depends(principal)):
 with db() as c:return [dict(x) for x in c.execute('SELECT slug,completed,last_visited,exercise_status,updated FROM learning_progress WHERE username=? ORDER BY slug',(u['username'],))]
@app.put('/api/learning/progress/{slug}')
def update_learning_progress(slug:str,x:LearningProgress,u=Depends(principal)):
 with db() as c:
  if not c.execute('SELECT 1 FROM lessons WHERE slug=?',(slug,)).fetchone():raise HTTPException(404,'Unknown lesson')
  c.execute('INSERT INTO learning_progress(username,slug,completed,last_visited,exercise_status,updated) VALUES(?,?,?,?,?,?) ON CONFLICT(username,slug) DO UPDATE SET completed=excluded.completed,last_visited=excluded.last_visited,exercise_status=excluded.exercise_status,updated=excluded.updated',(u['username'],slug,int(x.completed),now(),x.exercise_status,now()))
 audit(u['username'],'learning.progress.update',{'slug':slug,'completed':x.completed,'exercise_status':x.exercise_status});return {'ok':True,'slug':slug,'completed':x.completed,'exercise_status':x.exercise_status}
@app.put('/api/admin/lessons/{slug}')
def edit_lesson(slug:str,x:LessonEdit,u=Depends(admin)):
 with db() as c:c.execute('INSERT INTO lessons VALUES(?,?,?,?) ON CONFLICT(slug) DO UPDATE SET title=excluded.title,content=excluded.content,updated=excluded.updated',(slug,x.title,x.content,now()))
 audit(u['username'],'lesson.update',{'slug':slug});return {'ok':True}

def synthetic(seed=42,shift=0.0,n=2000):
 rng=np.random.default_rng(seed)
 amount=rng.lognormal(3.5+shift,1.2,n).clip(0,100000)
 hour=rng.integers(0,24,n);velocity=rng.poisson(2+shift,n).clip(0,1000)
 risk=rng.beta(2+shift,6,n);distance=rng.exponential(45+shift*70,n)
 X=np.column_stack([amount,hour,velocity,risk,distance])
 z=-6.2+0.000015*amount+0.13*velocity+4.2*risk+0.002*distance+0.6*(hour<5)
 p=1/(1+np.exp(-z));y=(rng.random(n)<p).astype(int)
 return X,y

def mlflow_log(version,metrics):
 if os.getenv('AWS_BANK_ENABLE_MLFLOW','false').lower()!='true':return 'disabled'
 try:
  import mlflow
  mlflow.set_tracking_uri((DATA/'mlruns').resolve().as_uri());mlflow.set_experiment('AWS_BANK_fraud')
  with mlflow.start_run(run_name=f'candidate-v{version}'):
   mlflow.log_params({'algorithm':'LogisticRegression','seed':42,'dataset':'synthetic'})
   mlflow.log_metrics(metrics)
  return 'logged'
 except Exception as e:return 'error: '+str(e)[:150]
@app.post('/api/admin/train')
def train(u=Depends(admin)):
 if not lock.acquire(blocking=False):raise HTTPException(409,'Training already in progress')
 try:
  X,y=synthetic();a,b,ya,yb=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import StandardScaler
  model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=250,class_weight='balanced',random_state=42))
  model.fit(a,ya);probs=model.predict_proba(b)[:,1];pred=(probs>=.5).astype(int)
  metrics={'precision':round(float(precision_score(yb,pred,zero_division=0)),4),'recall':round(float(recall_score(yb,pred,zero_division=0)),4),'f1':round(float(f1_score(yb,pred,zero_division=0)),4),'pr_auc':round(float(average_precision_score(yb,probs)),4),'samples':len(X),'fraud_rate':round(float(y.mean()),4)}
  with db() as c:version=c.execute('SELECT COALESCE(MAX(version),0)+1 FROM models').fetchone()[0]
  ArtifactStore(ART).save(model,version)
  with db() as c:c.execute('INSERT INTO models VALUES(?,?,?,?,?)',(version,now(),json.dumps(metrics),'candidate','synthetic'))
  tracking=mlflow_log(version,{k:v for k,v in metrics.items() if isinstance(v,(int,float))})
  audit(u['username'],'model.train',{'version':version,'tracking':tracking});return {'version':version,'status':'candidate','metrics':metrics,'mlflow':tracking}
 finally:lock.release()
@app.get('/api/models')
def models(u=Depends(principal)):
 with db() as c:return [{**dict(x),'metrics':json.loads(x['metrics'])} for x in c.execute('SELECT * FROM models ORDER BY version DESC')]
@app.post('/api/admin/models/{version}/promote')
def promote(version:int,u=Depends(admin)):
 if not ArtifactStore(ART).exists(version):raise HTTPException(404,'Artifact missing')
 with db() as c:
  if not c.execute('SELECT 1 FROM models WHERE version=?',(version,)).fetchone():raise HTTPException(404,'Version missing')
  for row in c.execute('SELECT results FROM evaluations ORDER BY id DESC LIMIT 50'):
   result=json.loads(row['results']);ml=result.get('ml_model_eval') or {};gate=ml.get('quality_gate') or {}
   if ml.get('model_version')==version and ml.get('status')=='completed' and gate.get('passed') is False:raise HTTPException(409,'Promotion blocked by the latest failed evaluation quality gate')
  c.execute("UPDATE models SET status='archived' WHERE status='active'")
  c.execute("UPDATE models SET status='active' WHERE version=?",(version,))
 audit(u['username'],'model.promote_or_rollback',{'version':version});return {'active_version':version}
@app.post('/api/score')
def score(x:Tx,u=Depends(principal)):
 with db() as c:r=c.execute("SELECT version FROM models WHERE status='active'").fetchone()
 if not r:raise HTTPException(409,'Admin must train and promote a model first')
 model=ArtifactStore(ART).load(r['version'])
 val=[getattr(x,k) for k in FEATURES];p=float(model.predict_proba(np.array([val]))[0,1])
 with db() as c:c.execute('INSERT INTO predictions(ts,version,features,score) VALUES(?,?,?,?)',(now(),r['version'],json.dumps(val),p))
 return {'fraud_probability':round(p,5),'flagged':p>=0.5,'model_version':r['version'],'threshold':0.5,'note':'Synthetic-trained educational model; not for real banking decisions'}
def psi(ref,cur):
 edges=np.unique(np.quantile(ref,np.linspace(0,1,11)))
 if len(edges)<3:return 0.0
 edges[0]=-np.inf;edges[-1]=np.inf
 a=np.histogram(ref,bins=edges)[0]/len(ref);b=np.histogram(cur,bins=edges)[0]/len(cur)
 a=np.maximum(a,1e-6);b=np.maximum(b,1e-6)
 return float(np.sum((b-a)*np.log(b/a)))
@app.post('/api/admin/drift-check')
def drift_check(shift:float=0.8,u=Depends(admin)):
 if not 0<=shift<=2:raise HTTPException(400,'shift must be between 0 and 2')
 ref,_=synthetic(seed=42,shift=0,n=2000);cur,_=synthetic(seed=99,shift=shift,n=1000)
 value=psi(ref[:,0],cur[:,0]);
 with db() as c:threshold=float(c.execute("SELECT value FROM settings WHERE key='drift_threshold'").fetchone()[0])
 flag=value>threshold
 with db() as c:c.execute('INSERT INTO drift(ts,psi,flag,details) VALUES(?,?,?,?)',(now(),value,int(flag),json.dumps({'shift':shift,'threshold':threshold,'feature':'amount'})))
 audit(u['username'],'drift.check',{'psi':value,'flag':flag})
 return {'psi':round(value,4),'alert':flag,'threshold':threshold,'feature':'amount','next_action':'Review labeled performance and candidate retraining' if flag else 'Continue monitoring'}
@app.get('/api/drift')
def drift_history(u=Depends(principal)):
 with db() as c:return [{**dict(r),'details':json.loads(r['details'])} for r in c.execute('SELECT * FROM drift ORDER BY id DESC LIMIT 30')]
@app.get('/api/admin/audit')
def audit_log(u=Depends(admin)):
 with db() as c:return [dict(x) for x in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')]
@app.get('/api/admin/governance/summary')
def governance_summary(u=Depends(admin)):
 with db() as c:
  models=[{**dict(x),'metrics':json.loads(x['metrics'])} for x in c.execute('SELECT * FROM models ORDER BY version DESC')]
  evaluations=[{**dict(x),'results':json.loads(x['results'])} for x in c.execute('SELECT * FROM evaluations ORDER BY id DESC LIMIT 20')]
  settings={r['key']:r['value'] for r in c.execute('SELECT * FROM settings')}
  audit_rows=[dict(x) for x in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 50')]
 return {'models':models,'evaluations':evaluations,'settings':settings,'audit':audit_rows,'policy_boundary':'Synthetic educational system; no regulatory certification claimed.'}
@app.get('/api/admin/settings')
def settings(u=Depends(admin)):
 with db() as c:return {r['key']:r['value'] for r in c.execute('SELECT * FROM settings')}
@app.put('/api/admin/settings/drift_threshold')
def set_threshold(x:Setting,u=Depends(admin)):
 with db() as c:c.execute("UPDATE settings SET value=? WHERE key='drift_threshold'",(str(x.value),))
 audit(u['username'],'settings.update',{'drift_threshold':x.value});return {'ok':True}
@app.get('/',response_class=HTMLResponse)
def home():return (Path(__file__).parent/'index.html').read_text()
@app.get('/banking',response_class=HTMLResponse)
def banking_home():return (Path(__file__).parent/'banking.html').read_text()

from .domains import router as domain_router
app.include_router(domain_router)
from .banking import router as banking_router
app.include_router(banking_router)
