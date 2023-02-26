from disnake.ext.commands import Cog

class UserCog(Cog):
    def __init__(self, bot):
        self.bot = bot