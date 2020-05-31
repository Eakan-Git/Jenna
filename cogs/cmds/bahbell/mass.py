import re

KG2LBS = 2.20462262185

def respond_kg2lbs(kg):
    lbs = kg * KG2LBS
    return f'**{kg:g}** kg = **{lbs:g}** lbs'

def respond_lbs2kg(lbs):
    kg = lbs / KG2LBS
    return f'**{lbs:g}** lbs = **{kg:g}** kg'

KG2LBS_PATTERN = '((?:\d*\.)?\d+)\s?kg\s?=\s?lbs'
LBS2KG_PATTERN = '((?:\d*\.)?\d+)\s?lbs\s?=\s?kg'

async def process_commands(message):
    response = None
    for p in [KG2LBS_PATTERN, LBS2KG_PATTERN]:
        number = re.findall(p, message.content.lower())
        if not number: continue

        number = float(number[0])
        if p == KG2LBS_PATTERN:
            response = respond_kg2lbs(number)
        elif p == LBS2KG_PATTERN:
            response = respond_lbs2kg(number)
    
    if response:
        await message.channel.send(response)