from fastapi import FastAPI, Header, Request
from service.decryptAlgorithmService import IcExcepcion
from service.logonService import put_logon
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/default")
def read_root():
    return {"Hello": "World"}

@app.put("/api/logon")
async def put_post_logon(x_user_iluscode: str = Header(...), x_pw_iluscode: str = Header(...)):
    return await put_logon(x_user_iluscode, x_pw_iluscode)

@app.exception_handler(IcExcepcion)
async def mi_excepcion_handler(request: Request, exc: IcExcepcion):
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"},
    )
