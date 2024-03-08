import api
import sqlite3

########### PROFILE FUNCTIONS ###########
def viewSongList(conn, userID):
    '''View the list of favorite songs for the user'''
    cursor = conn.cursor()
    cursor.execute("SELECT songID FROM favorites WHERE userID=?", (userID,))
    songs = cursor.fetchall()
    cursor.close()
    
    if songs:
        print("Your Song List:")
        count = 1
        for song in songs:
            info = api.songInfo(song[0], False)
            print(f"{count}) Title: {info['title']} | Artist: {info['artist']} | SongID: {song[0]}")
            count += 1
    else:
        print("Your song list is empty.")

    return songs

def addToSongList(conn, userID, songID):
    '''Add a song to the user's list of favorites'''
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO favorites (userID, songID) VALUES (?, ?)", (userID, songID))
        conn.commit()
        print("Song added to your list!")
    except sqlite3.IntegrityError:
        print(f"This song is already in your list!")
    cursor.close()

def deleteFromSongList(conn, userID, songID):
    '''Delete a song from the user's list of favorites'''
    cursor = conn.cursor()
    # first check if song exists in the list
    cursor.execute("SELECT * FROM favorites WHERE userID=? AND songID=?", (userID, songID))
    if cursor.fetchone() is None:
        print("The song does not exist in your list.")
    else:
        cursor.execute("DELETE FROM favorites WHERE userID=? AND songID=?", (userID, songID))
        conn.commit()
        print("Song deleted from your list!")
    cursor.close()

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
            songs = viewSongList(conn, userID)
            print("Enter the number of the song you want the lyrics to, or x to go back!")
            while True:
                try:
                    userInput = input("> ")
                    if userInput == 'x':
                        break
                    elif (int(userInput) > 0) and (int(userInput) <= len(songs)):
                        api.songInfo(str(songs[int(userInput) - 1])[1:-2], True)
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