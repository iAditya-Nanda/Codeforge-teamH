import ollama
import json
import re
import os

MODEL_NAME = "minicpm-v"
IMAGE_PATH = "./a.png"
OUTPUT_JSON = "a_output.json"

PROMPT = """
You are WasteSense, an expert waste management assistant.
For this input image, respond strictly in valid JSON with:
summary, disposal_category, recyclable (true/false),
hazardous (true/false), instructions (array of steps),
confidence (0–1), follow_up_question (null or string).
Do not include any explanation outside JSON.
"""

def clean_json_string(raw_text: str) -> str:
    """
    Fixes minor formatting errors like unquoted booleans or trailing commas.
    """
    text = raw_text.strip()

    # Extract the JSON portion if wrapped with extra text
    start = text.find("{")
    end = text.rfind("}") + 1
    text = text[start:end]

    # Fix common errors:
    text = re.sub(r'\b(no|yes)\b', lambda m: '"no"' if m.group(1) == "no" else '"yes"', text)
    text = re.sub(r'\btrue\b', 'true', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfalse\b', 'false', text, flags=re.IGNORECASE)
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*\]', ']', text)

    return text

def analyze_image_with_ollama(model, image_path, prompt):
    """
    Sends image + prompt to Ollama and returns structured JSON output.
    """
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are WasteSense, an AI waste classification expert."},
            {"role": "user", "content": prompt, "images": [image_path]},
        ],
    )

    raw_output = response["message"]["content"]
    cleaned = clean_json_string(raw_output)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON parse failed even after cleaning.\n")
        print("Raw output:\n", raw_output)
        print("\nCleaned text attempted:\n", cleaned)
        return None

def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"Image not found at {IMAGE_PATH}")
        return

    print("🔍 Analyzing image with WasteSense AI...\n")
    result = analyze_image_with_ollama(MODEL_NAME, IMAGE_PATH, PROMPT)

    if result:
        with open(OUTPUT_JSON, "w") as f:
            json.dump(result, f, indent=4)
        print(f"Saved structured output to {OUTPUT_JSON}")
        print(json.dumps(result, indent=4))
    else:
        print("No valid response generated.")

if __name__ == "__main__":
    main()
