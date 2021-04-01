# functions in this file are used to automatically update lyric display
import tkinter as tk  # lyric display management
import math  # to calculate minimum duration

# custom libraries
import spotify_func
import get_lyric
import lrc


# function to detect song change and grab song information if song changed (called every 1s)
# parameters: song properties class, spotify token, title bar class, tk window, lyric control buttons
def detect_song_change(song_properties, sp, title, window, button_show_all, button_add_sec, button_reduce_sec):
    temp = song_properties.song
    song_properties.song = spotify_func.check_spotify(sp)
    # if song changed
    if temp['name'] != song_properties.song['name']:
        # update and refresh song properties data
        search_result = get_lyric.get_search_result(song_properties.song)
        lyric, offset = get_lyric.get_lyric(search_result, 0, song_properties.song)
        song_properties.lyric = lrc.format_lyric(lyric)
        song_properties.lyric_original = lyric
        song_properties.search_result = search_result
        song_properties.lyric_offset = offset
        song_properties.nlyric = 0
        song_properties.dynamic_lyric_pos = 0
        song_properties.song_changed = True
        # update tkinter window title
        title.title(('歌曲: ' + song_properties.song['name'] + "  " + '歌词信息: ' +
                     song_properties.search_result[song_properties.nlyric][0] + " " +
                     song_properties.search_result[song_properties.nlyric][2] + " " +
                     str(song_properties.lyric_offset) + 'ms'))

    # if search result is empty, lyric adjustment button should be disabled, otherwise enable
    if song_properties.search_result == [['N/A', 'N/A', '']] or \
            song_properties.search_result[0][1] == ['[99:99.99]No lyrics found.', 0]:
        button_show_all.config(state=tk.DISABLED)
        button_add_sec.config(state=tk.DISABLED)
        button_reduce_sec.config(state=tk.DISABLED)
    else:
        button_show_all.config(state=tk.NORMAL)
        button_add_sec.config(state=tk.NORMAL)
        button_reduce_sec.config(state=tk.NORMAL)

    # call every 1s
    window.after(1000, lambda: detect_song_change(song_properties, sp, title, window,
                                                  button_show_all, button_add_sec, button_reduce_sec))


# function to control lyric, based on the length of each sentence, calculate the time needed for each letter
# Repetitively call this function based on the time needed for each letter
# parameters: tk text display, tk window, song properties class, window properties class
def update_lyric(lyric_display, window, song_properties, win_properties):
    # get and update lyric
    lyric_display['state'] = tk.NORMAL
    temp = lyric_display.get('1.0', 'end')  # store previous lyric
    lyric_display.delete('1.0', tk.END)
    lyric_displayed, time_to_update = lrc.get_sentence(song_properties.lyric,
                                                       song_properties.song['progress_ms'], win_properties.nrows,
                                                       song_properties.lyric_offset)
    lyric_display.insert('1.0', lyric_displayed)

    # if at end of song, then next refresh is at end of song
    if time_to_update == -1:
        time_to_update = song_properties.song['length']

    # if lyric changed (new sentence)
    if temp.strip() != lyric_displayed.strip():
        # update refresh duration (duration per word is different now)
        song_properties.dynamic_lyric_duration = time_to_update - (song_properties.song['progress_ms'] +
                                                                   song_properties.lyric_offset)
        length = len(lyric_displayed.split('\n')[0])
        if length != 0:  # check to avoid divide by 0
            song_properties.dynamic_lyric_duration = int(song_properties.dynamic_lyric_duration / length)

        # refresh dynamic lyric position to beginning of sentence, clear foreground coloring
        song_properties.dynamic_lyric_pos = 0
        lyric_display.tag_remove("past", '1.0', 'end')

    # keep refresh time to below 1s
    if song_properties.dynamic_lyric_duration > 1000:
        song_properties.dynamic_lyric_duration = int(song_properties.dynamic_lyric_duration /
                                                     math.ceil(song_properties.dynamic_lyric_duration / 1000))

    # dynamically highlight lyric and update position of next letter to highlight
    lyric_display.tag_add("past", '1.0', '1.' + str(song_properties.dynamic_lyric_pos))
    song_properties.dynamic_lyric_pos += 1

    lyric_display['state'] = tk.DISABLED

    # call function again
    window.after(song_properties.dynamic_lyric_duration,
                 lambda: update_lyric(lyric_display, window, song_properties, win_properties))
