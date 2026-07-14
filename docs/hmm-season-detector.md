# HMM季节检测模型

使用隐马尔可夫模型（Hidden Markov Model）概率化识别市场季节，替代固定阈值方法。

## 🎯 为什么使用HMM？

### 传统方法的局限

**固定阈值方法**：
```python
# 传统方法：简单阈值判断
if CAPE > 40:
    season = "秋季"
elif GDP_growth < 0:
    season = "冬季"
```

**问题**：
1. **硬边界**：CAPE=39.9是春季，CAPE=40.1变成秋季
2. **单一维度**：不能综合考虑多个指标
3. **无法量化不确定性**：不知道判断的置信度
4. **滞后性**：需要等数据出来才知道季节

### HMM的优势

1. **概率输出**：给出每个季节的概率分布
2. **多维综合**：同时考虑10+个指标
3. **提前预警**：状态转换有过渡期
4. **自适应**：基于历史数据学习状态特征

---

## 📊 HMM理论基础

### 什么是隐马尔可夫模型？

**核心思想**：
- 市场有**隐藏状态**（季节：春夏秋冬）
- 这些状态**不可直接观测**
- 但我们能观测到**可观测变量**（收益率、波动率、资金流向等）
- HMM通过观测变量**推断隐藏状态**

**类比**：
```
隐藏状态：当前是什么季节（春季/夏季/秋季/冬季）
观测变量：温度、湿度、降雨量、植物生长情况
目标：根据观测变量推断季节
```

### HMM的三个核心问题

#### 1. 评估问题
给定模型参数，计算观测序列的概率

#### 2. 解码问题
给定观测序列，找出最可能的隐藏状态序列

**算法**：Viterbi算法

#### 3. 学习问题
给定观测序列，学习模型参数

**算法**：Baum-Welch算法（EM算法）

---

## 🔧 模型设计

### 隐藏状态（季节）

定义4个隐藏状态：

| 状态 | 季节 | 特征 |
|------|------|------|
| S0 | 春季复苏期 | 盈利触底回升，流动性充裕，估值中等 |
| S1 | 夏季繁荣期 | 盈利高增长，通胀温和，流动性宽裕 |
| S2 | 秋季滞胀期 | 盈利下滑，通胀高企，流动性收紧 |
| S3 | 冬季衰退期 | 盈利负增长，通缩风险，流动性枯竭 |

### 可观测变量

选择10个关键指标：

#### 1. 宏观经济指标
- GDP增速（季度）
- CPI同比
- PPI同比
- 工业增加值（月度）

#### 2. 流动性指标
- M2同比增速
- 10年期国债收益率
- 信用利差（BBB-国债）
- 实际利率（名义利率-CPI）

#### 3. 市场指标
- 股市收益率（过去3个月）
- 股市波动率（VIX或历史波动率）

#### 4. 情绪指标
- 资金流向（北向资金/机构持仓变化）
- 恐慌指数（Put/Call Ratio或VIX）

**数据标准化**：
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
observations_scaled = scaler.fit_transform(observations)
```

### 转移矩阵（状态转换）

定义4×4的转移矩阵A：

```
      春季  夏季  秋季  冬季
春季  [0.70, 0.25, 0.04, 0.01]  // 70%概率留在春季
夏季  [0.10, 0.75, 0.13, 0.02]  // 75%概率留在夏季
秋季  [0.05, 0.10, 0.70, 0.15]  // 70%概率留在秋季
冬季  [0.02, 0.05, 0.18, 0.75]  // 75%概率留在冬季
```

**解读**：
- 季节倾向于持续（对角元素较大）
- 春季→夏季、夏季→秋季、秋季→冬季转换概率较高
- 反向转换概率极低（符合季节性规律）

### 发射概率（状态→观测）

每个季节有特定的观测变量分布：

**示例：春季的特征**
- 盈利增速：均值8%，标准差5%
- 通胀率：均值2%，标准差1%
- M2增速：均值12%，标准差4%
- VIX：均值18，标准差5

**学习方式**：
- 使用历史数据（如2000-2020年）
- Baum-Welch算法自动学习每个状态的均值和协方差

---

## 💻 代码实现

### 1. 基础HMM模型

```python
# src/hmm_detector/season_hmm.py
import numpy as np
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler
import pandas as pd

class SeasonHMM:
    """
    基于HMM的市场季节检测模型
    """
    
    def __init__(self, n_seasons: int = 4):
        self.n_seasons = n_seasons
        self.model = None
        self.scaler = StandardScaler()
        self.season_names = ['春季', '夏季', '秋季', '冬季']
        
    def prepare_features(self, macro_data: pd.DataFrame) -> np.ndarray:
        """
        准备特征变量
        
        参数:
            macro_data: 宏观经济数据，包含：
                - gdp_growth: GDP增速
                - cpi: CPI同比
                - ppi: PPI同比
                - m2_growth: M2增速
                - interest_rate: 10年期国债收益率
                - credit_spread: 信用利差
                - real_rate: 实际利率
                - stock_return_3m: 股市3个月收益率
                - volatility: VIX波动率
                - fund_flow: 资金流向
        """
        features = [
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ]
        
        # 填充缺失值（前向填充）
        macro_data = macro_data[features].ffill()
        
        # 标准化
        X = self.scaler.fit_transform(macro_data.values)
        
        return X
    
    def train(self, macro_data: pd.DataFrame):
        """
        训练HMM模型
        
        参数:
            macro_data: 历史宏观经济数据
        """
        X = self.prepare_features(macro_data)
        
        # 创建HMM模型
        self.model = hmm.GaussianHMM(
            n_components=self.n_seasons,
            covariance_type='full',
            n_iter=100,
            random_state=42
        )
        
        # 训练
        self.model.fit(X)
        
        print("HMM模型训练完成")
        print(f"收敛状态: {self.model.monitor_.converged}")
        print(f"最终对数似然: {self.model.score(X):.2f}")
    
    def predict_season(self, current_data: pd.DataFrame) -> Dict:
        """
        预测当前季节和概率分布
        
        参数:
            current_data: 当前宏观数据（单行DataFrame）
        
        返回:
            {
                'season': 最可能的季节,
                'probabilities': {季节: 概率},
                'confidence': 置信度,
                'regime_change_probability': 季节切换概率
            }
        """
        if self.model is None:
            raise ValueError("模型未训练，请先调用train()")
        
        X = self.prepare_features(current_data)
        
        # 预测隐藏状态
        hidden_state = self.model.predict(X)[0]
        season = self.season_names[hidden_state]
        
        # 计算概率分布
        state_probs = self.model.predict_proba(X)[0]
        probabilities = {
            name: prob
            for name, prob in zip(self.season_names, state_probs)
        }
        
        # 置信度 = 最大概率
        confidence = max(state_probs)
        
        # 季节切换概率 = 1 - 当前状态概率
        regime_change_prob = 1 - state_probs[hidden_state]
        
        return {
            'season': season,
            'season_index': hidden_state,
            'probabilities': probabilities,
            'confidence': confidence,
            'regime_change_probability': regime_change_prob
        }
    
    def predict_next_seasons(self, current_data: pd.DataFrame, 
                            n_steps: int = 3) -> List[Dict]:
        """
        预测未来N个季节
        
        使用前向算法（Forward Algorithm）
        """
        X = self.prepare_features(current_data)
        
        # 获取当前状态概率
        current_probs = self.model.predict_proba(X)[0]
        
        forecasts = []
        probs = current_probs.copy()
        
        for step in range(n_steps):
            # 下一步状态概率 = probs * 转移矩阵
            probs = probs @ self.model.transmat_
            
            # 最可能状态
            next_state = np.argmax(probs)
            season = self.season_names[next_state]
            
            forecasts.append({
                'step': step + 1,
                'season': season,
                'probabilities': {
                    name: prob
                    for name, prob in zip(self.season_names, probs)
                }
            })
        
        return forecasts
    
    def get_transition_matrix(self) -> pd.DataFrame:
        """获取状态转移矩阵（可解释性分析）"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        matrix = self.model.transmat_
        return pd.DataFrame(
            matrix,
            index=self.season_names,
            columns=self.season_names
        )
    
    def get_emission_parameters(self) -> Dict:
        """
        获取每个状态的发射概率参数（均值向量和协方差矩阵）
        用于分析每个季节的特征
        """
        if self.model is None:
            raise ValueError("模型未训练")
        
        feature_names = [
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ]
        
        emissions = {}
        for i, season in enumerate(self.season_names):
            emissions[season] = {
                'means': dict(zip(feature_names, self.model.means_[i])),
                'covariance': self.model.covars_[i]
            }
        
        return emissions
```

### 2. 多市场HMM检测器

```python
# src/hmm_detector/multi_market_detector.py
class MultiMarketHMMDetector:
    """
    支持多个市场（A股、美股、港股）的HMM季节检测
    """
    
    def __init__(self):
        self.detectors = {
            'A股': SeasonHMM(),
            '美股': SeasonHMM(),
            '港股': SeasonHMM()
        }
    
    def train_all(self, market_data: Dict[str, pd.DataFrame]):
        """训练所有市场的HMM模型"""
        for market, data in market_data.items():
            print(f"训练 {market} 模型...")
            self.detectors[market].train(data)
    
    def detect_current_seasons(self, current_data: Dict[str, pd.DataFrame]) -> Dict:
        """检测所有市场的当前季节"""
        results = {}
        
        for market, data in current_data.items():
            results[market] = self.detectors[market].predict_season(data)
        
        return results
    
    def get_season_alignment(self, current_data: Dict) -> Dict:
        """
        分析多市场季节共振
        
        返回：
            - aligned: 是否共振
            - strength: 共振强度（0-1）
            - dominant_season: 主导季节
        """
        seasons = self.detect_current_seasons(current_data)
        
        # 统计每个季节的市场数量
        season_counts = {}
        for market, result in seasons.items():
            season = result['season']
            season_counts[season] = season_counts.get(season, 0) + 1
        
        # 主导季节
        dominant_season = max(season_counts, key=season_counts.get)
        n_aligned = season_counts[dominant_season]
        n_total = len(seasons)
        
        return {
            'aligned': n_aligned == n_total,
            'strength': n_aligned / n_total,
            'dominant_season': dominant_season,
            'market_seasons': {
                market: result['season']
                for market, result in seasons.items()
            },
            'season_distribution': season_counts
        }
```

### 3. 完整工作流

```python
# src/hmm_detector/workflow.py
import yaml
from typing import Dict, List

class HMMSeasonDetectorWorkflow:
    """
    HMM季节检测完整工作流
    """
    
    def __init__(self, config_path: str = 'configs/hmm_config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.detector = MultiMarketHMMDetector()
    
    def load_historical_data(self) -> Dict[str, pd.DataFrame]:
        """
        加载历史数据
        
        数据来源：
        - 宏观数据：国家统计局、美联储
        - 市场数据：Tushare、Yahoo Finance
        - 情绪数据：Wind、Choice
        """
        data = {}
        
        for market in self.config['markets']:
            data[market] = self._load_market_data(market)
        
        return data
    
    def train(self, historical_data: Dict[str, pd.DataFrame]):
        """训练模型"""
        print("开始训练HMM模型...")
        self.detector.train_all(historical_data)
        
        # 输出状态转移矩阵
        for market, detector in self.detector.detectors.items():
            print(f"\n{market} 状态转移矩阵:")
            print(detector.get_transition_matrix())
    
    def detect_current_season(self, current_data: Dict[str, pd.DataFrame]) -> Dict:
        """检测当前季节"""
        # 1. 检测各市场季节
        season_results = self.detector.detect_current_seasons(current_data)
        
        # 2. 分析季节共振
        alignment = self.detector.get_season_alignment(current_data)
        
        # 3. 预测未来季节
        forecasts = {}
        for market, data in current_data.items():
            forecasts[market] = self.detector.detectors[market].predict_next_seasons(data)
        
        return {
            'current_seasons': season_results,
            'season_alignment': alignment,
            'forecasts': forecasts,
            'allocation_suggestion': self._suggest_allocation(alignment)
        }
    
    def _suggest_allocation(self, alignment: Dict) -> Dict:
        """基于季节共振结果给出配置建议"""
        dominant_season = alignment['dominant_season']
        strength = alignment['strength']
        
        # 基础配置（根据季节）
        base_allocation = {
            '春季': {'L1': 0.15, 'L2': 0.30, 'L3': 0.40, 'L4': 0.10, 'L5': 0.05},
            '夏季': {'L1': 0.10, 'L2': 0.20, 'L3': 0.45, 'L4': 0.20, 'L5': 0.05},
            '秋季': {'L1': 0.25, 'L2': 0.35, 'L3': 0.25, 'L4': 0.10, 'L5': 0.05},
            '冬季': {'L1': 0.40, 'L2': 0.35, 'L3': 0.15, 'L4': 0.05, 'L5': 0.05}
        }
        
        allocation = base_allocation[dominant_season].copy()
        
        # 如果共振强度低（< 0.5），增加L1/L2比例（防守）
        if strength < 0.5:
            allocation['L1'] += 0.10
            allocation['L3'] -= 0.10
        
        return allocation
    
    def _load_market_data(self, market: str) -> pd.DataFrame:
        """加载单个市场的数据"""
        # TODO: 实现实际的数据加载逻辑
        # 这里返回示例数据
        pass
```

---

## 📈 使用示例

### 训练模型

```python
from src.hmm_detector import HMMSeasonDetectorWorkflow

# 1. 创建工作流
workflow = HMMSeasonDetectorWorkflow('configs/hmm_config.yaml')

# 2. 加载历史数据（2000-2024年）
historical_data = workflow.load_historical_data()

# 3. 训练模型
workflow.train(historical_data)

# 输出示例：
# 开始训练HMM模型...
# 训练 A股 模型...
# HMM模型训练完成
# 收敛状态: True
# 最终对数似然: -1234.56
# 
# A股 状态转移矩阵:
#          春季      夏季      秋季      冬季
# 春季  [0.70    0.25     0.04     0.01]
# 夏季  [0.10    0.75     0.13     0.02]
# 秋季  [0.05    0.10     0.70     0.15]
# 冬季  [0.02    0.05     0.18     0.75]
```

### 检测当前季节

```python
# 1. 准备当前数据（最近一个季度）
current_data = {
    'A股': pd.DataFrame({
        'gdp_growth': [0.05],
        'cpi': [0.022],
        'ppi': [0.015],
        'm2_growth': [0.105],
        'interest_rate': [0.028],
        'credit_spread': [0.012],
        'real_rate': [0.006],
        'stock_return_3m': [0.08],
        'volatility': [0.16],
        'fund_flow': [500000000]
    }),
    '美股': pd.DataFrame({...}),
    '港股': pd.DataFrame({...})
}

# 2. 检测季节
result = workflow.detect_current_season(current_data)

print("当前季节:")
for market, season_info in result['current_seasons'].items():
    print(f"  {market}: {season_info['season']} "
          f"(置信度: {season_info['confidence']:.1%})")
    print(f"    概率分布: {season_info['probabilities']}")

print("\n季节共振分析:")
alignment = result['season_alignment']
print(f"  主导季节: {alignment['dominant_season']}")
print(f"  共振强度: {alignment['strength']:.1%}")
print(f"  各市场: {alignment['market_seasons']}")

print("\n配置建议:")
print(result['allocation_suggestion'])

# 输出示例:
# 当前季节:
#   A股: 春季 (置信度: 62.3%)
#     概率分布: {'春季': 0.623, '夏季': 0.281, '秋季': 0.072, '冬季': 0.024}
#   ...
```

### 可视化季节转换

```python
import matplotlib.pyplot as plt

# 绘制季节概率时间序列
def plot_season_probabilities(detector, historical_data):
    """绘制过去3年的季节概率变化"""
    X = detector.prepare_features(historical_data)
    
    # 预测每个时间点的状态概率
    state_probs = detector.model.predict_proba(X)
    
    # 绘制
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # 子图1：概率时间序列
    for i, season in enumerate(detector.season_names):
        axes[0].plot(state_probs[:, i], label=season, linewidth=2)
    
    axes[0].set_title('季节概率时间序列')
    axes[0].set_ylabel('概率')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 子图2：最可能状态
    states = detector.model.predict(X)
    axes[1].scatter(range(len(states)), states, c=states, cmap='Set1', alpha=0.6)
    axes[1].set_yticks(range(4))
    axes[1].set_yticklabels(detector.season_names)
    axes[1].set_title('最可能季节')
    axes[1].set_xlabel('时间')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 使用
plot_season_probabilities(detector, historical_data)
```

---

## ⚙️ 配置文件

```yaml
# configs/hmm_config.yaml
model:
  n_seasons: 4
  covariance_type: 'full'
  n_iter: 100
  random_state: 42

markets:
  - name: 'A股'
    code: '000300.SH'
    data_source: 'tushare'
    
  - name: '美股'
    code: '^GSPC'
    data_source: 'yfinance'
    
  - name: '港股'
    code: '^HSI'
    data_source: 'yfinance'

features:
  macroeconomic:
    - gdp_growth
    - cpi
    - ppi
    - industrial_production
  
  monetary:
    - m2_growth
    - interest_rate_10y
    - credit_spread
    - real_interest_rate
  
  market:
    - stock_return_3m
    - stock_return_12m
    - volatility_30d
    - vix
  
  sentiment:
    - fund_flow
    - put_call_ratio
    - margin_balance

training:
  start_date: '2000-01-01'
  end_date: '2024-12-31'
  validation_split: 0.2

detection:
  update_frequency: 'monthly'  # 月度更新
  min_confidence: 0.5          # 最小置信度阈值
  alert_on_regime_change: true # 季节切换时预警
```

---

## 📊 与传统方法对比

| 指标 | 固定阈值方法 | HMM模型 |
|------|------------|---------|
| **输出** | 单一季节 | 各季节概率分布 |
| **决策依据** | 1-2个指标 | 10+个指标综合 |
| **置信度** | 无 | 量化输出 |
| **预警能力** | 事后确认 | 状态转换有过渡期 |
| **多市场** | 人工分别判断 | 自动共振分析 |
| **可解释性** | 高 | 中（需训练转移矩阵） |
| **数据需求** | 低 | 高（至少10年历史） |

---

**下一章**：[风险可视化工具](visualization.md)
