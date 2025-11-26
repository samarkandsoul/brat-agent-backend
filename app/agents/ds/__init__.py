"""
DS package – Dropshipping System agents for Samarkand Soul.

Burada bütün DS agent modulları toplanır:
- ds01_market_research      – bazar araşdırması
- ds02_drive_agent          – Google Drive folder sistemləri
- ds03_shopify_agent        – Shopify inteqrasiyası
- ds21_product_auto_creator – məhsul auto yaradıcısı
- ds22_image_auto_agent     – image / vizual prompt generatoru
"""

# Bu importlar sayəsində lazım olsa
#   from app.agents.ds import ds01_market_research
# kimi istifadə edə bilərsən.

from . import ds01_market_research  # noqa: F401
from . import ds02_drive_agent      # noqa: F401
from . import ds03_shopify_agent    # noqa: F401
from . import ds21_product_auto_creator  # noqa: F401
from . import ds22_image_auto_agent      # noqa: F401

__all__ = [
    "ds01_market_research",
    "ds02_drive_agent",
    "ds03_shopify_agent",
    "ds21_product_auto_creator",
    "ds22_image_auto_agent",
]
