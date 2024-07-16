from fastapi import APIRouter
from Controllers.site_controller import (
    getSettingsSite,
    updateSettingsSite,
    disabelSettingsSite,
)

site = APIRouter()


@site.get("/configuracion-sitio")
def get_settings_site():
    return getSettingsSite()


@site.put("/configuracion-sitio")
def update_settings_site(data: dict):
    return updateSettingsSite(data)


@site.patch("/configuracion-sitio/")
def disable_settings_site(status: str):
    return disabelSettingsSite(status)
