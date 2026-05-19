from fastapi import FastAPI, Header, Request
from service.decryptAlgorithmService import IcExcepcion
from service.singleSignOnService import post_single_sign_on_info
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/default")
def read_root():
    return {"Hello": "World"}

@app.get("/sso-info")
async def get_sso_info(x_user_iluscode: str = Header(...), x_pw_iluscode: str = Header(...)):
    return await post_single_sign_on_info(x_user_iluscode, x_pw_iluscode)

@app.exception_handler(IcExcepcion)
async def mi_excepcion_handler(request: Request, exc: IcExcepcion):
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"},
    )
