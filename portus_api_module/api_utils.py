# portus_api_module/api_utils.py

import httpx
from openai import OpenAI

def init_openai_client(api_key: str, base_url: str) -> tuple[OpenAI, httpx.Client]:
    http_client = httpx.Client()
    client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
    return client, http_client

def wrap_streaming_generator(stream, yield_fn, skip_types=None):
    if skip_types is None:
        skip_types = set()

    def generator():
        try:
            for event in stream:
                if hasattr(event, "type") and event.type in skip_types:
                    continue
                result = yield_fn(event)
                if result is not None:
                    yield result
        finally:
            try:
                stream.close()
            except Exception:
                pass

    generator.cancel = stream.close
    return generator()

class BaseClient:
    def __init__(self, http_client):
        self._http = http_client

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
