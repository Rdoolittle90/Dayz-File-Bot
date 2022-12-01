from disnake import ApplicationCommandInteraction, Embed, SelectOption
from disnake.ui import View, Select



class select_vendors_select(Select):
    def __init__(self, product_name):
        self.product_name = product_name
        options=[
            SelectOption(label="BlackMarketTrader", emoji="🕶️", description="sDsd"),
            SelectOption(label="ClothingTrader", emoji="👕", description="sdfagsdfgsd"),
            SelectOption(label="ConsumeTrader", emoji="🍏", description="dsfdghdfh"),
            SelectOption(label="HelicopterTrader", emoji="🚁", description="ahfdjkjhl"),
            SelectOption(label="MiscTrader", emoji="🔩", description=";jkhgfd"),
            SelectOption(label="TheCollector", emoji="🪙", description="sDFGhjkl"),
            SelectOption(label="VehiclesTrader", emoji="🛻", description="Dhvjcfgdsdf"),
            SelectOption(label="WeaponSupplies", emoji="🔦", description="SDFGhjk"),
            SelectOption(label="WeaponTrader", emoji="🔫", description=";lkjhgfd")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: ApplicationCommandInteraction):
        await interaction.response.defer()
        embed = Embed(title=f"{self.values[0]}", description="Buy and Sell prices")
        
        await interaction.followup.send(embed=embed)


class select_vendors_view(View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(select_vendors_select())

