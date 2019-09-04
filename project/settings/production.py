from .base import *  # noqa: F403 F401
import os

DEBUG = os.environ.get("DEBUG_MODE", "NO") == "YES"

SECRET_KEY = os.environ.get("SECRET_KEY")
