"""
风险可视化工具

实现GSRVS风格的系统性风险网络图、L4崩塌传导分析、配置可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import networkx as nx
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SystemicRiskVisualizer:
    """
    系统性风险可视化器

    实现GSRVS（Global Systemic Risk Visualizer and Simulator）风格
    的多阶段传染建模和网络可视化
    """

    def __init__(self):
        self.risk_colors = {
            '极低': '#90EE90',    # 绿色
            '低': '#98FB98',      # 浅绿
            '中': '#FFD700',      # 金色
            '高': '#FFA500',      # 橙色
            '极高': '#FF6347',    # 红色
            '危险': '#8B0000'     # 深红
        }

        self.layer_colors = {
            'L1': '#4CAF50',    # 绿色
            'L2': '#2196F3',    # 蓝色
            'L3': '#FF9800',    # 橙色
            'L4': '#F44336',    # 红色
            'L5': '#9C27B0'     # 紫色
        }

    def plot_ecosystem_network(self,
                               assets: Dict[str, Dict],
                               title: str = "生态系统网络图") -> plt.Figure:
        """
        绘制生态系统网络图

        参数:
            assets: {
                '资产名': {
                    'layer': 'L1-L5',
                    'role': '生态角色',
                    'risk_score': 风险评分(0-100)
                }
            }

        返回:
            matplotlib Figure
        """
        G = nx.DiGraph()

        # 添加节点
        for asset, info in assets.items():
            layer = info['layer']
            risk = info['risk_score']
            color = self.layer_colors[layer]

            # 风险等级
            if risk < 20:
                risk_level = '极低'
            elif risk < 40:
                risk_level = '低'
            elif risk < 60:
                risk_level = '中'
            elif risk < 80:
                risk_level = '高'
            else:
                risk_level = '极高'

            G.add_node(asset,
                       layer=layer,
                       risk_level=risk_level,
                       color=color,
                       size=300 + risk * 3)

        # 添加关系（风险传导路径）
        # L5 → L4, L4 → L3, L3 → L2, L2 → L1
        layers_order = ['L5', 'L4', 'L3', 'L2', 'L1']
        for i in range(len(layers_order) - 1):
            upper_layer = layers_order[i]
            lower_layer = layers_order[i + 1]

            for asset1, info1 in assets.items():
                if info1['layer'] == upper_layer:
                    for asset2, info2 in assets.items():
                        if info2['layer'] == lower_layer:
                            # 添加传导关系（权重基于相关性）
                            correlation = np.random.uniform(0.3, 0.9)
                            G.add_edge(asset1, asset2,
                                      weight=correlation,
                                      style='dashed',
                                      alpha=0.3)

        # 绘图
        fig, ax = plt.subplots(figsize=(14, 10))

        # 布局：按层级分层
        pos = {}
        layer_counts = {layer: 0 for layer in layers_order}
        layer_spacing = 1.5

        for node in G.nodes():
            layer = G.nodes[node]['layer']
            layer_idx = layers_order.index(layer)
            pos[node] = (
                layer_counts[layer] * 0.8,
                -layer_idx * layer_spacing
            )
            layer_counts[layer] += 1

        # 绘制节点
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        node_sizes = [G.nodes[node]['size'] for node in G.nodes()]

        nx.draw_networkx_nodes(G, pos,
                              node_color=node_colors,
                              node_size=node_sizes,
                              alpha=0.8,
                              ax=ax)

        # 绘制边
        edges = G.edges()
        edge_weights = [G[u][v]['weight'] for u, v in edges]

        nx.draw_networkx_edges(G, pos,
                              edgelist=edges,
                              width=[w * 2 for w in edge_weights],
                              alpha=0.3,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=15,
                              ax=ax)

        # 节点标签
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

        # 图例
        legend_patches = [
            mpatches.Patch(color=color, label=layer)
            for layer, color in self.layer_colors.items()
        ]
        ax.legend(handles=legend_patches, loc='upper left', title='资产层级')

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        return fig

    def plot_contagion_path(self,
                            contagion_data: Dict,
                            title: str = "L4崩塌传导路径") -> plt.Figure:
        """
        绘制L4崩塌传导路径（GSRVS风格）

        参数:
            contagion_data: {
                'path': [
                    {
                        'layer': 'L4',
                        'asset': '比特币',
                        'shock': -0.70,  # 冲击强度
                        'time': 'T+0'
                    },
                    ...
                ],
                'amplification': 传导放大倍数
            }
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        path = contagion_data['path']
        amplification = contagion_data.get('amplification', 1.0)

        # 绘制传导路径
        for i, node in enumerate(path):
            x = i
            y = node['shock'] * 100  # 转换为百分比

            # 节点
            color = self.layer_colors[node['layer']]
            ax.scatter(x, y, s=500, c=color, zorder=3)

            # 标签
            ax.text(x, y + 2,
                   f"{node['asset']}\n({node['layer']})",
                   ha='center', va='bottom', fontsize=9)

            # 时间标签
            ax.text(x, y - 5,
                   node['time'],
                   ha='center', va='top', fontsize=8, color='gray')

            # 连接箭头
            if i > 0:
                prev_node = path[i - 1]
                prev_x = i - 1
                prev_y = prev_node['shock'] * 100

                ax.annotate('',
                           xy=(x, y),
                           xytext=(prev_x, prev_y),
                           arrowprops=dict(
                               arrowstyle='->',
                               color='red',
                               lw=2,
                               connectionstyle='arc3,rad=0.2'
                           ))

                # 标注冲击强度
                mid_x = (prev_x + x) / 2
                mid_y = (prev_y + y) / 2
                shock_text = f"冲击: {node['shock']*100:.0f}%"
                ax.text(mid_x, mid_y, shock_text,
                       ha='center', va='center',
                       fontsize=8, color='red',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 添加放大倍数标注
        ax.text(0.98, 0.98,
               f"传导放大倍数: {amplification:.1f}x",
               transform=ax.transAxes,
               ha='right', va='top',
               fontsize=11,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('时间阶段', fontsize=12)
        ax.set_ylabel('价格冲击 (%)', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_portfolio_allocation(self,
                                  allocation: Dict[str, float],
                                  target_allocation: Optional[Dict[str, float]] = None,
                                  title: str = "资产配置") -> plt.Figure:
        """
        绘制资产配置饼图

        参数:
            allocation: 当前配置 {L1: 0.15, L2: 0.30, ...}
            target_allocation: 目标配置（可选，用于对比）
        """
        fig, axes = plt.subplots(1, 2 if target_allocation else 1,
                                figsize=(12 if target_allocation else 6, 6))

        if target_allocation:
            ax1, ax2 = axes
            self._plot_pie(allocation, ax1, "当前配置")
            self._plot_pie(target_allocation, ax2, "目标配置")
        else:
            ax = axes if not isinstance(axes, np.ndarray) else axes[0]
            self._plot_pie(allocation, ax, title)

        return fig

    def _plot_pie(self, allocation: Dict, ax: plt.Axes, title: str):
        """绘制饼图"""
        labels = list(allocation.keys())
        sizes = list(allocation.values())
        colors = [self.layer_colors.get(l, 'gray') for l in labels]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )

        ax.set_title(title, fontsize=12, fontweight='bold')

        # 添加图例
        ax.legend(wedges, labels,
                 title="层级",
                 loc="center left",
                 bbox_to_anchor=(1, 0, 0.5, 1))

    def plot_season_probabilities(self,
                                  probabilities: Dict[str, float],
                                  current_season: str,
                                  forecasts: List[Dict],
                                  title: str = "季节概率分布") -> plt.Figure:
        """
        绘制季节概率分布（HMM输出可视化）

        参数:
            probabilities: 当前各季节概率
            current_season: 当前季节
            forecasts: 未来预测
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        seasons = list(probabilities.keys())
        colors = [self.SEASON_COLORS[s] for s in seasons]

        # 子图1：当前概率（饼图）
        ax = axes[0]
        wedges, texts, autotexts = ax.pie(
            list(probabilities.values()),
            labels=seasons,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90
        )
        ax.set_title(f"当前: {current_season}", fontweight='bold')

        # 子图2-4：未来3个月预测
        for i, forecast in enumerate(forecasts[:3]):
            ax = axes[i + 1]
            forecast_probs = forecast['probabilities']
            bars = ax.bar(
                list(forecast_probs.keys()),
                list(forecast_probs.values()),
                color=colors,
                alpha=0.7
            )
            ax.set_title(f"{forecast['step']}个月后", fontweight='bold')
            ax.set_ylabel('概率')
            ax.set_ylim(0, 1)
            ax.grid(True, alpha=0.3)

            # 标注最高概率
            max_prob = max(forecast_probs.values())
            max_season = max(forecast_probs, key=forecast_probs.get)
            ax.text(
                list(forecast_probs.keys()).index(max_season),
                max_prob + 0.02,
                f"{max_prob:.0%}",
                ha='center',
                fontweight='bold'
            )

        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig

    def plot_l4_collapse_sequence(self,
                                   l4_data: pd.DataFrame,
                                   threshold_liquidity: float = 0.5,
                                   title: str = "L4资产崩塌序列") -> plt.Figure:
        """
        绘制L4资产崩塌的时间序列

        参数:
            l4_data: DataFrame包含日期、价格、流动性、杠杆率
            threshold_liquidity: 流动性预警阈值
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

        # 子图1：价格
        ax1 = axes[0]
        ax1.plot(l4_data.index, l4_data['price'],
                color='red', linewidth=2, label='价格')
        ax1.set_ylabel('价格', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 标注崩盘点
        if 'collapse_event' in l4_data.columns:
            collapse_points = l4_data[l4_data['collapse_event'] == True]
            ax1.scatter(collapse_points.index, collapse_points['price'],
                       color='black', s=100, zorder=5, marker='v', label='崩盘')

        # 子图2：流动性
        ax2 = axes[1]
        ax2.plot(l4_data.index, l4_data['liquidity_ratio'],
                color='blue', linewidth=2, label='流动性比率')
        ax2.axhline(y=threshold_liquidity, color='red',
                   linestyle='--', alpha=0.5, label=f'预警线({threshold_liquidity})')
        ax2.set_ylabel('流动性比率', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 子图3：杠杆率
        ax3 = axes[2]
        ax3.plot(l4_data.index, l4_data['leverage'],
                color='purple', linewidth=2, label='杠杆率')
        ax3.set_ylabel('杠杆率', fontsize=12)
        ax3.set_xlabel('日期', fontsize=12)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 填充流动性不足区域
        ax2.fill_between(l4_data.index,
                        0, l4_data['liquidity_ratio'],
                        where=l4_data['liquidity_ratio'] < threshold_liquidity,
                        alpha=0.3, color='red', label='流动性危机')

        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig

    def plot_correlation_matrix(self,
                                correlation_matrix: pd.DataFrame,
                                title: str = "资产相关性矩阵") -> plt.Figure:
        """
        绘制相关性热力图（危机时相关性会趋近1）
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        im = ax.imshow(correlation_matrix.values,
                      cmap='RdYlGn',
                      vmin=-1, vmax=1,
                      aspect='auto')

        ax.set_xticks(range(len(correlation_matrix.columns)))
        ax.set_yticks(range(len(correlation_matrix.index)))
        ax.set_xticklabels(correlation_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(correlation_matrix.index)

        # 标注数值
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix.columns)):
                value = correlation_matrix.values[i, j]
                color = 'white' if abs(value) > 0.7 else 'black'
                ax.text(j, i, f'{value:.2f}',
                       ha='center', va='center',
                       color=color, fontsize=9)

        plt.colorbar(im, ax=ax, label='相关系数')
        ax.set_title(title, fontsize=14, fontweight='bold')

        plt.tight_layout()
        return fig


# 使用示例
if __name__ == "__main__":
    visualizer = SystemicRiskVisualizer()

    # 示例1：生态系统网络图
    assets = {
        '国债': {'layer': 'L1', 'risk_score': 10},
        '货币基金': {'layer': 'L1', 'risk_score': 5},
        '国债ETF': {'layer': 'L2', 'risk_score': 15},
        '沪深300': {'layer': 'L3', 'risk_score': 50},
        'REITs': {'layer': 'L4', 'risk_score': 65},
        '比特币': {'layer': 'L4', 'risk_score': 85},
        '个股期权': {'layer': 'L5', 'risk_score': 95}
    }

    fig1 = visualizer.plot_ecosystem_network(assets)
    fig1.savefig('ecosystem_network.png', dpi=150, bbox_inches='tight')
    print("已保存: ecosystem_network.png")

    # 示例2：L4传导路径
    contagion = {
        'path': [
            {'layer': 'L4', 'asset': '比特币', 'shock': -0.70, 'time': 'T+0'},
            {'layer': 'L4', 'asset': '以太坊', 'shock': -0.65, 'time': 'T+0'},
            {'layer': 'L3', 'asset': '纳指100', 'shock': -0.15, 'time': 'T+1'},
            {'layer': 'L3', 'asset': '标普500', 'shock': -0.12, 'time': 'T+1'},
            {'layer': 'L2', 'asset': '投资级债券', 'shock': -0.03, 'time': 'T+2'},
            {'layer': 'L1', 'asset': '国债', 'shock': +0.02, 'time': 'T+3'}
        ],
        'amplification': 2.3
    }

    fig2 = visualizer.plot_contagion_path(contagion)
    fig2.savefig('contagion_path.png', dpi=150, bbox_inches='tight')
    print("已保存: contagion_path.png")

    # 示例3：配置可视化
    current = {'L1': 0.15, 'L2': 0.30, 'L3': 0.38, 'L4': 0.12, 'L5': 0.05}
    target = {'L1': 0.20, 'L2': 0.30, 'L3': 0.35, 'L4': 0.10, 'L5': 0.05}

    fig3 = visualizer.plot_portfolio_allocation(current, target)
    fig3.savefig('allocation.png', dpi=150, bbox_inches='tight')
    print("已保存: allocation.png")

    print("\n可视化完成！")
