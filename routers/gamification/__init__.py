from aiogram import Router

from .rating_profile import router as rating_profile_router

router = Router(name=__name__)

router.include_router(rating_profile_router)