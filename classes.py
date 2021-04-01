# this file is to store all custom classes
import tkinter as tk


# class to store tkinter window properties
# font: tk font dictionary {family, size, weight, slant, underline, overstrike}
# font color: string
# nrows: the number of rows of lyric displayed (integer greater than 0)
# width: window width (int greater than 0)
# transparency: window transparency level (0.2 to 1)
# bg_color: [transparency: 1 or 2, background color (string), transparent color (string)]
# bd: border width in integers
# on_top: whether window is kept on top of all other windows (Boolean)
# x_pos, y_pos: window's x and y coordinates in pixels
class WindowProperties:
    def __init__(self, font, font_color, font_color_bg, nrows, width, transparency, bg_color, bd, on_top, x_pos, y_pos):
        self.font = font
        self.font_color = font_color
        self.font_color_bg = font_color_bg
        self.nrows = nrows
        self.width = width
        self.transparency = transparency
        self.bg_color = bg_color
        self.bd = bd
        self.on_top = on_top
        self.x_pos = x_pos
        self.y_pos = y_pos

    def save(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self.font['family']) + '\n')
            f.write(str(self.font['size']) + '\n')
            f.write(str(self.font['weight']) + '\n')
            f.write(str(self.font['slant']) + '\n')
            f.write(str(self.font['underline']) + '\n')
            f.write(str(self.font['overstrike']) + '\n')
            f.write(str(self.font_color) + '\n')
            f.write(str(self.font_color_bg) + '\n')
            f.write(str(self.nrows) + '\n')
            f.write(str(self.width) + '\n')
            f.write(str(self.transparency) + '\n')
            f.write(str(self.bg_color) + '\n')
            f.write(str(self.bd) + '\n')
            f.write(str(self.on_top) + '\n')
            f.write(str(self.x_pos) + '\n')
            f.write(str(self.y_pos) + '\n')


# helper function for title bar to save setting and then close window
def close_root(root, win_properties):
    win_properties.save('cache/user_setting.txt')
    root.destroy()


# custom title bar class
class TitleBar:
    # initialization takes x starting position, y starting position, and window
    def __init__(self, last_click_x, last_click_y, root, win_properties):
        # initialize title_bar, close button, and label
        self.title_bar = tk.Frame(root, bg='#2e2e2e', relief='groove', bd=0, highlightthickness=0)
        self.close_button = tk.Button(self.title_bar, text='×', bg="#2e2e2e", padx=5, activebackground='red',
                                   bd=0, font="bold", fg='white', command=lambda: close_root(root, win_properties))
        self.close_button.grid(row=0, column=1, sticky='E')
        self.title_text = tk.Label(self.title_bar, text='', bg='#2e2e2e', padx=5, fg='white')
        self.title_text.grid(row=0, column=0, sticky='W')
        self.title_bar.grid_columnconfigure(0, weight=1)
        # bind closing and drag
        self.last_click_x = last_click_x
        self.last_click_y = last_click_y
        self.title_bar.bind('<Button-1>', self.save_last_click)
        self.title_bar.bind('<B1-Motion>', lambda event: self.drag(event, root, win_properties))
        self.title_text.bind('<Button-1>', self.save_last_click)
        self.title_text.bind('<B1-Motion>', lambda event: self.drag(event, root, win_properties))

    # update title function
    def title(self, title_text):
        self.title_text.config(text=title_text)

    # update last position to help with drag function
    def save_last_click(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    # drag function
    def drag(self, event, root, win_properties):
        x, y = event.x - self.last_click_x + root.winfo_x(), event.y - self.last_click_y + root.winfo_y()
        root.geometry("+%s+%s" % (x, y))
        win_properties.x_pos = x
        win_properties.y_pos = y


# class to store song information
# song: Spotify current song data (see spotify_func.py for format)
# lyric: current lyric used (lrc file in string format)
# search_result: list of lyric results scraped from website ([[song, link, singer]..])
# lyric_offset: number of ms to offset lyrics by when displayed (integer)
# nlyric: the lyric currently being used from search_result (integer between 0 and len(search_result) - 1)
# dynamic lyric position: to track which letter should be highlighted a different color, integer
# dynamic lyric duration: to track how frequent the lyric update function should be refreshed, in ms
# lyric_original: original lyric (not formatted) to be saved to cache
class SongProperties:
    def __init__(self, songx, lyric_f, lyric_o, search_resultx, lyric_offsetx, nlyricx):
        self.song = songx
        self.lyric = lyric_f
        self.search_result = search_resultx
        self.lyric_offset = lyric_offsetx
        self.nlyric = nlyricx
        self.dynamic_lyric_pos = 0
        self.dynamic_lyric_duration = 100
        self.lyric_original = lyric_o
