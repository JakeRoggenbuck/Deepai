from main import Deep
import config
from os import listdir
from os.path import isfile, join


PATH = '/home/jake/.config/wallpaper/'
SAVEPATH = 'images/'

onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
for file_ in onlyfiles:
    files = file_.split('.')[-1].upper()
    if files == 'PNG' or files == 'JPG':
        print(f"Processing {file_}")
        deep = Deep(config.KEY, config.URL, PATH + file_, SAVEPATH)
        deep.download()
