import configparser
import asyncio
import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import nest_asyncio
import pandas as pd
import os

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient('username3', int(api_id), api_hash)

all_messages = []
limit = 100
until_date = datetime.datetime(2022, 9, 15).date()
end_date = datetime.datetime(2022, 2, 20).date()

async def main(phone, channel_name):
    await client.start(phone)
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
            
    user_input_channel = 'https://t.me/' + channel_name
    channel = await client.get_entity(user_input_channel)
    
    end_parsing = False
    current_date = until_date
    mes_offset = 0
    
    while not end_parsing:
        messages = await client.get_messages(channel, limit=limit, offset_date=until_date, add_offset=mes_offset)
        
        for message in messages:
            dic = message.to_dict()
            all_messages.append(dic)
            current_date = dic['date'].date()
        
        mes_offset = mes_offset + limit

        if current_date < end_date:
            end_parsing = True
            print("#### END ####")


def parse_channel(channel_name):
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(phone, channel_name))

    df = pd.DataFrame(all_messages)
    grouped = df.groupby([df['date'].dt.date])
    dfs_by_date = [{'key': key, 'data': group} for key, group in grouped]
    dfs_by_date.reverse()
    for df_for_day in dfs_by_date:
        current_date = df_for_day['key']
        path = 'messages/' + channel_name + '/messages_{}.csv'.format(current_date.strftime("%Y_%m_%d"))
        if os.path.isfile(path):
            df_for_day['data'].to_csv(path, mode='a')
        else:
            df_for_day['data'].to_csv(path)
        if (current_date.day == 1):
            print('Saved for : ', current_date.strftime("%Y-%m"))