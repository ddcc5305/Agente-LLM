import requests
from agente_rag.domain.ports import LLMPort

class OllamaLLM:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2) -> dict:
        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature}
            }
        )
        response.raise_for_status()
        payload = response.json()
        
        # Extraemos las métricas reales de Ollama[cite: 3, 5]
        return {
            "text": payload["response"],
            "stats": {
                "prompt_tokens": payload.get("prompt_eval_count", 0),
                "output_tokens": payload.get("eval_count", 0),
                "latencia_s": round(payload.get("total_duration", 0) / 1e9, 2),
                "tokens_per_sec": round(payload.get("eval_count", 0) / (payload.get("eval_duration", 1) / 1e9), 2)
            }
        }