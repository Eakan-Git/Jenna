from ...core import converter as conv
import colors

MALE_VALUES = [
    -216.0475144,
    16.2606339,
    -0.002388645,
    -0.00113732,
    7.01863e-6,
    -1.291e-8]

FEMALE_VALUES = [
    594.31747775582,
    -27.23842536447,
    0.82112226871,
    -0.00930733913,
    4.731582e-5,
    -9.054e-8
]

def wilks_coeff(bodyweight, values, lifted_weight=1):
    return 500 / sum(bodyweight**i * v for i, v in enumerate(values)) * lifted_weight

def male_wilks(bodyweight, lifted_weight):
    return wilks_coeff(bodyweight, MALE_VALUES, lifted_weight)

def female_wilks(bodyweight, lifted_weight):
    return wilks_coeff(bodyweight, FEMALE_VALUES, lifted_weight)

def embed(gender, bodyweight, lifted_weight):
    wilks_formula = male_wilks if gender == conv.MALE else female_wilks
    wilks_value = wilks_formula(bodyweight, lifted_weight)

    embed = colors.embed(title=f'{wilks_value:.2f}') \
                    .set_author(name='Wilks Points') \
                    .add_field(name='Bodyweight', value=f'**{bodyweight:g}** kg')
    
    if lifted_weight != 1:
        embed.add_field(name='Lifted', value=f'**{lifted_weight:g}** kg')
    
    return embed