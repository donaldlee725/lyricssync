import requests
import spotipy
import spotipy.util as util
import re
from hanziconv import HanziConv
from pykakasi import kakasi
import pinyin
from janome.tokenizer import Tokenizer

def initiate():
    token = util.prompt_for_user_token(
        username = "34nh76yhsh9bfy33gqljsjruu",
        scope = 'user-read-private user-read-playback-state user-modify-playback-state',
        client_id = "286d61bc23a54695955f977032a4b76b",
        client_secret = "89b7b779704b4fe2a0c2e1b39bb04f3d",
        redirect_uri = "http://localhost:8080"
        )   
    spotify = spotipy.Spotify(auth=token)
    return spotify

def song(spotify):
    return spotify.current_user_playing_track()

def songName(song):
    return song['item']['name']

def songArtist(song):
    return song['item']['artists'][0].get("name")

def songDuration(song):
    return (((song['item']['duration_ms']) / 1000) + 1)
    
def lyrics(songName, songArtist):
    url = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=json&callback=callback&q_artist=" + songArtist + "&q_track=" + songName
    apikey = "&apikey=87d7e8ae5e40d9f89ab69f760d9b2fb9"
    final_url = url + apikey
    response = requests.get(final_url).json()
    lyrics = response['message']['body']['lyrics']['lyrics_body']
    lyrics = lyrics[:-70]
    return lyrics

def finalPrint(lyrics):
    if re.search("[\u3040-\u30ff]", str(lyrics)):
        print(japExtension(lyrics))
    elif re.search("[\u4e00-\u9FFF]", str(lyrics)):
        print(chinesePinyin(lyrics))
    else:
        print(lyrics)

def japRomaji(lyrics):
    kks = kakasi()
    kks.setMode("H","a") 
    kks.setMode("K","a")
    kks.setMode("J","a") 
    kks.setMode("r","Hepburn") 
    kks.setMode("s", True) 
    conv1 = kks.getConverter()
    romaji = (conv1.do(lyrics))
    return romaji

def japExtension(lyrics):
    t = Tokenizer()
    token_reading = []
    token_part_of_speech = []
    line = ''
    for token in t.tokenize(lyrics):
        token_reading.append(token.reading)
        token_part_of_speech.append(token.part_of_speech[0:3])
    i = 0    
    while i < (len(token_part_of_speech)) - 1:
        if '助' in token_part_of_speech[i+1]:
            line += token_reading[i] + token_reading[i+1] + " "
            i+=2
        else:
            line += token_reading[i] + " "
            i+=1
    return japFormat(japRomaji(line))

def japFormat(lyrics):
    start = 0
    while lyrics.find("*") != -1:
        position = lyrics.find("*")
        text = lyrics[start:position].strip()
        print(text)
        lyrics = lyrics[(position + 1):]       
        
def chinesePinyin(lyrics):
    lyrics = HanziConv.toTraditional(lyrics)
    for lines in lyrics.splitlines():
        print(pinyin.get(lines))
        print(lines)
        
def run():
    spotify = initiate()
    song1 = song(spotify)
    name = songName(song1)
    artist = songArtist(song1)
    time = songDuration(song1)
    lyrics1 = finalPrint(lyrics(name, artist))
    finalPrint(lyrics1)
    return time
            
run()