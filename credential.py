# This library is to check user credentials and prompt them to enter credentials

import tkinter as tk
import tkinter.ttk as ttk
import spotify_func
import os


# function used to check and update credentials once user fills them in
# parameters: credentials dictionary, credential file path, tk window, tk widget user entry fields,
# authentication failure notice label
def valid_credentials(credentials, credential_file, credential_window, client_id, client_secret, username, fail_label):
    # update credentials
    credentials['SPOTIPY_CLIENT_ID'] = client_id.get()
    credentials['SPOTIPY_CLIENT_SECRET'] = client_secret.get()
    credentials['USERNAME'] = username.get()

    # check credentials
    sp = spotify_func.get_spotify_token(credentials)

    # if failed, update failure label
    if not sp:
        fail_label.config(text='Authentication failed')

    # otherwise, update txt file and exit window, note credentials dictionary is already updated
    else:
        output = []
        for i in credentials:
            output.append(i + '=' + credentials[i] + '\n')
        # file not found error caught elsewhere
        with open(credential_file, 'w') as f:
            f.writelines(output)
        credential_window.destroy()


# function to check credentials and prompt user to enter credentials if don't exist
# parameters: credential file path, failure warning (default should be ''), main tk window
def check_credentials(credential_file, retry_string, window):
    # set up credential tracker
    credentials = {}

    # read credentials
    try:
        with open(credential_file, 'r') as f:
            for line in f:
                line = line.split('=')
                credentials[line[0]] = line[1].replace('\n', '')
    except FileNotFoundError:
        if not os.path.exists('cache'):
            os.makedirs('cache')
        # create file if not exist
        f = open(credential_file, 'x')
        f.close()
        # set up dummy credentials
        credentials['SPOTIPY_CLIENT_ID'] = ''
        credentials['SPOTIPY_CLIENT_SECRET'] = ''
        credentials['USERNAME'] = ''

    # check if credentials are blank
    credentials_entered = True
    for i in credentials:
        if credentials[i] in ['', '\n']:
            credentials_entered = False

    # if blank, prompt for new credentials
    if not credentials_entered:

        # create tk window
        credentials_window = tk.Toplevel(window)
        credentials_window.title('Credentials')
        photo1 = tk.PhotoImage(file=r'static\spotify.png')
        credentials_window.iconphoto(False, photo1)
        credentials_window.attributes('-topmost', True)

        # create relevant labels and fields
        description_label = tk.Label(credentials_window, width=35, text='Please Enter Your Credentials:', anchor='w')
        client_id_label = tk.Label(credentials_window, width=18, text='Spotipy Client ID', anchor='e')
        client_id_field = tk.Entry(credentials_window, width=20)
        client_secret_label = tk.Label(credentials_window, width=18, text='Spotipy Client Secret', anchor='e')
        client_secret_field = tk.Entry(credentials_window, width=20)
        username_label = tk.Label(credentials_window, width=18, text='Spotify Username', anchor='e')
        username_field = tk.Entry(credentials_window, width=20)
        fail_label = tk.Label(credentials_window, width=18, fg='red', textvariable=retry_string, anchor='e')
        button_submit = ttk.Button(credentials_window, text='Submit', width=10,
                                   command=lambda: valid_credentials(credentials, credential_file, credentials_window,
                                                                     client_id_field, client_secret_field,
                                                                     username_field, fail_label))
        description_label.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        client_id_label.grid(row=1, column=0)
        client_id_field.grid(row=1, column=1, padx=5)
        client_secret_label.grid(row=2, column=0)
        client_secret_field.grid(row=2, column=1, padx=5)
        username_label.grid(row=3, column=0)
        username_field.grid(row=3, column=1, padx=5)
        fail_label.grid(row=4, column=0)
        button_submit.grid(row=4, column=1, pady=5)
        credentials_window.wait_window()  # tkinter main loop

    return spotify_func.get_spotify_token(credentials)  # return Spotify token
