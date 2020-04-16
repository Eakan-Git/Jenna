from math import *
import env

MATH_OPERATIONS = {
    'x': '*',
    ',': '',
    '^': '**',
    ' ': '',
}

async def compute(context, expr):
    if expr:
        for math, code in MATH_OPERATIONS.items():
            expr = expr.replace(math, code)
    else:
        return
    try:
        value = eval(expr)
        if value is not None:
            value = f'{value:,}'
            response = f"That's `{value}`"
            await context.send(response)
    except Exception as e:
        await context.message.add_reaction('⁉️')
        if env.TESTING:
            import traceback
            traceback.print_exc()