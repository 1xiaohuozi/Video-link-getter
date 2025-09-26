from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def 抓取Bilibili视频信息():
    bilibili_url = bilibili_url_entry.get()

    driver = webdriver.Chrome()
    driver.get(bilibili_url)
    time.sleep(10)
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    video_list = soup.select('#submit-video-list > ul.clearfix.cube-list > li')

    titles = []
    video_links = []

    for video in video_list:
        title = video.find('a', class_='title').text.strip()
        link = video.find('a', class_='title')['href']
        titles.append(title)
        video_links.append(f'https:{link}')

    data = {
        '标题': titles,
        '视频链接': video_links
    }

    df = pd.DataFrame(data)
    df.to_csv('bilibili_videos_info.csv', index=False)
    messagebox.showinfo("完成", "Bilibili视频信息抓取完成。数据已保存到bilibili_videos_info.csv")

def 抓取抖音视频信息():
    douyin_url = douyin_url_entry.get()

    driver = webdriver.Chrome()
    driver.get(douyin_url)
    messagebox.showinfo("提示", "请手动验证成功进入抖音主页后点击确定继续...")
    time.sleep(15)
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    video_list = soup.select('div.XjDZcrDT div.LPv6KBIL ul li')

    titles = []
    video_links = []

    for video in video_list:
        link_tag = video.find('a', class_='kpteEEN8 QbxvFWkS WgUmIxXx')
        if link_tag:
            link = link_tag['href']
            video_link = f'https://www.douyin.com{link}'
            video_links.append(video_link)

            title_tag = video.find('p', class_='Ja95nb2Z')
            if title_tag:
                title = title_tag.text.strip()
                titles.append(title)
            else:
                titles.append('')

    data = {
        '标题': titles,
        '视频链接': video_links
    }

    df = pd.DataFrame(data)
    df.to_csv('douyin_videos_info.csv', index=False)
    messagebox.showinfo("完成", "抖音视频信息抓取完成。数据已保存到douyin_videos_info.csv")


def 提取快手链接标识码(link):
    client_cache_key = None
    key_start = link.find('clientCacheKey=')

    if key_start != -1:
        key_start += len('clientCacheKey=')
        key_end = link.find('.jpg', key_start)
        if key_end != -1:
            client_cache_key = link[key_start:key_end]
            # 如果存在，从clientCacheKey中移除"_ccc"
            client_cache_key = client_cache_key.replace('_ccc', '')

    return client_cache_key


def 提取快手视频信息():
    driver = webdriver.Chrome()
    driver.get('https://cp.kuaishou.com/')
    messagebox.showinfo("提示", "请手动登录快手账号后点击确定继续...")

    time.sleep(15)
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    video_list = soup.select(
        '#app > div.complete > div.container > main > div > div > div:nth-of-type(1) > div > div.auto-load-list > div')

    titles = []
    publish_times = []
    video_links = []

    for video in video_list:
        video_title = video.select_one('.video-item__detail__row__title').get_text()

        video_link = video.select_one('.video-item__cover__img')['src']
        client_cache_key = 提取快手链接标识码(video_link)

        if client_cache_key:
            video_link = f"https://www.kuaishou.com/short-video/{client_cache_key}"

        publish_time = video.select_one('.video-item__detail__row__date').get_text()

        titles.append(video_title)
        publish_times.append(publish_time)
        video_links.append(video_link)

    data = {
        '标题': titles,
        '发布时间': publish_times,
        '视频链接': video_links
    }

    df = pd.DataFrame(data)
    df.to_csv('kuaishou_videos_info.csv', index=False)
    messagebox.showinfo("完成", "快手视频信息抓取完成。数据已保存到kuaishou_videos_info.csv")


# ...（之前的所有代码保持不变）

# 创建GUI界面
root = tk.Tk()
root.title("视频信息抓取")

bilibili_url_label = tk.Label(root, text="请输入Bilibili作者主页链接：")
bilibili_url_label.pack()

bilibili_url_entry = tk.Entry(root, width=50)
bilibili_url_entry.pack()

douyin_url_label = tk.Label(root, text="请输入抖音作者主页链接：")
douyin_url_label.pack()

douyin_url_entry = tk.Entry(root, width=50)
douyin_url_entry.pack()

bilibili_scrape_button = tk.Button(root, text="抓取Bilibili视频信息", command=抓取Bilibili视频信息)
bilibili_scrape_button.pack()

douyin_scrape_button = tk.Button(root, text="抓取抖音视频信息", command=抓取抖音视频信息)
douyin_scrape_button.pack()

kuaishou_scrape_button = tk.Button(root, text="抓取快手视频信息", command=提取快手视频信息)
kuaishou_scrape_button.pack()

root.mainloop()

