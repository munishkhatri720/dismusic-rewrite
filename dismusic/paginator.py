import discord 
from discord.ext import commands
from typing import List
from ._classes import Colors

class EntriesPaginator(discord.ui.View):
    def __init__(self,title:str, context:commands.Context | discord.Interaction, entries:List[str],per:int=10, timeout: float | None = 180):
        self.author = context.user if isinstance(context,  discord.Interaction) else context.author
        self.entries = [entries[i:i+per] for i in range(0,  len(entries),  per)]
        self.title = title
        self.current_page :int = 0 
        self.context = context
        self.response :discord.InteractionMessage = None
        super().__init__(timeout=timeout)
        
    def create_embed(self,  entry:List[str])->discord.Embed:
        embed = discord.Embed(color=Colors.default)
        embed.title = self.title
        embed.description = '\n'.join(e for e in entry)
        embed.set_footer(text=f"Showing Entry {self.current_page+1}/{len(self.entries)}",icon_url=self.author.display_avatar.url if self.author.display_avatar else self.author.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()
        return embed
        
    def disable_buttons(self):
        self.go_first.disabled = False
        self.go_previous.disabled = False
        self.go_close.disabled = False
        self.go_next.disabled = False
        self.go_last.disabled = False
        
        if self.current_page == 0:
            self.go_first.disabled = True
            self.go_previous.disabled = True
                
        elif self.current_page == len(self.entries) - 1:
            self.go_next.disabled = True
            self.go_last.disabled = True
                    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content=f"Only **{self.author.name}** can interact to this view.",ephemeral=True)
            return False
        return True
    
    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        try:
            await self.response.edit(view=self)
        except:
            pass        
            
                       
    async def update_page(self,interaction:discord.Interaction):
        entry = self.entries[self.current_page]
        embed = self.create_embed(entry)
        self.disable_buttons()
        await interaction.response.edit_message(embed=embed, view=self)            
                
    async def start(self):
        if len(self.entries) == 1:
            self.clear_items()
            if isinstance(self.context,  commands.Context):
                self.response = await self.context.reply(embed=self.create_embed(self.entries[0]),view=None)
            else:
                self.response = await self.context.response.send_message(embed=self.create_embed(self.entries[0]),view=None,ephemeral=True)    
        else:
            if isinstance(self.context,  commands.Context):
                self.response = await self.context.reply(embed=self.create_embed(self.entries[0]),view=self)
            else:
                self.response = await self.context.response.send_message(embed=self.create_embed(self.entries[0]),view=self,ephemeral=True)     
        
    @discord.ui.button(label="First",style=discord.ButtonStyle.primary,custom_id="1",disabled=True)
    async def go_first(self,  interaction:discord.Interaction,  button:discord.ui.Button):
        self.current_page = 0
        await self.update_page(interaction)
            
        
    @discord.ui.button(label="Back",style=discord.ButtonStyle.green,custom_id="2",disabled=True)
    async def go_previous(self,  interaction:discord.Interaction,  button:discord.ui.Button):
        self.current_page -= 1 
        await self.update_page(interaction)  
        
    @discord.ui.button(label="Close",style=discord.ButtonStyle.red,custom_id="3")
    async def go_close(self,  interaction:discord.Interaction,  button:discord.ui.Button):
        await interaction.message.delete()
        
        
    @discord.ui.button(label="Next",style=discord.ButtonStyle.green,custom_id="4")
    async def go_next(self,  interaction:discord.Interaction,button:discord.ui.Button):
        self.current_page += 1 
        await self.update_page(interaction)
            
        
    @discord.ui.button(label="Last",style=discord.ButtonStyle.primary,custom_id="5")
    async def go_last(self,  interaction:discord.Interaction,  button:discord.ui.Button):
        self.current_page = len(self.entries) - 1
        await self.update_page(interaction)   