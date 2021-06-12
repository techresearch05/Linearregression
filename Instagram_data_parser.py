import datetime
import glob
import json
import time

import pandas as pd
from tweet_parser.tweet import Tweet

from pathlib import Path

file_path = '/Users/raghava/Dropbox (CBS)/cbs-research/' \
            'research~projects/Lifestyle-Design-Cluster-BigSocial-Data' \
            '/data/instagram.json'

path = Path(file_path)

filename_without_prefix = path.stem

df = pd.DataFrame(columns=['s_no', 'id', 'ig_id', 'comments_count', 'like_count',
                           'media_type', 'media_url', 'permalink', 'timestamp', 'year', 'caption', 'comments_text'])

df = df.set_index('s_no')

index = 1

with open(file_path) as file:
    data = json.load(file)

    for line in data:

        id = line['id']

        ig_id = line['ig_id']

        comments_count = line['comments_count']

        like_count = line['like_count']

        media_type = line['media_type']

        if 'media_url' in line:
            media_url = line['media_url']
        else:
            media_url = ''

        permalink = line['permalink']

        timestamp = line['timestamp']

        dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+0000')

        if 'caption' in line:
            caption = line['caption']
        else:
            caption = ''

        comments_text = ''

        if not 'comments' in line:
            comments_text = ''
        else:
            comments_list = line['comments']
            for comment in comments_list['data']:
                comments_text = comments_text + comment['text'] + '$'

        #print(comments_text)

        df.loc[index] = [id, ig_id, comments_count, like_count,
                           media_type, media_url, permalink, timestamp, dt.year, caption, comments_text]

        index += 1

        print(index)


df = df.replace('\n', ' ', regex=True)

df = df.replace('\r', ' ', regex=True)

df = df.replace(';', ' ', regex=True)


df.to_csv(str(path.parent) + '/' + filename_without_prefix + '_text.csv', sep=';')

print('Done exporting excel to csv')
