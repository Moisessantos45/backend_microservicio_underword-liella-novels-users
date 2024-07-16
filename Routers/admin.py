from fastapi import APIRouter, Depends
from Middleware.auth_sesion import authSesion
from Models.admin import LoginSesion, UserRegister
from Controllers.admin_controller import (
    loginAdmin,
    logoutSession,
    panelAdministracion,
    getUsers,
    addRegisterUser,
    updateDataUser,
    disableUser,
    extendsSesion,
)

admin = APIRouter()


@admin.post("/login")
def login(data: LoginSesion):
    return loginAdmin(data)


@admin.post("/logout")
def logout(json: dict):
    return logoutSession(json)


@admin.get("/panel-administracion/")
def panel_administracion(token: dict = Depends(authSesion)):
    print(token)
    userId = token.get("id")
    return panelAdministracion(userId)


@admin.get("/panel-administracion/colaboradores")
def panel_administracion_colaboradores(id: dict = Depends(authSesion)):
    return getUsers()


@admin.post("/agregar-users")
def agregar_users(data: UserRegister, id: dict = Depends(authSesion)):
    return addRegisterUser(data)


@admin.post("/olvide-password")
def olvide_password():
    return {"message": "Olvide password"}


@admin.put("/actulizar-datos")
def actulizar_datos(data: dict):
    return updateDataUser(data)


@admin.patch("/desctivar-user")
def desctivar_user(data: dict):
    return disableUser(data)


@admin.patch("/extends-sesion/")
def extends_sesion(email: str):
    return extendsSesion(email)


@admin.delete("/eliminar-user/{id}")
def eliminar_user(id: int):
    return {"message": f"Eliminar user {id}"}
