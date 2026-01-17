# utils/plan_storage.py
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "plans_storage"
STORAGE_DIR.mkdir(exist_ok=True)

def _path(user_id: int) -> Path:
    return STORAGE_DIR / f"{user_id}.json"

def save_plan(user_id: int, meals_text: str | None = None, workouts_text: str | None = None) -> None:
    p = _path(user_id)
    data = {}
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))

    if meals_text is not None:
        data["meals"] = meals_text
        data["meals_saved_at"] = datetime.now().isoformat(timespec="seconds")
    if workouts_text is not None:
        data["workouts"] = workouts_text
        data["workouts_saved_at"] = datetime.now().isoformat(timespec="seconds")

    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_plan(user_id: int) -> dict:
    p = _path(user_id)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))
