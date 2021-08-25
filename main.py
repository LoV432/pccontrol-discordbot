import discord
from discord.ext import commands
from requests import get
import os
from pyautogui import screenshot, move
import subprocess
import edit_image
import asyncio
from notification import ToastNotifier
import ctypes

allowed_server_role = 'ALLOWED SERVER ROLE HERE'

async def deleteMessage(lastMessage,selectedMessage):
    for message in selectedMessage:
        await lastMessage[message].delete()

async def clearHistory(selectedMessage):
    lastMessage = await pccontrol.history(limit=2).flatten()
    await asyncio.sleep(10)
    await deleteMessage(lastMessage,selectedMessage)


async def checkChannel(ctx):
    if ctx.channel == pccontrol and ctx.author == bot_owner:
        return True
    else:
        await intruderAlert(ctx.channel,ctx.guild,ctx.author)


async def intruderAlert(channel,guild,author):
    async with channel.typing():
        edit_image.makeimage(author)
        await channel.send(file=discord.File('result.png'))
        await bot_owner.send(str(author)+" used the bot on Guild:" + str(guild) + ", Channel:" + str(channel))
        ToastNotifier().show_toast("PcControl INTRUDER", str(author)+" used the bot on Guild:" + str(guild) + ", Channel:" + str(channel),icon_path="notification.ico" ,duration=None)

async def getChannelUser():
    global pccontrol,bot_owner
    pccontrol = await bot.fetch_channel("CHANNEL ID AS INT HERE")
    bot_owner = await bot.fetch_user("USER ID AS INT HERE")



killAllowed = ["notepad"]
runAllowed = ["notepad" ]

bot = commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    await getChannelUser()

@bot.command(brief="Reboots PC")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def reboot(ctx):
    await ctx.send("Rebooting Device!")
    await clearHistory(selectedMessage=[0,1])
    os.system("shutdown /r")

@bot.command(brief="Puts PC to Sleep-ish")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def sleep(ctx):
    await ctx.send("Going to Kinda Sleep-ish")
    await clearHistory(selectedMessage=[0,1])
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@bot.command(brief="Shuts Down PC")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("zZZzzZz")
    await clearHistory(selectedMessage=[0,1])
    os.system("shutdown /s")

@bot.command(brief="Sends Screenshot")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def s(ctx):
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x00000002)
        screenshot().save("discord.png")
        ToastNotifier().show_toast("PcControl","SS TAKEN",icon_path="notification.ico",duration=None)
        await ctx.send(file=discord.File('discord.png'))
        await ctx.send("SS")
        lastMessage = await pccontrol.history(limit=3).flatten()
        await lastMessage[0].add_reaction('\N{THUMBS UP SIGN}',)
        await asyncio.sleep(10)
        await deleteMessage(lastMessage,selectedMessage=[1,2])
    except Exception as error:
        return

@bot.command(brief="Sends IP")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def ip(ctx):
    ip = get('https://api.ipify.org').text
    await ctx.send(ip)
    ToastNotifier().show_toast("PcControl","IP TAKEN", icon_path="notification.ico",duration=None)
    await clearHistory(selectedMessage=[0,1])

@bot.command(brief="run")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def run(ctx, arg):
    if arg in runAllowed:
        subprocess.call('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe \PATH\TO\run\\' +arg +".lnk", shell=True)
    ToastNotifier().show_toast("PcControl","Script ran " + arg, icon_path="notification.ico" ,duration=None)
    await clearHistory(selectedMessage=[0])

@bot.command(brief="kill")
@commands.check(checkChannel)
@commands.has_role(allowed_server_role)
@commands.is_owner()
async def kill(ctx, arg):
    if arg in killAllowed:
        subprocess.call('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe Stop-Process -Name "' +arg + '" -Force', shell=True)
    ToastNotifier().show_toast("PcControl","Script killed " + arg, icon_path="notification.ico" ,duration=None)
    await clearHistory(selectedMessage=[0])

@bot.event
async def on_raw_reaction_add(payload):
    author = await bot.fetch_user(payload.user_id)
    channel = await bot.fetch_channel(payload.channel_id)
    try:
        guild = await bot.fetch_guild(payload.guild_id)
    except:
        guild = "Direct Message"


    try:
        if payload.member.bot:
            return
    except:
        await intruderAlert(channel,guild,author)
        return


    if author == bot_owner and channel == pccontrol:
        await s(pccontrol) 
    else:
        await intruderAlert(channel,guild,author)
    

bot.run('BOT TOKEN HERE')

    
