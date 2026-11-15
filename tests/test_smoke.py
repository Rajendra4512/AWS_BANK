import os
os.environ.setdefault('AWS_BANK_BOOTSTRAP_PASSWORD','test-password-123456')
os.environ.setdefault('AWS_BANK_SESSION_SECRET','test-session-secret')
from app.main import synthetic,psi,password_hash,verify

def test_synthetic():
 x,y=synthetic(n=100)
 assert x.shape==(100,5) and len(y)==100

def test_psi():
 x,_=synthetic(n=1000)
 assert abs(psi(x[:,0],x[:,0]))<1e-9

def test_password():
 h=password_hash('secret');assert verify('secret',h) and not verify('wrong',h)
