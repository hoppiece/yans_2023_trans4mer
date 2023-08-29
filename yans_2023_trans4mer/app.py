import os

import dotenv
import gradio as gr
import openai

dotenv.load_dotenv()

openai.organization = os.getenv("API_ORG")
openai.api_key = os.getenv("API_KEY")
app_password = os.getenv("APP_PASSWORD")
app_username = os.getenv("APP_USERNAME")

def generate(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

examples = [
    ["きのこの山"],
    ["たけのこの里"],
]

demo = gr.Interface(
    fn=generate,
    inputs=gr.components.Textbox(lines=5, label="Prompt"),
    outputs=gr.components.Image(type="filepath", label="Generated Image"),
    flagging_options=[],
    examples=examples
)

demo.launch(share=False, auth=(app_username, app_password))