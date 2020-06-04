from ...core.converter.person import MALE, FEMALE
from discord.ext import commands
from ...core import converter as conv

import csv
import os
import math
import colors

CONSTANTS_FILE = os.path.join(os.path.dirname(__file__), 'ipfgl.csv')
with open(CONSTANTS_FILE, 'r') as file:
    reader = csv.reader(file)
    COMPO_CONSTANT = [list(map(float, row)) for row in reader]

EQUIPPED = 0    
CLASSIC = 1
POWERLIFTING = 0
BENCH_PRESS = 1

EQUIPMENTS = []

DISPLAYED_EQUIPMENTS = ['Equipped', 'Classic/Raw']
DISPLAYED_EVENTS = ['Powerlifting/Full Meet', 'Bench Press']

EQUIPMENT_ERROR = (
    'Available `equipment` values:\n'
    '• `E/Equipped`\n'
    '• `C/Classic/R/Raw`\n'
)

def Equipment(s):
    s = s.upper()
    if s in ['E', 'EQUIPPED']:
        return EQUIPPED
    elif s in ['C', 'CLASSIC', 'RAW', 'R']:
        return CLASSIC  
    raise commands.BadArgument(EQUIPMENT_ERROR)

EVENT_ERROR = (
    'Available `event`s:\n'
    '• `P/Powerlifting/F/FM/Full/FullMeet`'
    '• `B/BP/Bench/BenchPress`'
)

def Event(s):
    s = s.upper()
    if s in ['P', 'POWERLIFTING', 'F', 'FM', 'FULL', 'FULLMEET']:
        return POWERLIFTING
    elif s in ['B', 'BP', 'BENCH', 'BENCHPRESS']:
        return BENCH_PRESS
    raise commands.BadArgument(EVENT_ERROR)

def compute_coeff(constants, bodyweight):
    a, b, c = constants
    denom = a - b * math.exp(-c * bodyweight)
    return 100 / denom

def compute_points(constants, bodyweight, result):
    coeff = compute_coeff(constants, bodyweight)
    return coeff * result

def embed(gender, bodyweight, equipment, event, result):
    constant_index = (gender - 1) * 4 + event * 2 + equipment
    constants = COMPO_CONSTANT[constant_index]

    equipment = DISPLAYED_EQUIPMENTS[equipment]
    event = DISPLAYED_EVENTS[event]

    gender_emote = conv.get_gender_emote(gender)
    points = compute_points(constants, bodyweight, result)
    embed = colors.embed(title=f'{points:.2f}') \
                .set_author(name=f'{gender_emote} IPG GL Points') \
                .add_field(name='Bodyweight', value=f'**{bodyweight:g}** kg') \
                .add_field(name='Equipment', value=equipment) \
                .add_field(name='Event', value=event) \

    return embed