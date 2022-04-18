import discord
from discord.ext import commands
import random
import json
from hikari import Embed
import requests
import giphy_client
from giphy_client.rest import ApiException
import os


client = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

client.remove_command('help')


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)





@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = '.help'))


@client.command()
async def ching(ctx):
    em = discord.Embed(description = 'Chong', color = ctx.author.color)
    await ctx.send(embed = em)


@client.command()
async def ping(ctx):
    em = discord.Embed(title = 'Ping', description = f'Pong! {round(client.latency * 1000)}ms ', color = ctx.author.color)
    await ctx.send(embed = em)


@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    em = discord.Embed(title = '8ball', description = f'Question: {question}\nAnswer: {random.choice(responses)}', color = ctx.author.color)
    await ctx.send(embed = em)


@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Ask a question dummy')

@client.command()
async def kick (ctx, member : discord.Member, *, reason = None):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await member.kick(reason = reason)
        em = discord.Embed(title = 'Kick', description = f'{member.mention} has been kicked!', color = ctx.author.color)
        await ctx.send(embed = em)
    else:
        await ctx.send('You do not have Administrator role')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Could you mention who you would like to kick next time?')



@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await member.ban(reason = reason)
        await ctx.send(f'{member.mention} has been banned!')
    else:
        await ctx.send('You do not have the Administrator role')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Could you mention who you would like to ban next time?')


@client.command()
async def clear(ctx, amount: int):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit = amount + 1)
    else:
        await ctx.send('You do not have the manage messages permission')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Could you specify how many messages you want to clear next time?')
    elif (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.send('You do not have the manage messages permission')


@client.command()
async def say(ctx, *, arg):
    em = discord.Embed(title = arg, description = arg, color = ctx.author.color)
    await ctx.send(embed = em)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You gonna tell me what to say or ?')


@client.command()
async def quote(ctx):
    quote = get_quote()
    em = discord.Embed(title = 'Quote', description = quote, color = ctx.author.color)
    await ctx.send(embed = em)


@client.command()
async def gif(ctx, *, q = "Wave"):

    api_key = 'SKDqjbCEUp2FVlEaxgbs9GKz2XCH2zOz'
    api_instance = giphy_client.DefaultApi()

    try:
        api_responce = api_instance.gifs_search_get(api_key, q, limit = 7, rating = 'r')
        lst = list(api_responce.data)
        giff = random.choice(lst)
        emb = discord.Embed(title = q, color = ctx.author.color)
        emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed = emb)

    except ApiException as e:
        print("Exception when calling Api")



@client.command()
async def developers(ctx):
    
    em = discord.Embed(title = 'Developers', description = 'The developers of this project are Daniel HD and UrIntelMine', color = ctx.author.color)
    
    await ctx.send(embed = em)



@client.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title = 'Help', description = 'Use .help command to find information on our commands', color = ctx.author.color)

    em.add_field(name = 'Moderation', value = 'kick, ban, clear, developers')
    em.add_field(name = 'Fun', value = 'ching, 8ball, gif, quote, say')

    await ctx.send(embed = em)


@help.command()
async def kick(ctx):
    em = discord.Embed(title = 'Kick', description = 'Kicks a member from the server', color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.kick <member> [reason]')

    await ctx.send(embed = em)


@help.command()
async def ban(ctx):
    em = discord.Embed(title = 'Ban', description = 'Bans a member from the server', color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.ban <member> [reason]')

    await ctx.send(embed = em)


@help.command()
async def ching(ctx):
    em = discord.Embed(title = 'Ching', description = "Says 'chong'", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.ching')

    await ctx.send(embed = em)



@help.command()
async def quote(ctx):
    em = discord.Embed(title = 'Quote', description = "Gives an inspiring quote for some motivation", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.quote')

    await ctx.send(embed = em)


@help.command(aliases = ['8ball'])
async def _8ball(ctx):
    em = discord.Embed(title = '8ball', description = "Ask 8ball anything and it will respond with wise!", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.8ball will i win the lotto')

    await ctx.send(embed = em)


@help.command()
async def gif(ctx):
    em = discord.Embed(title = 'Gif', description = "Use this command to custom search giphy and send a gif! If you don't provide a search, it will automatically default to a wave gif", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.gif hello')

    await ctx.send(embed = em)


@help.command()
async def clear(ctx):
    em = discord.Embed(title = 'clear', description = "This command will purge a set amount of messages specified.  Server owners don't panic as only those with the manage messages role can use this", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.clear 30')

    await ctx.send(embed = em)


@help.command()
async def say(ctx):
    em = discord.Embed(title = 'Say', description = "Bubbli will say anything you want her to say!", color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.say hello')

    await ctx.send(embed = em)


@help.command()
async def developers(ctx):
    em = discord.Embed(title = 'Developers', description = 'Tells you the developers of this project', color = ctx.author.color)
    em.add_field(name = '**Syntax**', value = '.developers')

    await ctx.send(embed = em)








client.run(TOKEN)