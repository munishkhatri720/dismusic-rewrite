from dataclasses import dataclass
from typing import Union
import discord


@dataclass
class Colors:
    default = discord.Color.dark_theme()
    error = discord.Color.red()

@dataclass
class Emojis:
    PREV = "⬅️"
    NEXT = "➡️"
    FIRST = "⏮️"
    LAST = "⏭️"


@dataclass
class Loop:
    NONE = "NONE"
    CURRENT = "CURRENT"
    PLAYLIST = "PLAYLIST"

    TYPES = [NONE, CURRENT, PLAYLIST]
