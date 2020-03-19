import difflib
from discord.ext import commands

member_converter = commands.MemberConverter()

class MatchingMemberConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        try:
            member = await super().convert(ctx, argument)
        except:
            member = find_member(ctx, argument)
            if member:
                return member

ROLE_SCORE_WEIGHT = 0.025

def find_member(context, member_name):
    member = context.guild.get_member_named(member_name)

    if not member:
        members = context.guild.members
        members_by_name = {}
        for m in members:
            members_by_name[m.name] = m
            members_by_name[m.display_name] = m
            members_by_name[m.name.lower()] = m
            members_by_name[m.display_name.lower()] = m
        close_matches = difflib.get_close_matches(member_name, members_by_name, 5, 0.5)
        
        def score_member(name):
            similarity = match_ratio(member_name, name)
            similarity += match_ratio(member_name.lower(), name.lower()) / 2
            similarity /= 1.5

            member = members_by_name[name]
            role_score = score_member_role(context.guild, member)
            weighted_role_score = role_score * ROLE_SCORE_WEIGHT
            total_score = similarity + weighted_role_score

            print(f'{name}: {similarity:.2} + {(weighted_role_score):.2f} {total_score:.2f}')
            return total_score

        close_matches.sort(key=lambda name: score_member(name), reverse=True)
        print()

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