import datetime
import inspect
import json

import nextcord
from nextcord import (Button, ButtonStyle, Embed, Interaction, User,
                      slash_command)
from nextcord.ext import commands

from src.dayz.player_trading import player_trade
from src.discord.bot import DiscordBot
from src.helpers.colored_printing import colorized_print


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Testing"

    # =====================================================================================================
    @slash_command(dm_permission=False, name="trade", description="placeholder description 1")
    async def trade(self, interaction: Interaction, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
        colorized_print("WARNING", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(embed=await player_trade(self.bot, interaction.user, player_1_map.title(), player_2, player_2_map.title(), trade_amount))


    @slash_command(dm_permission=False, name="test_embed", description="placeholder description 1")
    async def test_embed(self, interaction: nextcord.Interaction):
        self.bot.get_settings_json()
        
        message_id = None
        if interaction.user.id in self.bot.settings["persistent_messages"].keys():
            message_id = self.bot.settings["persistent_messages"][interaction.user.id]["message_id"]
            number = self.bot.settings["persistent_messages"][interaction.user.id]["number"]
            self.bot.update_settings_file()

        embed = Embed(title="Persistent Embed", description="This embed is persistent.")
        embed.add_field(name="Number", value=number)
        if message_id is None:
            # Send new message
            message = await interaction.channel.send(embed=embed)
            self.bot.settings["persistent_messages"][interaction.user.id]["message_id"] = message.id
            with open('message_id.json', 'w') as f:
                json.dump({'message_id': message.id}, f)
                self.bot.update_settings_file()
        else:
            # Edit existing message
            message = await interaction.channel.fetch_message(message_id)
            await message.edit(embed=embed)

        # Add buttons
        button = Button(style=ButtonStyle.blurple, label="Increment", custom_id="increment")
        view = nextcord.ui.View()
        view.add_item(button)
        await message.edit(view=view)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: nextcord.Interaction):
        if interaction.custom_id == "increment":
            self.bot.settings["persistent_messages"][interaction.user.id]["number"] += 1
            number = self.bot.settings["persistent_messages"][interaction.user.id]["number"]
            embed = Embed(title="Persistent Embed", description="This embed is persistent.")
            embed.add_field(name="Number", value=f"{number - 1} -> {number}")
            self.bot.update_settings_file()
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()


def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))
    



