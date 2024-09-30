import time
from pypresence import Presence
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify credentials
SPOTIPY_CLIENT_ID = '668d3e6297fc4851b980970ff14cbeca'
SPOTIPY_CLIENT_SECRET = '2bf141d571db4970808dae7cd9624ec2'
SPOTIPY_REDIRECT_URI = 'https://discord.gg/KqvMuS6U'

# Set up Discord Rich Presence
DISCORD_CLIENT_ID = '1290361282226028555'
RPC = Presence(DISCORD_CLIENT_ID)
print("Connecting to Discord...")
RPC.connect()
print("Connected to Discord")

# Set up Spotify OAuth
scope = "user-read-currently-playing"
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope)

# Get the token
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(f"Please navigate to the following URL to authorize the application: {auth_url}")
    response = input("Enter the URL you were redirected to: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

sp = spotipy.Spotify(auth=token_info['access_token'])
print("Connected to Spotify")

def update_presence():
    try:
        current_track = sp.current_user_playing_track()
        if current_track is None:
            print("No track currently playing")
            RPC.clear()
        else:
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']
            album_cover = current_track['item']['album']['images'][0]['url']
            current_position = current_track['progress_ms']  # current position in milliseconds
            track_duration = current_track['item']['duration_ms']  # total duration in milliseconds

            print(f"Updating presence: {track_name} by {artist_name}")

            # Update Discord Rich Presence
            RPC.update(
                state=f"by {artist_name}",
                details=f"Listening to {track_name}",
                large_image=album_cover,
                large_text="Listening to Akrify",
                start=int(time.time()) - (current_position // 1000),  # Start time for the slider
                end=int(time.time()) + ((track_duration - current_position) // 1000)  # End time
            )
    except Exception as e:
        print(f"Error: {e}")
        RPC.clear()

if __name__ == "__main__":
    while True:
        update_presence()
        time.sleep(1)  # Update every second
