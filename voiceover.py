import base64
import os
import sys
import time
from google import genai
from google.genai import types

# Gemini API key GitHub Secret se aati hai
# v1beta zaroori hai, nahi to model 404 not found deta hai
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options=types.HttpOptions(api_version="v1beta"),
)

# script.txt me Hindi script hoti hai, uski awaaz banti hai
text = open("script.txt", encoding="utf-8").read().strip()
if not text:
    sys.exit("script.txt khali hai")

# pehle main model, fail ho to backup model
MODELS = ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]
TRIES_PER_MODEL = 3
WAIT_SECONDS = 20


def make_audio(model):
    interaction = client.interactions.create(
        model=model,
        input=[{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": text,
                "annotations": [{
                    "type": "speech_metadata",
                    "style": "रहस्यमयी और दिलचस्प अंदाज़ में, साफ़ हिंदी उच्चारण के साथ",
                }],
            }],
        }],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": "Charon"}]},
    )
    return base64.b64decode(interaction.output_audio.data)


audio = None
for model in MODELS:
    for attempt in range(1, TRIES_PER_MODEL + 1):
        try:
            print(f"model={model} koshish={attempt}")
            audio = make_audio(model)
            break
        except Exception as e:
            print(f"fail: {e}")
            time.sleep(WAIT_SECONDS)
    if audio:
        break

if not audio:
    sys.exit("sab models aur sab koshishein fail ho gayin")

with open("voiceover.wav", "wb") as f:
    f.write(audio)

print("voiceover.wav ban gayi")
