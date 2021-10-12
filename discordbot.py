import discord
from os import getenv
from discord.ext import commands

bot = commands.Bot(command_prefix="rb!", intents=discord.Intents.all(), help_command=None)
RESPONSES = {
    "おはよう": "おはよう！",
    "おやすみ": "おやすみ！",
    "疲れた": "おつかれ！"
}
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for rk, rv in RESPONSES.items():
        if rk in message.content:
            await message.reply(rv)
    
    await bot.process_commands(message)
@bot.event
async def on_ready():
    print("オンライン")
    game = discord.Game(f"rb! | {len(bot.guilds)}サーバー | {len(bot.users)}ユーザー | 作成者: aroko1#6837")
    await bot.change_presence(activity=game, status=discord.Status.do_not_disturb)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -MissingPermissions", description="実行者の必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -BotMissingPermissions", description=f"Botの必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title=":x: 失敗 -CommandNotFound", description=f"不明なコマンドもしくは現在使用不可能なコマンドです。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title=":x: 失敗 -MemberNotFound", description=f"指定されたメンバーが見つかりません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数がエラーを起こしているため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed) 
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数が足りないため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed) 
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed = discord.Embed(title=":x: 失敗 -CommandInvokeError", description=f"コマンドには属性がないため実行できません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、@aroko1#6837をメンションしてください。")
        await ctx.send(embed=embed)
    else:
        raise error

@bot.command()
async def hello(ctx):
    await ctx.send("こんにちは！")

@bot.command()
async def help(ctx):
    guild = ctx.message.guild
    embed = discord.Embed(title=f"コマンド一覧 - {guild.name}", timestamp=ctx.message.created_at, color=discord.Colour.dark_blue(), inline=False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="ここに移行しました", value="https://readybotcommands.web.fc2.com/", inline=False)
    embed.set_footer(text=f" 実行者: {ctx.author} ", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.listen()
async def on_message(message):
    if message.channel.name == global_channel_name:
        if message.author.bot:
            return
        for channel in bot.get_all_channels(): 
            if channel.name == global_channel_name: 
                if channel == message.channel: 
                    continue

                embed=discord.Embed(description=message.content, color=discord.Colour.dark_blue()) 
                embed.set_author(name="{}#{}".format(message.author.name, message.author.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(message.author.id, message.author.avatar))
                embed.set_footer(text="{} / メッセージid {}".format(message.guild.name, message.id),icon_url="https://media.discordapp.net/icons/{}/{}.png?size=1024".format(message.guild.id, message.guild.icon))
                if message.attachments != []: #添付ファイルが存在するとき
                    embed.set_image(url=message.attachments[0].url)

                if message.reference:
                    reference_msg = await message.channel.fetch_message(message.reference.message_id) 
                    if reference_msg.embeds and reference_msg.author == bot.user: 
                        reference_message_content = reference_msg.embeds[0].description 
                        reference_message_author = reference_msg.embeds[0].author.name 
                    elif reference_msg.author != bot.user:
                        reference_message_content = reference_msg.content 
                        reference_message_author = reference_msg.author.name+'#'+reference_msg.author.discriminator
                    reference_content = ""
                    for string in reference_message_content.splitlines(): 
                        reference_content += "> " + string + "\n"
                    reference_value = "**@{}**\n{}".format(reference_message_author, reference_content) 
                    embed.add_field(name='返信', value=reference_value, inline=True) 
                await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
            if after.author.bot: 
                return    
            await after.edit(after.id)

@bot.command()
async def report(ctx, *, value):
    channel = bot.get_channel(895268495745507348)
    await channel.send(f"{str(value)} - {ctx.author.name}|{ctx.author.id}")
    await ctx.send("送信しました。")
    
@bot.command()
async def idprofile(ctx, id=None):
    rc = discord.Colour.dark_blue()
    if id is None:
      await ctx.send("idを入力してください")
      return
    embed = discord.Embed(title=f":ballot_box_with_check: 処理中", description=f"読み込み中です", color=rc)
    message = await ctx.send(embed=embed)
    member = await bot.fetch_user(id)
    botcheak = member.bot
    if botcheak is True:
     cheak = "はい"
    if botcheak is False:
     cheak = "いいえ"
    if member.system is True:
     cheakk = "はい"
    if member.system is False:
     cheakk = "いいえ"
    e = discord.Embed(title=f"{member.name}の情報", description=f"{member.name}の詳細を表示します", color=rc)
    e.add_field(name=f"名前", value=member.name + "#" + member.discriminator, inline=False)
    e.add_field(name='ID', value=member.id, inline=False)
    e.add_field(name='作成時間(UTC)', value=member.created_at, inline=False)
    e.add_field(name="Bot", value=cheak, inline=False)
    e.add_field(name="System", value=cheakk)
    e.add_field(name="ニックネーム/メンション", value=f"{member.display_name} / {member.mention}", inline=False)
    e.set_thumbnail(url=member.avatar_url)
    await message.edit(embed=e)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.message.guild
    roles =[role for role in guild.roles]
    text_channels = [text_channels for text_channels in guild.text_channels]
    embed = discord.Embed(title=f"Serverinfo - {guild.name}", timestamp=ctx.message.created_at, color=discord.Colour.dark_blue(), inline=False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="地域", value=f"{ctx.guild.region}", inline=False)
    embed.add_field(name="チャンネル数", value=f"{len(text_channels)}", inline=False)
    embed.add_field(name="ロール数", value=f"{len(roles)}", inline=False)
    embed.add_field(name="サーバーブースター", value=guild.premium_subscription_count, inline=False)
    embed.add_field(name="メンバー数", value=guild.member_count, inline=False)
    embed.add_field(name="サーバー設立日", value=guild.created_at, inline=False)
    embed.set_footer(text=f" 実行者: {ctx.author} ", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"ユーザー {member}がサーバーからBanされました。")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kick", descriprtion=f"{member}がkickされました。", color=discord.Colour.dark_blue())
    await ctx.send(embed=embed)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
