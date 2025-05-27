# portus_api_module/api_google.py

from portus_api_module.api_utils import (
    init_openai_client,
    wrap_streaming_generator,
    BaseClient,
)

class GoogleClient(BaseClient):
    """
    Uses the OpenAI SDK pointed at Google’s REST endpoint.
    Supports streaming and non-streaming chat completions.
    """

    def __init__(self, api_key: str, model: str, base_url: str, stream: bool = False):
        self.model = model
        self.stream = stream
        self.client, http_client = init_openai_client(api_key, base_url)
        super().__init__(http_client)

    def chat(self, messages, **kwargs):
        kwargs.pop("max_output_tokens", None)

        if not self.stream:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            class _Stub: pass
            stub = _Stub()
            stub.choices = resp.choices
            return stub

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=self.stream,
            **kwargs
        )

        return wrap_streaming_generator(
            stream,
            yield_fn=lambda chunk: getattr(chunk.choices[0].delta, "content", "")
        )
