import api
from database import createConnection

supabase_client = createConnection()
########### PROFILE FUNCTIONS ###########
def viewSongList(conn, userID):
    '''View the list of favorite songs for the user'''
    # Retrieve song IDs for the user from Supabase
    response = supabase_client.table('favorites').select('songid').eq('userid', userID).execute()
    songs = response.data

    if songs:
        print("Your Song List:")
        count = 1
        for song in songs:
            info = api.songInfo(song['songid'], False)
            print(f"{count}) Title: {info['title']} | Artist: {info['artist']} | SongID: {song['songid']}")
            count += 1
    else:
        print("Your song list is empty.")

    return songs


def addToSongList(conn, userID, songID):
    '''Add a song to the user's list of favorites'''
    # Insert the song into the 'favorites' table in Supabase
    response = supabase_client.table('favorites').insert({'userid': userID, 'songid': songID}).execute()
    if not response.data:
        print("Failed to add the song to your list!")
    else:
        print("Song added to your list!")
    # cursor = conn.cursor()
    # try:
    #     cursor.execute("INSERT INTO favorites (userID, songID) VALUES (?, ?)", (userID, songID))
    #     conn.commit()
    #     print("Song added to your list!")
    # except Exception as e:
    #     print(f"This song is already in your list!")
    # cursor.close()

def deleteFromSongList(conn, userID, songID):
    '''Delete a song from the user's list of favorites'''
    # Check if the song exists in the 'favorites' table in Supabase
    response = supabase_client.table('favorites').select('*').eq('userid', userID).eq('songid', songID).execute()
    if response.data:
        # Song exists in the list, delete it
        response = supabase_client.table('favorites').delete().eq('userid', userID).eq('songid', songID).execute()
        if not response.data:
            print("Failed to delete the song from your list!")
        else:
            print("Song deleted from your list!")
    else:
        print("The song does not exist in your list.")


def profileMenu(conn, username, userID):
    '''Handler for the menu of a user when they are logged into their profile'''
    print(f"\n<<<<<<<<<< {username}'s Songbook >>>>>>>>>>")
    choice = ""
    while choice != "x":
        # Profile Menu
        print('''1 - View Song List
2 - Add to Song List
3 - Delete from Song List
x - Log Out''')
        # Reset choice to empty string
        choice = ""
        
        while choice not in ['1', '2', '3', 'x']:
            choice = input("> ")
            if choice not in ['1', '2', '3', 'x']:
                print("Invalid choice. Please choose between 1 (View Songs), 2 (Add Song), 3 (Delete Song), or 4 (Log Out)")
        if choice == "1":
            try:
                songs = viewSongList(conn, userID)
            except Exception as e:
                print('There are no songs in your list')
            if songs:
                print("Enter the number of the song you want the lyrics to, or x to go back!")
                while True:
                    try:
                        userInput = input("> ")
                        if userInput == 'x':
                            break
                        elif (int(userInput) > 0) and (int(userInput) <= len(songs)):
                            api.songInfo(str(songs[int(userInput) - 1]['songid']), True)
                            break
                        else:
                            print('pick a valid integer')
                    except ValueError:
                        print('please enter an integer')
        elif choice == "2":
            print("Enter the title of the song you want to add: ")
            title = input("> ")
            api.searchSong(title, conn, userID)
        elif choice == "3":
            songID = input("Enter the ID of the song you want to delete\n(View your song list to get the ID of the song): ")
            deleteFromSongList(conn, userID, songID)
        else:
            print("Logging Out...\nReturning to Main Menu")