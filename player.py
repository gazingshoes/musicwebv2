"""
Player Module
Handles file operations
Uses: Functions, File Handling, Exception Handling
"""

def save_songs_to_file(library, filename="songs.txt"):
    """
    Save all songs to a text file
    Uses: File handling (write mode), Exception handling, Loops
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("TITLE|ARTIST|DURATION|GENRE\n")
            
            for song in library.all_songs.values():
                song_data = song.to_string()
                line = "|".join(song_data)
                file.write(line + "\n")
        
        return f"✅ Saved {len(library.all_songs)} songs to {filename}"
    
    except IOError as e:
        return f"❌ Error saving file: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


def load_songs_from_file(library, filename="songs.txt"):
    """
    Load songs from a text file
    Uses: File handling (read mode), Exception handling
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            count = 0
            for line in lines[1:]:
                parts = line.strip().split('|')
                
                if len(parts) == 4:
                    title, artist, duration, genre = parts
                    library.add_song(title, artist, int(duration), genre)
                    count += 1
        
        return f"✅ Loaded {count} songs from {filename}"
    
    except FileNotFoundError:
        return f"⚠️ File '{filename}' not found. Starting with empty library."
    except ValueError as e:
        return f"❌ Error reading file data: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


def save_playlists_to_file(library, filename="playlists.txt"):
    """
    Save all playlists to a text file
    Uses: File handling, Nested loops
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for playlist in library.playlists:
                file.write(f"PLAYLIST:{playlist.title}\n")
                
                for song in playlist.get_songs():
                    file.write(f"  {song.title}\n")
                
                file.write("END_PLAYLIST\n")
        
        return f"✅ Saved {len(library.playlists)} playlists to {filename}"
    
    except Exception as e:
        return f"❌ Error saving playlists: {e}"


def load_playlists_from_file(library, filename="playlists.txt"):
    """
    Load playlists from a text file
    Uses: File handling, String methods, Conditionals
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            current_playlist = None
            count = 0
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("PLAYLIST:"):
                    playlist_name = line.replace("PLAYLIST:", "")
                    library.create_playlist(playlist_name)
                    current_playlist = library.get_playlist(playlist_name)
                    count += 1
                
                elif line == "END_PLAYLIST":
                    current_playlist = None
                
                elif current_playlist and line:
                    song = library.get_song(line)
                    if song:
                        current_playlist.add_song(song)
        
        return f"✅ Loaded {count} playlists from {filename}"
    
    except FileNotFoundError:
        return f"⚠️ File '{filename}' not found. No playlists loaded."
    except Exception as e:
        return f"❌ Error loading playlists: {e}"