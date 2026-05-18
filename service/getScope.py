from utils.database import coleccion

async def get_scope():
    return await coleccion.find().to_list()
    
