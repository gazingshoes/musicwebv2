"""
Audio Player Module
Handles actual music playback and the song queue.
"""

import pygame
import time

class AudioPlayer:
    """
    Manages audio playback, including play, stop, and queue.
    Uses: pygame.mixer
    """
    
    def __init__(self):
        """
        Initialize the pygame mixer and the queue.
        """
        try:
            pygame.mixer.init()
            print("AudioPlayer initialized successfully.")
        except Exception as e:
            print(f"Error initializing audio player: {e}")
            print("Playback may not work. Ensure you have audio drivers.")
            
        self.queue = []
        self.is_playing = False
            
    def play_now(self, song):
        """
        Clears the queue, adds this song, and plays it immediately.
        """
        self.queue = [] # Clear the queue
        self.queue.append(song)
        self.play_next_from_queue()
        
    def add_to_queue(self, song):
        """
        Adds a song to the end of the queue.
        """
        self.queue.append(song)
        print(f"✅ Added '{song.title}' to queue.")

    def play_next_from_queue(self):
        """
        Plays the next song in the queue.
        If a song is already playing, it does nothing.
        If the queue is empty, it stops.
        """
        # 1. Don't interrupt a song that is already playing
        if self.is_playing and pygame.mixer.music.get_busy():
            print("(Music is already playing.)")
            return

        # 2. Check if the queue is empty
        if len(self.queue) == 0:
            self.is_playing = False
            print("Queue is empty.")
            return

        # 3. Pop the next song and play it
        song = self.queue.pop(0) # Get the first song
        
        try:
            pygame.mixer.music.load(song.filepath)
            pygame.mixer.music.play()
            song.play() # This increments the play count
            self.is_playing = True
            print(f"▶️ Now playing: {song.title}")
        except Exception as e:
            print(f"❌ Error playing file {song.filepath}: {e}")
            self.is_playing = False
            
    def stop(self):
        """
        Stops the music and clears the entire queue.
        """
        self.queue = []
        pygame.mixer.music.stop()
        self.is_playing = False
        print("⏹️ Music stopped and queue cleared.")

    def get_queue_display(self):
        """
        Returns a formatted string of songs currently in the queue.
        """
        if not self.queue:
            return "Queue is empty."
            
        result = "--- 🎵 Current Queue ---\n"
        for i, song in enumerate(self.queue, 1):
            result += f"{i}. {song.get_info()}\n"
        return result