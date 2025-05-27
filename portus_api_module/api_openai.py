# portus_api_module/api_openai.py

from portus_api_module.api_utils import (
    init_openai_client,
    wrap_streaming_generator,
    BaseClient,
)

class OpenAIResponsesClient(BaseClient):
    """OpenAI streaming client for response output_text events."""

    def __init__(self, api_key, model, base_url, stream=False):
        self.model = model
        self.stream = stream
        self.client, http_client = init_openai_client(api_key, base_url)
        super().__init__(http_client)

    def chat(self, messages, **kwargs):
        """
        Returns a generator of delta events with a .cancel() method
        to abort the underlying HTTP stream.
        """
        stream = self.client.responses.create(
            model=self.model,
            input=messages,
            stream=self.stream,
            **kwargs
        )

        def yield_delta(event):
            if event.type == "response.output_text.delta":
                return event.delta
            elif event.type == "error":
                raise RuntimeError(f"Streaming error: {event.error}")
            return None

        return wrap_streaming_generator(
            stream,
            yield_fn=lambda event: yield_delta(event),
            skip_types={"response.created", "response.completed"},
        )
