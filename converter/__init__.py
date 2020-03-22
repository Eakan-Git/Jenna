import discord
import typing

from converter.emojis import NitroEmojiConverter as NitroEmoji
from converter.emojis import convert as emoji
from converter.members import MatchingMemberConverter

Member = typing.Union[discord.Member, MatchingMemberConverter]

from converter.person import to_dob as DOB
from converter.person import to_gender as Gender