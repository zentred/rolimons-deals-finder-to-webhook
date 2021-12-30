import requests, time, configparser, re, json, threading, ctypes
from threading import Thread
req = requests.Session()

completed = []

config = configparser.ConfigParser()
config.read('config.ini')

threshhold = 1-(int(config['config']['threshhold'])/100)
send_projected = config['config']['send_projected']
discord_id = config['config']['discord_id']
web = config['config']['webhook']
minimum_price = int(config['config']['minimum_price'])
maximum_price = int(config['config']['maximum_price'])

checked = 0
deals_a = 0

def title():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Pages Checked: {checked} | Deals Found: {deals_a}')

def deals():
    global checked
    checked += 1
    r = requests.get('https://www.rolimons.com/deals').text
    items = re.findall('item_details = (.*?);', r)[0]
    total = json.loads(items)
    for x in total:
        info = total[x]
        name, price, rap, projected, itemid = info[0], info[1], info[2], info[4], x
        check(name, price, rap, projected, itemid)

def check(name, price, rap, projected, itemid):
    global completed
    if not price == 0 and not rap == 0:
        drop = int(price) / int(rap)
        c = f'{itemid}:{drop}'
        if drop <= threshhold and not c in completed and price >= minimum_price and price <= maximum_price:
            completed.append(c)
            if send_projected == 'true':
                webhook(name, price, rap, projected, itemid)
            elif send_projected == 'false':
                if not projected == 1:
                    webhook(name, price, rap, projected, itemid)

def webhook(name, price, rap, projected, itemid):
    global deals_a
    data = {
      'content': f'<@{discord_id}>',
      'embeds':[{
          'author': {
              'name': name,
              'url': f'https://www.roblox.com/catalog/{itemid}',
              },
          'fields': [
              {'name': '\u200b','value': f'**Asset ID**: {itemid}\n**Asset Name**: {name}\n**Rap**: {rap}\n**Price**: {price}','inline':False},
          ],
          'thumbnail': {
              'url': f'https://www.roblox.com/asset-thumbnail/image?assetId={itemid}&width=420&height=420&format=png',
              }
      }]
    }
    requests.post(web, json=data).text
    deals_a += 1

Thread(target=title).start()
while True:
    deals()
    time.sleep(5)
