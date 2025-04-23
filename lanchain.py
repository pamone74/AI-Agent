
# Using GitHub models
import os
from typing import cast
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import chainlit as cl
from io import BytesIO

import os

OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = "https://<your-resource-name>.openai.azure.com/"
OPENAI_API_VERSION = "2023-12-01-preview"  # or current version
OPENAI_API_KEY = "<your-azure-api-key>"

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token)
)
SYSTEM_PROMPT = """
You are a helpful and intelligent AI agent who looks after children.
- Always speak politely and kindly.
- You are a family member
- Never say anything inappropriate.
- If the prompt contains 'daddy', respond gently like a loving father.
- If the prompt contains 'mummy', respond gently like a loving mother.
"""

@cl.step(name="Fun Fact Tool", type="tool")
async def tool():
    await cl.sleep(1)
    return "Did you know? Elephants can recognize themselves in a mirror!"

@cl.on_chat_start
async def on_chat_start():
    elements = [
        # cl.Audio(name="example.mp3", path="./example.mp3", display="inline"),
    ]
    await cl.Message(
        content="Here is an audio file",
        elements=elements,
    ).send()
    await cl.Message(content="👋 Hi! Ask me anything.").send()


@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.InputAudioChunk):
    pass

@cl.on_chat_start
# async def main():
#     elements = [
#         cl.Audio(name="", path="", display="inline"),
#     ]
#     await cl.Message(
#         content="here is an audi file",
#         elements=elements,
#     ).send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        response = client.complete(
            messages=[
                SystemMessage(SYSTEM_PROMPT),
                UserMessage(message.content)
            ],
            temperature=0.7,
            top_p=1.0,
            model=model
        )
        tool_res = await tool()
        reply = response.choices[0].message.content
        await cl.Message(content=reply).send()
    except Exception as e:
        await cl.Message(content=f"❌ Oops! Something went wrong:{str(e)}").send()