from fastapi import FastAPI
from service.singleSignOnService import get_single_sign_on_info

app = FastAPI()

@app.get("/default")
def read_root():
    return {"Hello": "World"}

@app.get("/sso-info")
def get_sso_info():
    return get_single_sign_on_info()