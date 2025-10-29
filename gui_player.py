"""
GUI Player Module
Creates graphical user interface using Tkinter
Uses: Tkinter, Classes, Functions, Event Handling
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
from music_library import MusicLibrary, Song, Playlist
from audio_player import AudioPlayer  # NEW IMPORT


class MusicPlayerGUI:
    """
    Main GUI class for the music player
    Uses: Tkinter widgets, Event handling, Class concepts
    """
    
    def __init__(self, library):
        """
        Initialize the GUI window
        Parameters:
        - library: MusicLibrary object to manage data
        """
        self.library = library
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("🎵 Python Music Player")
        self.window.geometry("900x650")  # Width x Height
        self.window.resizable(True, True)
        
        # Configure colors - modern look
        self.bg_color = "#1e1e1e"  # Dark background
        self.fg_color = "#ffffff"  # White text
        self.accent_color = "#1db954"  # Spotify green
        self.button_color = "#282828"  # Dark gray
        
        self.window.configure(bg=self.bg_color)
        
        # Create GUI components IN THE RIGHT ORDER!
        self.create_header()
        self.create_status_bar()  # CREATE STATUS BAR BEFORE NOTEBOOK!
        self.create_notebook()  # Tabbed interface
        
    def create_header(self):
        """
        Create header section with title
        Uses: Tkinter Label, Frame
        """
        # Header frame
        header_frame = tk.Frame(self.window, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Title label
        title_label = tk.Label(
            header_frame,
            text="🎵 PYTHON MUSIC PLAYER 🎵",
            font=("Arial", 24, "bold"),
            bg=self.accent_color,
            fg=self.fg_color
        )
        title_label.pack(pady=20)
    
    def create_status_bar(self):
        """
        Create status bar at bottom
        Uses: Label, StringVar for dynamic text
        """
        status_frame = tk.Frame(self.window, bg=self.button_color, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_text = tk.StringVar()
        self.status_text.set("Ready")
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_text,
            font=("Arial", 10),
            bg=self.button_color,
            fg=self.fg_color,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def create_notebook(self):
        """
        Create tabbed interface (notebook)
        Uses: ttk.Notebook for tabs
        """
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style for notebook
        style = ttk.Style()
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        
        # Create tabs
        self.create_library_tab()
        self.create_add_song_tab()
        self.create_playlist_tab()
        self.create_search_tab()
    
    def create_library_tab(self):
        """
        Create tab for viewing all songs
        Uses: Frame, Listbox, Scrollbar, Button
        """
        # Create frame for this tab
        library_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(library_frame, text="📚 Library")
        
        # Title label
        title = tk.Label(
            library_frame,
            text="All Songs in Library",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title.pack(pady=10)
        
        # Frame for listbox and scrollbar
        list_frame = tk.Frame(library_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox to display songs
        self.library_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 10),
            bg="#282828",
            fg=self.fg_color,
            selectbackground=self.accent_color,
            selectforeground=self.fg_color,
            height=20,
            yscrollcommand=scrollbar.set
        )
        self.library_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.library_listbox.yview)
        
        # Buttons frame
        button_frame = tk.Frame(library_frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_library,
            font=("Arial", 11, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.accent_color,
            cursor="hand2",
            width=15
        )
        refresh_btn.grid(row=0, column=0, padx=5)
        
        # Play button
        play_btn = tk.Button(
            button_frame,
            text="▶️ Play Selected",
            command=self.play_selected_song,
            font=("Arial", 11, "bold"),
            bg=self.accent_color,
            fg=self.fg_color,
            activebackground="#1ed760",
            cursor="hand2",
            width=15
        )
        play_btn.grid(row=0, column=1, padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete Selected",
            command=self.delete_selected_song,
            font=("Arial", 11, "bold"),
            bg="#c41e3a",
            fg=self.fg_color,
            activebackground="#ff0000",
            cursor="hand2",
            width=15
        )
        delete_btn.grid(row=0, column=2, padx=5)
        
        # Load songs initially
        self.refresh_library()
    
    def create_add_song_tab(self):
        """
        Create tab for adding new songs
        Uses: Entry widgets, Button, Label
        """
        add_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(add_frame, text="➕ Add Song")
        
        # Center frame for form
        form_frame = tk.Frame(add_frame, bg=self.bg_color)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title = tk.Label(
            form_frame,
            text="Add New Song to Library",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Song Title
        tk.Label(form_frame, text="Song Title:", font=("Arial", 12), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.title_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#282828", fg=self.fg_color)
        self.title_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Artist
        tk.Label(form_frame, text="Artist:", font=("Arial", 12), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.artist_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#282828", fg=self.fg_color)
        self.artist_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Duration
        tk.Label(form_frame, text="Duration (seconds):", font=("Arial", 12), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.duration_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#282828", fg=self.fg_color)
        self.duration_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Genre
        tk.Label(form_frame, text="Genre:", font=("Arial", 12), 
                 bg=self.bg_color, fg=self.fg_color).grid(row=4, column=0, sticky=tk.W, pady=10)
        self.genre_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#282828", fg=self.fg_color)
        self.genre_entry.grid(row=4, column=1, pady=10, padx=10)
        
        # Add button
        add_btn = tk.Button(
            form_frame,
            text="➕ Add Song",
            command=self.add_song,
            font=("Arial", 13, "bold"),
            bg=self.accent_color,
            fg=self.fg_color,
            activebackground="#1ed760",
            cursor="hand2",
            width=25,
            height=2
        )
        add_btn.grid(row=5, column=0, columnspan=2, pady=30)
    
    def create_playlist_tab(self):
        """
        Create tab for playlist management
        Uses: Multiple frames, Listbox, Button
        """
        playlist_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(playlist_frame, text="📁 Playlists")
        
        # Split into two sections
        left_frame = tk.Frame(playlist_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(playlist_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT SIDE - Playlist List
        tk.Label(left_frame, text="Your Playlists", font=("Arial", 14, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        
        # Listbox for playlists
        list_frame_left = tk.Frame(left_frame, bg=self.bg_color)
        list_frame_left.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_left = tk.Scrollbar(list_frame_left)
        scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox = tk.Listbox(
            list_frame_left,
            font=("Arial", 11),
            bg="#282828",
            fg=self.fg_color,
            selectbackground=self.accent_color,
            height=15,
            yscrollcommand=scrollbar_left.set
        )
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_left.config(command=self.playlist_listbox.yview)
        
        # Bind selection event
        self.playlist_listbox.bind('<<ListboxSelect>>', self.on_playlist_select)
        
        # Buttons for playlist
        btn_frame_left = tk.Frame(left_frame, bg=self.bg_color)
        btn_frame_left.pack(pady=10)
        
        tk.Button(btn_frame_left, text="➕ New Playlist", command=self.create_playlist_dialog,
                  font=("Arial", 10, "bold"), bg=self.accent_color, fg=self.fg_color,
                  cursor="hand2", width=15).grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame_left, text="🔄 Refresh", command=self.refresh_playlists,
                  font=("Arial", 10, "bold"), bg=self.button_color, fg=self.fg_color,
                  cursor="hand2", width=15).grid(row=0, column=1, padx=5)
        
        # RIGHT SIDE - Playlist Contents
        tk.Label(right_frame, text="Playlist Contents", font=("Arial", 14, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        
        # Listbox for songs in playlist
        list_frame_right = tk.Frame(right_frame, bg=self.bg_color)
        list_frame_right.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_right = tk.Scrollbar(list_frame_right)
        scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_songs_listbox = tk.Listbox(
            list_frame_right,
            font=("Courier", 10),
            bg="#282828",
            fg=self.fg_color,
            selectbackground=self.accent_color,
            height=15,
            yscrollcommand=scrollbar_right.set
        )
        self.playlist_songs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_right.config(command=self.playlist_songs_listbox.yview)
        
        # Buttons for playlist songs
        btn_frame_right = tk.Frame(right_frame, bg=self.bg_color)
        btn_frame_right.pack(pady=10)
        
        tk.Button(btn_frame_right, text="➕ Add Song", command=self.add_to_playlist_dialog,
                  font=("Arial", 10, "bold"), bg=self.accent_color, fg=self.fg_color,
                  cursor="hand2", width=15).grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame_right, text="➖ Remove Song", command=self.remove_from_playlist,
                  font=("Arial", 10, "bold"), bg="#c41e3a", fg=self.fg_color,
                  cursor="hand2", width=15).grid(row=0, column=1, padx=5)
        
        # Load playlists initially
        self.refresh_playlists()
    
    def create_search_tab(self):
        """
        Create tab for searching songs
        Uses: Combobox (dropdown), Entry, Listbox
        """
        search_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(search_frame, text="🔍 Search")
        
        # Search controls frame
        control_frame = tk.Frame(search_frame, bg=self.bg_color)
        control_frame.pack(pady=20)
        
        # Search type selection
        tk.Label(control_frame, text="Search by:", font=("Arial", 12, "bold"),
                 bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=10)
        
        self.search_type = ttk.Combobox(
            control_frame,
            values=["Artist", "Genre"],
            state="readonly",
            font=("Arial", 11),
            width=15
        )
        self.search_type.grid(row=0, column=1, padx=10)
        self.search_type.current(0)  # Default to Artist
        
        # Search entry
        tk.Label(control_frame, text="Search for:", font=("Arial", 12, "bold"),
                 bg=self.bg_color, fg=self.fg_color).grid(row=0, column=2, padx=10)
        
        self.search_entry = tk.Entry(control_frame, font=("Arial", 11), width=25,
                                      bg="#282828", fg=self.fg_color)
        self.search_entry.grid(row=0, column=3, padx=10)
        
        # Search button
        search_btn = tk.Button(
            control_frame,
            text="🔍 Search",
            command=self.perform_search,
            font=("Arial", 11, "bold"),
            bg=self.accent_color,
            fg=self.fg_color,
            cursor="hand2",
            width=12
        )
        search_btn.grid(row=0, column=4, padx=10)
        
        # Results frame
        results_frame = tk.Frame(search_frame, bg=self.bg_color)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="Search Results", font=("Arial", 14, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        
        # Results listbox
        list_frame = tk.Frame(results_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.search_results_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 10),
            bg="#282828",
            fg=self.fg_color,
            selectbackground=self.accent_color,
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.search_results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.search_results_listbox.yview)
    
    # ========== EVENT HANDLERS ==========
    
    def refresh_library(self):
        """
        Refresh the library listbox with all songs
        Uses: Listbox methods, Dictionary iteration
        """
        self.library_listbox.delete(0, tk.END)  # Clear listbox
        
        if len(self.library.all_songs) == 0:
            self.library_listbox.insert(tk.END, "No songs in library. Add some!")
            self.status_text.set("Library is empty")
        else:
            # Sort songs by title
            sorted_songs = sorted(self.library.all_songs.values(), 
                                  key=lambda song: song.title)
            
            for song in sorted_songs:
                # Format: Title - Artist (Genre) [Duration] [Plays: X]
                display_text = f"{song.title} - {song.artist} ({song.genre}) [{song.duration}s] [Plays: {song.get_play_count()}]"
                self.library_listbox.insert(tk.END, display_text)
            
            self.status_text.set(f"Loaded {len(self.library.all_songs)} songs")
    
    def play_selected_song(self):
        """
        Play the selected song from library
        Uses: Listbox selection, String parsing, messagebox
        """
        selection = self.library_listbox.curselection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a song to play!")
            return
        
        # Get selected text
        selected_text = self.library_listbox.get(selection[0])
        
        if "No songs" in selected_text:
            return
        
        # Extract song title (before " - ")
        song_title = selected_text.split(" - ")[0]
        
        # Get song object and play
        song = self.library.get_song(song_title)
        if song:
            play_message = song.play()
            messagebox.showinfo("Now Playing", play_message)
            self.status_text.set(f"Playing: {song_title}")
            self.refresh_library()  # Refresh to show updated play count
    
    def delete_selected_song(self):
        """
        Delete selected song from library
        Uses: Listbox selection, Dictionary deletion, messagebox
        """
        selection = self.library_listbox.curselection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a song to delete!")
            return
        
        selected_text = self.library_listbox.get(selection[0])
        
        if "No songs" in selected_text:
            return
        
        # Extract song title
        song_title = selected_text.split(" - ")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete '{song_title}'?")
        
        if confirm:
            # Delete from dictionary
            if song_title in self.library.all_songs:
                del self.library.all_songs[song_title]
                messagebox.showinfo("Success", f"Deleted '{song_title}' from library")
                self.status_text.set(f"Deleted: {song_title}")
                self.refresh_library()
    
    def add_song(self):
        """
        Add new song from form entries
        Uses: Entry.get(), Exception handling, Form validation
        """
        # Get values from entries
        title = self.title_entry.get().strip()
        artist = self.artist_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        genre = self.genre_entry.get().strip()
        
        # Validate inputs
        if not title or not artist or not duration_str or not genre:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            duration = int(duration_str)
            
            if duration <= 0:
                messagebox.showerror("Error", "Duration must be positive!")
                return
            
            # Add to library
            result = self.library.add_song(title, artist, duration, genre)
            
            if "already exists" in result:
                messagebox.showwarning("Warning", result)
            else:
                messagebox.showinfo("Success", result)
                self.status_text.set(f"Added: {title}")
                
                # Clear form
                self.title_entry.delete(0, tk.END)
                self.artist_entry.delete(0, tk.END)
                self.duration_entry.delete(0, tk.END)
                self.genre_entry.delete(0, tk.END)
                
                # Refresh library tab
                self.refresh_library()
        
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number!")
    
    def refresh_playlists(self):
        """
        Refresh playlist listbox
        Uses: List iteration
        """
        self.playlist_listbox.delete(0, tk.END)
        
        if len(self.library.playlists) == 0:
            self.playlist_listbox.insert(tk.END, "No playlists. Create one!")
        else:
            for playlist in self.library.playlists:
                display_text = f"{playlist.title} ({len(playlist.songs)} songs)"
                self.playlist_listbox.insert(tk.END, display_text)
        
        # Clear playlist contents view
        self.playlist_songs_listbox.delete(0, tk.END)
    
    def on_playlist_select(self, event):
        """
        Handle playlist selection event
        Uses: Event binding, Listbox selection
        """
        selection = self.playlist_listbox.curselection()
        
        if not selection:
            return
        
        selected_text = self.playlist_listbox.get(selection[0])
        
        if "No playlists" in selected_text:
            return
        
        # Extract playlist name (before "(")
        playlist_name = selected_text.split(" (")[0]
        
        # Get playlist object
        playlist = self.library.get_playlist(playlist_name)
        
        if playlist:
            # Display songs in playlist
            self.playlist_songs_listbox.delete(0, tk.END)
            
            if len(playlist.songs) == 0:
                self.playlist_songs_listbox.insert(tk.END, "Playlist is empty")
            else:
                for i, song in enumerate(playlist.songs, start=1):
                    display_text = f"{i}. {song.title} - {song.artist}"
                    self.playlist_songs_listbox.insert(tk.END, display_text)
            
            self.status_text.set(f"Viewing playlist: {playlist_name}")
    
    def create_playlist_dialog(self):
        """
        Show dialog to create new playlist
        Uses: Toplevel window (popup), Entry
        """
        # Create popup window
        dialog = tk.Toplevel(self.window)
        dialog.title("Create Playlist")
        dialog.geometry("400x150")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Label
        tk.Label(dialog, text="Enter Playlist Name:", font=("Arial", 12, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=20)
        
        # Entry
        name_entry = tk.Entry(dialog, font=("Arial", 12), width=30,
                              bg="#282828", fg=self.fg_color)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        # Button
        def create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Playlist name cannot be empty!")
                return
            
            result = self.library.create_playlist(name)
            messagebox.showinfo("Success", result)
            self.status_text.set(f"Created playlist: {name}")
            self.refresh_playlists()
            dialog.destroy()
        
        tk.Button(dialog, text="Create", command=create,
                  font=("Arial", 11, "bold"), bg=self.accent_color,
                  fg=self.fg_color, cursor="hand2", width=15).pack(pady=10)
    
    def add_to_playlist_dialog(self):
        """
        Show dialog to add song to selected playlist
        Uses: Toplevel, Listbox, Selection handling
        """
        # Check if playlist is selected
        playlist_selection = self.playlist_listbox.curselection()
        
        if not playlist_selection:
            messagebox.showwarning("No Selection", "Please select a playlist first!")
            return
        
        selected_text = self.playlist_listbox.get(playlist_selection[0])
        
        if "No playlists" in selected_text:
            return
        
        playlist_name = selected_text.split(" (")[0]
        playlist = self.library.get_playlist(playlist_name)
        
        if not playlist:
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Add Song to '{playlist_name}'")
        dialog.geometry("600x400")
        dialog.configure(bg=self.bg_color)
        
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Label
        tk.Label(dialog, text="Select a song to add:", font=("Arial", 12, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        
        # Listbox with songs
        list_frame = tk.Frame(dialog, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        song_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            bg="#282828",
            fg=self.fg_color,
            selectbackground=self.accent_color,
            yscrollcommand=scrollbar.set
        )
        song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=song_listbox.yview)
        
        # Populate with songs not in playlist
        for song_title, song in self.library.all_songs.items():
            # Check if song already in playlist
            already_in = any(s.title == song_title for s in playlist.songs)
            if not already_in:
                song_listbox.insert(tk.END, f"{song.title} - {song.artist}")
        
        # Add button
        def add():
            selection = song_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a song!")
                return
            
            selected_song_text = song_listbox.get(selection[0])
            song_title = selected_song_text.split(" - ")[0]
            
            song = self.library.get_song(song_title)
            if song:
                result = playlist.add_song(song)
                messagebox.showinfo("Success", result)
                self.status_text.set(f"Added '{song_title}' to '{playlist_name}'")
                self.refresh_playlists()
                self.on_playlist_select(None)  # Refresh playlist view
                dialog.destroy()
        
        tk.Button(dialog, text="Add to Playlist", command=add,
                  font=("Arial", 11, "bold"), bg=self.accent_color,
                  fg=self.fg_color, cursor="hand2", width=20).pack(pady=10)
    
    def remove_from_playlist(self):
        """
        Remove selected song from current playlist
        Uses: Listbox selection, String parsing
        """
        # Check if playlist is selected
        playlist_selection = self.playlist_listbox.curselection()
        
        if not playlist_selection:
            messagebox.showwarning("No Selection", "Please select a playlist first!")
            return
        
        # Check if song is selected
        song_selection = self.playlist_songs_listbox.curselection()
        
        if not song_selection:
            messagebox.showwarning("No Selection", "Please select a song to remove!")
            return
        
         # Get playlist
        selected_text = self.playlist_listbox.get(playlist_selection[0])
        
        if "No playlists" in selected_text:
            return
        
        playlist_name = selected_text.split(" (")[0]
        playlist = self.library.get_playlist(playlist_name)
        
        if not playlist:
            return
        
        # Get song
        selected_song_text = self.playlist_songs_listbox.get(song_selection[0])
        
        if "empty" in selected_song_text:
            return
        
        # Extract song title (remove numbering)
        song_title = selected_song_text.split(". ", 1)[1].split(" - ")[0]
        
        # Confirm removal
        confirm = messagebox.askyesno("Confirm Remove", 
                                      f"Remove '{song_title}' from '{playlist_name}'?")
        
        if confirm:
            result = playlist.remove_song(song_title)
            messagebox.showinfo("Success", result)
            self.status_text.set(f"Removed '{song_title}' from '{playlist_name}'")
            self.refresh_playlists()
            self.on_playlist_select(None)  # Refresh view
    
    def perform_search(self):
        """
        Perform search based on selected criteria
        Uses: Combobox value, Entry value, Conditionals
        """
        search_type = self.search_type.get()
        search_query = self.search_entry.get().strip()
        
        if not search_query:
            messagebox.showwarning("Empty Search", "Please enter a search term!")
            return
        
        # Clear previous results
        self.search_results_listbox.delete(0, tk.END)
        
        # Perform search based on type
        if search_type == "Artist":
            results = self.library.search_by_artist(search_query)
        else:  # Genre
            results = self.library.search_by_genre(search_query)
        
        # Display results
        if len(results) == 0:
            self.search_results_listbox.insert(tk.END, 
                f"No songs found for {search_type.lower()}: '{search_query}'")
            self.status_text.set("No results found")
        else:
            self.search_results_listbox.insert(tk.END, 
                f"Found {len(results)} song(s):")
            self.search_results_listbox.insert(tk.END, "")
            
            for i, song in enumerate(results, start=1):
                display_text = f"{i}. {song.get_info()}"
                self.search_results_listbox.insert(tk.END, display_text)
            
            self.status_text.set(f"Found {len(results)} results")
    
    def run(self):
        """
        Start the GUI main loop
        Uses: Tkinter mainloop
        """
        self.window.mainloop()


def save_on_close(library, window):
    """
    Save data when closing the application
    Uses: File handling functions, messagebox
    """
    try:
        # Import save functions
        from player import save_songs_to_file, save_playlists_to_file
        
        # Save data
        save_songs_to_file(library)
        save_playlists_to_file(library)
        
        messagebox.showinfo("Saved", "All data has been saved successfully!")
        window.destroy()
    
    except Exception as e:
        result = messagebox.askyesno("Error", 
            f"Error saving data: {e}\n\nClose anyway?")
        if result:
            window.destroy()