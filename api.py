import requests
from lyricsgenius import Genius
import account

# For accessing the Genius API holding song data
GENIUS_ACCESS_TOKEN = 'g2kgPBmdVl-4wB1haAiY5gCLH4XVlWtdHD5DzEDLJRm6una3AGtyrXGXkx-RQ3C_'
genius = Genius(GENIUS_ACCESS_TOKEN)
genius.verbose = False
genius.remove_section_headers

########## API INTERACTION FUNCTIONS ##########
def searchSong(songTitle, conn, userID):
    """This function takes a title, retrieves from the api infomration including id, title, artist and url. It
    saves this info in an array, and the passes the array to the savesong function"""
    base_url = 'https://api.genius.com'
    search_url = f'{base_url}/search'
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': songTitle}

    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()
    hits = data['response']['hits']

    if not hits:
        print(f"No songs found with the title '{songTitle}'.")
        # add some way to go back to previous menu here
    songArray = []
    for hit in hits:
        songInfo = {
            'id': hit['result']['id'],
            'title': hit['result']['title'],
            'artist': hit['result']['primary_artist']['name'],
            'url': hit['result']['url']
        }
        songArray.append(songInfo)

    saveSong(songArray, conn, userID)


def saveSong(songArray, conn, userID):
    """this function takes the array and checks how many songs are in the array, if just one, it adds to the database
    if several, prompts the user for a selection and validates the input"""
    if len(songArray) == 1:
        # add to database using id
        account.addToSongList(conn, userID, str(songArray[0]['id']))
        # print(songArray[0]['id'])  # test to see if correct selection, can remove
        print("One song Added")
    else:
        print("Select a Song")
        i = 1
        for song in songArray:
            print(f"    {i} - {song['title']} by {song['artist']}")
            i = i + 1
        print("    x - exit")
        while True:
            try:
                userInput = input("> ")
                if userInput == 'x':
                    break
                elif (int(userInput) > 0) and (int(userInput) <= len(songArray)):
                    print('song added')
                    # add to database songArray[userInput - 1]['id']
                    print(f'SONGARRAY: {str(songArray[int(userInput) - 1]['id'])}')
                    account.addToSongList(conn, userID, str(songArray[int(userInput) - 1]['id']))
                    # print(songArray[userInput - 1]['id'])  # test to see if correct selection, can remove
                    break
                else:
                    print('pick a valid integer')
            except ValueError:
                print('please enter an integer')


def songInfo(songID, printLyrics):
    """Takes a given songid, requests and returns from the api details about the song"""
    base_url = 'https://api.genius.com'
    song_url = f'{base_url}/songs/{songID}'
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}

    response = requests.get(song_url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        print(f"Error fetching data for song with ID {songID}.")
        return None

    song = {
        'title': data['response']['song']['title'],
        'artist': data['response']['song']['primary_artist']['name'],
        'id': data['response']['song']['id']
    }

    if printLyrics:
        gSong = genius.search_song(song['title'], song['artist'])
        print(gSong.lyrics)

    return song
