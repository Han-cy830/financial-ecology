"""
HMM季节检测器

基于隐马尔可夫模型概率化识别市场季节
"""

import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')


class SeasonHMM:
    """
    基于HMM的市场季节检测模型

    将市场状态分为4个季节：
    - 春季: 复苏期
    - 夏季: 繁荣期
    - 秋季: 滞胀期
    - 冬季: 衰退期
    """

    SEASONS = ['春季', '夏季', '秋季', '冬季']
    SEASON_COLORS = {
        '春季': '#90EE90',    # 浅绿色
        '夏季': '#FFD700',    # 金色
        '秋季': '#FFA500',    # 橙色
        '冬季': '#87CEEB'     # 浅蓝色
    }

    def __init__(self, n_seasons: int = 4, random_state: int = 42):
        self.n_seasons = n_seasons
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False

    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        准备特征变量

        参数:
            data: DataFrame，包含以下列（可根据实际数据调整）:
                - gdp_growth: GDP同比增速
                - cpi: CPI同比
                - ppi: PPI同比
                - m2_growth: M2同比增速
                - interest_rate: 10年期国债收益率
                - credit_spread: 信用利差
                - real_rate: 实际利率
                - stock_return_3m: 股市3个月收益率
                - volatility: VIX或历史波动率
                - fund_flow: 资金流向

        返回:
            X: 标准化后的特征矩阵 (n_samples, n_features)
        """
        # 定义必需特征（如果缺少则填充NaN）
        required_features = [
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ]

        # 确保所有特征都存在
        for feat in required_features:
            if feat not in data.columns:
                data[feat] = np.nan

        # 提取特征
        self.feature_names = required_features
        features = data[required_features].copy()

        # 前向填充缺失值
        features = features.ffill().bfill()

        # 标准化
        if self.is_trained:
            X = self.scaler.transform(features.values)
        else:
            X = self.scaler.fit_transform(features.values)

        return X

    def train(self, data: pd.DataFrame, verbose: bool = True) -> Dict:
        """
        训练HMM模型

        参数:
            data: 历史数据，包含特征列
            verbose: 是否打印训练信息

        返回:
            训练结果 {
                'converged': 是否收敛,
                'log_likelihood': 最终对数似然,
                'n_iter': 迭代次数
            }
        """
        X = self.prepare_features(data)

        if len(X) < 50:
            raise ValueError(f"数据量不足: {len(X)}行，至少需要50行")

        # 创建HMM模型
        self.model = hmm.GaussianHMM(
            n_components=self.n_seasons,
            covariance_type='full',
            n_iter=100,
            random_state=self.random_state,
            verbose=False
        )

        # 训练
        self.model.fit(X)

        self.is_trained = True

        result = {
            'converged': self.model.monitor_.converged,
            'log_likelihood': self.model.score(X),
            'n_iter': self.model.monitor_.iter
        }

        if verbose:
            print("=" * 60)
            print("HMM模型训练完成")
            print("=" * 60)
            print(f"收敛状态: {'✓' if result['converged'] else '✗'}")
            print(f"最终对数似然: {result['log_likelihood']:.2f}")
            print(f"迭代次数: {result['n_iter']}")
            print(f"\n状态转移矩阵:")
            print(self.get_transition_matrix().to_string())
            print(f"\n各季节特征（逆标准化后）:")
            self._print_emission_characteristics()

        return result

    def predict_season(self, data: pd.DataFrame) -> Dict:
        """
        预测当前季节

        参数:
            data: 当前数据（单行或多行）

        返回:
            {
                'season': 最可能的季节,
                'season_index': 季节索引 (0-3),
                'probabilities': {季节: 概率},
                'confidence': 置信度,
                'regime_change_probability': 状态切换概率,
                'next_3_seasons': 未来3个季节预测
            }
        """
        if not self.is_trained:
            raise ValueError("模型未训练，请先调用train()")

        X = self.prepare_features(data)

        # 预测隐藏状态
        hidden_states = self.model.predict(X)
        current_state = hidden_states[-1]
        current_season = self.SEASONS[current_state]

        # 计算概率分布
        state_probs = self.model.predict_proba(X)
        current_probs = state_probs[-1]

        probabilities = {
            season: float(prob)
            for season, prob in zip(self.SEASONS, current_probs)
        }

        # 置信度
        confidence = float(np.max(current_probs))

        # 状态切换概率
        regime_change_prob = 1.0 - current_probs[current_state]

        # 预测未来3个季节
        next_3 = self._forecast_next_seasons(current_probs, n_steps=3)

        return {
            'season': current_season,
            'season_index': int(current_state),
            'probabilities': probabilities,
            'confidence': confidence,
            'regime_change_probability': regime_change_prob,
            'next_3_seasons': next_3,
            'suggested_allocation': self._suggest_allocation(probabilities)
        }

    def _forecast_next_seasons(self, current_probs: np.ndarray, n_steps: int = 3) -> List[Dict]:
        """预测未来N个季节（使用转移矩阵）"""
        forecasts = []
        probs = current_probs.copy()

        for step in range(n_steps):
            # 下一步状态概率 = probs @ 转移矩阵
            probs = probs @ self.model.transmat_

            # 最可能状态
            next_state = int(np.argmax(probs))
            season = self.SEASONS[next_state]

            forecasts.append({
                'step': step + 1,
                'season': season,
                'probabilities': {
                    s: float(p) for s, p in zip(self.SEASONS, probs)
                }
            })

        return forecasts

    def _suggest_allocation(self, probabilities: np.ndarray) -> Dict[str, float]:
        """
        基于季节概率给出配置建议

        使用加权平均：sum(季节概率 * 该季节的基础配置)
        """
        base_allocations = {
            '春季': {'L1': 0.15, 'L2': 0.30, 'L3': 0.40, 'L4': 0.10, 'L5': 0.05},
            '夏季': {'L1': 0.10, 'L2': 0.20, 'L3': 0.45, 'L4': 0.20, 'L5': 0.05},
            '秋季': {'L1': 0.25, 'L2': 0.35, 'L3': 0.25, 'L4': 0.10, 'L5': 0.05},
            '冬季': {'L1': 0.40, 'L2': 0.35, 'L3': 0.15, 'L4': 0.05, 'L5': 0.05}
        }

        # 加权平均
        weighted_allocation = {}
        for layer in ['L1', 'L2', 'L3', 'L4', 'L5']:
            weighted_allocation[layer] = sum(
                probs[i] * base_allocations[season][layer]
                for i, season in enumerate(self.SEASONS)
            )

        # 标准化
        total = sum(weighted_allocation.values())
        weighted_allocation = {
            k: v / total for k, v in weighted_allocation.items()
        }

        return weighted_allocation

    def get_transition_matrix(self) -> pd.DataFrame:
        """获取状态转移矩阵"""
        if not self.is_trained:
            raise ValueError("模型未训练")

        matrix = self.model.transmat_
        return pd.DataFrame(
            matrix,
            index=self.SEASONS,
            columns=self.SEASONS
        )

    def get_emission_parameters(self) -> pd.DataFrame:
        """获取每个状态的均值向量（已逆标准化）"""
        if not self.is_trained:
            raise ValueError("模型未训练")

        means_original = self.scaler.inverse_transform(self.model.means_)
        return pd.DataFrame(
            means_original,
            index=self.SEASONS,
            columns=self.feature_names
        )

    def _print_emission_characteristics(self):
        """打印各季节的特征（用于调试）"""
        emissions = self.get_emission_parameters()

        descriptions = {
            'gdp_growth': 'GDP增速',
            'cpi': 'CPI',
            'ppi': 'PPI',
            'm2_growth': 'M2增速',
            'interest_rate': '10年期利率',
            'credit_spread': '信用利差',
            'real_rate': '实际利率',
            'stock_return_3m': '股市3M收益',
            'volatility': '波动率',
            'fund_flow': '资金流向'
        }

        for season in self.SEASONS:
            print(f"\n{season}:")
            row = emissions.loc[season]
            for feat, desc in descriptions.items():
                print(f"  {desc}: {row[feat]:.2f}")


class MultiMarketHMMDetector:
    """多市场HMM季节检测器"""

    def __init__(self):
        self.detectors = {}

    def add_market(self, name: str, **kwargs):
        """添加市场检测器"""
        self.detectors[name] = SeasonHMM(**kwargs)

    def train_market(self, market_name: str, data: pd.DataFrame, **kwargs) -> Dict:
        """训练单个市场模型"""
        if market_name not in self.detectors:
            self.add_market(market_name)

        return self.detectors[market_name].train(data, **kwargs)

    def detect(self, market_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        检测所有市场季节

        参数:
            market_data: {市场名称: 数据}

        返回:
            {
                market_name: {
                    'season': 季节,
                    'probabilities': 概率分布,
                    'confidence': 置信度,
                    'regime_change_probability': 切换概率,
                    'suggested_allocation': 配置建议
                }
            }
        """
        results = {}
        for market, data in market_data.items():
            if market in self.detectors:
                results[market] = self.detectors[market].predict_season(data)
            else:
                results[market] = {'error': f'{market}模型未训练'}

        return results

    def get_season_alignment(self, market_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        分析多市场季节共振

        返回:
            {
                'aligned': 是否全部共振,
                'strength': 共振强度 (0-1),
                'dominant_season': 主导季节,
                'market_seasons': {市场: 季节},
                'season_distribution': {季节: 市场数}
            }
        """
        results = self.detect(market_data)

        season_counts = {}
        market_seasons = {}

        for market, result in results.items():
            if 'error' in result:
                continue

            season = result['season']
            season_counts[season] = season_counts.get(season, 0) + 1
            market_seasons[market] = season

        if not season_counts:
            return {'error': '无有效结果'}

        dominant_season = max(season_counts, key=season_counts.get)
        n_aligned = season_counts[dominant_season]
        n_total = len(market_seasons)

        return {
            'aligned': n_aligned == n_total,
            'strength': n_aligned / n_total,
            'dominant_season': dominant_season,
            'market_seasons': market_seasons,
            'season_distribution': season_counts
        }


# 使用示例
if __name__ == "__main__":
    # 生成模拟数据
    np.random.seed(42)
    n_samples = 200

    # 模拟4个季节的特征
    seasonal_means = {
        '春季': [0.05, 0.02, 0.03, 0.12, 0.028, 0.012, 0.006, 0.08, 0.18, 0.3],
        '夏季': [0.08, 0.025, 0.04, 0.10, 0.032, 0.010, 0.008, 0.12, 0.15, 0.5],
        '秋季': [0.02, 0.045, 0.02, 0.08, 0.035, 0.020, -0.005, -0.03, 0.25, -0.2],
        '冬季': [-0.03, 0.01, -0.02, 0.06, 0.030, 0.025, -0.015, -0.10, 0.35, -0.5]
    }

    # 生成序列
    data = []
    for i in range(n_samples):
        # 循环选择季节
        season_idx = i // 50
        season = ['春季', '夏季', '秋季', '冬季'][season_idx % 4]
        mean = seasonal_means[season]

        # 添加噪声
        sample = [m + np.random.normal(0, 0.1) for m in mean]
        data.append(sample)

    columns = [
        'gdp_growth', 'cpi', 'ppi', 'm2_growth',
        'interest_rate', 'credit_spread', 'real_rate',
        'stock_return_3m', 'volatility', 'fund_flow'
    ]
    df = pd.DataFrame(data, columns=columns)

    # 训练模型
    print("训练HMM模型...")
    hmm_model = SeasonHMM(n_seasons=4)
    result = hmm_model.train(df, verbose=True)

    # 预测最后一个月
    print("\n" + "=" * 60)
    print("预测当前季节")
    print("=" * 60)

    last_month = df.iloc[[-1]]
    prediction = hmm_model.predict_season(last_month)

    print(f"当前季节: {prediction['season']}")
    print(f"置信度: {prediction['confidence']:.1%}")
    print(f"季节切换概率: {prediction['regime_change_probability']:.1%}")
    print(f"\n概率分布:")
    for season, prob in prediction['probabilities'].items():
        print(f"  {season}: {prob:.1%}")

    print(f"\n配置建议:")
    for layer, weight in prediction['suggested_allocation'].items():
        print(f"  {layer}: {weight:.1%}")

    print(f"\n未来3个季节预测:")
    for forecast in prediction['next_3_seasons']:
        print(f"  {forecast['step']}个月后: {forecast['season']}")
