import requests
import json
from auth import refresh_token, base_64, user_id

class SpotifyAssistance:
    def __init__(self):
        self.uris = ""
        self.playlist_id = ""
        self.refresh_token = refresh_token
        self.base_64 = base_64
        self.user_id = user_id
        
    #Gives user the option to create new playlist
    def createPlaylist(self):
        name = input("Write the playlist name: ")
        description = input("Write the playlist description: ")
        endpoint_url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        request_body = json.dumps({
                "name": name,
                "description": description,
                "public": True
                })

        head = {
            "Content-Type":"application/json", 
            "Authorization":f"Bearer {self.refreshToken()}"
        }
        #this post request will create a playlist if all criteria is correct 
        response = requests.post(url = endpoint_url, data = request_body, headers=head)
        print("Playlist created")

    #Function to search for track using the track name/title and artist name
    def searchTrack(self):
        track_name = input("Enter the track name: ")
        artist_name = input("Enter the artist name: ")
     
        #Correctly formating track name/title and store the string in q
        seperator = "%2B"
        q = track_name.split(' ')
        q = (seperator.join(q)+'&')
        typee = "track"

        head = {
            "Content-Type":"application/json",
            "Authorization":f"Bearer {self.refreshToken()}"
        }

        response = requests.get(url=f"https://api.spotify.com/v1/search?q={q}type={typee}", headers=head)
        response_json = response.json()
        #iterate over response_json(json format) and get the corresponding uri for the track
        #change the artist name to lower case
        for i in response_json['tracks']['items']:
            name = i["artists"][0]["name"]
            if name.lower() == artist_name.lower():
                self.uris = i ['uri']
        #print(self.uris)

    #Search for the playlist name/title 
    def getPlaylistInfo(self):
        playlist_title = input("Enter the playlist title: ")
        endpoint_url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        head = {
            "Content-Type":"application/json",
            "Authorization":f"Bearer {self.refreshToken()}"
        }
        response = requests.get(url = endpoint_url,headers=head)
        response_json = response.json()
        #iterate over response_json(json format) and get the playlist id
        for i in response_json["items"]:
            if i["name"] == playlist_title:
                self.playlist_id = i["id"]
                print(self.playlist_id)
            else:
                print("invalid playlist")
                break          
    #Inserts track into the playlist
    def addTracks(self):
        endpoint_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?uris={self.uris}"
        head = {
            "Content-Type":"application/json", 
            "Authorization":f"Bearer {self.refreshToken()}"
        }
        response = requests.post(url = endpoint_url,headers=head)
        
    #This function will return the access token
    def refreshToken(self):
        query = "https://accounts.spotify.com/api/token"
        d = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        head = {"Authorization": "Basic "+ self.base_64}
        
        response = requests.post(query,data=d,headers=head)
        response_json = response.json()
        return response_json["access_token"]
        
    def allOptions(self):
        menu = "1. Create a playlist\n2. Add songs to playlist\n3. Exit"
        print(menu)
        user_input = input("Select(1-3): ")
        
        while (user_input != "3"):
            if user_input == "1":
                print("1")
                self.createPlaylist()
                print(menu)
                user_input = input("Select(1-3): ")

            elif user_input == "2":
                print("2")
                self.getPlaylistInfo()
                self.searchTrack()
                self.addTracks()
                print(menu)
                user_input = input("Select(1-3): ")

            elif user_input == "3":
                print("3")
                break

            else:
                print("error")
                break
   

SA = SpotifyAssistance()
SA.allOptions()
