import discord
import asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands
import os
import random
import time
import json
from time import sleep
import requests
import shutil
from bs4 import BeautifulSoup
from discord.utils import get



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

    role_to_add = discord.utils.get(ctx.guild.roles, name="💉 Purged")
    a=0
    users[str(user.id)]={}
    removing_roles=[]
    for role in user.roles:
        if a==0:
            a=1
        else:
            removing_roles.append(f"{role.id}")
            role_id = int(role.id)
            role_name = discord.utils.get(ctx.guild.roles, id=role_id)
            role_to_remove = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await user.remove_roles(role_to_remove)
            print(role_to_remove)

    users[str(user.id)]=removing_roles

    with open('users.json', 'w') as f:
        json.dump(users, f)

    #print(user.roles)
    #for role in user.roles:
        #print(role.id)
    await user.add_roles(role_to_add)
    await ctx.send("Purged :smiling_imp:")







@bot.command(pass_context=True)
async def unpurge(ctx, user:discord.Member):
    with open('users.json', 'r') as f:
            users = json.load(f)

    for role in users[str(user.id)]:
        role_id = int(role)
        role_name = discord.utils.get(ctx.guild.roles, id=role_id)
        role_to_add = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
        await user.add_roles(role_to_add)
        print(role_to_add)

    role_to_remove = discord.utils.get(ctx.guild.roles, name="💉 Purged")

    await ctx.author.remove_roles(role_to_remove)
    await ctx.send("Unpurged :smiling_imp:")

    with open('users.json', 'w') as f:
        json.dump(users, f)



token = open("token.txt", "r")

bot.run(token.read())
