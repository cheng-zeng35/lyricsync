import vlc
import pafy
import youtube_dl
from time import sleep

url = 'https://www.youtube.com/watch?v=BzIiTsSnAzo'

# creating pafy object of the video
video = pafy.new(url)

# getting best stream
best = video.getbest()
playurl = best.url
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(playurl)
media.get_mrl()
player.set_media(media)
player.play()

sleep(10)
while player.is_playing():
    sleep(1)