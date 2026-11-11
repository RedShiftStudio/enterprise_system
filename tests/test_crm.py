import pytest
from app.services.ai_service import AIService

def test_sentiment_positive():
    text = "Клиенты очень довольны, готовы купить решение и подписать договор!"
    res = AIService.analyze_sentiment(text)
    assert res["sentiment"] == "positive"
    assert res["score"] > 0

def test_sentiment_negative():
    text = "Слишком дорого, отказ от сделки, появились серьезные проблемы."
    res = AIService.analyze_sentiment(text)
    assert res["sentiment"] == "negative"
    assert res["score"] < 0

def test_lead_scoring():
    res = AIService.score_deal(amount=600000, stage="negotiation", company_size=120, sentiment_scores=[0.8, 0.5])
    assert res["lead_score"] > 80
    assert res["win_probability"] > 0.8
    assert res["risk_level"] == "Low"
