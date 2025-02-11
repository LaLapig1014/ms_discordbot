# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
import json
import gspread
from google.oauth2.service_account import Credentials
import base64
import tempfile
# 讀取 JSON 文件
def get_cred():
    with open('ms_price.txt', 'r', encoding="UTF-8") as enc:
        encryptdata = enc.read()
        decoded_bytes = base64.b64decode(encryptdata)
        decoded_data = json.loads(decoded_bytes.decode('utf-8'))  # 轉回 JSON
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    with open(temp_file.name, "w", encoding="utf-8") as f:
        json.dump(decoded_data, f)
    
    return temp_file.name # 將 JSON 寫入臨時文件

# 設定 Google Sheets API 的範圍
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# 使用服務帳戶的憑證
creds = Credentials.from_service_account_file(get_cred(), scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "https://docs.google.com/spreadsheets/d/1sEsgGr2ajuHtrqAtlBrViphQxwtYFrGWjFiXIAQEalU/edit?gid=0#gid=0"
# 打開試算表
workbook = client.open_by_url(sheet_id)

# 取得第一個工作表
worksheet = workbook.sheet1

# intents是要求機器人的權限
intents = discord.Intents.all()

# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "%", intents = intents)


price_box=[[1,"經驗秘藥(大)",0,0]
,[2,"財物秘藥(大)",0,0]
,[3,"財物秘藥(小)",0,0]
,[4,"小型濃縮經驗",0,0]
,[5,"杜松種子精油",0,0]
,[6,"最高級怪物結晶",0,0]
,[7,"賢者之石",0,0]
,[8,"最高級空瓶",0,0]
,[9,"製作書",0,0]
,[10,"鮮明黃昏精隨",0,0]
,[11,"小型經驗",0,0]
,[12,"牛膝草精油",0,0]
]

id_convert={1:11,2:12,3:13,4:14,5:5,6:6,7:7,8:8,9:16,10:17,11:18,12:19,13:20}
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")



@bot.command()
# 輸入%Hello呼叫指令
async def Hello(ctx):
    # 回覆Hello, world!
    await ctx.send("Hello, world!")
@bot.command()
async def p(ctx):
    data = worksheet.get_all_values()
    #print(data)
    for item in data:
        #print(item,item[0],item[1])
        item[0]=item[0].strip()  #讀取出來的資料會多一個空格 要去除空格
        if item[0]:
            for it in price_box:
                if it[1] == item[0]:
                    #print(it[1],item[0])
                    it[2]=item[1].strip()
    price_box[0][3]=data[1][13]
    price_box[1][3]=data[3][13]
    price_box[2][3]=data[5][13]
    price_box[3][3]=data[7][13]
    #---------------------
    embed = discord.Embed(
        title="商品價格查詢",
        description=f"網址:\nhttps://docs.google.com/spreadsheets/d/1sEsgGr2ajuHtrqAtlBrViphQxwtYFrGWjFiXIAQEalU/edit?gid=0#gid=0",
        color=0x1e90ff  # 設定顏色（藍色）
    )
    embed.add_field(name=f"ID|      商品      |      價格      |      利潤      |", value=f"", inline=False)       
    temp=""
    
    for its in price_box:
        #temp=str(its[0]).ljust(2)+"|"+its[1].ljust(8)+"|"+its[2].ljust(10)+"|"+str(its[3]).ljust(4)
        temp= f"{str(its[0]):<4} | {str(its[1]):<10} | {str(its[2]):<12} | {str(its[3]):<6}\n"
        print(temp)
        embed.add_field(name=f"", value=f"```{temp}```", inline=False)
        print(its)
    await ctx.send(embed=embed)

@bot.command()
# 輸入%Hello呼叫指令
async def u(ctx,input_id:int,input_price:int):
    print(input_id,input_price)
    #print(id_convert[input_id])
    cid=id_convert[input_id]
    if cid:
        worksheet.update_cell(cid, 2, input_price)
    await ctx.send("update price")
def refreshjson():
    pass
bot.run("MTMwMzc2OTMyMTkxNDUwMzE5OA.GwBQjb.frA6B18-6XAqNHmFHvqziQ5o5eWguISmRPxhB8")