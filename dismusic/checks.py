from discord.ext import commands

from .errors import MustBeSameChannel, NotConnectedToVoice, PlayerNotConnected , NothingIsPlaying


def voicechannelcheck():
    def predicate(ctx:commands.Context):
        if not getattr(ctx.author , 'voice', 'channel'):
            raise NotConnectedToVoice("You are not connected to any voice channel.")
        return True
    return commands.check(predicate) 

def botinvccheck():
    def predicate(ctx:commands.Context):
        if not ctx.voice_client:
            raise PlayerNotConnected("I am not connected to any voice channel.")
        return True
    return commands.check(predicate)

def samevccheck():
    def predicate(ctx:commands.Context):
        if ctx.voice_client:
            if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
                raise MustBeSameChannel("You must be connected to the same channel as the player.")
        return True
    return commands.check(predicate)

def playingcheck():
    def predicate(ctx:commands.Context):
        if not ctx.voice_client.current:
            raise NothingIsPlaying("I am playing anything right now.")
        return True
    return commands.check(predicate)
                




