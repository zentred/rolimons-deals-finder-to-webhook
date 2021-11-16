import requests, time
req = requests.Session()

lst = []

print('The threshold refers to the percentage. With an input of example "20", if the price goes under 20% of the rap, it will tell you in discord')
threshold = int(input('Do not include any letters. Enter threshold: '))
threshold = threshold / 100
threshold = 1 - threshold

blacklist = open('blacklisted.txt','r',encoding='utf-8',errors='ignore').read().splitlines()

webhook = input('Enter webhook: ')
discord_id = input('Enter discord ID: ')

def deals():
    r = req.get('https://www.rolimons.com/deals', timeout=4).text.split('item_details = {')[1].split('};')[0].replace('],"', '\n"').splitlines()
    for line in r:
        try:
            format_check = line.split('"')[3]
            comma_count = format_check.count(',')
            if comma_count == 0:
                t = line.replace('"', '').replace(':[', ',').split(',')
                assetid, assetname, price, rap, projected = t[0], t[1], t[2], t[3], t[5]
                to_send = f'{assetid}/{assetname}/{price}/{rap}/{projected}'
                check(to_send)
            elif comma_count == 1:
                t = line.replace('"', '').replace(':[', ',').split(',')
                assetname = t[1] + ',' + t[2]
                assetid, assetname, price, rap, projected = t[0], assetname, t[3], t[4], t[5]
                to_send = f'{assetid}/{assetname}/{price}/{rap}/{projected}'
                check(to_send)
            elif comma_count == 2:
                t = line.replace('"', '').replace(':[', ',').split(',')
                assetname = t[1] + ',' + t[2] + ',' + t[3]
                assetid, assetname, price, rap, projected = t[0], assetname, t[4], t[5], t[6]
                to_send = f'{assetid}/{assetname}/{price}/{rap}/{projected}'
                check(to_send)
        except Exception as err:
            print(err)

def check(to_send):
    try:
        assetid, assetname, price, rap, projected = to_send.split('/',5)
        try:
            number = float(price) / float(rap)
        except: pass
        else:
            s = f'{assetid}:{number}'
            if float(number) <= float(threshold) and number != 0.0 and not s in lst and projected != '1' and not assetid in blacklist:
                lst.append(s)
                print(f'{assetid} - {assetname} - {price} - {rap} - {projected}')
                data = {
                      'content': f'<@{discord_id}>',
                      'embeds':[{
                          'author': {
                              'name': assetname,
                              'url': f'https://www.roblox.com/catalog/{assetid}',
                              },
                          'color': int('C875C4',16),
                          'fields': [
                              {'name': '\u200b','value': f'**Asset ID**: {assetid}\n**Asset Name**: {assetname}\n**Rap**: {rap}\n**Price**: {price}','inline':False},
                          ],
                          'thumbnail': {
                              'url': f'https://www.roblox.com/asset-thumbnail/image?assetId={assetid}&width=420&height=420&format=png',
                              }
                      }]
                    }
                r = requests.post(webhook, json=data).text
    except Exception as err:
        print(err)

i = 0

while True:
    i += 1
    deals()
    print(f'Checked deals page - {i}')
    time.sleep(5)
