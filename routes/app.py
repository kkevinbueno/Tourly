"""Compatibilidade: a aplicação Flask é iniciada pelo app.py na raiz do projeto."""
from app import app, create_app

__all__ = ["app", "create_app"]
