
import requests
import time
import os
client_id = os.getenv("osu_client_id")
client_secret = os.getenv("osu_client_secret")
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
        
    def get_user_beatmap_score(self, user_id, beatmap_id):
        self.is_token_valid()
        url = f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}/scores/users/{user_id}/all"
        url_params = {
            "mode": "osu!standart"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url=url, data=url_params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_best_score = data["scores"][0]
            accuracy_string = str(user_best_score["accuracy"]).split('.')[1]
            accuracy_organized = f"{accuracy_string[0:2]}.{accuracy_string[2:4]}%"
            score_data = {
                "combo": user_best_score["max_combo"],
                "accuracy": accuracy_organized,
                "mods": user_best_score["mods"],
                "pp": user_best_score["pp"],
            }
            return score_data
        else:
            raise Exception("Couldn't fetch user beatmap score")
    
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
                "username": data["username"],
                "avatar": data['avatar_url'],
            }
            return user_data
        

        
        
        


