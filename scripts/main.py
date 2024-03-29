import gradio as gr

from modules import script_callbacks
import modules.shared as shared

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import os
import time
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

status = 0

def on_ui_tabs():
    with gr.Blocks() as dfp_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):
                with gr.Column(variant='panel'):
                    download_dir = gr.Textbox(label="Download irectory", **shared.hide_dirs, placeholder="Download directory", value="downloads")
                    max_downloads = gr.Textbox(label="Max donwloads", **shared.hide_dirs, placeholder="Number of downloads", value="200", interactive=True)
                with gr.Column(variant='panel'):
                    find_tags0 = gr.Textbox(label="Tag1", placeholder="Search tag1")
                    find_tags1 = gr.Textbox(label="Tag2", placeholder="Search tag2")
                with gr.Column(variant='panel'):
                    extra_tag_option = gr.Radio(choices=["AND", "OR"], value="AND", label="Search option")
                    find_extra_tags0 = gr.Textbox(label="Extra tag1", placeholder="(Optional) Search extra tag1")
                    find_extra_tags1 = gr.Textbox(label="Exara tag2", placeholder="(Optional) Search extra tag2")
                    find_extra_tags2 = gr.Textbox(label="Exara tag3", placeholder="(Optional) Search extra tag3")
                with gr.Column(variant='panel'):
                    not_tag_option = gr.Radio(choices=["AND", "OR"], value="AND", label="Not search option")
                    not_find_tag0 = gr.Textbox(label="Not search tag1", placeholder="(Optional) Search extra tag1")
                    not_find_tag1 = gr.Textbox(label="Not search tag2", placeholder="(Optional) Search extra tag2")
                    not_find_tag2 = gr.Textbox(label="Not search tag3", placeholder="(Optional) Search extra tag3")
                with gr.Column(variant='panel'):
                    score_filter = gr.Textbox(label="Score filter", **shared.hide_dirs, placeholder="(Optional) Score filter")
            with gr.Column(variant='panel'):
                status = gr.Textbox(label="", interactive=False, show_progress=True)
                
        
        dir_run = gr.Button(elem_id="dir_run", label="Generate", variant='primary')
        
        dir_run.click(
            fn=main,
            inputs=[download_dir, max_downloads, find_tags0, find_tags1, find_extra_tags0, find_extra_tags1, find_extra_tags2, extra_tag_option,
                    not_find_tag0, not_find_tag1, not_find_tag2, not_tag_option, score_filter],
            outputs=[status]
        )

      
    return (dfp_interface, "Dataset From Danbooru", "dfp_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)


# ダウンロード(画像URL, 保存先パス)
def download_img(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    #pngDLできない場合、jpgでDL
    except urllib.error.URLError as e:
        url = url.replace('.png', '.jpg')
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)

def main(download_dir, max_downloads, find_tags0, find_tags1,
         find_extra_tags0, find_extra_tags1, find_extra_tags2, extra_tag_option,
         not_find_tag0, not_find_tag1, not_find_tag2, not_tag_option,
         score_filter):
    
    extra_tags = 1
    
    
    if (find_extra_tags0 == "" and
        find_extra_tags1 == "" and
        find_extra_tags2 == ""):
        extra_tags = 0
    
    if not score_filter:
        score_filter=-100
    
    #print(max_downloads)
    
    option = Options()                          # オプションを用意
    #option.add_argument('--headless')           # ヘッドレスモードの設定を付与

    #クロームの立ち上げ
    driver=webdriver.Chrome("extensions/Dataset_From_Danbooru/driver/chromedriver.exe", chrome_options=option)
    #driver=webdriver.Chrome("extensions/Dataset_From_Danbooru/driver/chromedriver.exe")

    #ページ接続
    driver.get('https://danbooru.donmai.us/')

    #10秒終了を待つ(認証対策)
    time.sleep(10)
    
    # Webページを取得して解析する
    load_url = "https://danbooru.donmai.us/posts?page=1&tags="  + find_tags0 + "+" + find_tags1
    print(load_url)
    
    # 最終ページNoを取得
    driver.get(load_url)
    time.sleep(3)
    last_pages = driver.find_elements(By.CSS_SELECTOR, ".paginator-page.desktop-only")
    last_pageNo = last_pages[-1].get_attribute("text")

    #html = requests.get(load_url)
    time.sleep(3)
    #soup = BeautifulSoup(html.content, "html.parser")
    
    #source = driver.page_source
    #print(source)

    img_urls = []
    limited = 0

    for num in range(1, int(last_pageNo)+1):
        load_url = "https://danbooru.donmai.us/posts?page=" + str(num) + "&tags="  + find_tags0 + "+" + find_tags1
        
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")

        #images = soup.find_all("img")
        
        driver.get(load_url)
        images =  driver.find_elements(By.TAG_NAME, 'img')

        for img in images:
            #src = img["src"]
            src = img.get_attribute("src")
            if 'cdn.donmai.us' not in src:
                continue

            #tags = img["title"]
            tags = img.get_attribute("title")
            if 'animated' in tags:
                continue
                
            score = tags.split(' ')[-1].split(":")[1]
            
            if int(score) < int(score_filter):
                continue
           
            match = 0
            if (not_find_tag0 != ""):
                if (not_tag_option == "AND"):
                    if ((not not_find_tag0 or (not_find_tag0 in tags)) and
                       (not not_find_tag1 or (not_find_tag1 in tags)) and
                       (not not_find_tag2 or (not_find_tag2 in tags))):
                        match = 1
                elif (not_tag_option == "OR"):
                    if not_find_tag0 and not_find_tag0 in tags:
                        match = 1
                    if not_find_tag1 and not_find_tag1 in tags:
                        match = 1
                    if not_find_tag2 and not_find_tag2 in tags:
                        match = 1
            if match == 1:
                continue
            
            match = 0
            if extra_tags == 1:
                if (extra_tag_option == "AND"):
                    if ((not find_extra_tags0 or (find_extra_tags0 in tags)) and
                       (not find_extra_tags1 or (find_extra_tags1 in tags)) and
                       (not find_extra_tags2 or (find_extra_tags2 in tags))):
                        match = 1
                elif (extra_tag_option == "OR"):
                    if find_extra_tags0 and find_extra_tags0 in tags:
                        match = 1
                    if find_extra_tags1 and find_extra_tags1 in tags:
                        match = 1
                    if find_extra_tags2 and find_extra_tags2 in tags:
                        match = 1

            if extra_tags == 1 and match == 0:
                continue

            src_org = src.replace('180x180', 'original')
            src_org = src_org.replace('.jpg', '.png')
            
            #print("src_org:" + src_org)

            img_urls.append(src_org)
            
            if len(img_urls) == int(max_downloads):
                limited = 1
                break
        if limited == 1:
            break


    sleep_time = 1
    no = 1

    for img_url in img_urls:
        # 保存先パス=保存先ディレクトリ+ファイル名
        dst_path = os.path.join(download_dir, str(no)+".png")
        #time.sleep(sleep_time)
        
        print('DL:' + img_url + "(" + str(no) + "/" + str(len(img_urls)) + ")")
        download_img(img_url, dst_path)
        no = no + 1
        
        
    #クロームの終了処理
    driver.close()
    
    print("download_finished")
    return "Download finished"