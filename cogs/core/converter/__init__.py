import discord
import typing

from .emojis import NitroEmojiConverter as NitroEmoji
from .emojis import convert as emoji
from .members import MatchingMemberConverter

Member = typing.Union[discord.Member, MatchingMemberConverter]

from .person import to_dob as DOB
from .person import to_gender as Gender
from .person import MALE, FEMALE