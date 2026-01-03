"""
Альтернативний модуль для роботи з власною моделлю на Google Colab.
Використовується, якщо потрібно розгорнути власну модель summarization.
"""
import os
from typing import Optional

import requests


class ColabSummarizer:
    """
    Клас для генерації резюме через власну модель на Google Colab.
    
    Вимоги:
    1. Розгорнути модель на Google Colab
    2. Створити API endpoint (наприклад, через Flask/FastAPI)
    3. Опублікувати через ngrok або інший сервіс
    4. Вказати URL у змінній оточення COLAB_API_URL
    """

    def __init__(self, api_url: Optional[str] = None):
        """
        Ініціалізація Colab summarizer.
        
        Args:
            api_url: URL до API на Google Colab (опціонально, береться з env)
        """
        self.api_url = api_url or os.getenv("COLAB_API_URL")
        if not self.api_url:
            raise ValueError(
                "COLAB_API_URL не вказано. "
                "Встановіть змінну оточення COLAB_API_URL з URL до вашого Colab API."
            )

    def summarize(
        self,
        text: str,
        max_length: int = 100,
        min_length: int = 30,
    ) -> Optional[str]:
        """
        Генерує коротке резюме тексту через власну модель на Colab.
        
        Args:
            text: Вхідний текст для резюме
            max_length: Максимальна довжина резюме
            min_length: Мінімальна довжина резюме
            
        Returns:
            Резюме тексту або None у разі помилки
        """
        if not text or len(text.strip()) < 20:
            return None

        if not self.api_url:
            return None

        payload = {
            "text": text,
            "max_length": max_length,
            "min_length": min_length,
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                # Очікуваний формат: {"summary": "..."} або {"summary_text": "..."}
                summary = result.get("summary") or result.get("summary_text", "")
                return summary.strip() if summary else None
            else:
                print(f"Colab API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error calling Colab API: {e}")
            return None


def get_colab_summarizer() -> Optional[ColabSummarizer]:
    """Отримує екземпляр Colab summarizer, якщо налаштовано."""
    try:
        colab_url = os.getenv("COLAB_API_URL")
        if not colab_url or not colab_url.strip():
            return None
        return ColabSummarizer(colab_url)
    except ValueError:
        # COLAB_API_URL не вказано - це нормально, просто не використовуємо Colab
        return None
    except Exception as e:
        # Інші помилки - логуємо, але не падаємо
        print(f"Failed to initialize Colab summarizer: {e}")
        return None

