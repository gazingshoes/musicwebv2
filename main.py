"""
main program file | untuk menjalankan program run file ini ya
"""

import pygame
from music_library import MusicLibrary
from player import (load_songs_from_file, save_songs_to_file)
from audio_player import AudioPlayer
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- HELPER: DURATION PARSER ---
def parse_duration(duration_str):
    """
    ini untuk mengubah tampilan durasi dari detik (s) ke format menit dan detik (m:ss)
    """
    if ":" in duration_str:
        parts = duration_str.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid format. Use M:SS.")
        minutes = int(parts[0])
        seconds = int(parts[1])
        if minutes < 0 or seconds < 0 or seconds > 59:
             raise ValueError("Invalid time value.")
        return (minutes * 60) + seconds
    else:
        return int(duration_str)

# --- HELPER: SONG SELECTOR ---
def select_song_from_list(library, prompt="Choose a song:"):
    """
    tampilan daftar lagu dengan nomor untuk dipilih user
    """
    song_list = library.get_sorted_song_list()
    if not song_list:
        print("❌ No songs in library to choose from.")
        time.sleep(2)
        return None
    clear_screen()
    print(f"--- {prompt} ---")
    for i, song in enumerate(song_list, 1):
        print(f"{i}. {song.get_info()}")
    print("\n0. Cancel")
    print("="*30)
    choice = input("Enter number: ").strip()
    try:
        choice_num = int(choice)
        if choice_num == 0:
            return None
        if 1 <= choice_num <= len(song_list):
            return song_list[choice_num - 1] # Return the actual Song object
        else:
            print("❌ Invalid number.")
            time.sleep(1.5)
            return None
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        time.sleep(1.5)
        return None

# ===================================================================
# --- SUB-MENU 1: PLAYER MENU ---
# ===================================================================
def show_player_menu(library, player):
    """sub menu player"""
    while True:
        clear_screen()
        # Auto-play next song if one just finished
        player.play_next_from_queue() 
        
        print("\n--- ▶️ Player Menu ---")
        print(player.get_queue_display()) # Show the queue at the top
        print("="*30)
        print("1. Play Next Song in Queue")
        print("2. Add Song to Queue")
        print("3. Play Song Immediately (Clears Queue)")
        print("4. Stop Music (Clears Queue)")
        print("5. Back to Main Menu")
        print("="*30)
        
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            # --- Play Next ---
            clear_screen()
            player.play_next_from_queue()
            input("\nPress Enter to return...")
            
        elif choice == '2':
            # --- Add to Queue ---
            song = select_song_from_list(library, "Select a Song to Add to Queue")
            if song:
                player.add_to_queue(song)
            else:
                print("Action cancelled.")
            input("\nPress Enter to return...")

        elif choice == '3':
            # --- Play Song Now ---
            song = select_song_from_list(library, "Select a Song to Play Now")
            if song:
                player.play_now(song)
            else:
                print("Action cancelled.")
            input("\nPress Enter to return...")
            
        # --- THIS IS THE FIX (was '4.') ---
        elif choice == '4':
            # --- Stop Music ---
            player.stop()
            input("\nPress Enter to return...")

        elif choice == '5':
            # --- Back ---
            break
        else:
            print("❌ Invalid choice. Please select from 1-5.")
            time.sleep(1.5)

# ===================================================================
# --- SUB-MENU 2: LIBRARY MENU ---
# ===================================================================
def show_library_menu(library):
    """Handles all logic for the Library sub-menu."""
    while True:
        clear_screen()
        print("\n--- 📚 Library Menu ---")
        print("1. View All Songs")
        print("2. Add New Song")
        print("3. Edit a Song")
        print("4. Delete a Song")
        print("5. Search Songs")
        print("6. Back to Main Menu")
        print("="*30)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            show_all_songs(library)
        elif choice == '2':
            add_new_song(library)
        elif choice == '3':
            edit_song(library)
        elif choice == '4':
            delete_song(library)
        elif choice == '5':
            search_songs(library)
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice. Please select from 1-6.")
            time.sleep(1.5)

# --- (Library Functions: These are now called by show_library_menu) ---

def show_all_songs(library):
    clear_screen()
    print("--- 📚 All Songs in Library ---")
    print(library.show_all_songs())
    input("\nPress Enter to return...")

def add_new_song(library):
    clear_screen()
    print("--- ➕ Add New Song ---")
    title = input("Enter Title: ").strip()
    artist = input("Enter Artist: ").strip()
    
    duration_str = input("Enter Duration (e.g., 4:32 or 272): ").strip()
    try:
        duration_sec = parse_duration(duration_str)
        if duration_sec <= 0:
            print("\n❌ Duration must be a positive number.")
            time.sleep(2)
            return
    except ValueError:
        print("\n❌ Invalid duration format. Use M:SS or total seconds.")
        time.sleep(2)
        return

    genre = input("Enter Genre: ").strip()
    filepath = input("Enter full File Path (e.g., /Users/me/music/song.mp3): ").strip()

    if not title or not artist or not genre or not filepath:
        print("\n❌ All fields are required.")
        time.sleep(2)
        return

    result = library.add_song(title, artist, duration_sec, genre, filepath)
    print(f"\n{result}")
    input("\nPress Enter to return...")

def edit_song(library):
    song = select_song_from_list(library, "Select a Song to Edit")
    if not song:
        print("Action cancelled.")
        input("\nPress Enter to return...")
        return
    
    clear_screen()
    print(f"--- Editing Song: {song.title} ---")
    print(f"1. Title:   {song.title}")
    print(f"2. Artist:  {song.artist}")
    print(f"3. Duration: {_format_duration(song.duration)}") 
    print(f"4. Genre:   {song.genre}")
    print(f"5. Filepath: {song.filepath}")
    print("6. Cancel")
    print("="*30)
    
    choice = input("Which field do you want to edit (1-6)?: ").strip()
    field_map = {"1": "title", "2": "artist", "3": "duration", "4": "genre", "5": "filepath"}
    
    if choice in field_map:
        field = field_map[choice]
        if field == "duration":
            new_value_str = input(f"Enter new value for {field} (e.g., 4:32): ").strip()
            if not new_value_str:
                print("❌ Value cannot be empty.")
            else:
                try:
                    new_value_sec = parse_duration(new_value_str)
                    result = library.edit_song(song, field, new_value_sec)
                    print(f"\n{result}")
                except ValueError:
                    print("\n❌ Invalid duration format.")
        else:
            new_value = input(f"Enter new value for {field}: ").strip()
            if not new_value:
                print("❌ Value cannot be empty.")
            else:
                result = library.edit_song(song, field, new_value)
                print(f"\n{result}")
    elif choice == "6":
        print("Edit cancelled.")
    else:
        print("❌ Invalid choice.")
    input("\nPress Enter to return...")

def delete_song(library):
    song = select_song_from_list(library, "Select a Song to Delete")
    if not song:
        print("Action cancelled.")
        input("\nPress Enter to return...")
        return
    confirm = input(f"Are you sure you want to delete '{song.title}'? (y/n): ").strip().lower()
    if confirm == 'y':
        result = library.delete_song(song.title)
        print(f"\n{result}")
    else:
        print("Delete cancelled.")
    input("\nPress Enter to return...")

def search_songs(library):
    clear_screen()
    print("--- 🔍 Search Songs ---")
    print("1. Search by Artist")
    print("2. Search by Genre")
    print("3. Back")
    choice = input("Enter your choice (1-3): ").strip()
    if choice == '3':
        return
    term = input("Enter search term: ").strip()
    if not term:
        print("❌ Search term cannot be empty.")
        time.sleep(2)
        return
    results = []
    search_type = ""
    if choice == '1':
        results = library.search_by_artist(term)
        search_type = "Artist"
    elif choice == '2':
        results = library.search_by_genre(term)
        search_type = "Genre"
    else:
        print("❌ Invalid choice.")
        time.sleep(2)
        return
    print(f"\n--- Found {len(results)} song(s) for {search_type}: '{term}' ---")
    if not results:
        print("No songs found.")
    else:
        for i, song in enumerate(results, 1):
            print(f"{i}. {song.get_info()}")
    input("\nPress Enter to return...")

# ===================================================================
# --- MAIN APPLICATION LOOP ---
# ===================================================================
def main():
    """fungsi utama yang akan di run untuk menjalankan program nya"""
    pygame.init()
    library = MusicLibrary()
    player = AudioPlayer()
    
    print(load_songs_from_file(library))
    
    print("\nWelcome to Musicify!")
    input("Press Enter to start...")

    while True:
        clear_screen()
        # Auto-play next song
        player.play_next_from_queue()
        
        print("\n" + "="*30)
        print("     🎵 Musicify 🎵")
        print("="*30)
        print("1. ▶️ Player")
        print("2. 📚 Library")
        print("3. 💾 Save and Exit")
        print("="*30)
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            show_player_menu(library, player)
        elif choice == '2':
            show_library_menu(library)
        elif choice == '3':
            print(save_songs_to_file(library))
            print("\n✅ Data saved. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select from 1-3.")
            time.sleep(1.5)

    pygame.quit()

if __name__ == "__main__":
    main()