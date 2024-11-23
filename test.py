import time
import os
import dotenv
import requests

# _client_id = os.getenv("osu_client_id")
# print(_client_id)


# # Define the endpoint and the parameters
# url = 'https://osu.ppy.sh/oauth/token'
# data = {
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'grant_type': 'client_credentials',
#     'scope': 'public'
# }

# # Make the POST request with the correct headers and body data
# response = requests.post(url, headers={'Accept': 'application/json'}, data=data)

# # Print the response
# print(response.text)

acc = 0.9773844641101278
acc_str = str(acc)

print(acc_str.split(".")[1])

list_of_dicts = [
    {
        "score": 200
    },
    {
        "score": 436324
    },
    {
        "score": 2003
    }
]

faceit_members_osu_ids = {
    "gal": 13485854,
    "berez": 16365355,
    "dvir": 16546385,
    "yarin": 16538964,
    "avraham": 16265489,
    "menash": 18338537
}

for mebmer, key in faceit_members_osu_ids.items():
    print(mebmer, key)