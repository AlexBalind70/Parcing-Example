# Import necessary modules
import vk_api
import json

# Connect to VK API using user access token
vk_session = vk_api.VkApi(token='TOKEN')
vk = vk_session.get_api()

# Get list of schools in a specific city (in this case, city_id=64 corresponds to Moscow)
schools = vk.database.getSchools(city_id=64)

# Initialize empty dictionary to store results
result = {"schools": []}

# Loop through each school in the list of schools
for school in schools['items']:
    school_id = school['id'] # Get school ID
    school_name = school['title'] # Get school name

    # Store school ID and name in a dictionary
    school_info = {"id": school_id, "name": school_name}

    # Add school dictionary to the 'schools' list in the 'result' dictionary
    result["schools"].append(school_info)

# Write result dictionary to a JSON file with proper encoding and indentation
with open("result_school.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
