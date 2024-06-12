"""Main module that will run on startup to boot the backend"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers.rabbit.setup import start_broker, stop_broker



