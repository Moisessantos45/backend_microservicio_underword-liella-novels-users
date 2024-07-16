import json
from fastapi import HTTPException
from Config.db import dataBase
from Helpers.bcryptSalt import comparePassword, encryptar
from Helpers.generete_token import generate_token


def loginAdmin(data):
    try:
        email = data.email
        password = data.password
        response = dataBase.table("Users").select("*").eq("email", email).execute()
        if not response.data:
            return HTTPException(status_code=400, detail="Email incorrecto")

        data = response.data[0]

        passwordDb = data.get("password")

        verifyPassword = comparePassword(password, passwordDb)
        if not verifyPassword:
            return HTTPException(status_code=400, detail="Password incorrecto")

        acceso = data.get("acceso")
        if not acceso:
            return HTTPException(status_code=400, detail="No tienes acceso")

        idUser = data.get("idUser")
        isActiveSession = data.get("activo")
        if isActiveSession:
            dataBase.table("Users").update({"activo": False, "token": ""}).eq(
                "idUser", idUser
            ).execute()
        token = generate_token(idUser)

        res = (
            dataBase.table("Users")
            .update({"activo": True, "token": token})
            .eq("idUser", idUser)
            .execute()
        )

        fromToJsonDict = res.data[0]
        user_without_password = fromToJsonDict.copy()

        user_without_password.pop("password", None)

        return user_without_password
    except Exception as e:
        return {"msg": str(e)}


def logoutSession(json):
    try:
        email = json.get("email")
        response = dataBase.table("Users").select("*").eq("email", email).execute()
        if not response.data:
            return HTTPException(status_code=400, detail="Email incorrecto")

        data = response.data[0]
        idUser = data.get("idUser")
        dataBase.table("Users").update({"activo": False, "token": ""}).eq(
            "idUser", idUser
        ).execute()

        return {"msg": "Sesión cerrada"}
    except Exception as e:
        return {"msg": str(e)}


def panelAdministracion(userId: str):
    try:
        responseUser = (
            dataBase.table("Users").select("*").eq("idUser", userId).execute()
        )
        responseUsers = dataBase.table("Users").select("*").execute()
        if not responseUser.data or not responseUsers.data:
            return HTTPException(status_code=400, detail="No hay usuarios")
        dataUser = responseUser.data[0]
        dataUsers = responseUsers.data

        totalUsers = len(dataUsers)

        return {"user": dataUser, "totalUsers": totalUsers}
    except Exception as e:
        return {"msg": str(e)}


def getUsers():
    try:
        response = dataBase.table("Users").select("*").execute()
        if not response.data:
            return HTTPException(status_code=400, detail="No hay usuarios")
        data = response.data

        return data
    except Exception as e:
        return {"msg": str(e)}


def addRegisterUser(data):
    try:
        response = (
            dataBase.table("Users").select("idUser").eq("email", data.email).execute()
        )
        if response.data:
            return HTTPException(status_code=400, detail="Email ya registrado")
        responseUser = (
            dataBase.table("Users").select("tipo").eq("idUser", data.id).execute()
        )
        if not responseUser.data:
            return HTTPException(status_code=400, detail="No tienes acceso")

        tipo = responseUser.data[0].get("tipo")
        if tipo != "administrador":
            return HTTPException(status_code=400, detail="No tienes acceso")

        salt = encryptar(data.password)
        data.password = salt
        dataDict = data.dict()
        dataDict["activo"] = False
        dataDict["token"] = ""
        dataDict["acceso"] = False
        dataDict.pop("id", None)

        res = dataBase.table("Users").insert(dataDict).execute()
        if not res.data:
            return HTTPException(status_code=400, detail="No se pudo registrar")

        return {"msg": "Usuario registrado"}
    except Exception as e:
        return {"msg": str(e)}


def updateDataUser(data):
    try:
        id = data.get("id")
        response = dataBase.table("Users").select("idUser").eq("idUser", id).execute()

        if not response.data:
            return HTTPException(status_code=400, detail="Usuario no registrado")

        dataDict = data.copy()
        dataDict.pop("id", None)
        dataDict.pop("password", None)
        dataDict["acceso"] = json.loads(data.get("acceso"))
        dataDict["activo"] = json.loads(data.get("activo"))
        if data.get("password").strip() != "":
            salt = encryptar(data.get("password"))
            dataDict["password"] = salt

        res = dataBase.table("Users").update(dataDict).eq("idUser", data.id).execute()
        if not res.data:
            return HTTPException(status_code=400, detail="No se pudo actualizar")
        dataUser = res.data[0]
        return {"email": dataUser.get("email"), "name_user": dataUser.get("name_user")}
    except Exception as e:
        return {"msg": str(e)}


def disableUser(data):
    try:
        id = data.get("id")
        active = json.loads(data.get("acceso"))
        response = dataBase.table("Users").select("idUser").eq("idUser", id).execute()

        if not response.data:
            return HTTPException(status_code=400, detail="Usuario no registrado")

        res = (
            dataBase.table("Users")
            .update({"acceso": active})
            .eq("idUser", data.id)
            .execute()
        )

        if not res.data:
            return HTTPException(status_code=400, detail="No se pudo desactivar")

        return {"msg": "Usuario desactivado"}
    except Exception as e:
        return {"msg": str(e)}


def extendsSesion(email):
    try:
        response = dataBase.table("Users").select("*").eq("email", email).execute()

        if not response.data:
            return HTTPException(status_code=400, detail="Email incorrecto")

        data = response.data[0]
        idUser = data.get("idUser")
        token = generate_token(idUser)
        res = (
            dataBase.table("Users")
            .update({"token": token})
            .eq("idUser", idUser)
            .execute()
        )

        if not res.data:
            return HTTPException(
                status_code=400, detail="No se pudo extender la sesión"
            )

        return token
    except Exception as e:
        return {"msg": str(e)}


def deleteUser(id):
    try:
        response = (
            dataBase.table("Users").update({"acceso": False}).eq("idUser", id).execute()
        )

        if not response.data:
            return HTTPException(status_code=400, detail="No se pudo eliminar")

        return {"msg": "Usuario eliminado"}
    except Exception as e:
        return {"msg": str(e)}
