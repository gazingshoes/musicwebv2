"""
Main Program File - GUI Version
Run this file to start the music player with GUI!
Uses: All concepts combined - Classes, Functions, File Handling, GUI
"""

# Import necessary modules
from music_library import MusicLibrary
from gui_player import MusicPlayerGUI, save_on_close
from player import load_songs_from_file, load_playlists_from_file


def main():
    """
    Main function - entry point of the program
    Uses: Classes, Functions, GUI
    """
    print("🎵 Starting Python Music Player GUI...")
    
    # Create main library object
    library = MusicLibrary()
    
    # Load existing data from files
    print(load_songs_from_file(library))
    print(load_playlists_from_file(library))
    
    # Create and run GUI
    app = MusicPlayerGUI(library)
    
    # Set up close event to save data
    app.window.protocol("WM_DELETE_WINDOW", 
                        lambda: save_on_close(library, app.window))
    
    # Start the GUI
    app.run()


# Entry point - program starts here
if __name__ == "__main__":
    main()