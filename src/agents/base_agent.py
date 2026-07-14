"""
基础智能体类

所有专业智能体的基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np


class BaseAgent(ABC):
    """
    智能体基类

    所有专业智能体都需要继承此类并实现analyze方法
    """

    def __init__(self, name: str, role: str, weight: float = 1.0):
        """
        初始化智能体

        参数:
            name: 智能体名称
            role: 角色描述
            weight: 决策权重
        """
        self.name = name
        self.role = role
        self.weight = weight
        self.history = []
        self.performance_log = []

    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析数据并返回建议

        参数:
            data: 市场数据字典

        返回:
            {
                'recommendation': 'buy'/'sell'/'hold',
                'confidence': 0.0-1.0,
                'reasoning': '分析理由',
                'target_weights': {'L1': 0.15, ...},
                'risk_alerts': ['预警信息'],
                'key_metrics': {'指标名': 值}
            }
        """
        pass

    def get_confidence(self) -> float:
        """获取当前建议的置信度"""
        if not self.history:
            return 0.5
        return np.mean([h.get('confidence', 0.5) for h in self.history[-10:]])

    def record_decision(self, decision: Dict, outcome: float):
        """
        记录决策结果（用于学习和改进）

        参数:
            decision: 决策内容
            outcome: 实际结果（收益率）
        """
        self.history.append({
            'timestamp': datetime.now(),
            'decision': decision,
            'outcome': outcome,
            'accuracy': 1.0 if (decision.get('recommendation') == 'buy' and outcome > 0) or
                               (decision.get('recommendation') == 'sell' and outcome < 0) else 0.0
        })

        # 保持最近100条记录
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def calculate_performance_score(self) -> float:
        """计算近期表现评分"""
        if not self.history:
            return 0.5

        recent = self.history[-20:]  # 最近20次决策
        accuracy = np.mean([h.get('accuracy', 0.5) for h in recent])

        return accuracy

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}', weight={self.weight})>"


class MarketData:
    """市场数据容器"""

    def __init__(self, **kwargs):
        self.data = kwargs
        self.timestamp = datetime.now()

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def to_dict(self) -> Dict:
        return {**self.data, 'timestamp': self.timestamp.isoformat()}
