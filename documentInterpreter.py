import os
import pdfplumber
import google.generativeai as genai
import json
import pandas as pd
import shutil

import sys
sys.set_int_max_str_digits(10000)
from typing import TypedDict

class Infestation(TypedDict):
    Cockroaches: int
    Rats: int
    Bats: int
    Flies: int
    Woodworm: int
    Moth: int
    Bookworm: int
    Termites: int

class UnlawfulRentIncrease(TypedDict):
    _0_10percent: int
    _10_20percent: int
    _20_30percent: int
    _30_40percent: int
    _40_50percent: int
    _50_60percent: int
    _60_70percent: int
    _70_80percent: int
    _80_90percent: int
    _90_pluspercent: int

class Harassment(TypedDict):
    Humiliation: int
    sexual_abuse: int
    verbal_threats: int
    written_threats: int
    discrimination: int
    racism: int
    xenophobia: int
    denying_rent: int
    shutting_utilities: int
    lockouts: int
    entering_unit_without_notice: int

class PropertyDamage(TypedDict):
    window_broken: int
    water_leak: int
    gas_leak: int
    leaky_roof: int
    damage_on_ceiling: int
    infiltration: int

class Mold(TypedDict):
    bathroom: int
    bedroom: int
    kitchen: int
    level_of_unusability: int
    living_room: int

class AppliancesBroken(TypedDict):
    heater_broken: int
    lights_broken: int
    lock_broken: int
    ac_broken: int
    broken_wiring: int

class NotFollowingRequiredStandards(TypedDict):
    insufficient_heating: int
    bad_water_quality: int
    smoking_around_unit: int
    no_emergency_services: int

class NameOfPetition(TypedDict):
    name_of_petition: str
    problems_included: str
    gravity_of_the_problems_1_10: int
class ReasoningForDecision(TypedDict):
    petition: NameOfPetition
class OutputSchema(TypedDict):
    Infestation: Infestation
    UnlawfulRentIncrease: UnlawfulRentIncrease
    Harassment: Harassment
    PropertyDamage: PropertyDamage
    Mold: Mold
    AppliancesBroken: AppliancesBroken
    NotFollowingRequiredStandards: NotFollowingRequiredStandards
    SummaryOfDecision: str
    SummaryOfComplaint: str
    ReasoningForDecision: ReasoningForDecision

genai.configure(api_key=os.environ['API_KEY'])
# Set the source and destination folders
source_folder = '/home/gabriel/VS Code Projects/Hack for Social Change/files/pdf/unread'
destination_folder = '/home/gabriel/VS Code Projects/Hack for Social Change/files/pdf/read'

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Get the list of PDF files in the source folder
pdf_files = [file for file in os.listdir(source_folder) if file.endswith('.pdf')]

# Initialize variables to store the text of each file
for i, file in enumerate(pdf_files):
    globals()[f'pdf_{i+1}'] = ''

# Iterate through the PDF files in the source folder
for i, file in enumerate(pdf_files):
    file_path = os.path.join(source_folder, file)
    print(f"File {i+1}: {file_path}")
    
    # Extract the text from the PDF file using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    # Add the text to the appropriate variable
    globals()[f'pdf_{i+1}'] = text
    
    # Move the file to the destination folder
    shutil.move(file_path, destination_folder)

# Print the text of each file
for i, file in enumerate(pdf_files):
    print(f"PDF {i+1} text:")
    # print(globals()[f'pdf_{i+1}'])

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

prompt = "what are the types of complaints being done in the pdf? In the the types of complaints within a specified category in the output schema and then in them, add the properties that are defined. To each property value, you will go to the part of the PDF that details the decision, and get the compensation attached to that problem. If a compensation is provided by a period, calculate the TOTAL amount in DOLLARS. Never provide a value for compensation in percentage. Always in dollars. If a compensation is not provided, do not add anything. For clarification, the unlawful rent increase is ONLY when that specific word is said in the pdf. Only add a value if there was compensation decided by the jury. If there was not compensation decided by the jury, do not add it, not even a 0. Don't refer to it if it doesn't have compensation. Otherwise, just do the summary of complaint and summary of decision. In the summary of complaint and summary of decision, add the amount of compensation (required or decided). In the reasoning for decision, add the name of the petition, the problems pointed out (in the format of the problems provided in the output schema, saying just the name of the problem (for example, mold) and its characteristics (bathroom)), along with their respective compensations, and their gravity based on how much compensation they got and alleged impact (from 1 to 10) always calculate this value."
prompt2 = "for me to provide as a guideline for an AI to classify the impact of the complaints, explain what each of the things in this output schema mean"
data1 = {
    "Infestation": {
        "Cockroaches": [],
        "Rats": [],
        "Bats": [],
        "Flies": [],
        "Woodworm": [],
        "Moth": [],
        "Bookworm": [],
        "Termites": []
    },
    "UnlawfulRentIncrease": {
        "_0_10percent": [],
        "_10_20percent": [],
        "_20_30percent": [],
        "_30_40percent": [],
        "_40_50percent": [],
        "_50_60percent": [],
        "_60_70percent": [],
        "_70_80percent": [],
        "_80_90percent": [],
        "_90_pluspercent": []
    },
    "Harassment": {
        "Humiliation": [],
        "sexual_abuse": [],
        "verbal_threats": [],
        "written_threats": [],
        "discrimination": [],
        "racism": [],
        "xenophobia": [],
        "denying_rent": [],
        "shutting_utilities": [],
        "lockouts": [],
        "entering_unit_without_notice": []
    },
    "PropertyDamage": {
        "window_broken": [],
        "water_leak": [],
        "gas_leak": [],
        "leaky_roof": [],
        "damage_on_ceiling": [],
        "infiltration": []
    },
    "Mold": {
        "bathroom": [],
        "bedroom": [],
        "kitchen": [],
        "living_room": []
    },
    "AppliancesBroken": {
        "heater_broken": [],
        "lights_broken": [],
        "lock_broken": [],
        "ac_broken": [],
        "broken_wiring": []
    },
    "NotFollowingRequiredStandards": {
        "insufficient_heating": [],
        "bad_water_quality": [],
        "smoking_around_unit": [],
        "no_emergency_services": []
    },
    "SummaryOfDecision": [],
    "SummaryOfComplaint": [],
    "ReasoningForDecision": {"petition": {"name_of_petition":"","problems_included": "", "gravity_of_the_problems_1_10": 0}}
}
# data1 = json.dumps(data1)

data_1 = data1
for i in range(len(pdf_files)):
    try:
        response = model.generate_content([prompt, globals()[f'pdf_{i+1}']], 
                                        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=OutputSchema))
        # print(response)
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
            continue
        # Parse the JSON string into a Python dictionary
        data2 = json.loads(text)
        # data_1 = json.loads(data1)

    # Iterate over the data in the second JSON file
        for column, value in data2.items():
            # print (column)
            # Iterate over the columns in the current element
            if True:
                print(column, type(value), value)
                # If the value is not already in the column, add it with a count of 1
                if isinstance(value, dict):
                    if column != "ReasoningForDecision":
                        for key, value in value.items():
                            print(key, value)
                            print(type(data_1[column][key]), data_1[column][key])
                            data_1[column][key].append(value)
                            print(data_1[column][key])
                    else:
                        data_1["ReasoningForDecision"][value["petition"]["name_of_petition"]] = {"name_of_petition":"","problems_included": "", "gravity_of_the_problems_1_10": 0}
                        data_1[column][value["petition"]["name_of_petition"]]["name_of_petition"] = value["petition"]["name_of_petition"]
                        data_1[column][value["petition"]["name_of_petition"]]["problems_included"] = value["petition"]["problems_included"]
                        data_1[column][value["petition"]["name_of_petition"]]["gravity_of_the_problems_1_10"] = value["petition"]["gravity_of_the_problems_1_10"]
                elif isinstance(value, str):
                    data_1[column].append(value)
    except:
        continue

with open('output.json', 'w') as f:
    data1 = json.dumps(data_1)
print(data1)