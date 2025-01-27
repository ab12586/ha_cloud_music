from bs4 import BeautifulSoup
import requests, re
from .models.music_info import MusicInfo, MusicSource

def get_music(keyword):
  # https://www.gequbao.com
  api = 'https://www.fangpi.net'
  session = requests.Session()
  try:
    response = session.get(f'{api}/s/{keyword}')
    soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
    items = soup.select('.card-text .row')
    if len(items) > 1:
      row = items[1]
      # print(td)
      song = row.select('.col-5 a')[0].get_text().strip()
      singer = row.select('.col-4')[0].get_text().strip()

      a = row.select('.col-3 a')
      href = a[0].attrs['href']
      
      # print(href)
      response = session.get(f'{api}{href}')
      html = response.text

      pattren = re.compile(r'https://[^\s]+.mp3')
      url_lst = pattren.findall(html)
      # print(url_lst)
      if len(url_lst) > 0:
        soup = BeautifulSoup(html, 'lxml')
        cover = soup.select('head meta[property="og:image"]')
        #print(cover)
        pic = 'https://p2.music.126.net/tGHU62DTszbFQ37W9qPHcg==/2002210674180197.jpg'
        # 封面
        if len(cover) > 0:
            pic = cover[0].attrs['content']

        songId = href.replace('/', '')
        album = ''
        audio_url = url_lst[0]
        return MusicInfo(songId, song, singer, album, 0, audio_url, pic, MusicSource.URL.value)
  except Exception as ex:
    print(ex)