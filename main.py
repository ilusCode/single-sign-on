from fastapi import FastAPI, Header
from service.singleSignOnService import post_single_sign_on_info

app = FastAPI()

@app.get("/default")
def read_root():
    return {"Hello": "World"}

@app.get("/sso-info")
async def get_sso_info(x_user_iluscode: str = Header(...), x_pw_iluscode: str = Header(...)):
    return await post_single_sign_on_info(x_user_iluscode, x_pw_iluscode)