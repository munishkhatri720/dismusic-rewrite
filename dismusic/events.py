import wavelink
import discord
from discord.ext import commands
from .utils import format_millisecond
from ._classes import Colors
from .errors import ( MustBeSameChannel, NotConnectedToVoice,
                     NotEnoughSong, NothingIsPlaying, PlayerNotConnected)
from .player import DisPlayer
from wavelink import TrackStartEventPayload , TrackEndEventPayload , TrackStuckEventPayload , TrackExceptionEventPayload , NodeReadyEventPayload

class MusicEvents(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_wavelink_track_start(self , payload : TrackStartEventPayload ):
        player : DisPlayer = payload.player
        track : wavelink.Playable = payload.track
        original : wavelink.Playable = payload.original
        player.client.dispatch('dismusic_track_start' , player , track , original)
            
            
            
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload : TrackEndEventPayload):
        player : DisPlayer = payload.player
        track = payload.track
        original = payload.original
        player.client.dispatch("dismusic_track_end", player , track , original)
        
    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, payload : TrackExceptionEventPayload):
        track = payload.track
        player = payload.player
        exception = payload.exception
        self.bot.dispatch("dismusic_track_exception", player, track , exception)
        

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, payload : TrackStuckEventPayload):
        self.bot.dispatch("dismusic_track_stuck", payload.player, payload.track , payload.threshold)

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context , error:commands.CommandError):
        errors = (

            MustBeSameChannel,
            NotConnectedToVoice,
            PlayerNotConnected,
            NothingIsPlaying,
            NotEnoughSong,
        )

        if isinstance(error, errors):
            await ctx.send(error)
        else:
            pass
