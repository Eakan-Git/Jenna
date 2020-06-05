from math import log

import colors

B = log(10) / log(2)

def compute_points(world_record, total_kg):
    return total_kg ** B / world_record ** B * 1000

def embed(world_record, total_kg):
    points = compute_points(world_record, total_kg)
    embed = colors.embed(title=f'{points:.2f}') \
                .set_author(name='Robi Points') \
                .add_field(name='World Record', value=f'**{world_record:g}** kg') \
                .add_field(name='Total', value=f'**{total_kg:g}** kg')
    return embed