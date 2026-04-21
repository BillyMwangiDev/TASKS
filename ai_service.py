"""Claude AI integration for TASKY — task breakdown, capture, and weekly digest."""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are TASKY's AI assistant, a productivity expert embedded in a task manager. "
    "Help users break down complex tasks, extract action items, and gain productivity insights. "
    "Always respond with valid JSON unless instructed otherwise. Be concise and actionable."
)


class AIService:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                try:
                    import anthropic
                    self._client = anthropic.Anthropic(api_key=api_key)
                except ImportError:
                    logger.warning("anthropic package not installed — run: pip install anthropic")
        return self._client

    def is_available(self) -> bool:
        return self.client is not None

    def _call(self, user_prompt: str, max_tokens: int = 600) -> str:
        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=[{
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text

    def _extract_json(self, text: str) -> dict:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
        return json.loads(text[start:end])

    def breakdown_task(self, title: str, description: str = "") -> list[dict]:
        """Break a vague task into 3–7 concrete subtasks."""
        if not self.client:
            raise RuntimeError("ANTHROPIC_API_KEY not configured")

        prompt = (
            f"Break this task into 3–7 actionable subtasks:\n"
            f"Task: {title}\n"
            f"{f'Description: {description}' if description else ''}\n\n"
            f'Return JSON: {{"subtasks": [{{"title": "...", "priority": 2, "estimated_minutes": 15}}]}}\n'
            f"Priority: 1=High 2=Medium 3=Low. estimated_minutes as integer."
        )
        raw = self._call(prompt)
        data = self._extract_json(raw)
        return data.get("subtasks", [])

    def capture_tasks_from_text(self, text: str) -> list[dict]:
        """Extract action items from freeform text (notes, emails, meeting transcripts)."""
        if not self.client:
            raise RuntimeError("ANTHROPIC_API_KEY not configured")

        prompt = (
            f"Extract all action items from this text as tasks:\n\n{text}\n\n"
            f'Return JSON: {{"tasks": [{{"title": "...", "priority": 2, "due_date": null}}]}}\n'
            f"Priority: 1=High 2=Medium 3=Low. due_date as ISO string or null."
        )
        raw = self._call(prompt, max_tokens=800)
        data = self._extract_json(raw)
        return data.get("tasks", [])

    def generate_weekly_digest(self, stats: dict) -> str:
        """Generate a 2–3 sentence narrative productivity insight from weekly stats."""
        if not self.client:
            return "Set ANTHROPIC_API_KEY to unlock AI-powered weekly insights."

        prompt = (
            f"Generate a 2–3 sentence productivity insight from this week's data:\n\n"
            f"{json.dumps(stats, indent=2)}\n\n"
            f"Be encouraging, specific, and end with one actionable suggestion. Plain text only."
        )
        return self._call(prompt, max_tokens=200).strip()
