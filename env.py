from dotenv import dotenv_values

def try_convert_bool(value):
    if type(value) == str:
        if value.lower() == 'on':
            value = True
        elif value.lower() == 'off':
            value = False
    return value

def try_convert_const(value):
    value = value.strip()
    value = try_convert_bool(value)
    return value

for key, value in dotenv_values().items():
    value = try_convert_const(value)
    globals()[key] = value