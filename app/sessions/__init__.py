import shelve

from .manager import SessionManager
session_manager = SessionManager()
cache_manager = SessionManager('cache')