# portus_api_module\api_factory.py

import os
import httpx

from portus_config_module.config_manager import (
    reload_config,
    get_provider_name,
    get_model,
    get_model_url,
    get_general_params,
)

from .api_openai import OpenAIResponsesClient
from .api_google import GoogleClient
from .api_xai import XAIClient

def get_client():
    reload_config()

    provider = get_provider_name()
    model    = get_model()
    base_url = get_model_url()
    stream   = get_general_params().get("stream", False)

    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    if not api_key:
        raise ValueError(f"API key for provider '{provider}' not found in environment variables.")

    if provider == "openai":
        return OpenAIResponsesClient(api_key, model, base_url, stream)

    elif provider == "google":
        return GoogleClient(api_key, model, base_url, stream)

    elif provider == "xai":
        return XAIClient(api_key, model, base_url, stream)

    else:
        raise ValueError(f"Unsupported provider: {provider}")

def get_understanding_client(provider="google"):
    base_url = get_model_url("base_url", provider)

    # print(f"[api_factory] 🔧 Initializing client for provider: {provider}")
    # print(f"[api_factory] 🌐 Base URL: {base_url}")

    if provider == "google":
        import google.genai as genai
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
        if not api_key:
            print("[get_understanding_client] ❌ Missing GOOGLE_API_KEY in environment.")
            return None
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            print(f"[get_understanding_client] ❌ Failed to initialize Google client: {e}")
            return None

    elif provider == "openai":
        from openai import OpenAI
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
        if not api_key:
            print("[get_understanding_client] ❌ Missing OPENAI_API_KEY in environment.")
            return None
        try:
            http_client = httpx.Client()
            return OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
        except Exception as e:
            print(f"[get_understanding_client] ❌ Failed to initialize OpenAI client: {e}")
            return None

    else:
        raise NotImplementedError(f"[get_understanding_client] Provider '{provider}' not supported.")
