"""
Модуль штучного інтелекту для генерації резюме текстів.
Використовує Hugging Face Inference API для summarization.

Для використання потрібно:
1. Зареєструватися на https://huggingface.co
2. Створити API токен: Settings → Access Tokens → New token
3. Додати токен у змінні оточення: HUGGINGFACE_API_TOKEN
"""
import os
from typing import Optional

import requests


class AISummarizer:
    """
    Клас для генерації коротких резюме текстів за допомогою Hugging Face API.
    Використовує модель facebook/bart-large-cnn для англійської мови
    та інші моделі для багатомовної підтримки.
    """

    # Модель для англійської мови (безкоштовна, не потребує API ключа для публічних моделей)
    DEFAULT_MODEL = "facebook/bart-large-cnn"
    
    # Альтернативна модель для багатомовної підтримки
    MULTILINGUAL_MODEL = "facebook/mbart-large-50-many-to-many-mmt"

    def __init__(self, api_token: Optional[str] = None, model: Optional[str] = None):
        """
        Ініціалізація summarizer.
        
        Args:
            api_token: Hugging Face API token (рекомендовано для стабільності)
            model: Назва моделі (за замовчуванням: facebook/bart-large-cnn)
        """
        self.api_token = api_token or os.getenv("HUGGINGFACE_API_TOKEN")
        self.model = model or os.getenv("HUGGINGFACE_MODEL", self.DEFAULT_MODEL)
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Попередження, якщо токен не вказано (для production)
        if not self.api_token and os.getenv("FLASK_ENV") == "production":
            print(
                "WARNING: HUGGINGFACE_API_TOKEN не вказано. "
                "API може працювати повільніше або з обмеженнями."
            )

    def summarize(
        self, 
        text: str, 
        max_length: int = 100, 
        min_length: int = 30,
        model: Optional[str] = None
    ) -> Optional[str]:
        """
        Генерує коротке резюме тексту.
        
        Args:
            text: Вхідний текст для резюме
            max_length: Максимальна довжина резюме
            min_length: Мінімальна довжина резюме
            model: Назва моделі (за замовчуванням використовується DEFAULT_MODEL)
            
        Returns:
            Резюме тексту або None у разі помилки
        """
        if not text or len(text.strip()) < 20:
            return None

        model_name = model or self.model
        url = f"{self.base_url}/{model_name}"

        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": False,
            },
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    summary = result[0].get("summary_text", "")
                    return summary.strip() if summary else None
                elif isinstance(result, dict) and "summary_text" in result:
                    return result["summary_text"].strip()
            elif response.status_code == 503:
                # Модель ще завантажується, повертаємо None
                return None
            else:
                # Логуємо помилку, але не падаємо
                print(f"Hugging Face API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling Hugging Face API: {e}")
            return None

    def summarize_fallback(self, text: str, max_sentences: int = 2) -> str:
        """
        Просте резюме без ШІ (fallback метод).
        Використовується, якщо API недоступне.
        
        Args:
            text: Вхідний текст
            max_sentences: Максимальна кількість речень
            
        Returns:
            Перші N речень тексту
        """
        if not text:
            return ""
        
        # Простий розбір на речення
        sentences = text.split(". ")
        if len(sentences) <= max_sentences:
            return text
        
        summary = ". ".join(sentences[:max_sentences])
        if not summary.endswith("."):
            summary += "."
        return summary


# Глобальний екземпляр для використання в додатку
_summarizer_instance: Optional[AISummarizer] = None


def get_summarizer() -> AISummarizer:
    """Отримує або створює глобальний екземпляр summarizer."""
    global _summarizer_instance
    if _summarizer_instance is None:
        _summarizer_instance = AISummarizer()
    return _summarizer_instance


def summarize_text(text: str, max_length: int = 100, min_length: int = 30) -> Optional[str]:
    """
    Зручна функція для генерації резюме.
    
    Args:
        text: Вхідний текст
        max_length: Максимальна довжина резюме
        min_length: Мінімальна довжина резюме
        
    Returns:
        Резюме або None
    """
    summarizer = get_summarizer()
    summary = summarizer.summarize(text, max_length=max_length, min_length=min_length)
    
    # Якщо ШІ не спрацював, використовуємо fallback
    if summary is None and len(text) > 50:
        return summarizer.summarize_fallback(text)
    
    return summary

