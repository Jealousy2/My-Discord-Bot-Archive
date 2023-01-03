#import
from turtle import width
import requests
import asyncio
import sys
import datetime
import json
import os
import random
import sqlite3 as sl
import time
from multiprocessing.sharedctypes import Value
from random import choice

import aiohttp
import animec
import colorama
import discord
import DiscordUtils
from colorama import Fore
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from nekobot import NekoBot
from pystyle import Box
from youtubesearchpython import Search
from discord import File
from easy_pil import Editor, load_image_async, Font


music = DiscordUtils.Music()
con = sl.connect('my-test.db')
cur = con.cursor()
colorama.init()
api = NekoBot()
img = api.get_image("neko").message
r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
snipe_message_author = {}
snipe_message_content = {}
with open('config.json', 'r+') as file:
    data = file.read()
    f = json.loads(data)
    token = f['token']
    pinglog = f['pinglog']
    ownerid = f['owneruserid']

if pinglog == "True":
    pinglogg = True

elif pinglog == "False":
    pinglogg = False

else:
    print(f"{Fore.RED}[!]{Fore.RESET} You need to fix wether or not pinglog is enabled. Only 'True', and 'False', will work. Make sure it's in quotes. By default it will be off.")
    pinglogg = False
    time.sleep(3); os.system("cls")

#defining shit for commands ig
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='>>', case_insensitive=True, intents=intents)
client.remove_command("help")



eballresponses = ["My sources point to yes", "My sources point to no.", "Maybe", "Yes.", "No.", "Absolutely!", "Absolutely not!", "No lol", "Yes ofc!"]
penissizes=["8D", "8=D", "8==D", "8===D", "8====D", "8=====D", "8======D", "8=======D", "8=========D", "8============================D"]

#titles
def title():
    os.system("cls")
    tittle = f"""{Fore.MAGENTA}
░░░░░██╗███████╗░█████╗░██╗░░░░░░█████╗░██╗░░░██╗░██████╗
░░░░░██║██╔════╝██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔════╝
░░░░░██║█████╗░░███████║██║░░░░░██║░░██║██║░░░██║╚█████╗░
██╗░░██║██╔══╝░░██╔══██║██║░░░░░██║░░██║██║░░░██║░╚═══██╗
╚█████╔╝███████╗██║░░██║███████╗╚█████╔╝╚██████╔╝██████╔╝
░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░╚═════╝░
{Fore.RESET}
"""
    print(tittle)
#client events
@client.event
async def on_ready():
    title()
    print(f"\n{Fore.MAGENTA}")
    print(Box.DoubleCube(f"Bot now online! Logged in as {client.user}"))
    print(f"\t{Fore.RESET}")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)



#default help menu
@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Help menu | Jealous Bot", description="Shows all commands", colour=discord.Colour.from_rgb(r, g, b))
    embed.add_field(name=f"Administator commands", value="Shows all admin commands | **>>admin**", inline=False)
    embed.add_field(name=f"General commands", value="All general commands for Jealous bot! | **>>general**", inline=False)
    embed.add_field(name=f"Fun commands", value="Shows all fun commands | **>>fun**", inline=False)
    embed.add_field(name=f"Music commands", value="Shows all music commands | **>>music**", inline=False)
    embed.add_field(name=f"nsfw commands", value="Shows all nsfw commands | **>>nsfw**", inline=False)
    await ctx.send(embed=embed)

#admin help menu
@client.command(name="admin")
async def _admin(ctx):
    embed = discord.Embed(title="Admin commands | Jealous Bot", description="Things in '{}' are optional!", colour=discord.Colour.from_rgb(r, g, b))
    embed.add_field(name="Ban", value="Bans a user | **>>ban @userhere {reason}**", inline=False)
    embed.add_field(name="Ticket", value="Creates a ticket for members to get support | **>>ticket**", inline=False)
    embed.add_field(name="Warn", value="Warns a user | **>>warn @userhere {reason}**", inline=False)
    embed.add_field(name="unban", value="unBans a user | **>>unban @userhere {reason}**", inline=False)
    embed.add_field(name="Kick", value="Kicks a user | **>>kick @userhere {reason}**", inline=False)
    embed.add_field(name="Purge", value="Purges a certain amount of messages | **>>purge numberhere**", inline=False)
    embed.add_field(name="snipe", value="snipes recently deleted messages | **>>snipe**", inline=False)
    embed.add_field(name="timeout", value="timeouts a user for a certain amount of time| **>>timeout @user (time)**", inline=False)
    await ctx.send(embed=embed)


#general command menu
@client.command(name="general")
async def _helpgeneral(ctx):
    embed = discord.Embed(title="General commands | Jealous Bot", description="All general commands | Things in '{}' are optional!")
    embed.add_field(name="whois", value="Gives you info on a user | **>>whois {@userhere}**", inline=False)
    embed.add_field(name="dm", value="dms a user | **>>dm {@userhere} (say whatever)**", inline=False)
    embed.add_field(name="drake", value="drake meme (example pint mega+pint) | **>>drake (say whatever)**", inline=False)
    embed.add_field(name="pooh", value="same as drake meme | **>>pooh (say whatever)**", inline=False)
    embed.add_field(name="oog", value="same as pooh & drake meme | **>>oog (say whatever)**", inline=False)
    embed.add_field(name="serverinfo", value="Gives you info on the server | **>>serverinfo**", inline=False)
    embed.add_field(name="creds", value=f"Credits of the bots devs/whatever :eyes: | **>>credits**", inline=False)


    await ctx.send(embed=embed)

#start of the rps
@client.command()
async def rps(ctx, message):
    answer = message.lower()
    choices = ["rock", "paper", "scissors"]
    computers_answer = random.choice(choices)
    if answer not in choices:
        await ctx.send("That is not a valid option! please use one of these options rock,paper,scissors")
        return
    else:
        if computers_answer == answer:
            await ctx.send(f"Tie! we both pickes {answer}")
        if computers_answer == "rock":
            if answer == "paper":
                await ctx.send(f"You Win! i picked {computers_answer} and you picked {answer}!")
        if computers_answer == "paper":
            if answer == "rock":
                await ctx.send(f"I Win! I picked {computers_answer} and you picked {answer}!")
        if computers_answer == "scissors":
            if answer == "rock":
                await ctx.send(f"I Win! I picked {computers_answer} and you picked {answer}!")
        if computers_answer == "rock":
            if answer == "scissors":
                await ctx.send(f"I Win I picked {computers_answer} and you picked {answer}!")
        if computers_answer == "paper":
            if answer == "scissors":
                await ctx.send(f"You Win I picked {computers_answer} and you picked {answer}!")
        if computers_answer == "scissors":
            if answer == "paper":
                await ctx.send(f"I Win I picked {computers_answer} and you picked {answer}!")        
#end of the rps

#meme command
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            



@client.command()
async def credits(ctx):
    embed = discord.Embed(title="Jealousy Bot")
    embed.add_field(name="Developers", value="Made by Jealousy#0001 (he has no friends)")
    embed.add_field(name="Upcoming updates", value="I plan on making fun commands (truth or dare) and more")
    
    await ctx.send(embed=embed)
#meme command

@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  icon = str(ctx.guild.icon)
  memberCount = str(ctx.guild.member_count)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )

  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  embed.add_field(name='Highest role', value=ctx.guild.roles[-2], inline=False)
  embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
  embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
  
  
  await ctx.send(embed=embed)


#fun command menu
@client.command(name="fun")
async def funcommands(ctx):
    embed = discord.Embed(title="Fun commands | Jealous Bot", description="All fun commands | Things in '{}' are optional!")
    embed.add_field(name="penis", value="See how big ur pp is | **>>penis {@userhere}**", inline=False)
    embed.add_field(name="emojify", value="emojifys words/numbers| **>>emojify word or numbers**", inline=False)
    embed.add_field(name="8ball", value="Ask eightball a question! | **>>8ball question here**", inline=False)
    embed.add_field(name="rps", value="Rock, Paper, Scissors | **>>rps**", inline=False)
    embed.add_field(name="meme", value="sends random memes (dont spam) | **>>meme**", inline=False)
    embed.add_field(name="Animemes", value="sends random Animemes (dont spam) | **>>Animemes**", inline=False)
    embed.add_field(name="dankmemes", value="sends random dankmemes (dont spam) | **>>dankmemes**", inline=False)
    embed.add_field(name="punch", value="punches user thats @ | **>>punch @user**", inline=False)
    embed.add_field(name="hug", value="hug user thats @ | **>>hug @user**", inline=False)
    embed.add_field(name="slap", value="slap user thats @ | **>>slap @user**", inline=False)
    embed.add_field(name="cuddle", value="cuddles user thats @ | **>>cuddle @user**", inline=False)
    embed.add_field(name="kill", value="kills user thats @ | **>>kill @user**", inline=False)
    embed.add_field(name="highfive", value="highfives user thats @ | **>>highfive @user**", inline=False)
    embed.add_field(name="kiss", value="kisses user thats @ | **>>kiss @user**", inline=False)
    embed.add_field(name="esex", value="esexes user thats @ | **>>esex @user**", inline=False)
    embed.add_field(name="coinflip", value="coin  | **>>coin**", inline=False)
    embed.add_field(name="cats", value="cat  | **>>cats**", inline=False)
    embed.add_field(name="birds", value="bird  | **>>bird**", inline=False)
    embed.add_field(name="dogs", value="dog  | **>>dogs**", inline=False)
    embed.add_field(name="pandas", value="panda  | **>>pandas**", inline=False)
    embed.add_field(name="frogs", value="frog  | **>>frogs**", inline=False)
    embed.add_field(name="penguins", value="penguin  | **>>penguins**", inline=False)
    await ctx.send(embed=embed)




 #attempt at coinflip command ( i hate making it shits annoying /yourgay)

determine_flip = [1, 0]

@client.command()
async def coinflip(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped coin, we got **Heads**!")
        embed.set_image(url=f"https://i.ebayimg.com/images/g/xtcAAOSwLwBaZigS/s-l400.jpg")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped coin, we got **Tails**!")
        embed.set_image(url=f"https://bjc.edc.org/June2017/bjc-r/img/5-algorithms/img_flipping-a-coin/Tails.png")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


#music command menu          
@client.command(name="music")
async def musichelp(ctx):
    embed = discord.Embed(title="Music commands | Jealous Bot")
    embed.add_field(name="Join", value="Makes the bot join your vc | **>>join**")
    embed.add_field(name="Play", value="Plays a song in your vc | **>>play songhere**")
    embed.add_field(name="Pause", value="Pauses the current song | **>>pause**")
    embed.add_field(name="Resume", value="Resumes a paused song | **>>resume**")
    embed.add_field(name="leave", value="leavesvc | **>>leave**")
    embed.add_field(name="loop", value="loops a song | **>>loop**")
    embed.add_field(name="queue", value="queue a song | **>>loop**")
    await ctx.send(embed=embed)
#client commands


@client.command()
async def penis(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author

    embed = discord.Embed(title="Penis size")
    embed.add_field(name=f"{member.display_name} Penis size is: ", value=random.choice(penissizes))
    await ctx.send(embed=embed)

@client.command(name="8ball")
async def eightball(ctx, *, args):
    thechoice = random.choice(eballresponses)
    embed = discord.Embed(title="8ball  :8ball:")
    embed.add_field(name="Response: ", value=thechoice)
    await ctx.send(embed=embed)
    
    
#ping
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")
#pong

    
#start of whois
@client.command()
async def whois(ctx, member: discord.Member=None):
    if member == None:
        member=ctx.author

    rlist = []
    for role in member.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at,)
    embed = discord.Embed(title="Jealousy bot (i get curious who people are too!)")
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name='ID:',value=member.id,inline=False)
    embed.add_field(name="Display name: ", value=member.display_name, inline=True)
    embed.add_field(name='Name:',value=member.display_name,inline=False)
    embed.add_field(name='Account Created at:',value=member.created_at,inline=False)
    embed.add_field(name='Account Joined at:',value=member.joined_at,inline=False)
    embed.add_field(name="Guild name:", value=member.display_name)
    embed.add_field(name='Bot?',value=member.bot,inline=False)
    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
    await ctx.send(embed=embed)
#end of whois

#dm
@client.command()
async def dm(ctx, user: discord.User, *, msg, reason = None):

 await ctx.send(f"I'm messaging {user.mention}!")
 await user.send({'From The Hangout'})
 await user.send(msg)
 await ctx.send(f':white_check_mark: Your Message has been sent')
 
#dm


#stat of avatar command
@client.command()
async def avatar(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
        
    embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at,)
    embed.add_field(name="Display Name:", value=member.display_name)
    await ctx.send(member.avatar.url)
    await ctx.send(embed = embed)
#end of it (updated it a little cuz im extra)


@client.command(name="ban")
@has_permissions(ban_members=True)
async def banmember(ctx, member: discord.Member, *, args=None):
    if args == None:
        reason=""
        dmmaybe = False
    else:
        reason=args
        dmmaybe = True

    if dmmaybe == False:
        return
    else:
        await member.send(f"You were banned from '{ctx.guild_name}' for '{reason}'")

    await member.ban(reason=reason)




@client.command(name="kick")
@has_permissions(kick_members=True)
async def kickmember(ctx, member: discord.Member, *, args=None):
    if args == None:
        reason=""
        dmmaybe = False
    else:
        reason=args
        dmmaybe = True

    if dmmaybe == False:
        return
    else:
        await member.send(f"You were kicked from '{ctx.guild_name}' for '{reason}'")

    await member.kick(reason=reason)

@client.command(name="purge")
@has_permissions(manage_messages=True)
async def _purgemessages(ctx, amount: int):
    removemsg = 1
    await ctx.channel.purge(limit=removemsg)
    await ctx.channel.purge(limit=amount)

client.sniped_messages = {}
@client.event
async def on_message_delete(message):
    if message.attachments:
        bob = message.attachments[0]
        client.sniped_messages[message.guild.id] = (bob.proxy_url, message.content, message.author, message.channel.name, message.created_at)
    else:
        client.sniped_messages[message.guild.id] = (message.content,message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        bob_proxy_url, contents,author, channel_name, time = client.sniped_messages[ctx.guild.id]
    except:
        contents,author, channel_name, time = client.sniped_messages[ctx.guild.id]
    try:
        embed = discord.Embed(description=contents , color=discord.Color.purple(), timestamp=time)
        embed.set_image(url=bob_proxy_url)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(description=contents , color=discord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")
        await ctx.channel.send(embed=embed)


#MUSIC FROM HERE ON
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    if player: player.delete()
    await ctx.voice_client.disconnect()
    await ctx.send('**Disconnected**')




@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused: **{song.name}**")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed: **{song.name}**")


@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for : **{song.name}**")
    else:
        await ctx.send(f"Disabled loop for: **{song.name}**")

@client.command()
async def queue(ctx):
    embedVar = discord.Embed(title="Queue",color=0x00ff00)
    player = music.get_player(guild_id=ctx.guild.id)
    i=1
    for song in player.current_queue():
      songnon = song.name
      embedVar.add_field(name=f'Song Number: {i}',value=songnon,inline=False)
      i+=1
    await ctx.send(embed=embedVar)



@client.command()
async def play(ctx, *, args: str):
    allSearch = Search('{}'.format(args), limit = 1)
    dataloadz = allSearch.result()
    link = dataloadz['result'][0]['link']
    title = dataloadz['result'][0]['title']
    dura = dataloadz['result'][0]['duration']
    urlthumb = dataloadz['result'][0]['thumbnails'][0]['url']
    await ctx.send('Loading song')
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(link, search=True)
        song = await player.play()
        request = ctx.author
        requested = str(request)
        embed = discord.Embed(title="Jealousy Music | **>>music**", colour=discord.Colour.from_rgb(r, g, b))
        embed.add_field(name="Now playing:", value = title, inline=True)
        embed.add_field(name="Duration:", value = dura, inline=True)
        embed.add_field(name="Link: ", value=f"[Click here]({link})", inline=True)
        embed.set_thumbnail(url=urlthumb)
        await ctx.send(embed=embed)
    else:
        song = await player.queue(link, search=True)
        await ctx.send(f"Queued: **{song.name}**")
        embed = discord.Embed(title="Queued your song")
        embed.add_field(name=f"{song.name}")
        

@client.command(name="np")
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    request = ctx.author
    requested = str(request)
    embed = discord.Embed(title="Jealous Music | **>>music**", colour=discord.Colour.from_rgb(r, g, b))
    embed.add_field(name="Now playing:", value = song.title, inline=True)
    embed.add_field(name="Duration", value = song.duration, inline=True)
    embed.set_thumbnail(url=song.thumbnail)
    await ctx.send(embed=embed)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    await ctx.send(f"Skipped **{data[0].name}**")

@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))

    await ctx.send(f"Removed **{song.name}** from queue. L")

punch_gifs = ['https://media.giphy.com/media/8D1upwhhOTHo3UKhGy/giphy.gif']
punch_names = ['Punches you!']

@client.command()
async def punch(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(punch_gifs)))
    
    
    
    await ctx.send(embed = embed)
    

hugs_gif = ['https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif']
hugs_name = ['hugs you!']

@client.command()
async def hug(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(hugs_gif)))
    
    
    
    await ctx.send(embed = embed)
    
slap_gif = ['https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif']
slap_name = ['slaps you!']

@client.command()
async def slap(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(slap_gif)))
    
    
    
    await ctx.send(embed = embed)
    
cuddle_gif = ['https://media.giphy.com/media/MrXjQjL5HV8urYBhLZ/giphy.gif']
cuddle_name = ['cuddles you!']

@client.command()
async def cuddle(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(cuddle_gif)))
    
    
    
    await ctx.send(embed = embed)
    
kill_gif = ['https://c.tenor.com/NbBCakbfZnkAAAAC/die-kill.gif']
kill_name = ['killes you cutely!']

@client.command()
async def kill(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(kill_gif)))
    
    
    
    await ctx.send(embed = embed)   

highfive_gif = ['https://c.tenor.com/JBBZ9mQntx8AAAAC/anime-high-five.gif']
highfive_name = ['high fives you cutely!']

@client.command()
async def highfive(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(highfive_gif)))
    
    
    
    await ctx.send(embed = embed)  
    
kiss_gif = ['https://c.tenor.com/UQwgkQbdp48AAAAC/kiss-anime.gif']
kissname = ['kisses you cutely!']

@client.command()
async def kiss(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(kiss_gif)))
    
    
    await ctx.send(embed = embed)  
#timeout
@client.command()
async def timeout(ctx, member: discord.Member, minutes: int=None):

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)

        embed=discord.Embed(description=f"", color=discord.Colour.blurple())
        embed.set_author(name=f"Successfully timedout {member.name} for {minutes} minutes", icon_url="https://cdn.discordapp.com/emojis/951165672031940668.gif?size=96&quality=lossless")

        await ctx.reply(embed=embed)     
    
 
esex_gif = ['https://media.discordapp.net/attachments/814308114325045248/960369307152429105/360f2e35ec74d7c16d98d4ddec5ce98d.gif']
esex_name = ['esexes you cutely!']

@client.command()
async def esex(ctx):
    embed = discord.Embed()
    colour = discord.Colour.random()
    description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    
    
    embed.set_image(url=(random.choice(esex_gif)))
    
    
    
    await ctx.send(embed = embed)  
    

#start of unban
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
             await ctx.guild.unban(user)
             await ctx.channel.send(f"Unbanned: {user.mention}")
#end of unban


#start of emojify command       
@client.command()
async def emojify(ctx, *, text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two',
                       '3':'three','4':'four','5':'five',
                       '6':'six','7':'seven','8':'eight',
                       '9':'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await ctx.send(''.join(emojis))
#end of emojify command



     
        
#start of meme commands   
@client.command()
async def drake(ctx, msg1, msg2):
    embed = discord.Embed(title="Drake meme")
    embed.set_image(url=f"https://api.popcat.xyz/drake?text1={msg1}&text2={msg2}")
    await ctx.send(embed=embed)
    request = ctx.author
    requested = str(request)
    

@client.command()
async def pooh(ctx, msg1, msg2):
    embed = discord.Embed(title="pooh meme")
    embed.set_image(url=f"https://api.popcat.xyz/pooh?text1={msg1}&text2={msg2}")
    await ctx.send(embed=embed)
    request = ctx.author
    requested = str(request)
    

@client.command()
async def oog(ctx, msg):
    embed = discord.Embed(title="oog meme")
    embed.set_image(url=f"https://api.popcat.xyz/oogway?text={msg}")
    await ctx.send(embed=embed)
    request = ctx.author
    requested = str(request)
    
#end of meme commands


#Ticket command (very basic im lazy)
@client.command(pass_context=True)
async def ticket(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title = 'Ticket system',
        description = 'React 📩 to make a ticket.',
        color = 0
    )

    embed.set_footer(text="ticket system")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")
    await client.wait_for("reaction_add")

    def check(reaction, user):
        return str(reaction.emoji) == '📩' and ctx.author == user
    await client.wait_for("reaction_add", check=check)
    await guild.create_text_channel(name=f'ticket - {ctx.author}')
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel('Ticket-Support', overwrites=overwrites)
#end of ticket command

#animec
@client.command()
async def anime(ctx,*, query,):
        try:
            anime = animec.Anime(query)
        except:
            await ctx.send(embed= discord.Embed(description = "No Anime is found", color = discord.Color.red()))
            return
        embed = discord.Embed(title = anime.title_english,url = anime.url,description = f"{anime.description[:200]}...",color = discord.Color.blue())
        embed.add_field(name = "Episodes",value = str(anime.episodes))
        embed.add_field(name = "Rating",value = str(anime.rating))
        embed.add_field(name = "Status",value = str(anime.status))
        embed.add_field(name = "NSFW status",value = str(anime.is_nsfw()))
        embed.add_field(name = "Type",value = str(anime.type))
        embed.add_field(name = "Description",value = str(anime.description))
        embed.set_thumbnail(url = anime.poster)
        await ctx.send(embed = embed)
        

#to verify nsfw channel or not
async def nsfwimgfunc(ctx, img_endpoint, title, description):
    if not ctx.channel.is_nsfw():
        embed = discord.Embed(title="Jealousy bot")
        embed.add_field(name="You tried running an NSFW command in a non-nsfw channel", value="Please run this command in an NSFW channel.")
        await ctx.send(embed=embed)
        return
    if ctx.channel.is_nsfw():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        embed = discord.Embed(title="Jealousy bot", description=description, colour=discord.Colour.from_rgb(r, g, b))
        image = nsfw.img(img_endpoint)
        embed.set_image(url=image)
        await ctx.send(embed=embed)










#nsfw from down on and others.




















#nsfw help menu
@client.command(name="nsfw")
async def nsfw(ctx):
    embed = discord.Embed(title="NSFW Commands | Jealousy Bot", description="All nsfw commands")
    embed.add_field(name="yaoi", value="yaoi pics :eyes: | **>>yaoi**", inline=False)
    embed.add_field(name="porn", value="porn pics :eyes: | **>>porn**", inline=False)
    embed.add_field(name="Feet", value="Feet pics :eyes: | **>>Feet**", inline=False)

    await ctx.send(embed=embed)
    await nsfwimgfunc(ctx,"nsfw","","")
    
    

#yaoi
@client.command(pass_context=True)
async def yaoi(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/Yaoi_IRL/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"yaoi","","")
#Lewdkem




@client.command(pass_context=True)
async def feet(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/feetpics/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"feet","","")
            
#Yuri https://www.reddit.com/r/Lesbian/new.json?sort=hot

@client.command(pass_context=True)
async def porn(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/Tits4U/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"Yuri","","")
            

#Animemes
@client.command(pass_context=True)
async def Animemes(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r//new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


#dankmemes
@client.command(pass_context=True)
async def dankmemes(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


#NEKOPARAGAME
@client.command(pass_context=True)
async def gay2(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r//new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"gay2","","")

@client.command(pass_context=True)
async def neko(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r//new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"neko","","")


#gifs4you



@client.command(pass_context=True)
async def handpics(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r//new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"handpics","","")
    
@client.command(pass_context=True)
async def milf(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r//new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await nsfwimgfunc(ctx,"milf","","")                                        
            
                    
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Made by Jealousy..'))


@client.command()
@has_permissions(ban_members=True)
async def Selfdestruct(ctx, *, guild_name):
    guild = discord.utils.get(client.guilds, name=guild_name)
    if guild is None:
        print("No guild with that name")
        return
    await guild.leave()
    await ctx.send(f"I left: {guild.name}")

@client.command(name='membercount')
async def membercount(ctx):
    await ctx.send(ctx.guild.member_count)



#animal commands.
#due today Cats, dogs, birds, pandas and frogs. 

@client.command(pass_context=True)
async def cats(ctx):
    embed = discord.Embed(title="cats!", description="puthy pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/Catswithjobs/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def dogs(ctx):
    embed = discord.Embed(title="dogs!", description="dog pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/rarepuppers/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def birds(ctx):
    embed = discord.Embed(title="birdsss!", description="bird pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/whatsthisbird/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def pandas(ctx):
    embed = discord.Embed(title="pandas!", description="panda pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/panda/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def frogs(ctx):
    embed = discord.Embed(title="frogs!", description="frog pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/frogs/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def penguins(ctx):
    embed = discord.Embed(title="penguins!", description="penguin pics")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/penguin/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)



#not working yet old code from github
@client.event
async def on_member_join(member):


  channel = client.get_channel(1047714272970559569)

  role = get(member.guild.roles, name="dead")
  await member.add_roles(role)

  pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)

  if pos == 1:
    te = "st"
  elif pos == 2:
    te = "nd"
  elif pos == 3:
    te = "rd"
  else: te = "th"

  background = Editor("pic3.jpg") 
  profile_image = await load_image_async(str(member.avatar.url))  #avatar.url (not avatar_url)

  profile = Editor(profile_image).resize((150, 150)).circle_image()
  poppins = Font.poppins(size=50, variant="bold")

  poppins_small = Font.poppins(size=20, variant="light")

  background.paste(profile, (325, 90))
  background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)

  background.text((400, 260), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")
  background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")
  background.text((400, 360), f"You Are The {pos}{te} Member", color="#0BE7F5", font=poppins_small, align="center")

  file = File(fp=background.image_bytes, filename="pic3.jpg")


  await channel.send(f"Heya {member.mention}! Welcome To **{member.guild.name} For More Information Go To <#1042408762918580274>**")


  await channel.send(file=file)

@client.event
async def on_member_remove(member):
  channel = client.get_channel(1047714272970559569)

  await channel.send(f"{member.name} Has Left The server, We are going to miss you :( ")
#not working yet old code from github





client.run(token)

#2/22/21 - project started.
#2/23/21- Added all nsfwimage.png commands(at school like a good pro hakkerman)
#2/23/21 4:35 pm - working on admin commands



#7/6/2022
#fix nasty nsfw commands
#fix ugly cuddles,hug,slap,kiss,
#fix credits command
#fix music command (in hell)
#add yaoi
#update music_help and fun commands
#update and add more admin commands
#--------   
#all fixed in one day except nsfw 


#add whatever else (fun commands)

