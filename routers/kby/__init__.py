from aiogram import Router

from .kby_flow import router as kby_router

router = Router(name=__name__)

router.include_router(kby_router)