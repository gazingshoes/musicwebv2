"""
Music Library Module
Contains classes for Song, Playlist, and MusicLibrary
Uses: Classes, Inheritance, Lists, Dictionaries, Tuples
"""

class MediaItem:
    """
    Base class for all media items (INHERITANCE concept)
    This is the parent class - demonstrates OOP inheritance
    """
    def __init__(self, title, duration):
        # Public attributes - accessible to everyone
        self.title = title  # Song/Playlist name
        self.duration = duration  # Length in seconds
        
    def get_info(self):
        """Return basic information about the media item"""
        return f"{self.title} - {self.duration}s"


class Song(MediaItem):
    """
    Song class - inherits from MediaItem (is-a relationship)
    Represents a single song with artist and genre
    Uses: Inheritance, Instance Variables
    """
    def __init__(self, title, artist, duration, genre):
        # Call parent class constructor using super()
        super().__init__(title, duration)
        self.artist = artist
        self.genre = genre
        self.__play_count = 0  # Private variable (double underscore)
        
    def play(self):
        """Simulate playing the song and increase play count"""
        self.__play_count += 1
        return f"🎵 Now playing: {self.title} by {self.artist}"
    
    def get_play_count(self):
        """Get the number of times this song has been played"""
        return self.__play_count
    
    def get_info(self):
        """
        Override parent method (POLYMORPHISM)
        Returns detailed song information
        """
        return f"{self.title} - {self.artist} ({self.genre}) [{self.duration}s]"
    
    def to_string(self):
        """
        Convert song to string format for file storage
        Uses: String manipulation, concatenation
        Returns: Tuple of song data
        """
        # Return as tuple - immutable data structure
        return (self.title, self.artist, str(self.duration), self.genre)


class Playlist(MediaItem):
    """
    Playlist class - inherits from MediaItem
    Contains a collection of songs
    Uses: Inheritance, Lists, Loops
    """
    def __init__(self, name):
        super().__init__(name, 0)
        self.songs = []  # List to store Song objects - MUTABLE
        
    def add_song(self, song):
        """
        Add a song to the playlist
        Uses: List method append()
        """
        self.songs.append(song)
        # Update total duration
        self.duration += song.duration
        return f"✅ Added '{song.title}' to playlist '{self.title}'"
    
    def remove_song(self, song_title):
        """
        Remove a song from playlist by title
        Uses: List iteration, list method remove()
        """
        for song in self.songs:
            if song.title.lower() == song_title.lower():
                self.songs.remove(song)
                self.duration -= song.duration
                return f"❌ Removed '{song_title}' from playlist"
        return f"⚠️ Song '{song_title}' not found in playlist"
    
    def get_songs(self):
        """Return list of all songs in playlist"""
        return self.songs
    
    def get_info(self):
        """
        Override parent method
        Returns playlist information
        """
        song_count = len(self.songs)  # Using len() function
        return f"📁 {self.title} - {song_count} songs, {self.duration}s total"
    
    def show_all_songs(self):
        """
        Display all songs in the playlist
        Uses: For loop, enumerate function
        """
        if len(self.songs) == 0:
            return "This playlist is empty!"
        
        result = f"\n{'='*50}\n"
        result += f"Playlist: {self.title}\n"
        result += f"{'='*50}\n"
        
        # Using enumerate to get index and item - LOOP
        for index, song in enumerate(self.songs, start=1):
            result += f"{index}. {song.get_info()}\n"
        
        return result


class MusicLibrary:
    """
    Main library class to manage all songs and playlists
    Uses: Dictionaries, Lists, Sets, File Handling
    """
    def __init__(self):
        # Dictionary to store all songs: {title: Song object}
        self.all_songs = {}
        
        # List to store all playlists
        self.playlists = []
        
        # Set to store unique genres (no duplicates!)
        self.genres = set()
        
    def add_song(self, title, artist, duration, genre):
        """
        Add a new song to the library
        Uses: Dictionary operations, Set operations
        """
        # Check if song already exists (dictionary key check)
        if title in self.all_songs:
            return f"⚠️ Song '{title}' already exists in library!"
        
        # Create new Song object
        new_song = Song(title, artist, duration, genre)
        
        # Add to dictionary - KEY:VALUE pair
        self.all_songs[title] = new_song
        
        # Add genre to set (duplicates automatically removed)
        self.genres.add(genre)
        
        return f"✅ Added song: {new_song.get_info()}"
    
    def get_song(self, title):
        """
        Retrieve a song by title
        Uses: Dictionary get() method
        """
        # Using .get() instead of [] to avoid KeyError
        return self.all_songs.get(title, None)
    
    def search_by_artist(self, artist):
        """
        Search for all songs by an artist
        Uses: List comprehension, String methods
        """
        # List comprehension - compact way to create lists
        results = [song for song in self.all_songs.values() 
                   if song.artist.lower() == artist.lower()]
        return results
    
    def search_by_genre(self, genre):
        """
        Search for all songs in a genre
        Uses: List comprehension
        """
        results = [song for song in self.all_songs.values() 
                   if song.genre.lower() == genre.lower()]
        return results
    
    def create_playlist(self, name):
        """
        Create a new playlist
        Uses: List append, Object creation
        """
        new_playlist = Playlist(name)
        self.playlists.append(new_playlist)
        return f"✅ Created playlist: {name}"
    
    def get_playlist(self, name):
        """
        Find a playlist by name
        Uses: For loop, String comparison
        """
        for playlist in self.playlists:
            if playlist.title.lower() == name.lower():
                return playlist
        return None
    
    def show_all_songs(self):
        """
        Display all songs in library
        Uses: Dictionary iteration, sorted() function
        """
        if len(self.all_songs) == 0:
            return "🎵 Library is empty! Add some songs first."
        
        result = f"\n{'='*60}\n"
        result += "ALL SONGS IN LIBRARY\n"
        result += f"{'='*60}\n"
        
        # Sort songs alphabetically by title
        sorted_titles = sorted(self.all_songs.keys())
        
        for index, title in enumerate(sorted_titles, start=1):
            song = self.all_songs[title]
            result += f"{index}. {song.get_info()} [Played: {song.get_play_count()}x]\n"
        
        return result
    
    def show_all_playlists(self):
        """
        Display all playlists
        Uses: List iteration
        """
        if len(self.playlists) == 0:
            return "📁 No playlists yet! Create one first."
        
        result = f"\n{'='*50}\n"
        result += "ALL PLAYLISTS\n"
        result += f"{'='*50}\n"
        
        for index, playlist in enumerate(self.playlists, start=1):
            result += f"{index}. {playlist.get_info()}\n"
        
        return result
    
    def get_all_genres(self):
        """
        Get all unique genres
        Uses: Set operations
        Returns: Sorted list of genres
        """
        return sorted(list(self.genres))