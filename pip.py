import os
while True:
    download_name = input("请所需输入安装的库，pip会自动帮你安装：")
    os.system(f"pip install {download_name}")
