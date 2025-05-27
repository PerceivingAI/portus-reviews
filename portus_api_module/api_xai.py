# portus_api_module/api_xai.py

from portus_config_module.config_manager import XAI_ADD_PARAMS
from portus_api_module.api_utils import (
    init_openai_client,
    wrap_streaming_generator,
    BaseClient,
)
from openai.types.chat import ChatCompletionChunk

class XAIClient(BaseClient):
    """
    Chat Completion client pointed at xAI's GPT endpoint.
    Mirrors the OpenAI interface (chat.completions.create).
    """

    def __init__(self, api_key: str, model: str, base_url: str, stream: bool = False):
        self.model = model
        self.stream = stream
        self.client, http_client = init_openai_client(api_key, base_url)
        super().__init__(http_client)

    def chat(self, messages, **kwargs):
        # xAI-specific config
        kwargs.pop("max_output_tokens", None)
        kwargs.pop("tool_choice", None)

        reasoning = XAI_ADD_PARAMS.get("reasoning_effort")
        if reasoning:
            kwargs["reasoning_effort"] = reasoning

        # Convert message format to xAI's structure
        adapted = [
            {
                "role": msg["role"],
                "content": [{"type": "text", "text": msg["content"]}]
            }
            for msg in messages
        ]

        if not self.stream:
            return self.client.chat.completions.create(
                model=self.model,
                messages=adapted,
                **kwargs
            )

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=adapted,
            stream=self.stream,
            **kwargs
        )

        return wrap_streaming_generator(
            stream,
            yield_fn=lambda chunk: getattr(chunk.choices[0].delta, "content", ""),
        )
