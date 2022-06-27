import discord
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    color = 0x1FE0B3

    def footer(self):
        return f"{self.clean_prefix}{self.invoked_with} [command] for more information."
    
    def get_command_signature(self, command):
        return f"```{self.clean_prefix}{command.qualified_name} {command.signature}```"
    
    async def send_cog_help(self, cog):
        e = discord.Embed(title = f"**{cog.qualified_name}** Commands", color = self.color)

        if cog.description:
            e.description = cog.description
        
        filtered = await self.filter_commands(cog.get_commands(), sort = True)

        for command in filtered:
            e.add_field(name = command.qualified_name, value = command.short_doc or "No description")
        
        e.set_footer(text = self.footer())
        await self.get_destination().send(embed = e)
    
    async def send_command_help(self, command):
        e = discord.Embed(title = command.qualified_name, color = self.color)

        if command.help:
            e.description = command.help
        
        e.add_field(name = "Signature", value = self.get_command_signature(command))
        e.set_footer(text = self.footer())

        await self.get_destination().send(embed = e)
    
    async def send_bot_help(self, mapping):
        e = discord.Embed(title = "Bot commands", color = self.color)
        description = self.context.bot.description
        if description:
            e.description = description
        
        for cog, commands in mapping.items():
            if not cog:
                continue

            filtered = await self.filter_commands(commands, sort = True)

            if filtered:
                value = "\t".join(f"`{i.name}`" for i in commands)
                e.add_field(name = cog.qualified_name, value = value)
        
        e.set_footer(text = self.footer())
        await self.get_destination().send(embed = e)

def setup(bot : commands.Bot):
    bot.help_command = HelpCommand()