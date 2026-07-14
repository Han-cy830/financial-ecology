"""
季节判断问卷 - 交互式工具

帮助用户判断当前市场季节
"""

from typing import Dict, List, Tuple
import json


class SeasonQuestionnaire:
    """
    交互式季节判断问卷

    通过10个核心问题，综合判断当前市场季节
    """

    def __init__(self):
        self.questions = self._load_questions()
        self.weights = self._load_weights()

    def _load_questions(self) -> List[Dict]:
        """加载问卷问题"""
        return [
            {
                'id': 'gdp_growth',
                'question': 'GDP增速如何？',
                'options': [
                    {'text': '明显负增长（<-2%）', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.2, '冬季': 0.7}},
                    {'text': '轻微负增长或接近零（-2%~0%）', 'scores': {'春季': 0.4, '夏季': 0, '秋季': 0.3, '冬季': 0.3}},
                    {'text': '温和正增长（0%~5%）', 'scores': {'春季': 0.6, '夏季': 0.3, '秋季': 0.3, '冬季': 0}},
                    {'text': '强劲正增长（>5%）', 'scores': {'春季': 0.1, '夏季': 0.7, '秋季': 0, '冬季': 0}}
                ]
            },
            {
                'id': 'inflation',
                'question': '通胀水平如何？',
                'options': [
                    {'text': '严重通胀（>8%）', 'scores': {'春季': 0, '夏季': 0.1, '秋季': 0.7, '冬季': 0.2}},
                    {'text': '较高通胀（4%~8%）', 'scores': {'春季': 0.1, '夏季': 0.2, '秋季': 0.6, '冬季': 0.1}},
                    {'text': '温和通胀（1%~4%）', 'scores': {'春季': 0.3, '夏季': 0.5, '秋季': 0.1, '冬季': 0.1}},
                    {'text': '低通胀或通缩（<1%）', 'scores': {'春季': 0.2, '夏季': 0, '秋季': 0.1, '冬季': 0.7}}
                ]
            },
            {
                'id': 'monetary_policy',
                'question': '央行货币政策？',
                'options': [
                    {'text': '持续加息或QT（缩表）', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.7, '冬季': 0.2}},
                    {'text': '暂停加息或观望', 'scores': {'春季': 0.2, '夏季': 0.1, '秋季': 0.5, '冬季': 0.2}},
                    {'text': '开始降息或QE', 'scores': {'春季': 0.5, '夏季': 0.2, '秋季': 0.1, '冬季': 0.2}},
                    {'text': '大幅降息或无限QE', 'scores': {'春季': 0.3, '夏季': 0.5, '秋季': 0, '冬季': 0.2}}
                ]
            },
            {
                'id': 'corporate_earnings',
                'question': '企业盈利情况？',
                'options': [
                    {'text': '普遍负增长', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.3, '冬季': 0.6}},
                    {'text': '增长乏力（<5%）', 'scores': {'春季': 0.3, '夏季': 0, '秋季': 0.5, '冬季': 0.2}},
                    {'text': '温和增长（5%~15%）', 'scores': {'春季': 0.5, '夏季': 0.4, '秋季': 0.1, '冬季': 0}},
                    {'text': '强劲增长（>15%）', 'scores': {'春季': 0.1, '夏季': 0.6, '秋季': 0, '冬季': 0}}
                ]
            },
            {
                'id': 'market_sentiment',
                'question': '市场情绪如何？',
                'options': [
                    {'text': '极度恐慌（VIX>40）', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.2, '冬季': 0.7}},
                    {'text': '谨慎悲观（VIX 25-40）', 'scores': {'春季': 0.3, '夏季': 0, '秋季': 0.4, '冬季': 0.3}},
                    {'text': '中性（VIX 15-25）', 'scores': {'春季': 0.5, '夏季': 0.2, '秋季': 0.3, '冬季': 0}},
                    {'text': '乐观（VIX<15）', 'scores': {'春季': 0.2, '夏季': 0.6, '秋季': 0.1, '冬季': 0.1}}
                ]
            },
            {
                'id': 'stock_market',
                'question': '股市表现如何？',
                'options': [
                    {'text': '持续下跌（3个月收益<-20%）', 'scores': {'春季': 0, '夏季': 0, '秋季': 0.2, '冬季': 0.8}},
                    {'text': '震荡走弱（-20%~0%）', 'scores': {'春季': 0.3, '夏季': 0, '秋季': 0.5, '冬季': 0.2}},
                    {'text': '温和上涨（0%~20%）', 'scores': {'春季': 0.5, '夏季': 0.4, '秋季': 0.2, '冬季': 0}},
                    {'text': '强劲上涨（>20%）', 'scores': {'春季': 0.2, '夏季': 0.7, '秋季': 0, '冬季': 0}}
                ]
            },
            {
                'id': 'liquidity',
                'question': '市场流动性如何？',
                'options': [
                    {'text': '极度紧张（流动性危机）', 'scores': {'春季': 0, '夏季': 0, '秋季': 0.2, '冬季': 0.8}},
                    {'text': '较为紧张', 'scores': {'春季': 0.2, '夏季': 0, '秋季': 0.6, '冬季': 0.2}},
                    {'text': '正常', 'scores': {'春季': 0.4, '夏季': 0.3, '秋季': 0.3, '冬季': 0}},
                    {'text': '充裕', 'scores': {'春季': 0.3, '夏季': 0.5, '秋季': 0.1, '冬季': 0.1}}
                ]
            },
            {
                'id': 'employment',
                'question': '就业市场如何？',
                'options': [
                    {'text': '失业率大幅上升', 'scores': {'春季': 0.2, '夏季': 0, '秋季': 0.3, '冬季': 0.5}},
                    {'text': '失业率上升', 'scores': {'春季': 0.4, '夏季': 0, '秋季': 0.4, '冬季': 0.2}},
                    {'text': '稳定', 'scores': {'春季': 0.5, '夏季': 0.3, '秋季': 0.2, '冬季': 0}},
                    {'text': '强劲', 'scores': {'春季': 0.1, '夏季': 0.6, '秋季': 0.1, '冬季': 0.2}}
                ]
            },
            {
                'id': 'credit_condition',
                'question': '信贷环境如何？',
                'options': [
                    {'text': '信贷紧缩', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.4, '冬季': 0.5}},
                    {'text': '信贷趋紧', 'scores': {'春季': 0.3, '夏季': 0.1, '秋季': 0.5, '冬季': 0.1}},
                    {'text': '正常', 'scores': {'春季': 0.5, '夏季': 0.3, '秋季': 0.2, '冬季': 0}},
                    {'text': '宽松', 'scores': {'春季': 0.3, '夏季': 0.5, '秋季': 0.1, '冬季': 0.1}}
                ]
            },
            {
                'id': 'geopolitical',
                'question': '地缘政治环境？',
                'options': [
                    {'text': '严重冲突升级', 'scores': {'春季': 0.1, '夏季': 0, '秋季': 0.3, '冬季': 0.6}},
                    {'text': '局部冲突或紧张', 'scores': {'春季': 0.3, '夏季': 0.1, '秋季': 0.4, '冬季': 0.2}},
                    {'text': '相对稳定', 'scores': {'春季': 0.4, '夏季': 0.4, '秋季': 0.2, '冬季': 0}},
                    {'text': '和平合作', 'scores': {'春季': 0.3, '夏季': 0.5, '秋季': 0.1, '冬季': 0.1}}
                ]
            }
        ]

    def _load_weights(self) -> Dict[str, float]:
        """加载各问题权重"""
        return {
            'gdp_growth': 1.5,          # GDP权重最高
            'inflation': 1.3,
            'corporate_earnings': 1.2,
            'monetary_policy': 1.1,
            'market_sentiment': 1.0,
            'stock_market': 1.0,
            'liquidity': 1.0,
            'credit_condition': 0.9,
            'employment': 0.8,
            'geopolitical': 0.7
        }

    def run_interactive(self) -> Dict:
        """交互式问卷"""
        print("\n" + "=" * 60)
        print("金融生态学 - 市场季节判断问卷")
        print("=" * 60)
        print("\n请根据当前市场状况，选择最符合的选项。\n")

        scores = {'春季': 0, '夏季': 0, '秋季': 0, '冬季': 0}

        for q in self.questions:
            print(f"\n问题{q['id']}: {q['question']}")
            for i, opt in enumerate(q['options'], 1):
                print(f"  {i}. {opt['text']}")

            while True:
                try:
                    choice = int(input("\n请选择 (1-4): ")) - 1
                    if 0 <= choice < len(q['options']):
                        break
                    else:
                        print("请输入1-4之间的数字")
                except ValueError:
                    print("请输入有效的数字")

            selected = q['options'][choice]
            weight = self.weights[q['id']]

            for season, score in selected['scores'].items():
                scores[season] += score * weight

            print(f"✓ 已记录")

        # 计算结果
        total = sum(scores.values())
        probabilities = {season: score / total for season, score in scores.items()}

        # 找出最可能季节
        dominant_season = max(probabilities, key=probabilities.get)
        confidence = probabilities[dominant_season]

        # 输出结果
        print("\n" + "=" * 60)
        print("问卷结果")
        print("=" * 60)

        print("\n各季节概率:")
        for season, prob in sorted(probabilities.items(), key=lambda x: -x[1]):
            bar = '█' * int(prob * 50)
            print(f"  {season}: {prob:6.1%} {bar}")

        print(f"\n诊断结果: {dominant_season}")
        print(f"置信度: {confidence:.1%}")

        # 提供建议
        self._print_recommendation(dominant_season, confidence)

        return {
            'season': dominant_season,
            'probabilities': probabilities,
            'confidence': confidence
        }

    def _print_recommendation(self, season: str, confidence: float):
        """打印配置建议"""
        recommendations = {
            '春季': {
                'description': '经济复苏，风险资产开始回暖',
                'allocation': 'L3股票40%, L2债券30%, L1现金15%, L4另类10%, L5投机5%',
                'action': '逐步从L2转向L3，保持一定流动性'
            },
            '夏季': {
                'description': '经济繁荣，市场乐观',
                'allocation': 'L3股票45%, L4另类20%, L2债券20%, L1现金10%, L5投机5%',
                'action': '重仓股票，积极参与L4，保持适度杠杆'
            },
            '秋季': {
                'description': '滞胀环境，增长放缓通胀高企',
                'allocation': 'L2债券35%, L1现金25%, L3股票25%, L4另类10%, L5投机5%',
                'action': '降低L3/L4仓位，增加L1/L2防御'
            },
            '冬季': {
                'description': '经济衰退，现金为王',
                'allocation': 'L1现金40%, L2债券35%, L3股票15%, L4另类5%, L5投机5%',
                'action': '大量持有现金，等待机会，不要抄底'
            }
        }

        print(f"\n季节特征: {recommendations[season]['description']}")
        print(f"参考配置: {recommendations[season]['allocation']}")
        print(f"操作建议: {recommendations[season]['action']}")

        if confidence < 0.5:
            print("\n⚠️  注意: 置信度较低，建议使用HMM模型进一步验证")

    def calculate_score(self, answers: Dict[str, int]) -> Dict:
        """
        批量计算季节分数（用于自动化）

        参数:
            answers: {问题ID: 选项索引(1-4)}

        返回:
            {
                'season': 季节,
                'probabilities': 概率分布,
                'confidence': 置信度
            }
        """
        scores = {'春季': 0, '夏季': 0, '秋季': 0, '冬季': 0}

        for question in self.questions:
            q_id = question['id']
            if q_id in answers:
                choice_idx = answers[q_id] - 1
                if 0 <= choice_idx < len(question['options']):
                    selected = question['options'][choice_idx]
                    weight = self.weights[q_id]

                    for season, score in selected['scores'].items():
                        scores[season] += score * weight

        total = sum(scores.values())
        probabilities = {season: score / total for season, score in scores.items()}
        dominant_season = max(probabilities, key=probabilities.get)
        confidence = probabilities[dominant_season]

        return {
            'season': dominant_season,
            'probabilities': probabilities,
            'confidence': confidence
        }


# 使用示例
if __name__ == "__main__":
    questionnaire = SeasonQuestionnaire()

    # 交互式运行
    result = questionnaire.run_interactive()

    print("\n" + "=" * 60)
    print("最终结果")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
