"""
金融生态学 - 核心包

提供资产配置框架、生态模型、季节检测、多智能体决策等功能
"""

__version__ = '1.0.0'
__author__ = 'Financial Ecology Community'

from .ecosystem.asset_classifier import AssetClassifier, EcologicalRole
from .hmm_detector.season_hmm import SeasonHMM, MultiMarketHMMDetector

__all__ = [
    'AssetClassifier',
    'EcologicalRole',
    'SeasonHMM',
    'MultiMarketHMMDetector'
]
