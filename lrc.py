# functions in this library are used to format and extract lyrics from lrc strings

# convert lrc timestamp (min:sec.hsec) into ms
def convert_to_ms(time_stamp):
    time_stamp = time_stamp.split(':')
    minute = int(time_stamp[0])
    time_stamp = time_stamp[1].split('.')
    second = int(time_stamp[0])
    hsecond = int(time_stamp[1][:2])
    return minute * 60 * 1000 + second * 1000 + hsecond * 10


# split aggregate lrc string into a list of sentences [[timestamp, lyric]...]
def format_lyric(lyric):
    lyric_list = lyric.strip().splitlines()
    lyric_list = list(filter(lambda x: x != '', lyric_list))  # remove empty lines if necessary
    for i, sentence in enumerate(lyric_list):
        lyric_list[i] = sentence.split(']')
        lyric_list[i][0] = convert_to_ms(lyric_list[i][0][1:])
    return lyric_list


# based on current play progress (time_stamp), extract x (nsentence) sentences from lyric data (lyric_list)
# lyric data should be in the format of [[timestamp, lyric]...]
# offset play progress by the offset (offset) input
def get_sentence(lyric_list, time_stamp, nsentence, offset):
    result = ''
    count = 1
    time_to_refresh = -1  # this is when the next sentence comes on, calculated but not used in this version
    # check each sentence to see if they come after time_stamp until nsentence are found
    for sentence in lyric_list:
        if count >= nsentence:
            break
        elif sentence[0] >= time_stamp + offset:
            if count == 1:
                time_to_refresh = sentence[0]
            result += sentence[1] + '\n'
            count += 1
        else:
            result = sentence[1] + '\n'
    result = result[:-1]
    return result, time_to_refresh
