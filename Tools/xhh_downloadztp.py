import requests
import json
import hashlib
import time
from tqdm import tqdm

def get_zty_sign_url_get(base_url,method):
    timestamp = str(int(time.time() * 1000))
    SIGNATURE_KEY = "eptim]q34imt5b]-q04i5q=fdkfjfsadlkjfasdfrt573df4pltoy]-pn965498d"
    sign_raw_string = f"{method}{base_url}{timestamp}{SIGNATURE_KEY}"
    sign = hashlib.md5(sign_raw_string.encode('utf-8')).hexdigest()
    final_url = f"{base_url}&sign={sign}&t={timestamp}"
    #print(f"[*] 待签名串: {sign_raw_string}")
    #print(f"[*] 最终 URL: {final_url}")
    
    return final_url

def get_ztp_url(device_id,appid):

    base_url = "https://ztp.yunzuoye.net/api/v2/platform/apk"

    user_agent = f"com.xuehai.launcher/v1.21.06.20251212hwS (SM-P200; android; 9; {device_id})"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": user_agent
    }
    version_code="1021006"
    payload_dict = {
        "appId": appid,
        "versionCode": version_code
    }
    payload_data = json.dumps(payload_dict, separators=(',', ':'))
    
    new_url=base_url+f"?appId={appid}&versionCode={version_code}"
    method="GET"
    final_url=get_zty_sign_url_get(new_url,method)
    
    try:
        response = requests.get(final_url, headers=headers)

        if response.status_code!=200 :
            print("Something unexpected...")
            print(response.text)

        response.raise_for_status()  
        
        print("请求地址成功！")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f" 错误！{e}")
        return None
def download(url, filename):
    response = requests.head(url, allow_redirects=True)
    total_size = int(response.headers.get('content-length', 0))
    try:
        first_byte = os.path.getsize(filename)
    except:
        first_byte = 0
    progress = tqdm(
        total=total_size, 
        unit='B', 
        unit_scale=True,
        initial=first_byte,
        desc=f"下载 {filename.split('/')[-1]}",
        ascii=True
    )
    headers = {'Range': f'bytes={first_byte}-'}
    response = requests.get(url, headers=headers, stream=True)
    mode = 'ab' if first_byte else 'wb'
    with open(filename, mode) as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                progress.update(len(chunk))
    
    progress.close()
    if total_size != 0 and progress.n != total_size:
        print("警告：文件可能不完整")

device_id = "R52RXXXXXXX"

appids=["mdm_stu_to_c","mdm_stu","mdm_tea"]
print("""智通平台下载工具
----------------------------------
0 = TOC版 1=学生端 2=教师端 可多选
""")
bb=input("要下载的版本为:")
for version in bb:
    ztpurlraw=get_ztp_url( device_id,appids[int(version)])
    download(ztpurlraw['url'],f"{appids[int(version)]}_{str(int(time.time() * 1000))}.apk")
