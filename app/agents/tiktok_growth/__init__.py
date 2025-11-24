# app/agents/tiktok_growth/__init__.py

"""
TikTok Growth Agent (TGA)

High-level interface that other parts of the system can import.
For now this just exposes the main manager class.
"""

from .TGA_Main_Brain_manager import TikTokGrowthAgent

__all__ = ["TikTokGrowthAgent"]
def __init__(self) -> None:
    self.video_queue: List[TGAVideoDraft] = []
    self.trend_brain = TrendBrain()
    self.video_lab = VideoLab()
    self.tiktok_client = TikTokApiClient()  # not used yet, just ready
