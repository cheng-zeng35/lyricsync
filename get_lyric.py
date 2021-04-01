# functions in this library are used to extract lyric from kugeci.com

import re  # regit used to remove unnecessary spaces in lyric

# libraries used for web scraping
import requests
from bs4 import BeautifulSoup

# used for cache management
from os import listdir


# function to remove illegal characters from file name, if they exist
def clean_file_name(file_name):
    illegal_char = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']
    for char in illegal_char:
        file_name = file_name.replace(char, '')
    return file_name


# check if song (dictionary) already exists in cache, if so, return lyric
def read_cache(song):
    file_name = clean_file_name(song['name'] + '-' + song['artist'] + '.txt')
    offset = 0
    lyric = ''
    # for each file in cache
    files = listdir('cache/')
    for file in files:
        # if name matches
        if file == file_name:
            file_path = 'cache/' + file_name
            # read file, first line is the offset
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i == 0:
                        offset = int(line.split(':')[1])
                    else:
                        lyric += line
    return lyric, offset


# based on song name, search for lyric on kugeci.com, return a list of results [[song, link, singer]..]
def get_search_result(song):
    name = song['name']
    # remove irrelevant information from song name
    # Spotify uses - and ( to add extra information behind song names
    illegal_token = ['-', ' -', '(', ' (']
    for token in illegal_token:
        if name.find(token) != -1:
            name = name[0:name.find(token)]

    url = 'https://www.kugeci.com/search?q=' + name  # define URL
    user_agent = {'User-agent': 'Mozilla/5.0'}  # general tag to say browser is Firefox compatible
    response = requests.get(url, headers=user_agent)  # create a connection with the website
    soup = BeautifulSoup(response.text, 'html.parser')  # parse the website HTML into Beautiful Soup
    songs_matched = soup.find('table', id='tablesort')  # find the table on the page listing search results

    lyric, offset = read_cache(song)  # check cache

    # if no table found and song not in cache, return dummy result
    if songs_matched is None:
        if lyric == '':
            return [['N/A', 'N/A', '']]
        else:
            return [[song['name'], [lyric, offset], song['artist'] + ' (Cache File)']]
    else:
        # extract results from results table
        songs_matched = songs_matched.find_all('td')
        # based on the website, every 2nd and 3rd result are the song and singer, if we read in batches of 5
        count = 1
        search_result = []
        for songs in songs_matched:
            # append song name and link to lyrics
            # use TypeError to pass exceptions when reading empty table rows
            if count % 5 == 2:
                try:
                    search_result.append([re.sub(' +', ' ', songs.text.strip()), songs.find('a')['href']])
                except TypeError:
                    pass
            # add singer
            # use TypeError to pass exceptions when reading empty table rows
            elif count % 5 == 3:
                try:
                    search_result[-1].append(re.sub(' +', ' ', songs.text.strip()))
                except TypeError:
                    pass
            count += 1
        # insert cache lyric if applicable
        if lyric != '':
            search_result.insert(0, [song['name'], [lyric, offset], song['artist'] + ' (Cache File)'])
        return search_result


# based on search results [[song, link, singer]..], return the nth (num) result as lyric
# song parameter used to store and read cache
# also return offset as applicable
def get_lyric(search_result, num, song):
    # if search_result is dummy result, return no lyrics found message as lyric to display
    if search_result == [['N/A', 'N/A', '']]:
        lyric = '[99:99.99]No lyrics found.'
        offset = 0
    # if reading cache, return cached result
    elif type(search_result[num][1]) is list:
        lyric = search_result[num][1][0]
        offset = search_result[num][1][1]
    else:
        url = search_result[num][1]  # extract relevant url
        user_agent = {'User-agent': 'Mozilla/5.0'}  # general tag to say browser is Firefox compatible
        response = requests.get(url, headers=user_agent)  # create a connection with the website
        soup = BeautifulSoup(response.text, 'html.parser')  # parse the website HTML into Beautiful Soup
        lyric = soup.find(id='lyricsContainer').text  # find container for lyric
        offset = 0
    # save lyric to cache
    file_path = 'cache/' + clean_file_name(song['name'] + '-' + song['artist'] + '.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('offset:' + str(offset) + '\n')
        f.write(lyric)
    return lyric, offset
