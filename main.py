import yt_dlp
import os

videos = []
con = []
config = {}

with open('videos.txt', 'r') as f:
    videos = f.read().splitlines()

with open('config.txt', 'r') as f:
    con = f.read().splitlines()
    for i in con:
        config[i.split('=')[0]] = i.split('=')[1]

class YTNAMES(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        file_extension = info['filepath'].split('.')[1]
        os.rename(info['filepath'], "{}.{}".format(info['title'], file_extension))
        self.to_screen('File "{}.{}" has been downloaded'.format(info['title'], file_extension))
        return [], info

class Episodes(yt_dlp.postprocessor.PostProcessor):
    folge = int(config.get('START'))
    key = config.get('KEY')
    def run(self, info):
        file_extension = info['filepath'].split('.')[1]
        print(self.folge)
        file_name = '{} {}.{}'.format(self.key, self.folge, file_extension)
        os.rename(info['filepath'], file_name)
        self.folge += 1
        self.to_screen('File "{} {}.{}" has been downloaded'.format(self.key, self.folge, file_extension))
        return [], info

with yt_dlp.YoutubeDL() as ydl:
    if config.get("YTNAMES") == "true":
        ydl.add_post_processor(YTNAMES())
    elif config.get("EPISODES"):
        ydl.add_post_processor(Episodes())
    ydl.download(videos)