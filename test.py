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