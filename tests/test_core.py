import pytest
import numpy as np
import pandas as pd
import sys, os, importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestAssetClassifier:
    def setup_method(self):
        from src.ecosystem.asset_classifier import AssetClassifier
        self.clf = AssetClassifier()

    def test_treasury(self):
        r = self.clf.classify(name='Guokai', volatility=0.08, cash_flow_positive=True,
            correlation_with_stocks=0.1, leverage_ratio=1.0, liquidity_score=0.95)
        assert r['role'] == '猎物'

    def test_stock_index(self):
        r = self.clf.classify(name='CSI300', volatility=0.25, cash_flow_positive=True,
            correlation_with_stocks=0.98, leverage_ratio=1.0, liquidity_score=0.90)
        assert r['role'] == '价值创造者'

    def test_bitcoin(self):
        r = self.clf.classify(name='BTC', volatility=0.80, cash_flow_positive=False,
            correlation_with_stocks=0.30, leverage_ratio=2.0, liquidity_score=0.85,
            regulatory_status='semi_regulated')
        assert r['role'] == '纯投机捕食者'

    def test_batch(self):
        assets = [dict(name='A', volatility=0.08, cash_flow_positive=True,
            correlation_with_stocks=0.1, leverage_ratio=1.0, liquidity_score=0.95)]
        df = self.clf.batch_classify(assets)
        assert len(df) == 1

    def test_guidance(self):
        r = self.clf.classify(name='T', volatility=0.1, cash_flow_positive=True,
            correlation_with_stocks=0.2, leverage_ratio=1.0, liquidity_score=0.9)
        assert 'allocation_guidance' in r


class TestAllocationCalculator:
    def setup_method(self):
        mod = importlib.import_module('tools.allocation-calculator.allocation_calculator')
        self.calc = mod.AllocationCalculator()

    def test_keys(self):
        r = self.calc.calculate(season='春季', risk_preference='moderate', total_capital=1000000)
        assert 'allocation' in r

    def test_sums(self):
        seasons = ['春季', '夏季', '秋季', '冬季']
        for s in seasons:
            for risk in ['conservative','moderate','aggressive']:
                r = self.calc.calculate(season=s, risk_preference=risk)
                assert abs(sum(r['allocation'].values()) - 1.0) < 0.01

    def test_sharpe(self):
        r = self.calc.calculate(season='春季', risk_preference='moderate')
        assert r['sharpe_ratio'] > 0

    def test_invalid(self):
        with pytest.raises(ValueError):
            self.calc.calculate(season='invalid', risk_preference='moderate')


class TestRiskManager:
    def setup_method(self):
        from src.agents.risk_manager import RiskManager
        self.rm = RiskManager()

    def test_no_veto(self):
        data = dict(portfolio=dict(L1=0.4,L2=0.35,L3=0.2,L4=0.03,L5=0.02),
            l4_indicators=dict(liquidity_ratio=0.8,leverage=1.5,daily_return=0.01),
            market_conditions=dict(vix=15,credit_spread=0.01,market_sentiment=70))
        assert self.rm.analyze(data)['has_veto'] is False

    def test_veto_l4(self):
        data = dict(portfolio=dict(L1=0.1,L2=0.2,L3=0.3,L4=0.35,L5=0.05),
            l4_indicators=dict(liquidity_ratio=0.05,leverage=10.0,daily_return=-0.2),
            market_conditions=dict(vix=50,credit_spread=0.08,market_sentiment=10))
        assert self.rm.analyze(data)['has_veto'] is True

    def test_var_negative(self):
        data = dict(portfolio=dict(L1=0.3,L2=0.3,L3=0.25,L4=0.1,L5=0.05),
            l4_indicators=dict(liquidity_ratio=0.5,leverage=2.0,daily_return=0.0),
            market_conditions=dict(vix=20,credit_spread=0.02,market_sentiment=50))
        assert self.rm.analyze(data)['key_metrics']['var_95'] < 0

    def test_no_alerts_crash(self):
        data = dict(portfolio=dict(L1=0.2,L2=0.3,L3=0.3,L4=0.15,L5=0.05),
            l4_indicators=dict(liquidity_ratio=0.5,leverage=2.0,daily_return=-0.03),
            market_conditions=dict(vix=25,credit_spread=0.02,market_sentiment=45))
        r = self.rm.analyze(data)
        assert isinstance(r['risk_alerts'], list)
