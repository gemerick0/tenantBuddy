import google.generativeai as genai
import os
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

os.environ["API_KEY"] = "AIzaSyB1RnQt9FUwyQEGBLM-jR0tWVHt3nrYaCY"
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    system_instruction = "Your name is Tendant Buddy and you are inside an app, your purpose is to hear tenants issues, make up to 4 questions to understand the issue. After you fully understood the issue, give them a summary of what is happening, recommend further actions and tell that you are generating a report from this conversation. Keep the messages short, asking one question at a time. This app is working with a non profit called community legal services.")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello!"},
        {"role": "model", "parts": "Great to meet you, my name is Tendant Buddy. What is the issue in your home?"},
        {"role": "user", "parts": "Please, after the conversation, if further actions is to report a complaint to the landlord, explain their possible rights. If the landlord actions seems to be unfair of unrightful, ask me to SHARE the conversation to a lawyer."},
    ]
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/messages/")
async def read_item(q: Union[str, None] = None):
    print(q)
    response = chat.send_message(q)
    print(response.text)
    return {"message": response.text}