import requests
import time
req = requests.Session()

lst = []

start = 'item_details = {'
end = '};'
print('The threshold refers to the percentage. With an input of example "20", if the price goes under 20% of the rap, it will tell you in discord')
threshold = int(input('Do not include any letters. Enter threshold: '))
threshold = threshold / 100
threshold = 1 - threshold
print(threshold)

webhook = 'webhook here'

def deals():
    r = req.get('https://www.rolimons.com/deals').text
    r = r.split(start)[1]
    r = r.split(end)[0]
    r = r.replace('],"', '\n"')
    r = r.splitlines()
    for line in r:
        try:
            t = line.replace('"', '').replace(':[', ',').split(',')
            assetid, assetname, price, rap, projected = t[0], t[1], t[2], t[3], t[5]
            number = float(price) / float(rap)
            s = f'{assetid}:{number}'
            if float(number) <= float(threshold) and number != 0.0 and s not in lst:
                lst.append(s)
                print(f'{assetid} - {assetname} - {price} - {rap} - {projected}')
                data = {
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
                time.sleep(0.5)
        except: pass

i = 0

while True:
    i += 1
    deals()
    print(f'Checked deals page - {i}')
    time.sleep(60)
