from fake_useragent import UserAgent
import requests
import time

ua = UserAgent()


def downloader(url, path):
    start = time.time()  # 开始时间
    size = 0
    headers = {
        'User-Agent': ua.random
    }
    response = requests.get(url, headers=headers, stream=True)  # stream 属性必须带上
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))  # 换算单位
        with open(path, 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)  # 已下载的文件大小
                print('\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size *
                                                                                             100)), end=" ")
    end = time.time()  # 结束时间
    print('\n' + '视频下载完成！用时%.2f秒' % (end - start))


def The_URL(page):
    URL = 'http://api.vc.bilibili.com/board/v1/ranking/top?page_size=10&next_offset={}&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platform=pc'.format(
        page)
    headers = {
        'User-Agent': ua.random
    }
    sponse = requests.get(URL, headers=headers).json()
    item = sponse.get('data').get('items')
    for i in item:
        ite = i.get('item')
        # 视频标题
        Video_name = ite.get('description')

        # 发布日期
        Release_time = ite.get('upload_time_text')

        # 视频下载地址
        Video_download_link = ite.get('video_playurl')

        # 视频作者
        The_name = i.get('user').get('name')

        try:
            print('当前下载的是:%s' % Video_name)
            downloader(Video_download_link, path='%s.mp4' % Video_name)
        except Exception as e:
            print(e.args)


for i in range(0, 100):
    i = i * 10 + 1
    The_URL(i)