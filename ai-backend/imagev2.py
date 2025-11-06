import ollama
import json
import re
import os

MODEL_NAME = "llava:13b"      # change to llava:34b for higher accuracy
IMAGE_PATH = "./a.png"
OUTPUT_JSON = "a_output.json"

PROMPT = """
You are WasteSense, a professional AI for visual waste classification.
Look carefully at the image and describe what the object actually is,
not what it vaguely resembles.

Return ONLY valid JSON with:
summary: brief description with material (e.g., "Amul milk pouch – LDPE plastic")
disposal_category: one of ["recyclable","non-recyclable","organic","hazardous","mixed"]
recyclable: true/false
hazardous: true/false
instructions: list of clear disposal steps
confidence: 0–1
follow_up_question: null or a relevant user question

No extra text outside JSON.
"""

def clean_json(raw):
    text = raw.strip()
    start, end = text.find("{"), text.rfind("}") + 1
    text = text[start:end]
    text = re.sub(r',\s*([\]}])', r'\1', text)
    text = re.sub(r'\bTrue\b', 'true', text)
    text = re.sub(r'\bFalse\b', 'false', text)
    text = re.sub(r'\bYes\b', '"yes"', text)
    text = re.sub(r'\bNo\b', '"no"', text)
    return text

def analyze_image(model, img_path, prompt):
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are WasteSense, an AI waste-management expert."},
            {"role": "user", "content": prompt, "images": [img_path]},
        ],
    )
    raw = response["message"]["content"]
    cleaned = clean_json(raw)
    try:
        return json.loads(cleaned)
    except Exception:
        print("⚠️ Model returned invalid JSON:\n", raw)
        return None

def logic_layer(result):
    """Simple domain rules to improve accuracy."""
    summary = result.get("summary", "").lower()

    # Example corrections
    if "amul" in summary and "milk" in summary:
        result["summary"] = "Amul milk pouch – LDPE plastic"
        result["hazardous"] = False
        result["recyclable"] = True
        result["disposal_category"] = "recyclable"
        result["instructions"] = [
            "Empty the pouch completely.",
            "Rinse and dry it to remove milk residue.",
            "If your municipality recycles LDPE, place in plastic recycling.",
            "Otherwise, dispose in general waste."
        ]
        result["confidence"] = max(result.get("confidence", 0.8), 0.95)

    if "metal" in summary or "tin" in summary:
        result["disposal_category"] = "recyclable"
        result["recyclable"] = True

    return result

def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Image not found: {IMAGE_PATH}")
        return

    print("🔍 WasteSense v2 analyzing image...\n")
    data = analyze_image(MODEL_NAME, IMAGE_PATH, PROMPT)
    if not data:
        print("❌ AI failed to produce valid output.")
        return

    corrected = logic_layer(data)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(corrected, f, indent=4)

    print(f"✅ Saved refined output to {OUTPUT_JSON}\n")
    print(json.dumps(corrected, indent=4))

if __name__ == "__main__":
    main()
