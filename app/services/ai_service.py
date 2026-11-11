import re
from typing import Dict, Any, List

class AIService:
    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, Any]:
        """Быстрый лексико-статистический анализ тональности текста (рус/англ)."""
        positive_keywords = {
            "интересно", "согласны", "отлично", "готовы", "купить", "подписать", "договор",
            "нравится", "бюджет", "утвердили", "great", "interested", "deal", "approved", "ready"
        }
        negative_keywords = {
            "дорого", "отказ", "не подходит", "позже", "передумали", "конкуренты",
            "проблема", "долго", "нет", "expensive", "cancel", "rejected", "problem", "delayed"
        }

        tokens = re.findall(r'\w+', text.lower())
        pos_count = sum(1 for t in tokens if t in positive_keywords)
        neg_count = sum(1 for t in tokens if t in negative_keywords)

        total = pos_count + neg_count
        if total == 0:
            return {"sentiment": "neutral", "score": 0.0}
        
        score = round((pos_count - neg_count) / max(total, 1), 2)
        if score > 0.15:
            sentiment = "positive"
        elif score < -0.15:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {"sentiment": sentiment, "score": score}

    @staticmethod
    def score_deal(amount: float, stage: str, company_size: int, sentiment_scores: List[float]) -> Dict[str, Any]:
        """
        Интеллектуальная оценка сделки (Lead Scoring & Win Probability).
        Учитывает финансовый объем, стадию воронки, размер компании и среднюю тональность коммуникации.
        """
        base_scores = {
            "new": 20.0,
            "qualification": 40.0,
            "proposal": 65.0,
            "negotiation": 80.0,
            "closed_won": 100.0,
            "closed_lost": 0.0
        }

        score = base_scores.get(stage.lower(), 25.0)

        # Фактор размера компании (B2B сегментация)
        if company_size >= 100:
            score += 10.0
        elif company_size >= 20:
            score += 5.0

        # Фактор объема сделки
        if amount > 500000:
            score += 5.0
        elif amount <= 0:
            score -= 15.0

        # Фактор тональности общения
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        score += avg_sentiment * 15.0

        # Нормализация скора от 0 до 100
        score = max(0.0, min(100.0, round(score, 1)))
        win_probability = round(score / 100.0, 2)

        # Оценка рисков и Next Best Action
        insights = []
        if stage == "negotiation" and win_probability > 0.75:
            action = "Отправить финальный счет и проект договора на подписание."
            risk = "Low"
            insights.append("Высокая вовлеченность клиента, сделка на финальной стадии.")
        elif avg_sentiment < -0.1:
            action = "Организовать срочный звонок с техническим экспертом / тимлидом."
            risk = "High"
            insights.append("Зафиксированы возражения или негативный контекст в последних беседах.")
        elif stage == "proposal":
            action = "Запросить обратную связь по отправленному коммерческому предложению."
            risk = "Medium"
            insights.append("Ожидается валидация условий лицом, принимающим решения.")
        else:
            action = "Провести квалификационный бриф и выявить ключевые боли клиента."
            risk = "Medium"
            insights.append("Необходимо детализировать технические требования.")

        return {
            "lead_score": score,
            "win_probability": win_probability,
            "risk_level": risk,
            "recommended_action": action,
            "insights": insights
        }
