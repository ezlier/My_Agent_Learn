import json

from model import Lesson

def parse_json(json_text: str):
    text = json_text.strip()

    if text.startswith("```json"):
        text = text[7:].strip()

    elif text.startswith("```JSON"):
        text = text[7:].strip()

    elif text.startswith("```"):
        text = text[3:].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    data = json.loads(text)

    lesson = Lesson.model_validate(data)
    return lesson