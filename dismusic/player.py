import asyncio
import os
from typing import Any
import discord
from wavelink import Player , AutoPlayMode 


class DisPlayer(Player):
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        self._volume : int = os.getenv('DISMUSIC_DEFAULT_VOLUME', 80)
        self.autoplay : AutoPlayMode = AutoPlayMode.partial
        self.source : str = os.getenv('DISMUSIC_DEFAULT_SOURCE' , 'ytsearch')
        self.bound_channel  = None
    
    async def connect(self, *, timeout: float = 10, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        self.client.dispatch('dismusic_player_create' , self)
        return await super().connect(timeout=timeout, reconnect=reconnect, self_deaf=self_deaf, self_mute=self_mute)    
    
    async def pause(self)->None:
        self.client.dispatch('dismusic_player_pause',self)
        return await super().pause(True)
    
    async def resume(self) -> None:
        self.client.dispatch('dismusic_player_resume',self)
        return await super().pause(False)
    
    async def disconnect(self, **kwargs: Any) -> None:
        self.client.dispatch('dismusic_player_destroy', self.guild)
        return await super().disconnect(**kwargs)
    



