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

#colors




@bot.event
async def on_ready():
    print("ALLAH BOT ONLINE")


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

    with open('users.json', 'r') as f:
        users = json.load(f)

    #if str(ctx.guild.id) not in users:
        #users[str(ctx.guild.id)] = {}
        #users[str(ctx.guild.id)]["members"]={}
        #users[str(ctx.guild.id)]["server"]={}

#BOT ADMIN
@bot.command(pass_context=True)
async def ssh_run(ctx, *, arg):
    if ctx.author.id == 336180549192515585:
        os.system(arg)
        await ctx.send("Command excecuted")
    else:
        print("NOT ANDRE TRIED SSH RUN")
        pass

@bot.command(pass_context=True)
async def update(ctx):
    if ctx.author.id == 336180549192515585:
        embed=discord.Embed(color=0xfffffe)
        embed.set_author(name=f"UPDATING...")
        await ctx.send(embed=embed)
        os.system("python3 update.py")
    else:
        print("NOT ANDRE TRIED SSH RUN")
        pass


@bot.command(pass_context=True)
async def help(ctx):
    await ctx.send("help")




#server staff
@bot.command(pass_context=True)
async def kick(ctx, user:discord.Member, *, reason=None):
    try :
        if discord.Permissions.kick_members:
            await user.kick(reason=reason)
            embed=discord.Embed(title="Kick", description="{} Just got kicked by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
            embed.set_footer(text="Reason : {}".format(reason))
            await ctx.send(embed=embed)
        else:
            pass
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
            pass
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
@has_permissions(kick_members=True)
async def mute(ctx, user:discord.Member, *, arg=None):
    #struser=str(user)
    #username=struser[:-5]
    if user.guild_permissions.kick_members:
        await ctx.send("You cannot mute a staff member :pensive:")
    else:
        with open('users_warning.json', 'r') as f:
                users = json.load(f)

        role_to_add = discord.utils.get(ctx.guild.roles, name="Muted")
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

        await user.add_roles(role_to_add)

        embed=discord.Embed(color=0x940000)
        if arg:
            embed.set_author(name=f"Muted {user} for {arg} 🔇")
        else :
            embed.set_author(name=f"Muted {user} 🔇")
        await ctx.send(embed=embed)




@bot.command(pass_context=True)
@has_permissions(kick_members=True)
async def unmute(ctx, user:discord.Member):
    #struser=str(user)
    #username=struser[:-5]
    if user.guild_permissions.kick_members:
        await ctx.send("You cannot unmute a staff member :pensive:")
    else:
        with open('users_warning.json', 'r') as f:
                users = json.load(f)

        for role in users[str(user.id)]:
            role_id = int(role)
            role_name = discord.utils.get(ctx.guild.roles, id=role_id)
            role_to_add = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await user.add_roles(role_to_add)
            print(role_to_add)

        role_to_remove = discord.utils.get(ctx.guild.roles, name="Muted")

        await user.remove_roles(role_to_remove)
        embed=discord.Embed(color=0x197500)
        embed.set_author(name=f"Unmuted {user} 🔊")
        await ctx.send(embed=embed)

        with open('users_warning.json', 'w') as f:
            json.dump(users, f)



@bot.command(pass_context=True)
@has_permissions(kick_members=True)
async def purge(ctx, user:discord.Member):
    #struser=str(user)
    #username=struser[:-5]
    if user.guild_permissions.administrator:
        await ctx.send("You cannot purge a staff member :pensive:")
    else:
        with open('users_warning.json', 'r') as f:
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

        with open('users_warning.json', 'w') as f:
            json.dump(users, f)

        await user.add_roles(role_to_add)

        embed=discord.Embed(color=0x940000)
        embed.set_author(name=f"Purged {user} 👿💉")
        await ctx.send(embed=embed)



@bot.command(pass_context=True)
@has_permissions(kick_members=True)
async def unpurge(ctx, user:discord.Member):
    #struser=str(user)
    #username=struser[:-5]
    if user.guild_permissions.administrator:
        await ctx.send("You cannot purge a staff member :pensive:")
    else:
        with open('users_warning.json', 'r') as f:
                users = json.load(f)

        for role in users[str(user.id)]:
            role_id = int(role)
            role_name = discord.utils.get(ctx.guild.roles, id=role_id)
            role_to_add = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await user.add_roles(role_to_add)
            print(role_to_add)

        role_to_remove = discord.utils.get(ctx.guild.roles, name="💉 Purged")

        await user.remove_roles(role_to_remove)
        embed=discord.Embed(color=0x197500)
        embed.set_author(name=f"Unpurged {user} 👿💉")
        await ctx.send(embed=embed)

        with open('users_warning.json', 'w') as f:
            json.dump(users, f)




@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def purgespam(ctx, arg1, arg2):
    channel=ctx.guild.get_channel(772524551292190740)
    role = discord.utils.get(ctx.guild.roles, name="💉 Purged")
    s=["S","S","SECONDS","SECOND","SECOUNDS","SECOUND","SEC","SECS"]
    m=["M","M","MINUTES","MINUTE","MINS","MINS","MINUT","MINUTS", "MIN"]
    h=["H","HS","HRS","HR","HOUR","HOURS","HOR","HORS","HUR","HURS"]

    embed=discord.Embed(color=0x751900)

    str(arg2)
    arg1=int(arg1)
    if arg2.upper() in s:
        embed.set_author(name=f"Summoning started for {arg1} seconds 👿")
        await ctx.send(embed=embed)
        while arg1 != 0:
            await channel.send(f"{role.mention}")
            await asyncio.sleep(1)
            arg1=arg1-1
            if arg1==0:
                embed.set_author(name=f"Summoning has finished 🩸")
                await ctx.send(embed=embed)

    if arg2.upper() in m:
        embed.set_author(name=f"Summoning started for {arg1} minutes 👿")
        await ctx.send(embed=embed)
        arg1=arg1*60
        while arg1 !=0:
            await channel.send(f"{role.mention}")
            await asyncio.sleep(1)
            arg1=arg1-1
            if arg1==0:
                embed.set_author(name=f"Summoning has finished 🩸")
                await ctx.send(embed=embed)

    if arg2.upper() in h:
        embed.set_author(name=f"Summoning started for {arg1} hours 👿")
        await ctx.send(embed=embed)
        arg1=arg1*3600
        while arg1 !=0:
            await channel.send(f"{role.mention}")
            await asyncio.sleep(1)
            arg1=arg1-1
            if arg1==0:
                embed.set_author(name=f"Summoning has finished 🩸")
                await ctx.send(embed=embed)

@purgespam.error
async def purgespam_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed=discord.Embed(color=0x751900)
        embed.set_author(name=f"YOU ARE NOT ADMIN 😂")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0x751900)
        embed.set_author(name=f"COMMAND ERROR")
        embed.add_field(name="You must send in this format :", value="A?purgespam <number> <seconds, minutes or hours>", inline=True)
        embed.set_footer(text="Example : A?purgespam 50 seconds | Permissions needed : Administrator")
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def color(ctx, arg):
    arg=arg.lower()
    colors=["Red","Green","Blue","Pink","Purple","Yellow","Orange","Cyan"]


    if arg==help:
        pass

    if arg.capitalize() in colors:
        if arg.capitalise() in [y.name for y in ctx.author.roles]:
            color = discord.utils.get(ctx.guild.roles, name=f"{arg.capitalize()}")
            embed=discord.Embed(color=color.color)
            embed.set_author(name=f"{arg.upper()} IS REMOVED")
            await ctx.author.remove_roles(color)
            await ctx.send(embed=embed)
        else:
            color = discord.utils.get(ctx.guild.roles, name=f"{arg.capitalize()}")
            embed=discord.Embed(color=color.color)
            embed.set_author(name=f"YOU ARE NOW {arg.upper()}")
            await ctx.author.add_roles(color)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xfffffe)
        embed.set_author(name=f"WE DO NOT HAVE YOUR COLOR 😔")
        await ctx.send(embed=embed)







@bot.command(pass_context=True)
async def maths_game(ctx, *, arg):
    pass






token = open("token.txt", "r")

bot.run(token.read())
