# reply_module\reply_engine.py

"""
Builds prompt, calls chosen provider via portus_api_module, returns reply text.
"""

from typing import List, Dict
import time

from portus_api_module.api_factory import get_client
from portus_config_module.config_manager import (
    reload_config,
    get_user_prompt,
    get_system_prompt,
    get_general_params,
)

client = get_client()

def _build_messages(review_text: str, title_text: str = "") -> List[Dict[str, str]]:
    reload_config()
    msgs: List[Dict[str, str]] = []

    system_prompt = get_system_prompt()
    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})

    user_prompt = get_user_prompt()
    if user_prompt:
        msgs.append({"role": "user", "content": user_prompt})

    combined = f"title: {(title_text or '').strip()}\nreview: {(review_text or '').strip()}"
    msgs.append({"role": "user", "content": combined})

    return msgs

def generate_reply(provider: str, review_text: str, title_text: str = "") -> str:
    reload_config()
    messages = _build_messages(review_text, title_text)

    params = get_general_params()
    temperature = params.get("temperature")
    top_p = params.get("top_p")

    kwargs = {}
    if temperature is not None:
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p

    retry_delays = [2, 5, 10]
    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            response = client.chat(messages=messages, **kwargs)
            break
        except Exception as e:
            print(f"❌ Attempt {attempt}: Model call failed – {e}")
            if attempt == len(retry_delays):
                raise
            time.sleep(delay)

    if hasattr(response, "choices"):
        return response.choices[0].message.content

    reply_parts: List[str] = []
    for chunk in response:
        if isinstance(chunk, str):
            reply_parts.append(chunk)

    return "".join(reply_parts)
