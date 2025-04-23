import os
import json
import websockets
import asyncio
import pyaudio

# WebSocket URI and API Key (ensure these are correct)
AZURE_ENDPOINT = "wss://ai-amonepatrickwpdi9703ai016025149940.openai.azure.com/openai/realtime?api-version=2024-10-01-preview&deployment=gpt-4o-mini-realtime-preview"
AZURE_API_KEY = "4rcobxChu7pAs9MBjuWes0JcV1iR2XiXJyxhVlLsvPiYlHWQZXGlJQQJ99BDACHYHv6XJ3w3AAAAACOGWRzq"

import os
import base64
import asyncio
import chainlit as cl
from openai import AsyncAzureOpenAI

AZURE_DEPLOYMENT = "gpt-4o-mini-realtime-preview"

client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version="2024-10-01-preview"
)

import pyaudio

def play_audio(audio_data):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

async def stream_chat(message_text: str) -> str:
    collected_text = ""

    async with client.beta.realtime.connect(model=AZURE_DEPLOYMENT) as connection:
        await connection.session.update(session={"modalities": ["text", "audio"]})

        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": message_text}],
            }
        )

        await connection.response.create()

        async for event in connection:
            if event.type == "response.text.delta":
                collected_text += event.delta
            elif event.type == "response.audio.delta":
                audio_data = base64.b64decode(event.delta)
                play_audio(audio_data)
                # TODO: you can play or store audio_data here
            elif event.type == "response.done":
                break

    return collected_text

@cl.on_message
async def handle_message(message: cl.Message):
    reply = await stream_chat(message.content)
    await cl.Message(content=reply).send()
