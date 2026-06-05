import yt_dlp
from feedgen.feed import FeedGenerator
import os

# 貼上你條 YouTube Playlist 網址
YOUTUBE_URL = 'https://youtube.com/playlist?list=PLJBAW4UyTo7624szsxgPW154jfBq0nHc4'

ydl_opts = {
    'extract_flat': False,
    'skip_download': True, # 唔使下載實體檔案，純粹爬取音訊流
}

fg = FeedGenerator()
# 這裡填寫你的 Podcast 頻道基本資料
fg.id('tesla-podcast-custom-id')
fg.title('我的 Tesla 專屬 YouTube 播客')
fg.author({'name': 'Queenie'})
fg.link(href='https://github.com', rel='alternate')
fg.description('自動更新的 YouTube 播放清單純音訊 Feed')

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        info = ydl.extract_info(YOUTUBE_URL, download=False)
        # 拿取最新 50 集
        entries = info.get('entries', [])[:50]
        
        for entry in entries:
            if not entry:
                continue
            
            # 從 YouTube 格式中撈出純音訊 (Audio-only) 嘅直接串流網址
            formats = entry.get('formats', [])
            audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
            
            if audio_formats:
                # 選擇音質最好嘅串流網址
                best_audio_url = audio_formats[-1]['url']
                
                fe = fg.add_entry()
                fe.id(entry['id'])
                fe.title(entry['title'])
                fe.description(entry.get('description', '無詳細說明'))
                # 偽裝成標準 M4A 音訊，讓 Apple Podcasts 乖乖開口讀取
                fe.enclosure(best_audio_url, '0', 'audio/mp4')
                
    except Exception as e:
        print(f"Error extracting playlist: {e}")

# 產出標準的 Podcast XML 檔案
fg.rss_file('podcast.xml')
print("Successfully generated podcast.xml")
