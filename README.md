# Introduction
I've done many scrapers and automation tools so far. There are the most interesting and useful (all these projects are old, so the code may be dirty):
+ Steam/mail account registrator
+ Puzzle game solver
+ Shkolkovo video/files downloader
+ Avito products listing with sorting by seller's rating, registration date.
+ Lecta books downloader

I use Selenium webdriver, BeautifulSoup and requests modules in every project.

## Steam/mail registrator
Steam account and mail box creation using [SMS service](https://5sim.net/) API for getting verification codes. Automatically adding a Steam Desktop Authentication. User have to solve captcha.

## Puzzle game solver
First plan was to detect numbers in grid by using Tesseract Python, but it wasn't good at recognising digits in a low resolution image, so I decided to load just a color pallete, because puzzles made from it are easy to distinguish. The solver was written for abusing a GC.skins app that was giving big amount of coins for completing this game. With paid subscription I was able to load my own "puzzles". I used Nox player to run the game on PC.

## Shkolkovo downloader
The program is able to download all files from bought courses and capture lectures with OBS.
### Capture instructions
+ Install [win-audio-capture extension for OBS](https://obsproject.com/forum/resources/win-capture-audio.1338/).
+ Install [Sandboxie](https://sandboxie-plus.com/downloads/).
+ Run OBS in portable mode.
+ Run [capture.py](Shkolkovo%20downloader/capture.py) script.
+ Set window and audio capture in OBS. <br>
### Files downloading
+ Make sure you have only one profile in chrome and enter Shkolkovo account.
+ Start [drive.py](Shkolkovo%20downloader/drive.py) script.

**Use only for personal education. Not for sharing!**
