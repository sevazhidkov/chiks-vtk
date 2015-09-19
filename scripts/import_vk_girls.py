import os
import vk_api

from app.db import db

vk = vk_api.VkApi(os.environ['VK_LOGIN'], os.environ['VK_PASSWORD'])
vk.authorization()

# Сканируем все возраста от 14 до 21
for i in range(14, 21):
    response = vk.method('users.search', {
        'sort': 0,
        'count': 250,
        'fields': 'photo_200',
        'city': 1100,
        'sex': 1,
        'age_from': i,
        'age_to': i
    })
    for girl in response['items']:
        if 'photo_200' not in girl:
            continue
        db.girls.insert_one({
            'name': girl['first_name'] + ' ' + girl['last_name'],
            'photo': girl['photo_200'],
            'link': 'https://vk.com/id' + str(girl['id']),
            'rating': 1000,
            'checks': 0
        })
        print(girl['id'], '- done.')
    print(i, 'age done.')
