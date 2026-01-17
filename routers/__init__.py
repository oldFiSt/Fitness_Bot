from aiogram import Router
from .commands import router as commands_router

from .menu import router as menu_router
from .gamification import router as gamification_router
from .kby import router as kby_router

router = Router()
router.include_router(commands_router)

# ✅ сначала меню и профиль/рейтинг
router.include_router(menu_router)
router.include_router(gamification_router)

# ✅ потом FSM расчёта
router.include_router(kby_router)
