"""
Shim module for Render & legacy imports.

Real implementation is in app.mamos.MAMOS.mamos_loader,
but other parts of the code expect `app.mamos.mamos_loader`.
"""

from app.mamos.MAMOS.mamos_loader import MAMOSLoader  # noqa: F401
