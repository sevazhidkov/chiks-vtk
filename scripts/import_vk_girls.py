import os
import vk_api

from app.db import db

vk = vk_api.VkApi(os.environ['VK_LOGIN'], os.environ['VK_PASSWORD'])
vk.authorization()

girls = {}
# Сканируем все возраста от 14 до 25
for i in range(14, 26):
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
        girls[girl['id']] = {
            'name': girl['first_name'] + ' ' + girl['last_name'],
            'photo': girl['photo_200'],
            'link': 'https://vk.com/id' + str(girl['id']),
            'rating': 1000,
            'checks': 0
        }
        print(girl['id'], '- added.')
    print(i, 'age done.')


response = vk.method('groups.getMembers', {
    'group_id': 'slyhivtk',
    'count': 1000,
    'fields': 'photo_200,sex',
    'offset': 0
})
i = 0
while response['items']:
    for girl in response['items']:
        # Если это действительно девушка и у нее есть фотка
        if girl['sex'] == 1 and 'photo_200' in girl:
            girls[girl['id']] = {
                'name': girl['first_name'] + ' ' + girl['last_name'],
                'photo': girl['photo_200'],
                'link': 'https://vk.com/id' + str(girl['id']),
                'rating': 1000,
                'checks': 0
            }
            print(girl['id'], '- added.')

    response = vk.method('groups.getMembers', {
        'group_id': 'slyhivtk',
        'count': 1000,
        'fields': 'photo_200,sex',
        'offset': i + 1000
    })
    print(i, '- offset')

print('Adding to db')
db.girls.inset_many(list(girls.values()))
