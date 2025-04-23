import os
import base64
import asyncio
from openai import AsyncAzureOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider

async def main() -> None:
    """
    When prompted for user input, type a message and hit enter to send it to the model.
    Enter "q" to quit the conversation.
    """

    client = AsyncAzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-10-01-preview",
    )
    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview",  # deployment name of your model
    ) as connection:
        await connection.session.update(session={"modalities": ["text", "audio"]})  
        while True:
            user_input = input("Enter a message: ")
            if user_input == "q":
                break

            await connection.conversation.item.create(
                item={
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_input}],
                }
            )
            await connection.response.create()
            async for event in connection:
                if event.type == "response.text.delta":
                    print(event.delta, flush=True, end="")
                elif event.type == "response.audio.delta":

                    audio_data = base64.b64decode(event.delta)
                    print(f"Received {len(audio_data)} bytes of audio data.")
                elif event.type == "response.audio_transcript.delta":
                    print(f"Received text delta: {event.delta}")
                elif event.type == "response.text.done":
                    print()
                elif event.type == "response.done":
                    break

asyncio.run(main())