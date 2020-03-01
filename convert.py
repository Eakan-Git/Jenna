import difflib
from discord.ext import commands

member_converter = commands.MemberConverter()

async def to_user(context, member_name):
    if member_name:
        try:
            member = await member_converter.convert(context, member_name)
        except:
            member = find_member(context, member_name)
            if member:
                return member
            await context.send(f"Who's **{member_name}**?")
            import traceback; traceback.print_exc()
            return
    else:
        member = context.author
    return member

def find_member(context, member_name):
    member = context.guild.get_member_named(member_name)

    if not member:
        members = context.guild.members
        members_by_nick_lower = { mem.display_name.lower(): mem for mem in members}
        members_by_name_lower = { mem.name.lower(): mem for mem in members}
        members_by_nick = { mem.display_name: mem for mem in members}
        members_by_name = { mem.name: mem for mem in members}
        members_by_name = { **members_by_nick_lower, **members_by_name_lower, **members_by_nick, **members_by_name }
        close_matches = difflib.get_close_matches(member_name, members_by_name, 5, 0.25)
        
        def score_member(name):
            similarity = match_ratio(member_name, name)
            similarity += match_ratio(member_name.lower(), name.lower()) / 2
            similarity /= 1.5

            member = members_by_name[name]
            role_score = score_member_role(context.guild, member)

            total_score = similarity + role_score * .02
            
            return total_score

        close_matches.sort(key=lambda name: score_member(name), reverse=True)

        if close_matches:
            name = close_matches[0]
            member = members_by_name[name]
    
    return member

def match_ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def score_member_role(guild, member):
    role_count = len(guild.roles)
    role_score = [role.position / role_count for role in member.roles]
    return sum(role_score)