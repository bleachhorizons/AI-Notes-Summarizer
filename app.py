import os
import json
import gradio as gr
from openai import OpenAI

# Initialization
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Export it in Terminal first.")

client = OpenAI(api_key=api_key)

def study_buddy(text):
    if not text.strip():
        return "Please paste some text first.", "", ""

    prompt = f"""
You are a helpful study assistant.
Analyze the following text and return a valid JSON object with these exact keys:
"summary": a 2-sentence summary in plain English,
"key_points": a list of 3 strings,
"questions": a list of 2 strings

Text:
{text}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        
        # Clean response to ensure it's valid JSON
        raw = response.output_text.strip()
        if raw.startswith("```json"):
            raw = raw.replace("```json", "").replace("```", "")
        
        data = json.loads(raw)
        
        # Format lists into bullet points
        summary = data.get("summary", "No summary available.")
        key_points = "\n".join([f"• {p}" for p in data.get("key_points", [])])
        questions = "\n".join([f"• {q}" for q in data.get("questions", [])])
        
        return summary, key_points, questions

    except Exception as e:
        return f"Error parsing AI response: {str(e)}", "", ""

demo = gr.Interface(
    fn=study_buddy,
    inputs=gr.Textbox(lines=10, label="Paste notes or text"),
    outputs=[
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Key Points"),
        gr.Textbox(label="Discussion Questions"),
    ],
    title="Study Buddy"
)

demo.launch()
