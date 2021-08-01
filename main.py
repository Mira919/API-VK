TOKEN = '35cbc798d0e2fc93d9e9fb388b93ea44d42e26fb1e2b6ec8cd1788cabb17c52eba8d01f4f4ee608edcffa'

def get_params(TOKEN): # обязательные параметры
    return {
    'access_token': TOKEN,
    'v': 5.89,
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