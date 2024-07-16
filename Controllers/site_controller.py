import json
from Config.db import dataBase
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def getSettingsSite():
    try:
        response = dataBase.table("config_site").select("*").execute()
        if not response.data:
            return HTTPException(status_code=400, detail="No hay configuraciones")

        data = response.data[0]
        return JSONResponse(content={"data": data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)


def updateSettingsSite(data):
    try:
        response = dataBase.table("config_site").update(data).execute()

        if not response.data:
            return HTTPException(
                status_code=400, detail="No se pudo actualizar la configuracion"
            )
        data = response.data[0]
        data.pop("id")

        return JSONResponse(content={data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)


def disabelSettingsSite(status):
    try:
        validateStatus = ["true", "false"].index(status)
        if validateStatus == -1:
            return HTTPException(status_code=400, detail="El estado no es valido")

        isStatus = json.loads(status)

        response = (
            dataBase.table("config_site")
            .update({"isMaintenanceMode": isStatus})
            .execute()
        )

        if not response.data:
            return HTTPException(
                status_code=400, detail="No se pudo desactivar el sitio"
            )

        return JSONResponse(
            content={"msg": "Configuracion desactivada"}, status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)
