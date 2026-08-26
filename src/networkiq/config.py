import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "NetworkIQ",
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:1.5b",
)


# Project root:
# NetworkIQ/
# ├── src/
# ├── data/
# └── ...
PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


DATA_DIR = PROJECT_ROOT / "data"