from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


main_window = Tk()
main_window.title("MP3 Player")
main_window.geometry("560x420")

# Initialize pygame mixer to play sound
pygame.mixer.init()

# Create global pause variable
global paused
paused = False
PATH = ""  # must end with /


# Grab song's lenght time info
def play_time():
	if stopped:
		return
	current_time = pygame.mixer.music.get_pos() / 1000
	converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

	song = song_box.get(ACTIVE)
	song = f"{PATH}{song}.mp3"
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))
	current_time +=1

	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f"Time Elapsed:  {converted_song_length}  of  {converted_song_length}  ")
	elif paused:
		pass
	elif int(my_slider.get()) == int(current_time): # slider is not moved
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))
	
	else: #slider is moved
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(my_slider.get()))
		converted_current_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
		status_bar.config(text=f"Time Elapsed:  {converted_current_time}  of  {converted_song_length}  ")
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)

	status_bar.after(1000, play_time)


# Add song function
def add_song():
	song = filedialog.askopenfilename(initialdir="audio/", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	song = song.replace(f"{PATH}", "")
	song = song.replace(".mp3", "")
	song_box.insert(END, song)  # add song to list box


# Add many songs
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir="audio/", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	for song in songs:
		song = song.replace("{PATH}", "")
		song = song.replace(".mp3", "")
		song_box.insert(END, song)


# Play selected song
def play():
	global stopped
	stopped = False
	song = song_box.get(ACTIVE)
	song = f"{PATH}{song}.mp3"
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	pygame.mixer.music.set_volume(volume_slider.get())
	play_time()


# Stop playback
global stopped
stopped = False
def stop():
	status_bar.config(text="")
	my_slider.config(value=0)
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)
	status_bar.config(text="")
	global stopped
	stopped = True


def next_song():
	status_bar.config(text="")
	my_slider.config(value=0)
	next_one = song_box.curselection() # returns a tuple
	next_one = next_one[0] + 1
	song = song_box.get(next_one)
	song = f"{PATH}{song}.mp3"
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	song_box.selection_clear(0, END)
	song_box.activate(next_one)
	song_box.selection_set(next_one, last=None)


def previous_song():
	status_bar.config(text="")
	my_slider.config(value=0)
	next_one = song_box.curselection() # returns a tuple
	next_one = next_one[0] - 1
	song = song_box.get(next_one)
	song = f"{PATH}{song}.mp3"
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	song_box.selection_clear(0, END)
	song_box.activate(next_one)
	song_box.selection_set(next_one, last=None)


def delete_song():
	stop()
	song_box.delete(ANCHOR)
	pygame.mixer.music.stop()


def delete_all_songs():
	stop()
	song_box.delete(0, END)
	pygame.mixer.music.stop()


# Pause / unpause the current song
def pause(is_paused):
	global paused
	paused= is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True


def slide(x):
	song = song_box.get(ACTIVE)
	song = f"{PATH}{song}.mp3"
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())


# =========================== UI ====================================

# Create frame for loading and removing songs
buttons_frame = Frame(main_window)
buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)
buttons_frame.columnconfigure(2, weight=1)
buttons_frame.columnconfigure(3, weight=1)
buttons_frame.pack()

# Create button to load / remove songs
add_song_button = Button(buttons_frame, text="Add Song", command=add_song)
add_many_songs_button = Button(buttons_frame, text="Add Songs", command=add_many_songs)
delete_song_button = Button(buttons_frame, text="Remove Song", command=delete_song)
delete_all_songs_button = Button(buttons_frame, text="Remove Songs", command=delete_all_songs)

# Place buttons inside frame
add_song_button.grid(row=0, column=0, sticky=W+E, pady=20, padx=10)
add_many_songs_button.grid(row=0, column=1, sticky=W+E, pady=20, padx=10)
delete_song_button.grid(row=0, column=2, sticky=W+E, pady=20, padx=10)
delete_all_songs_button.grid(row=0, column=3, sticky=W+E, pady=20, padx=10)

# Create frame for playlist and volume
playlist_and_volume_frame = Frame(main_window)
playlist_and_volume_frame.columnconfigure(0, weight=4)
playlist_and_volume_frame.columnconfigure(0, weight=1)
playlist_and_volume_frame.pack()

# Create playlist and volume box
song_box = Listbox(playlist_and_volume_frame, bg="black", fg="green", width=40, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)
volume_frame = LabelFrame(playlist_and_volume_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=0.2, command=volume, length=125)
volume_slider.pack(pady=10)

# Create player controls frame
player_controls_frame = Frame(main_window)
player_controls_frame.columnconfigure(0, weight=1)
player_controls_frame.columnconfigure(1, weight=1)
player_controls_frame.columnconfigure(2, weight=1)
player_controls_frame.columnconfigure(3, weight=1)
player_controls_frame.columnconfigure(4, weight=1)
player_controls_frame.pack()

# Define player control buttons images
back_btn_img = PhotoImage(file="images/backward-button.png").subsample(2, 2)
forward_btn_img = PhotoImage(file="images/forward-button.png").subsample(2, 2)
play_btn_img = PhotoImage(file="images/play-button.png").subsample(2, 2)
pause_btn_img = PhotoImage(file="images/pause-button.png").subsample(2, 2)
stop_btn_img = PhotoImage(file="images/stop-button.png").subsample(2, 2)

# Create player control buttons
back_button = Button(player_controls_frame, image=back_btn_img, command=previous_song)
forward_button = Button(player_controls_frame, image=forward_btn_img, command=next_song)
play_button = Button(player_controls_frame, image=play_btn_img, command=play)
pause_button = Button(player_controls_frame, image=pause_btn_img, command=lambda: pause(paused))
stop_button = Button(player_controls_frame, image=stop_btn_img, command=stop)

back_button.grid(row=0, column=0, padx=10, pady=20)
forward_button.grid(row=0, column=1, padx=10, pady=20)
play_button.grid(row=0, column=2, padx=10, pady=20)
pause_button.grid(row=0, column=3, padx=10, pady=20)
stop_button.grid(row=0, column=4, padx=10, pady=20)

status_bar = Label(main_window, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

my_slider = ttk.Scale(main_window, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=400)
my_slider.pack()

main_window.mainloop()
