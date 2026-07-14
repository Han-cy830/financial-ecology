# 多智能体执行层

基于TradingAgents和ai-hedge-fund的多智能体协同决策系统，用于执行金融生态学框架的配置决策。

## 🤖 智能体架构

### 核心设计理念

借鉴TradingAgents的"动态讨论"模式，构建一个专业分工、互相协作的多智能体系统：

```
战略层（生态框架）
    ↓
    ↓ "春季复苏期，建议L3股票配置40%"
    ↓
执行层（多智能体协同）
    ├─ 基本面分析师   → 筛选L3中的优质标的
    ├─ 情绪分析师     → 评估市场情绪和新闻风险
    ├─ 技术分析师     → 判断入场时机
    ├─ 风控专员       → 评估风险和仓位限制
    ├─ 交易员         → 生成具体交易指令
    └─ 组合经理       → 综合决策，最终拍板
    ↓
操作层
    └─ 执行交易、监控持仓
```

### 智能体角色定义

#### 1. 基本面分析师 (Fundamental Analyst)

**职责**：
- 计算L2-L4层资产的ROE、市赚率、估值分位
- 评估企业盈利质量和增长潜力
- 识别被低估/高估的资产

**输入**：
- 财务报表数据
- 宏观数据（GDP、通胀、利率）
- 行业景气度指标

**输出**：
- 估值报告（PE/PB分位、PEG、DCF估值）
- 盈利预测（未来1-4个季度EPS增速）
- 投资建议（买入/持有/卖出）

**示例输出**：
```json
{
  "asset": "沪深300ETF",
  "valuation": {
    "pe_percentile": 0.35,  // 35%历史分位
    "pb_percentile": 0.28,
    "roe": 0.132
  },
  "earnings_growth": {
    "next_quarter": 0.08,
    "next_year": 0.15
  },
  "recommendation": "买入",
  "target_weight": 0.25,
  "confidence": 0.75
}
```

---

#### 2. 情绪/新闻分析师 (Sentiment Analyst)

**职责**：
- 解析"气候系统"（地缘政治、政策变化）
- 监测市场情绪（VIX、社交媒体情绪、资金流向）
- 识别潜在的"黑天鹅"风险

**输入**：
- 新闻API（Bloomberg、Reuters）
- 社交媒体情绪（微博、Twitter、Reddit）
- 资金流向数据（北向资金、ETF申赎）
- 政策公告（央行、政府）

**输出**：
- 情绪指数（0-100）
- 关键风险事件清单
- 地缘政治评估

**示例输出**：
```json
{
  "market_sentiment": 0.65,
  "sentiment_trend": "改善中",
  "key_events": [
    {
      "type": "政策",
      "description": "央行降准0.5%",
      "impact": "正面",
      "magnitude": 0.7
    },
    {
      "type": "地缘政治",
      "description": "中美贸易谈判重启",
      "impact": "正面",
      "magnitude": 0.5
    }
  ],
  "geo_political_risk": 0.3,
  "recommendation": "适度乐观"
}
```

---

#### 3. 技术分析师 (Technical Analyst)

**职责**：
- 判断入场/出场时机
- 识别趋势和反转信号
- 评估短期动量

**输入**：
- 价格数据（日线、周线）
- 技术指标（MA、MACD、RSI、布林带）
- 成交量数据

**输出**：
- 趋势判断（上升/下降/震荡）
- 关键支撑/压力位
- 入场信号

**示例输出**：
```json
{
  "asset": "沪深300ETF",
  "trend": "上升",
  "momentum": {
    "rsi": 0.58,
    "macd": "金叉",
    "ma_position": "站上60日均线"
  },
  "key_levels": {
    "support": 3800,
    "resistance": 4200
  },
  "signal": "买入",
  "timing_confidence": 0.7
}
```

---

#### 4. 风控专员 (Risk Manager)

**职责**：
- 监控L4崩塌信号和地缘冲击矩阵
- 触发减仓预警
- 评估组合风险暴露

**输入**：
- 持仓数据
- 风险指标（VaR、回撤、相关性矩阵）
- 生态健康度指标
- 预警规则库

**输出**：
- 风险评分（0-100）
- 预警信号
- 减仓/清仓建议

**L4崩塌预警规则**：
```python
def check_l4_collapse_risk():
    # 触发条件
    if (流动性比率 < 0.3 or          # 流动性枯竭
        信用利差 > 500 or            # 信用环境恶化
        杠杆率 > 5.0 or              # 过度杠杆
        VIX > 35):                   # 恐慌指数飙升
        return "立即清仓L4b"
    
    elif (相关性矩阵趋近1.0 or        # 所有资产同跌
          L4单日回撤 > 10%):
        return "减仓50%L4"
    
    return "正常"
```

**示例输出**：
```json
{
  "portfolio_risk_score": 72,
  "risk_level": "中高",
  "warnings": [
    {
      "type": "L4流动性预警",
      "severity": "高",
      "description": "加密资产流动性比率降至0.25",
      "action": "建议减仓50%"
    }
  ],
  "var_95": -0.08,  // 95%VaR
  "max_drawdown_risk": -0.25,
  "portfolio_correlation": 0.65
}
```

---

#### 5. 交易员 (Executor)

**职责**：
- 将决策转化为具体交易指令
- 优化执行成本
- 考虑交易时机和流动性

**输入**：
- 目标配置权重
- 当前持仓
- 市场流动性数据
- 交易成本估算

**输出**：
- 具体买卖指令
- 执行策略（市价/限价/算法交易）
- 成本估算

**示例输出**：
```json
{
  "instructions": [
    {
      "asset": "沪深300ETF",
      "action": "买入",
      "target_weight": 0.25,
      "current_weight": 0.15,
      "amount": 100000,
      "execution": {
        "strategy": "TWAP",
        "duration": "2小时",
        "price_limit": "±0.5%"
      }
    }
  ],
  "estimated_cost": 0.0015,  // 0.15%
  "cash_needed": 100000
}
```

---

#### 6. 组合经理 (Portfolio Manager)

**职责**：
- 综合所有智能体的意见
- 做出最终决策
- 协调不同智能体的分歧

**决策机制**：

**方法1：加权投票**
```python
# 各智能体权重
weights = {
    "fundamental": 0.30,
    "sentiment":   0.20,
    "technical":   0.20,
    "risk":        0.30  # 风控拥有一票否决权
}

# 计算综合得分
final_score = sum(agent.score * weights[agent.role] for agent in agents)

# 风控否决权
if risk_manager.has_veto():
    return "否决"
```

**方法2：贝叶斯融合**
```python
# 基于历史准确率动态调整权重
# 如果基本面分析师过去3个月准确率60%，情绪分析师40%
# 则：belief = 0.6 * fundamental + 0.4 * sentiment
```

**动态讨论流程**：

```
Round 1: 各智能体独立分析
├─ 基本面分析师：建议买入股票（置信度75%）
├─ 情绪分析师：建议观望（地缘风险未解除）
├─ 技术分析师：建议买入（技术形态良好）
├─ 风控专员：无预警（风险可接受）
└─ 交易员：等待决策

Round 2: 组合经理协调分歧
├─ "基本面+技术面都看多，情绪面担忧地缘风险"
├─ "是否降低仓位至60%（而非80%）？"
└─ 各智能体投票

Round 3: 最终决策
└─ 决策：买入股票，但仓位降至60%
```

---

## 💻 代码实现

### 基础架构

```python
# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight
        self.history = []
    
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """分析数据并返回建议"""
        pass
    
    @abstractmethod
    def get_confidence(self) -> float:
        """返回当前建议的置信度"""
        pass
    
    def record_decision(self, decision: Dict, outcome: float):
        """记录决策结果（用于学习）"""
        self.history.append({
            'decision': decision,
            'outcome': outcome,
            'timestamp': datetime.now()
        })
```

### 基本面分析师实现

```python
# agents/fundamental_analyst.py
import pandas as pd
import numpy as np

class FundamentalAnalyst(BaseAgent):
    def __init__(self):
        super().__init__("基本面分析师", weight=0.30)
    
    def analyze(self, data: Dict) -> Dict:
        """
        分析资产基本面
        
        参数:
            data: {
                'pe': 市盈率,
                'pb': 市净率,
                'roe': 净资产收益率,
                'eps_growth': 盈利增速,
                'free_cash_flow': 自由现金流
            }
        """
        # 1. 估值评分
        valuation_score = self._score_valuation(data)
        
        # 2. 质量评分
        quality_score = self._score_quality(data)
        
        # 3. 成长性评分
        growth_score = self._score_growth(data)
        
        # 4. 综合评分
        composite_score = (
            0.4 * valuation_score +
            0.35 * quality_score +
            0.25 * growth_score
        )
        
        # 5. 生成建议
        if composite_score > 0.7:
            recommendation = "买入"
        elif composite_score > 0.4:
            recommendation = "持有"
        else:
            recommendation = "卖出"
        
        return {
            'role': self.name,
            'composite_score': composite_score,
            'valuation_score': valuation_score,
            'quality_score': quality_score,
            'growth_score': growth_score,
            'recommendation': recommendation,
            'target_weight': self._calculate_weight(composite_score),
            'confidence': min(composite_score * 1.2, 1.0),
            'reasoning': self._generate_reasoning(data, composite_score)
        }
    
    def _score_valuation(self, data: Dict) -> float:
        """估值评分 (0-1)"""
        pe_percentile = data.get('pe_percentile', 0.5)
        pb_percentile = data.get('pb_percentile', 0.5)
        
        # 历史分位越低，分数越高
        score = 1 - (pe_percentile * 0.6 + pb_percentile * 0.4)
        return score
    
    def _score_quality(self, data: Dict) -> float:
        """质量评分 (0-1)"""
        roe = data.get('roe', 0.10)
        
        # ROE > 15% 得满分
        score = min(roe / 0.15, 1.0)
        return score
    
    def _score_growth(self, data: Dict) -> float:
        """成长性评分 (0-1)"""
        eps_growth = data.get('eps_growth', 0.05)
        
        # 盈利增速越高越好，但超过30%不额外加分
        score = min(eps_growth / 0.30, 1.0)
        return score
    
    def _calculate_weight(self, score: float) -> float:
        """根据评分计算建议权重"""
        # 基础权重10%，最高可增加至40%
        base_weight = 0.10
        max_additional = 0.30
        return base_weight + score * max_additional
    
    def _generate_reasoning(self, data: Dict, score: float) -> str:
        """生成分析理由"""
        reasons = []
        
        if data.get('pe_percentile', 1) < 0.3:
            reasons.append(f"估值处于历史低位（{data['pe_percentile']*100:.0f}%分位）")
        
        if data.get('roe', 0) > 0.15:
            reasons.append(f"ROE优秀（{data['roe']*100:.1f}%）")
        
        if data.get('eps_growth', 0) > 0.20:
            reasons.append(f"盈利增长强劲（{data['eps_growth']*100:.1f}%）")
        
        return "；".join(reasons) if reasons else "基本面一般"
```

### 风控专员实现

```python
# agents/risk_manager.py
class RiskManager(BaseAgent):
    def __init__(self):
        super().__init__("风控专员", weight=0.30)
        self.veto_power = True  # 拥有一票否决权
    
    def analyze(self, data: Dict) -> Dict:
        """
        评估组合风险
        
        参数:
            data: {
                'current_portfolio': 当前组合,
                'proposed_allocation': 建议配置,
                'market_conditions': 市场环境,
                'l4_indicators': L4资产指标
            }
        """
        # 1. 计算组合风险指标
        var_95 = self._calculate_var(data['current_portfolio'])
        max_drawdown_risk = self._estimate_max_drawdown(data)
        correlation = self._calculate_correlation(data['current_portfolio'])
        
        # 2. 检查L4崩塌风险
        l4_risk = self._check_l4_collapse(data.get('l4_indicators', {}))
        
        # 3. 生态健康度检查
        ecosystem_health = self._check_ecosystem_health(data['current_portfolio'])
        
        # 4. 是否触发否决
        veto = self._check_veto(var_95, l4_risk, ecosystem_health)
        
        # 5. 生成风险报告
        return {
            'role': self.name,
            'has_veto': veto,
            'risk_metrics': {
                'var_95': var_95,
                'max_drawdown_risk': max_drawdown_risk,
                'portfolio_correlation': correlation
            },
            'l4_risk': l4_risk,
            'ecosystem_health': ecosystem_health,
            'recommendation': '否决' if veto else '通过',
            'adjustments': self._suggest_adjustments(var_95, l4_risk) if not veto else {},
            'confidence': 0.85
        }
    
    def _check_l4_collapse(self, l4_indicators: Dict) -> Dict:
        """检查L4崩塌风险"""
        liquidity_ratio = l4_indicators.get('liquidity_ratio', 1.0)
        leverage = l4_indicators.get('leverage', 2.0)
        daily_return = l4_indicators.get('daily_return', 0.0)
        
        # 风险等级
        if liquidity_ratio < 0.3 or daily_return < -0.10:
            level = "极高"
            action = "立即清仓L4b"
        elif liquidity_ratio < 0.5 or leverage > 5.0:
            level = "高"
            action = "减仓50%L4"
        elif liquidity_ratio < 0.7 or daily_return < -0.05:
            level = "中"
            action = "减仓25%L4"
        else:
            level = "低"
            action = "正常"
        
        return {
            'level': level,
            'action': action,
            'liquidity_ratio': liquidity_ratio,
            'leverage': leverage,
            'daily_return': daily_return
        }
    
    def _check_ecosystem_health(self, portfolio: Dict) -> Dict:
        """检查生态健康度"""
        total = sum(portfolio.values())
        
        if total == 0:
            return {'score': 0, 'status': '空仓'}
        
        # 计算各层占比
        l1_ratio = portfolio.get('L1', 0) / total
        l2_ratio = portfolio.get('L2', 0) / total
        l3_ratio = portfolio.get('L3', 0) / total
        l4_ratio = portfolio.get('L4', 0) / total
        l5_ratio = portfolio.get('L5', 0) / total
        
        # 捕食者占比
        predator_ratio = l4_ratio + l5_ratio
        
        # 猎物-捕食者比
        prey_ratio = (l1_ratio + l2_ratio) / (l4_ratio + l5_ratio) if (l4_ratio + l5_ratio) > 0 else 999
        
        # 健康度评分 (0-100)
        score = 100
        
        # 惩罚过度集中
        if predator_ratio > 0.40:
            score -= 30
        elif predator_ratio > 0.30:
            score -= 15
        
        # 惩罚流动性不足
        if l1_ratio < 0.05:
            score -= 40
        elif l1_ratio < 0.10:
            score -= 20
        
        # 惩罚猎物-捕食者比失衡
        if prey_ratio < 1.0:
            score -= 30
        elif prey_ratio < 1.5:
            score -= 15
        
        status = "健康" if score >= 70 else "警示" if score >= 50 else "危险"
        
        return {
            'score': score,
            'status': status,
            'l1_ratio': l1_ratio,
            'l2_ratio': l2_ratio,
            'l3_ratio': l3_ratio,
            'l4_ratio': l4_ratio,
            'l5_ratio': l5_ratio,
            'predator_ratio': predator_ratio,
            'prey_predator_ratio': prey_ratio
        }
    
    def _check_veto(self, var_95: float, l4_risk: Dict, ecosystem_health: Dict) -> bool:
        """检查是否触发否决"""
        # 条件1: VaR > 15%
        if var_95 < -0.15:
            return True
        
        # 条件2: L4风险极高
        if l4_risk['level'] == '极高':
            return True
        
        # 条件3: 生态健康度低于40分
        if ecosystem_health['score'] < 40:
            return True
        
        return False
```

### 组合经理实现

```python
# agents/portfolio_manager.py
class PortfolioManager:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.name: agent for agent in agents}
    
    def make_decision(self, market_data: Dict, current_portfolio: Dict) -> Dict:
        """
        综合各方意见做出最终决策
        
        流程：
        1. 各智能体独立分析
        2. 识别分歧点
        3. 第二轮讨论（针对分歧）
        4. 加权决策（风控有一票否决权）
        5. 生成最终配置建议
        """
        # Round 1: 独立分析
        opinions = {}
        for agent in self.agents.values():
            opinions[agent.name] = agent.analyze(market_data)
        
        # 识别分歧
        disagreements = self._identify_disagreements(opinions)
        
        # Round 2: 讨论分歧（如果有）
        if disagreements:
            opinions = self._discuss_disagreements(opinions, disagreements, market_data)
        
        # 综合决策
        final_decision = self._synthesize(opinions, current_portfolio)
        
        return final_decision
    
    def _synthesize(self, opinions: Dict, current_portfolio: Dict) -> Dict:
        """综合各方意见"""
        # 1. 检查风控否决权
        risk_manager = self.agents['风控专员']
        risk_opinion = opinions['风控专员']
        
        if risk_opinion['has_veto']:
            return {
                'decision': '否决',
                'reason': risk_opinion['recommendation'],
                'risk_metrics': risk_opinion['risk_metrics'],
                'suggested_adjustments': risk_opinion.get('adjustments', {})
            }
        
        # 2. 加权计算各资产的目标权重
        target_allocation = {}
        total_confidence = 0
        
        for agent_name, opinion in opinions.items():
            if agent_name == '风控专员':
                continue  # 已处理
            
            agent = self.agents[agent_name]
            weight = agent.weight * opinion['confidence']
            
            # 累加权重（需要根据意见映射到具体资产）
            # 这里简化处理：假设每个agent给出L1-L5的建议
            for layer, w in opinion.get('layer_weights', {}).items():
                target_allocation[layer] = target_allocation.get(layer, 0) + w * weight
            
            total_confidence += weight
        
        # 归一化
        if total_confidence > 0:
            target_allocation = {
                layer: w / total_confidence
                for layer, w in target_allocation.items()
            }
        
        # 3. 平滑调整（避免突变）
        smoothed_allocation = self._smooth_allocation(
            current_portfolio,
            target_allocation,
            max_change=0.15  # 单次最多调整15%
        )
        
        return {
            'decision': '执行',
            'current_allocation': current_portfolio,
            'target_allocation': target_allocation,
            'smoothed_allocation': smoothed_allocation,
            'opinions': opinions,
            'confidence': total_confidence / len(self.agents)
        }
    
    def _smooth_allocation(self, current: Dict, target: Dict, max_change: float) -> Dict:
        """平滑调整，避免单次大幅变动"""
        smoothed = {}
        total = sum(current.values()) if sum(current.values()) > 0 else 1.0
        
        for layer in set(list(current.keys()) + list(target.keys())):
            current_ratio = current.get(layer, 0) / total
            target_ratio = target.get(layer, 0)
            
            # 限制单次调整幅度
            change = target_ratio - current_ratio
            if abs(change) > max_change:
                change = max_change * (1 if change > 0 else -1)
            
            smoothed[layer] = current_ratio + change
        
        # 重新归一化
        total_smoothed = sum(smoothed.values())
        smoothed = {k: v / total_smoothed for k, v in smoothed.items()}
        
        return smoothed
```

---

## 🔄 动态讨论示例

### 场景：2026年春季复苏期

**背景**：
- 判断当前处于春季复苏期
- 生态框架建议：L3股票40%，L2债券30%，L1现金15%，L4另类10%，L5投机5%

**智能体讨论**：

**Round 1: 独立分析**

```
基本面分析师：
  沪深300估值分位35%，ROE 13%，盈利增速15% → 建议L3配置35%（置信度75%）

情绪分析师：
  北向资金连续3周净流入，VIX从20降至15 → 市场情绪改善 → 建议L3配置45%

技术分析师：
  沪深300站上60日均线，MACD金叉 → 技术面看多 → 建议L3配置45%

风控专员：
  L4（加密资产）流动性比率0.45，处于警戒 → 建议L4b从5%降至2%
  生态健康度72分 → 正常

交易员：
  等待最终决策
```

**Round 2: 组合经理协调**

```
组合经理："基本面和技术面都支持高配L3，但情绪面担忧地缘风险。
          是否将L3从40%降至38%，预留部分现金？"

情绪分析师："同意，中美关系存在不确定性。"

基本面分析师："可以，估值不算贵，留10%现金观望。"

风控专员："同意，生态健康度仍将保持在70分以上。"
```

**Round 3: 最终决策**

```
最终配置：
L1 现金:   15%
L2 债券:   30%
L3 股票:   38%  ← 从40%略降
L4 另类:   12%  （L4a 10%, L4b 2%）
L5 投机:    5%

执行指令：
- 买入沪深300ETF 23万（从15%→38%）
- 维持债券配置
- 加密资产减仓60%（从5%→2%）
```

---

## 🛠️ 使用示例

```python
from agents import PortfolioManager, FundamentalAnalyst, SentimentAnalyst, \
                 TechnicalAnalyst, RiskManager, Executor

# 1. 创建智能体
agents = [
    FundamentalAnalyst(),
    SentimentAnalyst(),
    TechnicalAnalyst(),
    RiskManager(),
    Executor()
]

# 2. 创建组合经理
pm = PortfolioManager(agents)

# 3. 准备市场数据
market_data = {
    # 基本面数据
    'pe_percentile': 0.35,
    'pb_percentile': 0.28,
    'roe': 0.132,
    'eps_growth': 0.15,
    
    # 情绪数据
    'market_sentiment': 0.65,
    'northbound_flow': 500000000,  # 北向资金50亿
    'vix': 15.0,
    
    # 技术数据
    'trend': '上升',
    'rsi': 0.58,
    'macd': '金叉',
    
    # L4指标
    'l4_indicators': {
        'liquidity_ratio': 0.45,
        'leverage': 3.2,
        'daily_return': -0.02
    }
}

# 4. 当前组合
current_portfolio = {
    'L1': 0.20,
    'L2': 0.35,
    'L3': 0.30,
    'L4': 0.12,
    'L5': 0.03
}

# 5. 获取决策
decision = pm.make_decision(market_data, current_portfolio)

print(decision)
# 输出:
# {
#     'decision': '执行',
#     'target_allocation': {...},
#     'smoothed_allocation': {...},
#     ...
# }
```

---

**下一章**：[HMM季节检测模型](hmm-season-detector.md)
