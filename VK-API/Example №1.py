import json  # Import the JSON library for working with JSON data
import vk_api  # Import the vk_api library for working with the VK API

vk_session = vk_api.VkApi(token='TOKEN')  # Create a VK API session with the provided access token
vk = vk_session.get_api()  # Create an instance of the VK API class for making API requests

cities = vk.database.getCities(country_id=1, q='Write a city here')  # Retrieve a list of cities in a specific country that match the given query string

result = {"cities": []}  # Initialize an empty dictionary that will eventually hold the results of the data retrieval

# Iterate through each city in the cities list and retrieve the list of universities and faculties in each city using the VK API
for city in cities['items']:
    city_id = city['id']
    city_name = city['title']

    universities = vk.database.getUniversities(city_id=city_id)
    university_list = []

    for university in universities['items']:
        university_id = university['id']
        university_name = university['title']

        faculties = vk.database.getFaculties(university_id=university_id)
        faculty_list = []

        for faculty in faculties['items']:
            faculty_name = faculty['title']
            faculty_list.append(faculty_name)
        university_info = {"id": university_id, "name": university_name, "faculties": faculty_list}
        university_list.append(university_info)

    city_info = {"id": city_id, "name": city_name, "universities": university_list}
    result["cities"].append(city_info)

# Save the result dictionary to a JSON file named "result_univer.json"
with open("result_univer.json", "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
