# to create executable, run: pyinstaller main.spec

import tkinter as tk  # used to create display window
from tkinter import font  # used to manage fonts
from tkinter import ttk  # used to make prettier buttons
import ast  # used to convert cached data

# custom libraries
import get_lyric
import lrc
import spotify_func
import tk_adj
import credential
import classes
import lrc_mgmt

sp = False # initialize Spotify token for initial check in check_credentials
# initialize additional variables to avoid repetitive querying
song = False
cache_file = False

window = tk.Tk() # initialize tk window

window.wm_attributes('-transparentcolor', 'gray1')  # set transparent color, use gray1 to minimize antialiasing issue

# set up Spotify API environment variables
credential_file = 'cache/credentials.txt'
sp = credential.check_credentials(credential_file, '', sp, window)  # access token

window.overrideredirect(True)  # turn off default window

# first check on launch
if not song:
    song = spotify_func.check_spotify(sp)  # Spotify play information
    search_result = get_lyric.get_search_result(song)  # lyric search result
    lyric, offset = get_lyric.get_lyric(search_result, 0, song)  # use first lyric on search result as default
    lyric_f = lrc.format_lyric(lyric)  # format lyric, separately store for efficiency purposes

# read user cache on launch
if not cache_file:
    cache_file = 'cache/user_setting.txt'
    # start with default
    cache = ['Microsoft YaHei\n', '32\n', 'normal\n', 'roman\n', '0\n', '0\n',
             'blue\n', 'black\n', '2\n', '55\n', '0.8\n', '[1, "white", "gray1"]\n', '1\n', '1\n', '0\n', '0\n']
    try:
        with open(cache_file, 'r') as f:
            temp = f.readlines()
        if len(temp) == 16:
            cache = temp
    except FileNotFoundError:
        pass

# set up window
font = font.Font(family=cache[0][:-1], size=int(cache[1][:-1]), weight=cache[2][:-1], slant=cache[3][:-1],
                 underline=tk_adj.eval_bool(cache[4][:-1]), overstrike=tk_adj.eval_bool(cache[5][:-1]))
win_properties = classes.WindowProperties(font, cache[6][:-1], cache[7][:-1], int(cache[8][:-1]), int(cache[9][:-1]),
                                          float(cache[10][:-1]), ast.literal_eval(cache[11][:-1]), int(cache[12][:-1]),
                                          tk_adj.eval_bool(cache[13][:-1]), int(cache[14][:-1]), int(cache[15][:-1]))
window.geometry("+%s+%s" % (win_properties.x_pos, win_properties.y_pos))

# update song properties
song_properties = classes.SongProperties(song, lyric_f, lyric, search_result, offset, 0)

# set up title bar
title = classes.TitleBar(0, 0, window, win_properties)
title.title_bar.grid(row=0, column=0, sticky='EW')
window.grid_rowconfigure(0, weight=1)

# create tkinter window with default attributes
title.title(('歌曲: ' + song_properties.song['name'] + "  " + '歌词信息: ' +
              song_properties.search_result[song_properties.nlyric][0] + " " +
              song_properties.search_result[song_properties.nlyric][2] + " " +
              str(song_properties.lyric_offset) + 'ms'))
photo = tk.PhotoImage(file=r'static\spotify.png')
window.iconphoto(False, photo)
window.resizable(width=False, height=False)
window.attributes('-topmost', win_properties.on_top)
window.attributes('-alpha', win_properties.transparency)

# create other widgets on window
# define widgets
# note lambda is used such that the functions are not immediately called when program is ran
# this is needed because the function calls include parameters
# define a tk Frame to hold all the buttons, lyric panel is outside of Frame
# this way we can hide and show the buttons easily
frame = tk.Frame(window)
photo_use_next = tk.PhotoImage(file=r'static\button\forward.png').subsample(5, 5)
button_use_next = ttk.Button(frame, text='Next Lyric >>', image=photo_use_next, 
                            command=lambda: tk_adj.change_lyric(1, title, win_properties, lyric_display,
                                                                button_use_previous, button_use_next, song_properties))
# default status for use previous lyric button is disabled because we are using the first lyric result
photo_use_previous = tk.PhotoImage(file=r'static\button\back.png').subsample(5, 5)
button_use_previous = ttk.Button(frame, text='<< Prev Lyric', image=photo_use_previous, 
                                state=tk.DISABLED,
                                command=lambda: tk_adj.change_lyric(-1, title, win_properties, lyric_display,
                                                                    button_use_previous, button_use_next,
                                                                    song_properties))
photo_show_all = tk.PhotoImage(file=r'static\button\select.png').subsample(5, 5)
button_show_all = ttk.Button(frame, text='Select Lyric', image=photo_show_all, 
                            command=lambda: tk_adj.select_lyric(song_properties, lyric_display, title, window,
                                                                win_properties, button_use_previous,
                                                                button_use_next))
photo_add_sec = tk.PhotoImage(file=r'static\button\more_time.png').subsample(5, 5)
button_add_sec = ttk.Button(frame, text='+ 1s', image=photo_add_sec, 
                           command=lambda: tk_adj.lyric_offset(500, song_properties, title))
photo_reduce_sec = tk.PhotoImage(file=r'static\button\less_time.png').subsample(5, 5)
button_reduce_sec = ttk.Button(frame, text='- 1s', image=photo_reduce_sec, 
                              command=lambda: tk_adj.lyric_offset(-500, song_properties, title))
# if first song doesn't have a valid lyric, adjustment buttons should be disabled
if song_properties.search_result == [['N/A', 'N/A', '']]:
    button_add_sec.config(state=tk.DISABLED)
    button_reduce_sec.config(state=tk.DISABLED)
photo_inc_font = tk.PhotoImage(file=r'static\button\inc_font.png').subsample(5, 5)
button_inc_font = ttk.Button(frame, text='A+', image=photo_inc_font, 
                            command=lambda: tk_adj.adj_font_size(lyric_display, win_properties, 1, button_red_font))
photo_red_font = tk.PhotoImage(file=r'static\button\dec_font.png').subsample(5, 5)
button_red_font = ttk.Button(frame, text='A-', image=photo_red_font, 
                            command=lambda: tk_adj.adj_font_size(lyric_display, win_properties, -1, button_red_font))
photo_pick_font = tk.PhotoImage(file=r'static\button\font.png').subsample(5, 5)
button_pick_font = ttk.Button(frame, text='A', image=photo_pick_font, 
                             command=lambda: tk_adj.adj_font(lyric_display, window, win_properties))
photo_font_color = tk.PhotoImage(file=r'static\button\font_color.png').subsample(5, 5)
button_font_color = ttk.Button(frame, text='A Color', image=photo_font_color, 
                              command=lambda: tk_adj.adj_font_color(lyric_display, win_properties))
photo_font_color_bg = tk.PhotoImage(file=r'static\button\font_color_bg.png').subsample(5, 5)
button_font_color_bg = ttk.Button(frame, text='A Color Bg', image=photo_font_color_bg,
                                  command=lambda: tk_adj.adj_font_color_bg(lyric_display, win_properties))
photo_inc_row = tk.PhotoImage(file=r'static\button\inc_row.png').subsample(5, 5)
button_inc_row = ttk.Button(frame, text='Row+', image=photo_inc_row, 
                           command=lambda: tk_adj.adj_nrow(lyric_display, win_properties, 1, button_red_row))
photo_red_row = tk.PhotoImage(file=r'static\button\dec_row.png').subsample(5, 5)
button_red_row = ttk.Button(frame, text='Row-', image=photo_red_row, 
                           command=lambda: tk_adj.adj_nrow(lyric_display, win_properties, -1, button_red_row))
photo_bg_color = tk.PhotoImage(file=r'static\button\color.png').subsample(5, 5)
button_background_color = ttk.Button(frame, text='Bckg Color', image=photo_bg_color, 
                                    command=lambda: tk_adj.adj_bg_color(lyric_display, window, win_properties))
photo_inc_width = tk.PhotoImage(file=r'static\button\inc_width.png').subsample(5, 5)
button_inc_width = ttk.Button(frame, text='Width+', image=photo_inc_width, 
                             command=lambda: tk_adj.adj_width(1, lyric_display, win_properties, button_red_width))
photo_red_width = tk.PhotoImage(file=r'static\button\dec_width.png').subsample(5, 5)
button_red_width = ttk.Button(frame, text='Width-', image=photo_red_width, 
                             command=lambda: tk_adj.adj_width(-1, lyric_display, win_properties, button_red_width))
photo_inc_trans = tk.PhotoImage(file=r'static\button\dec_inv.png').subsample(5, 5)
button_inc_trans = ttk.Button(frame, text='+ Trsp', image=photo_inc_trans, 
                             command=lambda: tk_adj.adj_transparency(0.1, window, win_properties, button_red_trans,
                                                                     button_inc_trans))
photo_red_trans = tk.PhotoImage(file=r'static\button\inc_inv.png').subsample(5, 5)
button_red_trans = ttk.Button(frame, text='- Trsp', image=photo_red_trans, 
                             command=lambda: tk_adj.adj_transparency(-0.1, window, win_properties, button_red_trans,
                                                                     button_inc_trans))
photo_trans_on = tk.PhotoImage(file=r'static\button\inv_on.png').subsample(5, 5)
photo_trans_off = tk.PhotoImage(file=r'static\button\inv_off.png').subsample(5, 5)
button_trans = ttk.Button(frame, text='Trsp', image=photo_trans_on,
                          command=lambda: tk_adj.toggle_transparency(lyric_display, win_properties,
                                                                     button_trans, photo_trans_on, photo_trans_off))
photo_enable_top_most = tk.PhotoImage(file=r'static\button\enable_ontop.png').subsample(5, 5)
photo_disable_top_most = tk.PhotoImage(file=r'static\button\disable_ontop.png').subsample(5, 5)
button_top_most = ttk.Button(frame, text='On Top', image=photo_enable_top_most,
                            command=lambda: tk_adj.adj_on_top(window, win_properties, button_top_most,
                                                              photo_enable_top_most, photo_disable_top_most))
lyric_display = tk.Text(window, width=win_properties.width, height=win_properties.nrows,
                        font=win_properties.font, fg=win_properties.font_color_bg,
                        bg=win_properties.bg_color[win_properties.bg_color[0]], bd=win_properties.bd)
# configure alternative text for lyric on the portion of song already played
lyric_display.tag_configure("past", font=win_properties.font, foreground=win_properties.font_color)
# get text to display
lyric_displayed = lrc.get_sentence(song_properties.lyric, song_properties.song['progress_ms'],
                                   win_properties.nrows,
                                   song_properties.lyric_offset)
lyric_display.insert('1.0', lyric_displayed[0])
lyric_display['state'] = tk.DISABLED  # disable user text editing

# display widgets using grid format
frame.grid(row=1, column=0, sticky='EW')
button_use_next.grid(row=0, column=1, sticky='NSEW')
button_use_previous.grid(row=0, column=0, sticky='NSEW')
button_show_all.grid(row=0, column=2, sticky='NSEW')
button_add_sec.grid(row=0, column=4, sticky='NSEW')
button_reduce_sec.grid(row=0, column=3, sticky='NSEW')
button_inc_font.grid(row=0, column=6, sticky='NSEW')
button_red_font.grid(row=0, column=5, sticky='NSEW')
button_pick_font.grid(row=0, column=7, sticky='NSEW')
button_font_color.grid(row=0, column=8, sticky='NSEW')
button_font_color_bg.grid(row=0, column=9, sticky='NSEW')
button_inc_row.grid(row=0, column=11, sticky='NSEW')
button_red_row.grid(row=0, column=10, sticky='NSEW')
button_inc_width.grid(row=0, column=13, sticky='NSEW')
button_red_width.grid(row=0, column=12, sticky='NSEW')
button_inc_trans.grid(row=0, column=15, sticky='NSEW')
button_red_trans.grid(row=0, column=14, sticky='NSEW')
button_trans.grid(row=0, column=16, sticky='NSEW')
button_background_color.grid(row=0, column=17, sticky='NSEW')
button_top_most.grid(row=0, column=18, sticky='NSEW')
lyric_display.grid(row=2, rowspan=2, column=0, sticky='EW')
# give lyric display row a weight such that empty spaces in tk window are allocated to lyric display
# note lyric display above is set to sticky in East and West directitons
window.grid_rowconfigure(2, weight=1)
# give button frame row and each button column a weight such that their width are evenly distributed too
window.grid_rowconfigure(1, weight=1)
for i in range(19):
    frame.grid_columnconfigure(i, weight=1)

# bind window to detect mouse enter and exit
window.bind("<Enter>", lambda event: tk_adj.on_enter(title, frame, window, win_properties, event))
window.bind("<Leave>", lambda event: tk_adj.on_exit(title, frame, window, win_properties, event))

# check song status from Spotify every 1s
lrc_mgmt.detect_song_change(song_properties, sp, title, window, button_show_all, button_add_sec, button_reduce_sec)

# update lyric (recurive function that continuously updates)
lrc_mgmt.update_lyric(lyric_display, window, song_properties, win_properties)

window.mainloop()  # tkinter main loop
