from fastapi import FastAPI, Header, Request
from service.CryptographyalgorithmService import IcExcepcion
from service.LogonService import put_logon
from service.RegisterService import put_create_account
from fastapi.responses import JSONResponse
from model.CreateUserRequest import CreateUserRequest
from service.ValidateTokenService import validate_token

app = FastAPI()

@app.get("/default")
def read_root():
    return {"Hello": "World"}

@app.put("/api/logon")
async def put_post_logon(x_user_iluscode: str = Header(...), x_pw_iluscode: str = Header(...)):
    return await put_logon(x_user_iluscode, x_pw_iluscode)

@app.put("/api/register")
async def put_post_register(requestBody:CreateUserRequest):
    return await put_create_account(requestBody)

@app.get("/api/validate")
async def get_validate(Authorization: str = Header(...)):
    return await validate_token(Authorization)

@app.exception_handler(IcExcepcion)
async def mi_excepcion_handler(request: Request, exc: IcExcepcion):
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"},
    )
