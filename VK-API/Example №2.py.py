# -*- coding: utf-8 -*-
import vk_api
import csv

# Authorization in VK API
vk_session = vk_api.VkApi(token='TOKEN')
vk = vk_session.get_api()

# Get ID of the "Lentach" group
group_ids = [29534144]  # replace with the actual group ID(s)
group_info = vk.groups.getById(group_ids=group_ids)
group_id = group_info[0]['id']

# Get list of subscribers of the "Lentach" group
subscribers = vk.groups.getMembers(group_id=group_id, fields='sex,city,relation', count=1000)

# Sort subscribers by registration date
subscribers = sorted(subscribers['items'], key=lambda x: x.get('date_register', 0))

# List for storing results
result = []

# Iterate through the list of subscribers
for subscriber in subscribers:
    # Get information about the user
    user_info = {
        'sex': subscriber.get('sex', ''),
        'city': subscriber.get('city', {}).get('title', ''),
        'relation': subscriber.get('relation', '')
    }
    # Add information about the user to the result list
    result.append(user_info)

# Write the result to a CSV file
with open('lentach_subscribers.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sex', 'city', 'relation'])
    writer.writeheader()
    writer.writerows(result)