 
import pandas as pd
from uagents import Agent, Bureau, Context, Model, Protocol
import os
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import google.generativeai as genai
class Message(Model):
    message: str
"""class JsonOutput(Model):
    jsonOutput: str"""
proto = Protocol(name="proto", version="1.0")
os.environ["API_KEY"] = "AIzaSyB1RnQt9FUwyQEGBLM-jR0tWVHt3nrYaCY"
genai.configure(api_key=os.environ["API_KEY"])
interpreter = Agent(name="sigmar", seed="interpreterOfMessages")
responder = Agent(name="slaanesh", seed="responderOfMessages")
dataviz = Agent(name="dataviz", seed="datavizOfInterpretations")
list_of_messages = []
@interpreter.on_message(model=Message)
async def send_message(ctx: Context):
    ctx.logger.info(f"Received message from {ctx.sender}: {ctx.message}")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = """With this user message, interpret the impact of each problem on the sender, and put each problem into one that fits into the categories that are in the context included into the json, appending it to the existing problems in list_of_messages.

Use this JSON schema:

Problem = {'problem': str, 'impact': int}
Return: list[Problem]

A good example is

Return: [{'problem': 'mold', 'impact': 10}, {'problem': 'noise', 'impact': 5}]
"""
    response = model.generate_content([prompt, ctx.list_of_messages, ctx.message])
    res = getattr(response, "_result")
    candidates = getattr(res, "candidates")[0]
    content = getattr(candidates, "content")
    try:
        parts = getattr(content, "parts")[0]
    except:
        try:
            parts = getattr(content, "parts")
        except:
            parts = content
    try:
        text = str(getattr(parts, "text"))
    except:
        ctx.logger.info("no text")
    list_of_messages.append(json.loads(text.split(", ")))
    await ctx.add_to_context("list_of_messages", list_of_messages) 
    await ctx.send(responder.address, Message(message="If the issue is still not clear enough, please send me another message"))

@responder.on_message(model=Message)
async def send_message(ctx: Context):
    ctx.logger.info(f"Received message from {ctx.sender}: {ctx.message}")
    # send back to the user to assess more information (this is on the other code but we didn't have time to implement it in the uagents)

@dataviz.on_message(model=Message)
async def send_message(ctx: Context):
    ctx.logger.info(f"Received message from {ctx.sender}: {ctx.message}")
    prompt = """With this list of problems, identify the cases in output.json that fit the most with it, and add their names, and considering this, assess the average compensation one of these problems would give to the sender of the message.

Use this JSON schema:

Problem = {'problem': str, 'expected_compensation': int}
Similar_Cases = {'name_of_case': str, 'compensation': int}
Return: list[Similar_Cases], list[Problem]

"""
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt, ctx.list_of_messages])
    res = getattr(response, "_result")
    candidates = getattr(res, "candidates")[0]
    content = getattr(candidates, "content")
    try:
        parts = getattr(content, "parts")[0]
    except:
        try:
            parts = getattr(content, "parts")
        except:
            parts = content
    try:
        text = str(getattr(parts, "text"))
    except:
        ctx.logger.info("no text")
    with open('output.json', 'w') as f:
        dat = json.dumps(text)
        f.write(dat)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    system_instruction = "Your name is Tenant Buddy and you are inside an app, your purpose is to hear tenants issues, make up to 4 questions to understand the issue. After you fully understood the issue, give them a summary of what is happening, recommend further actions and tell that you are generating a report from this conversation. Keep the messages short, asking one question at a time. This app is working with a non profit called community legal services.")


outputFile = json.dumps('/home/gabriel/VS Code Projects/Hack for Social Change/output_schema.json')

chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello!"},
        {"role": "model", "parts": "Great to meet you, my name is Tenant Buddy. What is the issue in your home?"},
        {"role": "user", "parts": "Please, after the conversation, if further actions is to report a complaint to the landlord, explain their possible rights. If the landlord actions seems to be unfair of unrightful, ask me to SHARE the conversation to a lawyer."},
        {"role": "user", "parts": "Please, use the following JSON as context. I want it to be what you find the problems characterisitics from. It works as a database that resumes the previous court cases we have knowledge of. The number for each problem is the compensation gotten for each case. Through each iteration, assess a case using the last 3 parameters 'SummaryOfComplaint', 'SummaryOfDecision', 'ReasoningForDecision'. After the 4th message question, send a concluding message that includes the word 'report'. A good example is 'Would you like to see the report of what you can get for a petition on this case?'"},
    ]
)

chat.send_message(outputFile)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/messages/")
async def read_item(q: Union[str, None] = None):
    print(q)
    response = chat.send_message(q)
    print(response.text)
    await interpreter.send_message(Message(message=q))
    if 'report' in response.text:
        await dataviz.send_message(Message(message='Final Report'))
    return {"message": response.text}

bureau = Bureau(port=8000, endpoint="http://localhost:8000/submit")

bureau.add(responder)
bureau.add(interpreter)
bureau.add(dataviz)

if __name__ == "__main__":
    bureau.run()