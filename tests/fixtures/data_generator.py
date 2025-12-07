#!/usr/bin/env python3
"""
测试数据生成器
提供各种测试数据的生成函数
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json


def generate_stock_kline_data(days=252, start_price=100.0, symbol='000001'):
    """生成股票K线数据

    Args:
        days: 交易天数
        start_price: 起始价格
        symbol: 股票代码

    Returns:
        DataFrame with OHLCV data
    """
    # 生成日期序列
    end_date = datetime.now()
    dates = pd.date_range(end=end_date, periods=days, freq='D')
    dates = dates[dates.weekday < 5]  # 只保留工作日
    dates = dates[-days:]  # 取最近的天数

    # 生成价格序列
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = start_price * np.exp(np.cumsum(returns))

    # 生成OHLC数据
    data = {
        'datetime': dates,
        'open': prices * (1 + np.random.normal(0, 0.005, len(dates))),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, len(dates)))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, len(dates)))),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, len(dates)),
        'symbol': symbol
    }

    return pd.DataFrame(data)


def generate_technical_indicators(df):
    """生成技术指标数据

    Args:
        df: K线数据DataFrame

    Returns:
        dict: 技术指标数据
    """
    closes = df['close'].values

    # 移动平均线
    ma5 = np.mean(closes[-5:])
    ma10 = np.mean(closes[-10:])
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else np.mean(closes)

    # RSI (简化计算)
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else np.mean(gains)
    avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else np.mean(losses)

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # MACD (简化计算)
    ema12 = closes[-12:].mean() if len(closes) >= 12 else closes.mean()
    ema26 = closes[-26:].mean() if len(closes) >= 26 else closes.mean()
    macd = ema12 - ema26
    signal = macd * 0.9
    histogram = macd - signal

    # KDJ (简化计算)
    high_9 = df['high'][-9:].max()
    low_9 = df['low'][-9:].min()
    close_9 = closes[-1]

    rsv = (close_9 - low_9) / (high_9 - low_9) * 100 if high_9 != low_9 else 50
    k = rsv * (1/3) + 50 * (2/3)  # 简化计算
    d = k * (1/3) + 50 * (2/3)
    j = 3 * k - 2 * d

    return {
        'MA5': round(ma5, 2),
        'MA10': round(ma10, 2),
        'MA20': round(ma20, 2),
        'MA60': round(ma60, 2),
        'RSI': round(rsi, 2),
        'MACD': round(macd, 4),
        'Signal': round(signal, 4),
        'Histogram': round(histogram, 4),
        'K': round(k, 2),
        'D': round(d, 2),
        'J': round(j, 2)
    }


def generate_market_sentiment_data(days=30):
    """生成市场情绪数据

    Args:
        days: 天数

    Returns:
        list: 新闻数据列表
    """
    sentiments = ['positive', 'neutral', 'negative']
    sentiment_weights = [0.4, 0.4, 0.2]  # 积极和中性新闻较多

    titles = [
        "市场大幅上涨，投资者信心增强",
        "经济数据超预期，股市迎来上涨行情",
        "政策利好频出，相关板块表现活跃",
        "外资持续流入，A股市场受青睐",
        "技术面走强，指数突破关键阻力位",
        "市场震荡调整，投资者观望情绪浓厚",
        "获利盘出逃，指数出现回调",
        "不确定性增加，市场风险偏好下降"
    ]

    news_list = []
    for i in range(days * 10):  # 每天10条新闻
        sentiment = np.random.choice(sentiments, p=sentiment_weights)

        # 根据情绪调整影响分数
        if sentiment == 'positive':
            impact_score = np.random.uniform(6, 10)
        elif sentiment == 'neutral':
            impact_score = np.random.uniform(3, 7)
        else:
            impact_score = np.random.uniform(0, 4)

        news = {
            'title': random.choice(titles),
            'content': f"这是第{i+1}条新闻的内容，市场情绪为{sentiment}",
            'sentiment': sentiment,
            'impact_score': round(impact_score, 1),
            'timestamp': datetime.now() - timedelta(hours=i)
        }

        news_list.append(news)

    return news_list


def generate_stock_fundamental_data():
    """生成股票基本面数据"""
    return {
        'pe_ratio': round(np.random.uniform(5, 50), 2),
        'pb_ratio': round(np.random.uniform(0.5, 10), 2),
        'roe': round(np.random.uniform(0, 30), 2),
        'roa': round(np.random.uniform(0, 15), 2),
        'eps': round(np.random.uniform(0.5, 5), 2),
        'bps': round(np.random.uniform(5, 50), 2),
        'market_cap': round(np.random.uniform(100, 5000), 2),  # 亿元
        'dividend_yield': round(np.random.uniform(0, 5), 2),
        'debt_ratio': round(np.random.uniform(10, 70), 2),
        'current_ratio': round(np.random.uniform(0.5, 3), 2),
        'revenue_growth': round(np.random.uniform(-10, 50), 2),
        'profit_growth': round(np.random.uniform(-20, 100), 2)
    }


def generate_market_overview_data():
    """生成市场概览数据"""
    indices = ['上证指数', '深证成指', '沪深300', '中证500', '创业板指']
    index_data = {}

    for index in indices:
        base_value = {
            '上证指数': 3200,
            '深证成指': 11000,
            '沪深300': 3800,
            '中证500': 5500,
            '创业板指': 2100
        }

        base = base_value[index]
        change_percent = np.random.uniform(-3, 3)
        current_value = base * (1 + change_percent / 100)

        index_data[index] = {
            'value': round(current_value, 2),
            'change': round(current_value - base, 2),
            'change_percent': round(change_percent, 2),
            'volume': np.random.randint(100000000, 500000000),  # 成交量
            'turnover': np.random.randint(1000000000, 5000000000)  # 成交额
        }

    # 市场情绪
    fear_greed_index = round(np.random.uniform(0, 100), 1)

    # 涨跌统计
    total_stocks = 5000
    up_stocks = int(total_stocks * np.random.uniform(0.3, 0.7))
    down_stocks = total_stocks - up_stocks

    # 资金流向
    northbound_flow = round(np.random.uniform(-100, 100), 2)  # 亿元
    main_flow = round(np.random.uniform(-200, 200), 2)  # 亿元

    return {
        'indices': index_data,
        'market_sentiment': {
            'fear_greed_index': fear_greed_index,
            'sentiment_text': '贪婪' if fear_greed_index > 50 else '恐惧',
            'up_stocks': up_stocks,
            'down_stocks': down_stocks,
            'limit_up': np.random.randint(10, 100),
            'limit_down': np.random.randint(0, 20)
        },
        'money_flow': {
            'northbound': northbound_flow,
            'main': main_flow,
            'super_large': round(np.random.uniform(-100, 100), 2),
            'large': round(np.random.uniform(-100, 100), 2),
            'medium': round(np.random.uniform(-50, 50), 2),
            'small': round(np.random.uniform(-50, 50), 2)
        }
    }


def generate_ai_analysis_report(entity_type='stock', entity_name='平安银行'):
    """生成AI分析报告

    Args:
        entity_type: 实体类型 ('stock' 或 'market')
        entity_name: 实体名称

    Returns:
        str: AI生成的分析报告
    """
    if entity_type == 'stock':
        templates = [
            f"## {entity_name}技术面分析\n\n从技术指标来看，该股票目前处于上升趋势中。MACD金叉形成，RSI指标处于强势区域，建议关注后续走势。",
            f"## {entity_name}基本面分析\n\n公司基本面稳健，盈利能力良好。PE估值处于合理区间，具备长期投资价值。",
            f"## {entity_name}新闻面分析\n\n近期利好消息较多，市场关注度提升。需关注后续政策变化和行业动态。",
            f"## {entity_name}筹码分析\n\n筹码集中度较高，主力资金控盘迹象明显。成交量温和放大，资金流向积极。",
            f"## {entity_name}综合分析\n\n综合各方面因素，该股票短期内有上涨空间，建议逢低介入，注意控制风险。"
        ]
    else:
        templates = [
            f"## 市场整体分析\n\n当前市场情绪{np.random.choice(['乐观', '谨慎', '中性'])}，指数{np.random.choice(['震荡上行', '区间震荡', '弱势调整'])}。",
            f"## 技术面分析\n\n主要指数{np.random.choice(['突破关键阻力位', '获得支撑', '承压回调'])}，技术形态{np.random.choice(['向好', '中性', '偏弱'])}。",
            f"## 资金面分析\n\n北向资金{np.random.choice(['持续流入', '小幅流出', '进出平衡'])}，市场{np.random.choice(['活跃度提升', '交投清淡', '分化明显'])}。",
            f"## 操作建议\n\n建议投资者{np.random.choice(['保持谨慎', '积极布局', '控制仓位'])}，重点关注{np.random.choice(['优质成长股', '低估值蓝筹', '热点题材板块'])}。"
        ]

    return np.random.choice(templates)


def save_test_data():
    """保存测试数据到文件"""
    # 生成并保存股票数据
    stock_data = generate_stock_kline_data()
    stock_data.to_json('tests/fixtures/sample_stock_data.json', orient='records', date_format='iso')

    # 生成并保存技术指标
    tech_data = generate_technical_indicators(stock_data)
    with open('tests/fixtures/sample_technical_data.json', 'w', encoding='utf-8') as f:
        json.dump(tech_data, f, ensure_ascii=False, indent=2)

    # 生成并保存市场数据
    market_data = generate_market_overview_data()
    with open('tests/fixtures/sample_market_data.json', 'w', encoding='utf-8') as f:
        json.dump(market_data, f, ensure_ascii=False, indent=2)

    # 生成并保存新闻数据
    news_data = generate_market_sentiment_data()
    with open('tests/fixtures/sample_news_data.json', 'w', encoding='utf-8') as f:
        json.dump(news_data[:100], f, ensure_ascii=False, indent=2)  # 只保存100条

    print("测试数据已生成并保存到 tests/fixtures/ 目录")


if __name__ == "__main__":
    save_test_data()