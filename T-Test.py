import spotipy
import spotipy.util as util
import csv
from statsmodels.stats.weightstats import ttest_ind

# Gather audio features of playlists from Spotify that represent certain contextual conditions
# Directly carry out t-test for each possible pair of conditions within a dimension
CLIENT_ID = ""
CLIENT_SECRET = ""
USER = ""
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "speechiness", "tempo", "valence"]

### Activities playlists ###
# 546 songs: Running Music 2019 Cardio Music & Workout Music, Running Hits, Running Workout Goals, Run Wild, Running Songs, Cardio Gym Workout Motivation
running_pl = ["0VSg3Ize1XJArEzV6fCVW5", "7gO9WmJaPmIviOlvK1m95P", "7wBpRbIoatquCDVcxybHEk", "37i9dQZF1DX35oM5SPECmN",
              "00KoqT6MZlEeYJG0FRYwr1",
              "7C2PBX7oHqN7n34XZMpfmX"]
# 535 songs: Relax & Unwind, Relaxing Songs, Ambient Relaxation, Relaxed Driving Music, Hanging Out and Relaxing
relaxing_pl = ["37i9dQZF1DWU0ScTcjJBdj", "4D3hxAbOjVu5jaC5Bnlmky", "37i9dQZF1DX3Ogo9pFvBkY", "37i9dQZF1DXci7j0DJQgGp"]
# 502 songs: Walking Back to Happiness, Walking, Walking Music, A Walk Alone, Night Walk
walking_pl = ["37i9dQZF1DWWqNJmH2i89D", "1zwJ7hZo8P7un57dfUpjpA", "3yiX3ROHK4vo82pR6BO8eW", "37i9dQZF1DWZLcGGC0HJbc",
              "37i9dQZF1DXbOIXGhM8qKA"]
# 614 songs: Sleeping Music, Songs For Sleeping, A Different Sleeping List, Strings for Sleeping, Slow Pop// Sleeping, Sleeping Songs
sleeping_pl = ["5iL9NYIEfckRxTJEJ93p2T", "37i9dQZF1DWStLt4f1zJ6I", "37i9dQZF1DX7heGeZ10YDi", "37i9dQZF1DWXIrropGBmnR",
               "1tz2zye8AhEfzyDy9Ah9sq",
               "1jRY1aM9WgrndDPyO7AGeO"]
# 559 songs: Deep Focus, Just Focus, Focus Flow, Focus Now
focus_pl = ["37i9dQZF1DWZeKCadgRdKQ", "37i9dQZF1DWYRcvdDwEl3O", "37i9dQZF1DWZZbwlv3Vmtr", "37i9dQZF1DWZIOAPKUdaKS"]

### Mood playlists ###
# 511 songs: Happy Hits!, Wake Up Happy, Happy Beats, Happy Tunes, Happy Monday
happy_pl = ["37i9dQZF1DXdPec7aLTmlC", "37i9dQZF1DX0UrRvztWcAU", "37i9dQZF1DWSf2RDTDayIx", "37i9dQZF1DX9u7XXOp0l5L",
            "0td1u8hQfP9GTmbRRbvQTz"]
# 513 songs: Sad Songs, Sad Beats, Sad Covers, Sad Songs, Sad Songs for Crying yourself to Sleep
sad_pl = ["37i9dQZF1DX7qK8ma5wgG1", "37i9dQZF1DWVrtsSlLKzro", "37i9dQZF1DX64Y3du11rR1", "54ozEbxQMa0OeozoSoRvcL",
          "7ABD15iASBIpPP5uJ5awvq"]

### Time of Day playlists ###
# 569 songs: Morning Stroll, Morning Commute, Morning Tea, Morning Acoustic, Morning Motivation, Morning Rhythm, Wake Up Gently
morning_pl = ["37i9dQZF1DWWLToO3EeTtX", "37i9dQZF1DX2MyUCsl25eb", "37i9dQZF1DX5dJCW6dyCUe", "37i9dQZF1DXdd3gw5QVjt9",
              "37i9dQZF1DXc5e2bJhV6pu",
              "37i9dQZF1DX3ohNxI5tB79", "37i9dQZF1DX7cZxYLqLUJl"]
# 538 songs: Afternoon Accoustic, Afternoon Train Ride, Sunny Afternoon, Afternoon Chill Sessions, Chilled Afternoon, Chill Afternoons, Good Afternoon Music
afternoon_pl = ["37i9dQZF1DX4E3UdUs7fUx", "37i9dQZF1DX8MbMfAHb8U0", "7biW5BR2AsbEsPJnndirjV", "18fiFDqqP8seBZ76hD9A6J",
                "37i9dQZF1DX5qwHeIGQ14o",
                "2YplQyTHA3mujnidu1gCRI", "4MGjsC9FFb2SlwoNuSdI9d"]
# 548 songs: Evening Commute, Evening Chill, Evening Tap, Cosy evening, Evening Accoustic, Evening Indie, Chill Evening Vibes
evening_pl = ["37i9dQZF1DX3bSdu6sAEDF", "37i9dQZF1DWZ0OzPeadl0h", "37i9dQZF1DXbPWdR4IOz73", "2smkSmOoD3p6iD9pSJQtzd",
              "37i9dQZF1DXcWBRiUaG3o5",
              "37i9dQZF1DWUu64dvFdPQk", "0Za0sdSeIwq7VBwIPc99Mn"]
# 587 songs: Night Rider, Late Night Vibes, Night Pop, Peaceful Summer Nights
night_pl = ["37i9dQZF1DX6GJXiuZRisr", "37i9dQZF1DXdQvOLqzNHSW", "37i9dQZF1DXbcP8BbYEQaO", "37i9dQZF1DWTjLfR5thd2p"]

all_feat = {"acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "key": [], "liveness": [],
            "loudness": [], "speechiness": [], "tempo": [], "valence": []}

all_feat_2 = {"acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "key": [], "liveness": [],
            "loudness": [], "speechiness": [], "tempo": [], "valence": []}

pl = happy_pl
pl_name = "happy"
pl_2 = sad_pl
pl_name_2 = "sad"

# Spotify authentication
token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)


# All functions
def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


def save_all_features(audio_features):
    for song in audio_features:
        for feat in AUDIO_FEATURES:
            all_feat[feat].append(song[feat])


def save_all_features_2(audio_features):
    for song in audio_features:
        for feat in AUDIO_FEATURES:
            all_feat_2[feat].append(song[feat])


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def avg(lst):
    return sum(lst) / len(lst)


def get_all_songs(pl):
    items_returned = 100
    cntr = 0
    all_tracks = []
    while (items_returned == 100):
        songs = spotify.user_playlist_tracks(USER, pl, limit=100, offset=cntr)
        items_returned = len(songs["items"])
        cntr += items_returned
        for item in songs["items"]:
            # print(json.dumps(item, sort_keys=True, indent=4, separators=(',', ': ')))
            all_tracks.append(item["track"]["id"])
    all_tracks = list(dict.fromkeys(all_tracks))
    return all_tracks


def count_tracks(playlists):
    all_tracks = []
    for playlist in playlists:
        all_tracks.extend(get_all_songs(playlist))
    print(f'Amount of tracks: {len(all_tracks)}')
    return list(set(all_tracks))


def calculate_averages(amount_of_tracks):
    feat_avg = {}
    feat_avg["tracks_amount"] = amount_of_tracks
    for key in all_feat:
        feat_average = avg(all_feat[key])
        feat_avg[key] = feat_average
    feat_avg["loudness"] = (feat_avg["loudness"] + 40) / 40
    feat_avg["tempo"] = feat_avg["tempo"] / 220
    with open(f'audio_features/audio_features_{pl_name}.csv', 'w') as f:
        w = csv.DictWriter(f, feat_avg.keys())
        w.writeheader()
        w.writerow(feat_avg)


def calculate_t_p_values():
    res = []
    for feat in AUDIO_FEATURES:
        set_1 = all_feat[feat]
        set_2 = all_feat_2[feat]
        ttest = ttest_ind(set_1, set_2)
        print(f'{feat} t-test')
        print(ttest)
        print('\n')
        res.append({"audio_feature":feat, "t":ttest[0], "p":ttest[1], "degrees_of_freedom":ttest[2]})

    with open(f'ttest/{pl_name}-{pl_name_2}.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=["audio_feature", "t", "p", "degrees_of_freedom"])
        w.writeheader()
        for item in res:
            w.writerow(item)


# Splitting of tracks to smaller parts (Spotify API limit of 50)
all_tracks = count_tracks(pl)
tracks_chunks = list(chunks(all_tracks, 50))
all_tracks_2 = count_tracks(pl_2)
tracks_chunks_2 = list(chunks(all_tracks_2, 50))

# Extracting all the features for all the chunks
for chunk_of_tracks in tracks_chunks:
    save_all_features(spotify.audio_features(chunk_of_tracks))
for chunk_of_tracks in tracks_chunks_2:
    save_all_features_2(spotify.audio_features(chunk_of_tracks))

calculate_t_p_values()