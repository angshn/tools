import sys
import requests as req
from urllib import parse
from urllib.parse import urlparse, parse_qs
from PIL import Image
from io import BytesIO
from threading import Thread
import regex

from auth import encryp

class Serv:
    rsa_password = None
    def __init__(self,args) -> None:
        self.args = args

    def down(self):
        login_return=self.login()
        if login_return==1:
            print("登录失败。")
            return 
        device_list = list(self.get_online_list())
        if len(device_list) == 0:
            print("没有需要下线的设备。")
            return
        # 筛选
        for n,(ip,name,datetime) in enumerate(device_list):
            print(f'{n+1}',ip,name,datetime)
        index_down=input("输入要下线的设备序号（用空格分隔，输入 0 则下线所有设备）：")
        target = list(map(int,index_down.split(' ')))

        if len(target)==1 and  target[0]==0:
            self.down_all([item[0] for item in device_list])
        else :
            li = [item[0] for i, item in enumerate(device_list) if i+1 in target ]
            self.down_all(li)
        self._logout

    def show_verify(self, cont):
        image = Image.open(BytesIO(cont))
        self._show_verify(image)

    def _show_verify(self,img):

        width    = img.width  #获取图片宽度
        height   = img.height #获取图片高度
        
        gray_img = img.convert('L')  #图片转换为'L'模式  模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度
        
        char_lst = ' .:-=+*@%.'  #要替换的字符
        char_len = len(char_lst)  #替换字符的长度
        
        for y in range(0, height, 1):  #根据缩放长度 遍历高度
            for x in range(0, width, 1):  #根据缩放长度 遍历宽度
                choice =gray_img.getpixel((x, y)) * char_len // 255  #获取每个点的灰度  根据不同的灰度填写相应的 替换字符
                if choice==char_len:
                    choice=char_len-1
                sys.stdout.write(char_lst[choice])  #写入控制台
            sys.stdout.write('\n')
            sys.stdout.flush()
    
    def login(
        self,
    ):
        res = req.get("https://serv.ysu.edu.cn/selfservice/module/scgroup/web/login_self.jsf")
        self.cookies = res.cookies

        # get rsa_password
        rules = 'publicKey"  value="(.{0,300})"'
        pattern_publicKey = regex.compile(rules)
        publicKey=pattern_publicKey.findall(res.text)[0]
        userpwd = self.args.password
        self.rsa_password=encryp.encryp(publicKey,userpwd)

        verify_image_res = req.get(
            "https://serv.ysu.edu.cn/selfservice/common/web/verifycode.jsp",
            cookies=res.cookies,
        )

        thread = Thread(target=self.show_verify, args=[verify_image_res.content])
        thread.start()
        verify_code = input("input verify code.\n>")

        json_data = {
            "from": "rsa",
            "name": f"{self.args.user}",
            "password": self.rsa_password,
            "verify": verify_code,
        }
        data = parse.urlencode(json_data)
        login_res = req.post(
            "https://serv.ysu.edu.cn/selfservice/module/scgroup/web/login_judge.jsf",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
            cookies=self.cookies,
        )
        if("verifyError" in login_res.text):
            # 登录失败
            return 1
        else:
            return 0

    def get_online_list(
        self,
    ):
        online_device_res = req.get(
            "https://serv.ysu.edu.cn/selfservice/module/webcontent/web/onlinedevice_list.jsf",
            cookies=self.cookies,
        )
        rules = "IP.:.(.*?)<"
        pattern_ip = regex.compile(rules)
        device_ip_list=pattern_ip.findall(online_device_res.text)

        rules = 'title="([\s\S]{2,20})" st'
        pattern_name = regex.compile(rules)
        device_name_list=pattern_name.findall(online_device_res.text)

        rules = '上线时间 ：&nbsp;([\s\S]{2,20})<'
        pattern_time = regex.compile(rules)
        device_time_list=pattern_time.findall(online_device_res.text)

        return zip(device_ip_list,device_name_list,device_time_list)

    def down_all(self, groups):
        for ip in groups:
            key = f"key={self.args.user}:{ip}"
            offline_res = req.post(
                "https://serv.ysu.edu.cn/selfservice/module/userself/web/userself_ajax.jsf?methodName=indexBean.kickUserBySelfForAjax",
                cookies=self.cookies,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                data=key,
            )
            print(f"{ip}：{offline_res.text.strip()}")

    def _logout(self):
        res = req.get(
            "https://serv.ysu.edu.cn/selfservice/module/webcontent/web/init.jsf?goto=module/scgroup/web/logout.jsp",
            cookies=self.cookies,
        )
        print(res.text.strip("\r\n\t "))
