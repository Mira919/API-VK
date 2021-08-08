import json
import requests
import pprint
import time

TOKEN = 'beeaf7e82cda0751791175f11855355aa9eb9f945e4e3dcc0b22aac63bf94b95de7c0a954be1fafc3f68b'

def get_params(TOKEN): # обязательные параметры
    return {
    'access_token': TOKEN,
    'v': 5.131,
    }

def get_groupINFO_user(): # получаем информацию о группах пользователя
    params = get_params(TOKEN)
    params['extended'] = 1
    params['fields'] = 'members_count'
    groups_user = requests.get(
        'https://api.vk.com/method/groups.get',
        params = params
    )
    print(groups_user.json())
    groups_user = groups_user.json()['response']
    groups_user = groups_user['items']
    return groups_user

def get_friendID(): # получаем id друзей пользователя
    params = get_params(TOKEN)
    friends_user = requests.get(
        'https://api.vk.com/method/friends.get',
        params = params
    )
    friends_user = friends_user.json()['response']
    friends_user = friends_user['items']
    return friends_user

def get_groupID_friends(): # получаем id групп друзей пользователя
    params = get_params(TOKEN)
    list_group_friend = []
    for friend in get_friendID():
        params['user_id'] = friend
        try: # чтобы поймать ошибку когда страница пользователя закрыта
            friend_group = requests.get(
                'https://api.vk.com/method/groups.get',
                params = params
            )
            friend_group = friend_group.json()['response']
            friend_group = friend_group['items']
            list_group_friend += friend_group
            print('Идет поиск групп у пользователя c id:', params['user_id']) # показывает что программа не зависла
            time.sleep(2) # чтобы не было ошибки: слишком много обращений к API (Too many requests per second)
        except KeyError:
            print(f"У пользователя c id {params['user_id']} закрыта страница")
    return list_group_friend

def get_group(): # получаем группы, где состоит пользователь, но не состоит никто из его друзей
    list1 = []
    dict1 = {}
    groups_user = get_groupINFO_user()
    list_group_friend = get_groupID_friends()
    for group in groups_user:
        if group['id'] not in list_group_friend:
            dict1['name'] = group['name']
            dict1['gid'] = group['id']
            dict1['members_count'] = group['members_count']
            list1.append(dict1)
            dict1 = {}
    return list1

with open('groups.json', 'w', encoding='utf-8') as file:
    json.dump(get_group(), file, ensure_ascii=False, indent=2)

with open('groups.json', encoding='utf-8-sig') as file:
    data = json.load(file)
print(data)