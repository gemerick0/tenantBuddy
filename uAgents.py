 
from uagents import Agent, Bureau, Context, Model, Protocol
import os

import json
import google.generativeai as genai
class Message(Model):
    message: str
class Json(Model):
    json: str
proto = Protocol(name="proto", version="1.0")
genai.configure(api_key=os.environ['API_KEY'])
interpreter = Agent(name="sigmar", seed="interpreterOfMessages")
responder = Agent(name="slaanesh", seed="responderOfMessages")
dataviz = Agent(name="dataviz", seed="datavizOfInterpretations")
list_of_messages = []
@interpreter.on_message()
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

@responder.on_message()
async def send_message(ctx: Context):
    ctx.logger.info(f"Received message from {ctx.sender}: {ctx.message}")
    # send back to the user to assess more information (this is on the other code but we didn't have time to implement it in the uagents)

@dataviz.on_message()
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
    # send the response back to the user in the format of json (to integrate with frontend)