
import requests
import time
import os
client_id = os.getenv("osu_client_id")
client_secret = os.getenv("osu_client_secret")
faceit_members_osu_ids = {
    "GaGex": 13485854,
    "ItsBerez": 16365355,
    "XxVeNoMXx171": 16546385,
    "HashiramaSenju": 16538964,
    "StiTumpy": 16265489,
    "menash": 18338537,
    "ilayalimlh": 17507515
}
class osuApiClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_expires_at = None
        self.access_token = None

    def get_access_token(self):
        endpoint = "https://osu.ppy.sh/oauth/token"
        url_params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(endpoint, data=url_params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            token_expiration = data["expires_in"]
            self.access_token = data["access_token"]
            self.token_expires_at = time.time() + token_expiration
        else:
            print("Failed obtaining key!")
    
    def is_token_valid(self):
        if self.access_token is None or time.time() >= self.token_expires_at:
            self.get_access_token()
        
    def get_faceit_beatmap_scores(self, beatmap_id):
        self.is_token_valid()

        url_params = {
            "mode": "osu!standart"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        all_members_beatmap_data = []

        for member, osu_id in faceit_members_osu_ids.items():
            url = f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}/scores/users/{osu_id}/all"
            response = requests.get(url=url, data=url_params, headers=headers)
            print(response.json())
            if response.status_code == 200:
                data = response.json()
                if len(data["scores"]) > 0: # check if the user even have a score on the map
                    user_best_score = data["scores"][0]
                    accuracy_organized = None
                    if str(user_best_score["accuracy"]) == "1":
                        accuracy_organized = "100"
                    else:
                        accuracy_string = str(user_best_score["accuracy"]).split('.')[1]
                        accuracy_organized = f"{accuracy_string[0:2]}.{accuracy_string[2:4]}"                        

                    user_mods = None
                    if len(user_best_score["mods"]) > 0:
                        user_mods = "".join(user_best_score["mods"])
                    else:
                        user_mods = "NM"

                    score_data = {
                        "username": member,
                        "user_id": user_best_score["user_id"],
                        "combo": user_best_score["max_combo"],
                        "accuracy": accuracy_organized,
                        "mods": user_mods,
                        "rank": user_best_score["rank"],
                        "pp": user_best_score["pp"],
                        "score": user_best_score["score"],
                        "date": user_best_score['created_at'].split('T')[0]
                    }
                    all_members_beatmap_data.append(score_data)
            else:
                raise Exception("Couldn't fetch user beatmap score")
        sorted_beatmap_data = [data for data in sorted(all_members_beatmap_data, key=lambda x: x["score"], reverse=True)]
        return sorted_beatmap_data
    
    def get_user_info(self, user_id):
        self.is_token_valid()

        url = f"https://osu.ppy.sh/api/v2/users/{user_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            user_data = {
                "avatar": data['avatar_url'],
            }
            return user_data
    
    def get_beatmap_info(self, beatmap_id):
        self.is_token_valid()

        url = f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data["beatmapset_id"])
            beatmap_info = {
                "title": data["beatmapset"]["title"],
                "version": data["version"],
                "image": data["beatmapset"]["covers"]["card@2x"]
            }
            return beatmap_info
        
    def get_faceit_users_info(self):
        self.is_token_valid()

        users_array = []
        for user, user_id in faceit_members_osu_ids.items():
            users_array.append(str(user_id))
        print(users_array)
        
        url = "https://osu.ppy.sh/api/v2/users"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        url_params = {
            "ids[]": users_array
        }
        users_response = requests.get(url=url, params=url_params, headers=headers)
        if users_response.status_code == 200:
            print(users_response.json())
            user_results = {}
            for user in users_response.json()["users"]:
                user_global_rank = user["statistics_rulesets"]["osu"]["global_rank"]
                print(user_global_rank)
                user_results.update({user["username"]: {"global_rank": user_global_rank}})
            print(user_results)


osucient = osuApiClient(client_id=client_id, client_secret=client_secret)

osucient.get_faceit_users_info()
        

        
        
        


