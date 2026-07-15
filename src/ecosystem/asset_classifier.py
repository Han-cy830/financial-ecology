"""
生态资产分类器

基于Tokenomics-Ecological-Network项目，将金融资产分为捕食者/猎物/共生体/价值创造者
"""

import numpy as np
import pandas as pd
from enum import Enum
from typing import Dict, Optional


class EcologicalRole(Enum):
    """生态角色"""
    PREY = "猎物"           # L1/L2: 提供稳定收益
    SYMBIONT = "共生体"     # L2中特殊角色: 保险、券商
    VALUE_CREATOR = "价值创造者"  # L3: 通过业务创造价值
    PREDATOR_VALUE = "价值型捕食者"  # L4a: 有现金流支撑
    PREDATOR_SPECULATIVE = "纯投机捕食者"  # L4b: 纯投机
    SUPER_PREDATOR = "顶级捕食者"  # L5: 极高风险


class AssetClassifier:
    """
    资产生态角色分类器

    使用多维度特征识别资产的生态角色
    """

    def __init__(self):
        self.role_thresholds = {
            'cash_flow_positive': {
                'threshold': 0.5,  # 现金流为正概率>50%
                'weight': 0.3
            },
            'volatility': {
                'thresholds': [0.15, 0.40, 0.70],  # 波动率分界点
                'weight': 0.25
            },
            'correlation_with_stocks': {
                'threshold': 0.6,
                'weight': 0.2
            },
            'leverage_ratio': {
                'threshold': 3.0,
                'weight': 0.15
            },
            'liquidity_score': {
                'threshold': 0.5,
                'weight': 0.1
            }
        }

    def classify(self, name: str, **kwargs) -> Dict:
        """
        分类资产生态角色

        参数:
            name: 资产名称
            **kwargs:
                - volatility: 年化波动率 (0.0-1.0)
                - cash_flow_positive: 现金流是否为正 (bool)
                - correlation_with_stocks: 与股票相关性 (0.0-1.0)
                - leverage_ratio: 杠杆率
                - liquidity_score: 流动性评分 (0.0-1.0)
                - regulatory_status: 监管状态 ('regulated', 'semi_regulated', 'unregulated')
                - business_model: 业务模式 ('asset_based', 'trading', 'hybrid', 'platform')

        返回:
            {
                'name': 资产名称,
                'role': 生态角色,
                'risk_level': 风险等级,
                'confidence': 分类置信度,
                'features': 特征,
                'allocation_guidance': 配置指导
            }
        """
        # 提取特征
        features = self._extract_features(**kwargs)

        # 计算生态角色得分
        role_scores = self._calculate_role_scores(features)

        # 选择最可能的角色
        dominant_role = max(role_scores, key=role_scores.get)

        # 分类置信度
        confidence = role_scores[dominant_role] / sum(role_scores.values())

        # 风险等级
        risk_level = self._assess_risk_level(dominant_role, features)

        # 配置指导
        allocation_guidance = self._get_allocation_guidance(dominant_role)

        return {
            'name': name,
            'role': dominant_role,
            'risk_level': risk_level,
            'confidence': confidence,
            'role_scores': role_scores,
            'features': features,
            'allocation_guidance': allocation_guidance
        }

    def _extract_features(self, **kwargs) -> Dict:
        """提取并标准化特征"""
        return {
            'volatility': kwargs.get('volatility', 0.2),
            'cash_flow_positive': kwargs.get('cash_flow_positive', True),
            'correlation_with_stocks': kwargs.get('correlation_with_stocks', 0.5),
            'leverage_ratio': kwargs.get('leverage_ratio', 1.0),
            'liquidity_score': kwargs.get('liquidity_score', 0.7),
            'regulatory_status': kwargs.get('regulatory_status', 'regulated'),
            'business_model': kwargs.get('business_model', 'hybrid')
        }

    def _calculate_role_scores(self, features: Dict) -> Dict[str, float]:
        """计算各生态角色的得分"""
        scores = {}

        # 猎物得分 (L1/L2)
        scores['猎物'] = self._score_prey(features)

        # 共生体得分
        scores['共生体'] = self._score_symbiont(features)

        # 价值创造者得分 (L3)
        scores['价值创造者'] = self._score_value_creator(features)

        # 价值型捕食者得分 (L4a)
        scores['价值型捕食者'] = self._score_predator_value(features)

        # 纯投机捕食者得分 (L4b)
        scores['纯投机捕食者'] = self._score_predator_speculative(features)

        # 顶级捕食者得分 (L5)
        scores['顶级捕食者'] = self._score_super_predator(features)

        return scores

    def _score_prey(self, f: Dict) -> float:
        """猎物得分"""
        score = 0.0

        # 低波动率
        if f['volatility'] < 0.10:
            score += 0.4
        elif f['volatility'] < 0.20:
            score += 0.2

        # 稳定现金流
        if f['cash_flow_positive']:
            score += 0.3

        # 低相关性
        if f['correlation_with_stocks'] < 0.3:
            score += 0.2

        # 高流动性
        if f['liquidity_score'] > 0.8:
            score += 0.1

        return score

    def _score_symbiont(self, f: Dict) -> float:
        """共生体得分"""
        score = 0.0

        # 业务模式：hybrid（混合业务）
        if f['business_model'] in ['hybrid', 'platform']:
            score += 0.3

        # 受监管
        if f['regulatory_status'] == 'regulated':
            score += 0.3

        # 中等波动率
        if 0.15 < f['volatility'] < 0.35:
            score += 0.2

        # 中等相关性（提供分散化）
        if 0.3 < f['correlation_with_stocks'] < 0.7:
            score += 0.2

        return score

    def _score_value_creator(self, f: Dict) -> float:
        """价值创造者得分"""
        score = 0.0

        # 有正向现金流
        if f['cash_flow_positive']:
            score += 0.35

        # 中等偏高波动率
        if 0.20 < f['volatility'] < 0.50:
            score += 0.25

        # 中等相关性
        if f['correlation_with_stocks'] > 0.5:
            score += 0.2

        # 中等流动性
        if f['liquidity_score'] > 0.6:
            score += 0.2

        return score

    def _score_predator_value(self, f: Dict) -> float:
        """价值型捕食者得分"""
        score = 0.0

        # 正向现金流（但不稳定）
        if f['cash_flow_positive']:
            score += 0.2

        # 高波动率
        if f['volatility'] > 0.35:
            score += 0.3

        # 适度杠杆
        if 1.0 < f['leverage_ratio'] < 3.0:
            score += 0.25

        # 中等流动性
        if 0.4 < f['liquidity_score'] < 0.8:
            score += 0.25

        return score

    def _score_predator_speculative(self, f: Dict) -> float:
        """纯投机捕食者得分"""
        score = 0.0

        # 极高波动率
        if f['volatility'] > 0.60:
            score += 0.35

        # 负向或无现金流
        if not f['cash_flow_positive']:
            score += 0.25

        # 高杠杆
        if f['leverage_ratio'] > 3.0:
            score += 0.2

        # 低监管
        if f['regulatory_status'] in ['semi_regulated', 'unregulated']:
            score += 0.2

        return score

    def _score_super_predator(self, f: Dict) -> float:
        """顶级捕食者得分"""
        score = 0.0

        # 极高波动率
        if f['volatility'] > 0.80:
            score += 0.4

        # 极高杠杆
        if f['leverage_ratio'] > 5.0:
            score += 0.3

        # 低流动性
        if f['liquidity_score'] < 0.3:
            score += 0.3

        return score

    def _assess_risk_level(self, role: str, features: Dict) -> str:
        """评估风险等级"""
        risk_map = {
            '猎物': '极低' if features['volatility'] < 0.10 else '低',
            '共生体': '低-中',
            '价值创造者': '中-高' if features['volatility'] > 0.30 else '中',
            '价值型捕食者': '高',
            '纯投机捕食者': '极高',
            '顶级捕食者': '极高（可能归零）'
        }
        return risk_map.get(role, '未知')

    def _get_allocation_guidance(self, role: str) -> Dict:
        """获取配置指导"""
        guidance = {
            '猎物': {
                'max_weight': 0.50,
                'seasons': ['春季', '夏季', '秋季', '冬季'],
                'notes': '核心底仓，各季节均可持有'
            },
            '共生体': {
                'max_weight': 0.20,
                'seasons': ['秋季', '冬季'],
                'notes': '滞胀期和衰退期表现优异'
            },
            '价值创造者': {
                'max_weight': 0.50,
                'seasons': ['春季', '夏季'],
                'notes': '复苏期和繁荣期核心配置'
            },
            '价值型捕食者': {
                'max_weight': 0.15,
                'seasons': ['春季', '夏季'],
                'notes': '繁荣期可增持，衰退期必须减仓'
            },
            '纯投机捕食者': {
                'max_weight': 0.05,
                'seasons': ['夏季'],
                'notes': '仅夏季可持有，其他季节清仓'
            },
            '顶级捕食者': {
                'max_weight': 0.03,
                'seasons': ['夏季'],
                'notes': '纯粹娱乐，输得起才碰'
            }
        }
        return guidance.get(role, {})

    def batch_classify(self, assets: list) -> pd.DataFrame:
        """批量分类资产"""
        import pandas as pd

        results = []
        for asset in assets:
            result = self.classify(**asset)
            results.append({
                '名称': result['name'],
                '生态角色': result['role'],
                '风险等级': result['risk_level'],
                '置信度': f"{result['confidence']:.1%}",
                '最大配置比例': f"{result['allocation_guidance'].get('max_weight', 0):.0%}",
                '适合季节': ', '.join(result['allocation_guidance'].get('seasons', []))
            })

        return pd.DataFrame(results)


# 使用示例
if __name__ == "__main__":
    classifier = AssetClassifier()

    # 分类国债
    bond = classifier.classify(
        name="10年期国债",
        volatility=0.08,
        cash_flow_positive=True,
        correlation_with_stocks=0.10,
        leverage_ratio=1.0,
        liquidity_score=0.95
    )
    print(f"\n国债: {bond['role']} (置信度: {bond['confidence']:.1%})")

    # 分类沪深300
    index = classifier.classify(
        name="沪深300ETF",
        volatility=0.25,
        cash_flow_positive=True,
        correlation_with_stocks=0.98,
        leverage_ratio=1.0,
        liquidity_score=0.90
    )
    print(f"沪深300: {index['role']} (置信度: {index['confidence']:.1%})")

    # 分类比特币
    btc = classifier.classify(
        name="比特币",
        volatility=0.80,
        cash_flow_positive=False,
        correlation_with_stocks=0.30,
        leverage_ratio=2.0,
        liquidity_score=0.85,
        regulatory_status='semi_regulated'
    )
    print(f"比特币: {btc['role']} (置信度: {btc['confidence']:.1%})")
