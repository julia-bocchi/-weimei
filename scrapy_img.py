import requests
from bs4 import BeautifulSoup
import time

# 正确的URL字符串，移除了HTML实体
url = "https://www.umei.cc/e/search/result/?searchid=284"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    "referer": "https://umei.ojbkcdn.com/file/bizhi/20221017/u4tugpgvlxp.jpg"
}


try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
except requests.exceptions.RequestException as e:
    print(f"请求主页时出错：{e}")
    exit()

main_page = BeautifulSoup(response.text, 'html.parser')
imgs = main_page.find_all("div", attrs={"class": "picbox"})

for img in imgs:
    try:
        # 正确的URL字符串，移除了HTML实体
        url2 = "https://www.umei.cc" + img.find("a").get("href")
        child_response = requests.get(url2, headers=headers)
        img_page = BeautifulSoup(child_response.text, 'html.parser')
        img_url = img_page.find("div", attrs={"class": "big-pic"}).find("img").get("src")
        print(img_url)
        header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    "referer": f'{img_url}'
}
        if img_url:
            try:
                img_response = requests.get(img_url, headers=header)
                print(img_response.status_code)  # 打印状态码而不是整个响应对象
                if img_response.status_code == 200:
                    content = img_response.content
                    file_path = f"D:/新建文件夹/python/weimei/{img_url.split('/')[-1]}"
                    with open(file_path, "wb") as f:
                        f.write(content)
                        print(f"图片已保存到：{file_path}")
                        time.sleep(2)  # 每次请求后等待2秒，以避免频繁请求导致服务器拒绝服务
                else:
                    print("图片请求失败，状态码：", img_response.status_code)
            except requests.exceptions.RequestException as e:
                print(f"请求图片时出错：{e}{child_response.status_code}")
        else:
            print("未找到图片URL")
    except requests.exceptions.RequestException as e:
        print(f"请求子页面时出错：{e}{child_response.status_code}")     