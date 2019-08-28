import requests
import time
import threading



def findRegStreams(token, user):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'X-Auth-User': user,
        'X-Auth-Token': token
    }

    r = requests.get('https://api.sliver.tv/v1/channel_need_raffles/list?number=100', headers=head)
    body = r.json()['body']
    streamIDs = []
    for item in body:
        streamIDs.append(item['live_stream_id'])
        print(
            f"The livestream {item['live_stream_id']} rewards {item['live_stream']['base_reward_amount']} coins per minute")
    return streamIDs


def findTFuelStreams(streams, token, user):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'X-Auth-User': user,
        'X-Auth-Token': token
    }

    r = requests.get('https://api.sliver.tv/v1/theta/channel/list?number=100', headers=head)
    body = r.json()['body']
    for item in body:
        streams.append(item['live_stream_id'])
        print(
            f"The livestream {item['live_stream_id']} rewards {item['live_stream']['base_reward_amount']} coins per minute")
    return streams


def watchStream(streamID, token, user):
    print(f"\nWatching stream for {streamID}\n")
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'X-Auth-User': user,
        'X-Auth-Token': token
    }
    num = 0
    while True:
        num += 1
        r = requests.get(f'https://api.sliver.tv/v1/live/{streamID}', headers=head)
        if num >= 2:
            print(f"\nCoins added for {streamID}\n")
        time.sleep(60)


def getAccounts():
    with open('auths.txt', 'r') as f:
        users = f.read().splitlines()
    return users


def body(account):
    hold = account.split(':')
    token = hold[0]
    user = hold[1]
    streams = findRegStreams(token, user)
    streams = findTFuelStreams(streams, token, user)  # note, doesnt't seem to affect the amount of streams found
    holdList = []
    # sort out duplicates
    for stream in streams:
        if stream in holdList:
            pass
        else:
            holdList.append(stream)
    for stream in holdList:
        threading.Thread(target=watchStream, args=(stream, token, user, )).start()


accounts = getAccounts()
for account in accounts:
    threading.Thread(target=body, args=(account, )).start()
