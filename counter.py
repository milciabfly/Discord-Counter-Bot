'''モジュール読み込み'''
import os 
import discord
from discord import app_commands
from dotenv import load_dotenv
import json
from func import CounterView
import global_value as g_value
import global_value as g_path


'''環境変数読み込み'''
load_dotenv()

'''定数/変数'''
TOKEN = os.getenv("DISCORD_TOKEN")
SAVE_PATH = "data/count.json"
count = 0

intents = discord.Intents.all()
client = discord.Client(intents=intents)
slash_command = app_commands.CommandTree(client)

# カウント保存用のパス

'''メソッド'''
# ボタンを設置するためのコマンド
@slash_command.command(name = "ボタン設置", description = "カウンターボタンを設置するためのボタン")
async def set_button(interaction : discord.Interaction):
    print("ボタンを設置します。")

    # 管理者以外は除外
    if(not interaction.permissions.administrator):
         await interaction.response.send_message(content="このコマンドはサーバー管理者のみ使用できます。", ephemeral=True)
         return
    
    await interaction.response.send_message(content=f"現在のカウント数：{g_value.count}", view=CounterView())

    

'''BOT 起動時に実行'''
@client.event
async def on_ready():
    await slash_command.sync(guild=None)

    # jsonをロードしてFunc.pyにインスタンス変数を設定
    global count
    if(not os.path.isdir(SAVE_PATH.split("/")[0])): # フォルダが無かったら作成
        print("[data] ディレクトリが存在しなかっため作成")
        os.mkdir(SAVE_PATH.split("/")[0])
    elif(os.path.isfile(SAVE_PATH)): # ファイルがあれは読み込み
        with open(SAVE_PATH, "r") as file:
            count = int(json.load(file))
    
    # グローバル変数登録
    g_path.path = SAVE_PATH
    g_value.count = count

    # ステータス変更
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f"クリックしてね ₍ᐢ｡•༝•｡ᐢ₎"))

    # 再起動時 ボタンを有効化
    client.add_view(CounterView())


'''DISCORD BOT 起動'''
client.run(TOKEN)