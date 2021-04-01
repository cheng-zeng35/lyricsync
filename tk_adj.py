# functions in this library are used to update the tkinter window

import tkinter as tk  # used to create display window
import tkfontchooser  # font chooser
from tkinter import colorchooser  # color palette tool

# custom libraries
import get_lyric
import lrc


# function to switch between different lyric based on search result
# parameters: forward (1) or backward (-1) adjustment, tkinter window, window properties, tkinter lyric display
# backward lyric control button, forward lyric control button, song properties
def change_lyric(adj, title, win_properties, lyric_display, button_use_previous, button_use_next, song_properties):
    # update lyric
    song_properties.nlyric += adj
    new_lyric, new_offset = get_lyric.get_lyric(song_properties.search_result, song_properties.nlyric,
                                                song_properties.song)
    song_properties.lyric = lrc.format_lyric(new_lyric)
    song_properties.lyric_original = new_lyric
    song_properties.lyric_offset = new_offset
    lyric_display['state'] = tk.NORMAL
    lyric_display.delete('1.0', tk.END)
    lyric_displayed = lrc.get_sentence(song_properties.lyric, song_properties.song['progress_ms'],
                                       win_properties.nrows, new_offset)
    lyric_display.insert('1.0', lyric_displayed[0])
    lyric_display['state'] = tk.DISABLED
    title.title(('歌曲: ' + song_properties.song['name'] + "  " + '歌词信息: ' +
                 song_properties.search_result[song_properties.nlyric][0] + " " +
                 song_properties.search_result[song_properties.nlyric][2] + " " +
                 str(song_properties.lyric_offset) + 'ms'))
    # disable/enable buttons accordingly based on lyric used and research results
    # if lyric is the first search result, then backward control button is disabled, etc.
    if song_properties.nlyric <= 0:
        button_use_previous['state'] = tk.DISABLED
    else:
        button_use_previous['state'] = tk.NORMAL
    if song_properties.nlyric >= len(song_properties.search_result) - 1:
        button_use_next['state'] = tk.DISABLED
    else:
        button_use_next['state'] = tk.NORMAL


# helper function to select lyric below, used to call change lyric function whenever a select is made
def select_lyric_helper(event, lyric_choice, song_properties, lyric_display, title, window_properties,
                        button_use_previous, button_use_next, insert_first):
    song_properties.nlyric = lyric_choice.curselection()[0] + insert_first
    change_lyric(0, title, window_properties, lyric_display, button_use_previous, button_use_next, song_properties)


# function to pop up a window for user to select the correct lyric
# parameters: song properties var, tk lyric display, tk main window, window properties var, tk lyric selection buttons
def select_lyric(song_properties, lyric_display, title, window, window_properties,
                 button_use_previous, button_use_next):
    # create pop up window
    lyric_window = tk.Toplevel(window)
    lyric_window.title('Available Lyrics')
    photo2 = tk.PhotoImage(file=r'static\spotify.png')
    lyric_window.iconphoto(False, photo2)
    lyric_window.attributes('-topmost', True)

    # create selection list (listbox) with scroll bars
    scrollx = tk.Scrollbar(lyric_window, orient=tk.HORIZONTAL)
    scrolly = tk.Scrollbar(lyric_window, orient=tk.VERTICAL)
    lyric_choice = tk.Listbox(lyric_window, width=40, height=5, font=(None, 20),
                              selectmode=tk.SINGLE, xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
    scrollx.config(command=lyric_choice.xview)
    scrolly.config(command=lyric_choice.yview)

    # variable to determine whether the first research result should be included in choice
    # if cached file is in result, exclude first result by changing var to 0
    insert_first = 1
    if song_properties.search_result[0][2].find('Cache File') == -1:
        insert_first = 0

    # add selections into listbox
    for i, result in enumerate(song_properties.search_result[insert_first:]):
        lyric_choice.insert(i, result[0] + ' ' + result[2])
    lyric_choice.grid(row=0, column=0)
    scrollx.grid(row=1, columnspan=2, sticky='EW')
    scrolly.grid(row=0, column=1, sticky='NS')
    # bind double click action to helper function above
    lyric_choice.bind('<Double-1>',
                      lambda event: select_lyric_helper(event, lyric_choice, song_properties, lyric_display, title,
                                                        window_properties, button_use_previous, button_use_next,
                                                        insert_first))
    # add weight to allow scrollbars to stretch across the entire window
    lyric_choice.grid_columnconfigure(1, weight=1)
    lyric_choice.grid_rowconfigure(1, weight=1)

    lyric_window.wait_window()  # main loop


# function to change lyric offset
# parameters: adj (int), song properties
def lyric_offset(adj, song_properties, title):
    song_properties.lyric_offset += adj

    # update window title
    title.title(('歌曲: ' + song_properties.song['name'] + "  " + '歌词信息: ' +
                 song_properties.search_result[song_properties.nlyric][0] + " " +
                 song_properties.search_result[song_properties.nlyric][2] + " " +
                 str(song_properties.lyric_offset) + 'ms'))

    # update text file
    song = song_properties.song
    file_path = 'cache/' + song['name'] + '-' + song['artist'] + '.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('offset:' + str(song_properties.lyric_offset) + '\n')
        f.write(song_properties.lyric_original)


# function to adjust tkinter window transparency
# parameters: adjustment (0.1 or -0.1), tkinter window, window properties, reduce transparency control button,
# increase transparency control button
def adj_transparency(adj, window, win_properties, button_red_trans, button_inc_trans):
    temp = win_properties.transparency + adj
    # disable/enable buttons accordingly. Min transparency is 0.2, otherwise the window is basically invisible
    if temp <= 0.2:
        button_red_trans['state'] = tk.DISABLED
    else:
        button_red_trans['state'] = tk.NORMAL
    if temp >= 1:
        button_inc_trans['state'] = tk.DISABLED
    else:
        button_inc_trans['state'] = tk.NORMAL
    # update transparency
    if 0.2 <= temp <= 1:
        win_properties.transparency = temp
        window.attributes('-alpha', win_properties.transparency)


# function to make entire background transparent
# parameters: tk text display, window properties class, toggle tk button, icon enable, icon disable
def toggle_transparency(lyric_display, win_properties, button, image_enable, image_disable):
    if win_properties.bg_color[0] == 1:
        win_properties.bg_color[0] = 2
        button.config(image=image_disable)
        lyric_display.config(bd=0)  # remove border
    else:
        win_properties.bg_color[0] = 1
        button.config(image=image_enable)
        lyric_display.config(bd=1)  # add border
    # because the transparent color is already stored in window properties, just need to switch which one is read
    lyric_display.config(bg=win_properties.bg_color[win_properties.bg_color[0]])


# function to toggle keep window on top of all other windows
# parameters: tkinter window, window properties, control button, icon enable, icon disable
def adj_on_top(window, win_properties, button_top_most, image_enable, image_disable):
    if win_properties.on_top:
        win_properties.on_top = False
        button_top_most.config(image=image_enable)
    else:
        win_properties.on_top = True
        button_top_most.config(image=image_disable)
    window.attributes('-topmost', win_properties.on_top)


# function to change number of rows of lyric displayed
# parameters: tk text window, window properties, adj (1 or -1), reduce lines button
def adj_nrow(lyric_display, window_properties, adj, button_dec):
    temp = window_properties.nrows + adj
    # disable/enable buttons accordingly. Min row is 1.
    if temp <= 1:
        button_dec['state'] = tk.DISABLED
    else:
        button_dec['state'] = tk.NORMAL
    # update text
    if temp >= 1:
        window_properties.nrows = temp
        lyric_display.config(height=window_properties.nrows)


# function to change font size
# parameters: tk text window, window properties, adj (1 or -1), reduce font size button
def adj_font_size(lyric_display, window_properties, adj, button_dec):
    temp = window_properties.font['size'] + adj
    # disable/enable buttons accordingly. Min row is 1.
    if temp <= 1:
        button_dec['state'] = tk.DISABLED
    else:
        button_dec['state'] = tk.NORMAL
    # update text
    if temp >= 1:
        window_properties.font['size'] = temp
        lyric_display.config(font=window_properties.font)


# function to change font
# takes in tk text display, tk window, and window properties class
def adj_font(lyric_display, window, window_properties):
    temp = tkfontchooser.askfont(window)
    for font_attr in temp:
        window_properties.font[font_attr] = temp[font_attr]
    lyric_display.config(font=window_properties.font)


# function to change color of font
# takes in tk text lyric display window and window properties class
def adj_font_color(lyric_display, window_properties):
    window_properties.font_color = colorchooser.askcolor(title="Choose color")[1]
    lyric_display.tag_configure("past", font=window_properties.font, foreground=window_properties.font_color)


# function to change unlighted color of font
# takes in tk text lyric display window and window properties class
def adj_font_color_bg(lyric_display, window_properties):
    window_properties.font_color_bg = colorchooser.askcolor(title="Choose color")[1]
    lyric_display.config(fg=window_properties.font_color_bg)


# function to change color of background
# takes in tk text lyric display window, tk window, and window properties class
def adj_bg_color(lyric_display, window, window_properties):
    window_properties.bg_color[1] = colorchooser.askcolor(title="Choose color")[1]
    lyric_display.config(bg=window_properties.bg_color[window_properties.bg_color[0]])
    window.config(bg=window_properties.bg_color[window_properties.bg_color[0]])


# function to adjust window width
# parameters: adjustment, tk text display, window properties class, decrease width button
def adj_width(adj, lyric_display, window_properties, button_dec):
    temp = window_properties.width + adj
    if temp <= 22:
        button_dec['state'] = tk.DISABLED
    else:
        button_dec['state'] = tk.NORMAL
    if temp >= 22:
        window_properties.width = temp
        lyric_display.config(width=window_properties.width)


# function to show buttons when mouse enters window
# check event widget master to ensure enter occurred on root window instead of widget
def on_enter(title, frame, root, win_properties, event):
    if event.widget.master is None:
        title.title_bar.grid()
        frame.grid()
        # adjust window position so lyric window doesn't move
        root.geometry("+%s+%s" % (win_properties.x_pos, win_properties.y_pos))


# function to hide buttons when mouse exists window
# check mouse position to ensure outside of window to avoid flickering
def on_exit(title, frame, root, win_properties, event):
    win_width = root.winfo_width()
    win_height = root.winfo_height()
    relative_x_pos = root.winfo_pointerx() - win_properties.x_pos
    relative_y_pos = root.winfo_pointery() - win_properties.y_pos

    if relative_x_pos < 0 or relative_x_pos > win_width or relative_y_pos < 0 or relative_y_pos > win_height:
        title.title_bar.grid_remove()
        frame.grid_remove()
        # adjust window position so lyric window doesn't move
        root.geometry("+%s+%s" % (win_properties.x_pos, win_properties.y_pos + 60))


# helper function to evaluate string to Boolean
def eval_bool(string):
    if string == '1' or string == 'True':
        return True
    else:
        return False
