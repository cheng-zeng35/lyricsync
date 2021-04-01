# Spotify Lyric Display

Spotify Lyric Display is a small tool that can be run alongside Spotify to display real-time lyric for Chinese Songs 
(something that is currently not supported natively by Spotify).  

Lyrics are obtained from [kugeci.com](kugeci.com).

## Installation and Setup

### Direct Download (Method 1)
Download <strong>Spotify Lyric.zip</strong>, unzip to a folder at your discretion, and run the 
<strong>main.exe</strong> file within the folder.  

### Direct Download (Method 2)
Download the source file and navigate to <strong>dist/main</strong>. Find the <strong>main.exe</strong> file and run.

### Run from Source Code
Download the source file and run <strong>main.py</strong> from <strong>root directory</strong>.

### Logging into Spotify
On first time use, the tool will ask you for three pieces of information:
<ul>
<li>Spotify API Client ID<sup>1</sup></li>
<li>Spotify API Client Secret<sup>1</sup></li>
<li>Spotify Username<sup>2</sup></li>
</ul>
<sub>1. Spotify API information can be obtained at developer.spotify.com/dashboard. 
Log in with your Spotify account and request free API access. You can then create a free application within the 
Dashboard tab and acquire Client ID and Client Secret. Please use separate API accounts for each user because Spotify 
imposes rate limits on these free accounts.</sub><br>
<sub>2. Spotify Username can be obtained at spotify.com/us/account/overview.</sub><br><br>
Once these information are correctly entered, you will be redirected to the Spotify website to log into Spotify.

## Usage

### Title Bar
The Title Bar will display three pieces of information:
<ul>
<li>Current song</li>
<li>Lyric used</li>
<li>Lyric time offset compared to original lrc file</li>
</ul>  
If no song is being played or there is a Spotify API server error, the Title Bar will display "Nothing played right now 
or Spotify server error." This issue should correct itself once music starts or once the Spotify API server is back on.

### Button Functions
The function buttons (see screenshots below), from left to right, serves the following purposes:
<ol>
<li>Use previous lyric: switch to the previous lyric result found on kugeci.com.</li>
<li>Use next lyric: switch to the next lyric result found on kugeci.com.</li>
<li>Select lyric: select from a list of lyric results.</li>
<li>Adjust lyric sync (-0.5s): adjust lyrics back by 0.5 seconds.</li>
<li>Adjust lyric sync (+0.5s): adjust lyrics forward by 0.5 seconds.</li>
<li>Shrink font: decrease font size by 1.</li>
<li>Enlarge font: increase font size by 1.</li>
<li>Change font: update font with a font selector.</li>
<li>Change font color (foreground): change the color of lyrics highlighted.</li>
<li>Change font color (background): change the color of lyrics not highlighted.</li>
<li>Reduce row: decrease the rows of lyrics shown by 1.</li>
<li>Increase row: increase the rows of lyrics shown by 1.</li>
<li>Reduce width: decrease the width of window by 1 letter.</li>
<li>Increase width: increase the width of the window by 1 letter.</li>
<li>Increase transparency: make the window more transparent.</li>
<li>Reduce transparency: make the window less transparent.</li>
<li>Full transparency toggle: make the lyric window background fully transparent.</li>
<li>Stay on top toggle: make the lyric window stay on top of other windows.</li>
</ol>

### Caching
After initial run, the tool will create a cache folder within its root directory in order to store previously entered 
Spotify information (<strong>credentials.txt</strong>), previous made settings (<strong>user_setting.txt</strong>), and 
previously downloaded lyrics. You can also directly change your Spotify information and settings in these files.

### Other
The Title Bar and function buttons will appear/disappear based on mouse hover.

## Planning Improvements
<ul>
<li>Add support for genius.com</li>
<li>Add song controls for Spotify Premium Users (Spotify API does not seem to support song controls for free users.)</li>
</ul>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Any suggestion on functionality and/or code improvement is welcomed!

## Screenshots
With background, Title Bar, and function buttons:
<img src="https://github.com/cheng-zeng35/lyricsync/blob/608c5a09a6f411e4987b1ed681b9a8312a154c18/static/screenshot1.png" width="800"><br><br>
Fully transparent:
<img src="https://github.com/cheng-zeng35/lyricsync/blob/608c5a09a6f411e4987b1ed681b9a8312a154c18/static/screenshot2.png" width="800">

## License
[MIT](https://choosealicense.com/licenses/mit/)