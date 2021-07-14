import discord
import youtube_dl
import os
from discord.ext import commands

TOKEN = 'ODY0NDk1NTUyODM0MTc0OTg2.YO2SOQ.nnNRPX5EjQckUSr0JE_nCktwirk'

client = commands.Bot(command_prefix='ydl!')

@client.event
async def on_ready():
    print('Bot is ready')


@client.command()
async def DL(ctx, url=None):
    await ctx.message.delete()

    if url == None:
        await ctx.channel.send('エラー:引数が入力されていません。')
        await ctx.channel.send('入力したにも関わらず、エラーが繰り返し起こる場合は、DLコマンドとURLが全角空白または空白がない可能性があります。')
        return

    await ctx.channel.send('ダウンロード中...')
    ydl = youtube_dl.YoutubeDL({'outtmpl': './cache/%(title)s.%(ext)s','format': 'best'})

    with ydl:
        result = ydl.extract_info(
            url,
            download=True
        )

        path = './cache'
        file_info = os.listdir(path)
        #print(file_info)

        await ctx.channel.send('ダウンロード完了', file=discord.File(f'./cache/{file_info[0]}'))
        print('[INFO]アップロード完了')

        os.remove(f'./cache/{file_info[0]}')
        print('[INFO]キャッシュを削除しました。')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        sentence = 'エラー:容量が超過しているため。アップロードできませんでした…'

        await ctx.channel.send(sentence)
        print(f'[INFO Error]{sentence}')
        
        path = './cache'
        file_info = os.listdir(path)
        print('[INFO]キャッシュを調べています。')
        
        os.remove(f'./cache/{file_info[0]}')
        print('[INFO]キャッシュを削除しました。')

client.run(str(TOKEN))