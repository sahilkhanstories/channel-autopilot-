import base64
import os
import sys
from google import genai

# Gemini API key GitHub Secret se aati hai
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# script.txt me Hindi script hoti hai, uski awaaz banti hai
text = open("script.txt", encoding="utf-8").read().strip()
if not text:
    sys.exit("script.txt khali hai")

interaction = client.interactions.create(
    model="gemini-3.8-flash-tts",
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

with open("voiceover.wav", "wb") as f:
    f.write(base64.b64decode(interaction.output_audio.data))

print("voiceover.wav ban gayi")
