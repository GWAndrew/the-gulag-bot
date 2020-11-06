import discord
import asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands
import os
import random
import time
import json
from PIL import Image, ImageDraw, ImageFilter,ImageFont
from time import sleep
import requests
import shutil
from bs4 import BeautifulSoup
from igramscraper.instagram import Instagram


intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="A?", intents = intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("ALLAH BOT ONLINE")


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)



@bot.command(pass_context=True)
async def help(ctx):
    await ctx.send("help")


#server admins
@bot.command(pass_context=True)
async def kick(ctx, user:discord.Member, *, reason=None):
    try :
        if discord.Permissions.kick_members:
            await user.kick(reason=reason)
            embed=discord.Embed(title="Kick", description="{} Just got kicked by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
            embed.set_footer(text="Reason : {}".format(reason))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Kick", description="You do not have permissions to kick members", color=0x0a0a0a)
            await ctx.send(embed=embed)
    except :
        embed=discord.Embed(title="Kick", description="You cannot kick a staff member", color=0x0a0a0a)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def ban(ctx, user:discord.Member, *, reason=None):
    try :
        if discord.Permissions.ban_members:
            await user.ban(reason=reason)
            embed=discord.Embed(title="Ban", description="{} Just got banned by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
            embed.set_footer(text="Reason : {}".format(reason))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Ban", description="You do not have permissions to ban members", color=0x0a0a0a)
            await ctx.send(embed=embed)
    except :
        embed=discord.Embed(title="Ban", description="You cannot ban a staff member", color=0x0a0a0a)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def unban(ctx, id: int):
    if discord.Permissions.ban_members:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed=discord.Embed(title="Unban", description="{} Just got unbanned by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def purge(ctx, user:discord.Member):
    with open('users.json', 'r') as f:
            users = json.load(f)

    role = discord.utils.get(ctx.guild.roles, name="💉 Purged")

    users["members"][str(user.id)]={}

    await ctx.author.add_roles(role)
    await ctx.send("Purged :smiling_imp:")

    with open('users.json', 'w') as f:
        json.dump(users, f)


token = open("token.txt", "r")

bot.run(token.read())
