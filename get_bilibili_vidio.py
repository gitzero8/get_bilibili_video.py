import random
import requests
import re
import json
import os
import time
from fake_useragent import UserAgent

url = input("请输入哔哩哔哩视频网页空降URL：")
video_url_list = []; video_url_list.append(url)
video_url = video_url_list[0]
user_agent_list = []

print("[来自针对页面反爬系统]随机User-Agent启动...") ; time.sleep(2)

user_agent_range = 0
for i in range(0,5):
    UAR = UserAgent().random
    user_agent_range+=1
    time.sleep(0.5) ; print("[+]"+UAR+"【第%d条】"%user_agent_range)
    user_agent_list.append(UAR)
time.sleep(1)
random_user_agent = random.choice(user_agent_list) ; print(f"本次User-Agent：{random_user_agent}")
header = {
    "referer":"https://www.bilibili.com/video",
    "User-Agent":random_user_agent
}
class BiliBili_video_draw():
    def __init__(self):
        video_url_get = requests.get(headers=header,url=video_url)
        self.video_url_get_code = video_url_get.text
    def get_video_name(self):
        video_name_re = re.findall('"title":"(.*?)","pubdate"',self.video_url_get_code)
        self.video_name = video_name_re[0] ; print(self.video_name)

        # 改进文件名解析时字符解析报错
        if (' ' in self.video_name) or ('-'in self.video_name) or \
                ('【'in self.video_name) or ('】' in self.video_name) or \
                ('|' in self.video_name) or (':' in self.video_name):
            self.video_name = (self.video_name).replace(" ","_")
            self.video_name = (self.video_name).replace("-","_")
            self.video_name = (self.video_name).replace("【","[")
            self.video_name = (self.video_name).replace("】","]")
            self.video_name = (self.video_name).replace("|","_")
            self.video_name = (self.video_name).replace(":","：")
        else:
            pass
    def get_video_audio_data(self):
        video_data_re = re.findall("<script>window.__playinfo__=(.*?)</script>",self.video_url_get_code)
        video_data_str = video_data_re[0] # type --> str
        video_audio_data_dict = json.loads(video_data_str) # 将字符串转化为字典，以便提取url
        video_audio_data_dict_str = json.dumps(json.loads(video_data_str),indent=5) # 将刚转化的字典转化为格式化的字符串以便查找内容数据
        # print(video_audio_data_dict_str)
        #解析视频/音频链接
        self.video_data_base_url = video_audio_data_dict['data']['dash']['video'][0]["baseUrl"] #视频数据_URL
        self.audio_data_base_url = video_audio_data_dict["data"]["dash"]["audio"][0]["baseUrl"] #音频数据_URL
        print("视频链接："+self.video_data_base_url) ;print("\r\n"); print("音频链接："+self.audio_data_base_url)
        print("======================================")
    def download_video_audio_url(self):
        video_data_base_url_get_data = requests.get(self.video_data_base_url,headers=header).content #视频数据
        print("获取视频数据...") ; time.sleep(2)
        print(video_data_base_url_get_data)
        self.bilibili_video_audio_file = "bilibili_video_audio"
        os.system(f"mkdir {self.bilibili_video_audio_file}")

        with open(f"./{self.bilibili_video_audio_file}/{self.video_name}.mp4",'wb') as op_1:
            op_1.write(video_data_base_url_get_data)
            print("[+]下载完成，已保存至--->{bilibili_video_audio}文件夹目录下！")

        audio_data_base_url_get_data = requests.get(self.audio_data_base_url,headers=header).content #音频数据
        print("获取音频数据...") ; time.sleep(2)
        print(audio_data_base_url_get_data)
        with open(f"./{self.bilibili_video_audio_file}/{self.video_name}.mp3","wb") as op_2:
            op_2.write(audio_data_base_url_get_data)
            print(f"[+]下载完成，已保存至--->{self.bilibili_video_audio_file}文件夹目录下！")
    def merge_video_audio(self):
        os.system("mkdir bilibili_video")
        os.system(f"ffmpeg -i ./{self.bilibili_video_audio_file}/{self.video_name}.mp4 -i ./{self.bilibili_video_audio_file}/{self.video_name}.mp3 -c:v copy -c:a aac -strict experimental ./bilibili_video/{self.video_name}.mp4")
        # -  -i input.mp3 ：指定输入的MP3文件。 input.mp3 是您要合并的MP3文件的文件名。
        # -  -i input.mp4 ：指定输入的MP4文件。 input.mp4 是您要合并的MP4文件的文件名。
        # -  -c:v copy ：指定视频编码器。 copy 表示将视频流从输入文件直接复制到输出文件，而不进行重新编码。
        # -  -c:a aac ：指定音频编码器。 aac 表示使用AAC编码器对音频流进行重新编码。
        # -  -strict experimental ：启用实验性的AAC编码器。这是为了确保兼容性，因为AAC编码器在某些情况下可能需要这个参数。
        # -  output.mp4 ：指定合并后的输出文件名。 output.mp4 是您希望生成的合并后的MP4文件的文件名。

def main():
    bilibli_video_draw = BiliBili_video_draw()
    bilibli_video_draw.get_video_name()
    bilibli_video_draw.get_video_audio_data()
    bilibli_video_draw.download_video_audio_url()
    select_merge = input("是否需要合并音频与视频?（Y/N）：")
    if (select_merge == 'Y') or (select_merge == 'y'):
        bilibli_video_draw.merge_video_audio()
        print("音频与视频合成完毕！已保存至:bilibili_video文件夹目录下面！") ; input("Enter键退出...")
    else:
        print("已拆分音频与视频！") ; input("Enter键退出...")
if __name__ == "__main__":
    main()
