import json
import logging
import requests, time, random
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_status(self):
    if self['code'] == 0:
        return "日检日报成功"
    elif self['code'] == 1:
        return "日检日报时间结束"
    elif self['code'] == -10:
        return "···Token已失效"
    else:
        return "！！！发生未知错误"

class answer:
    def __init__(self):      # 使用前请阅读 新版必读.txt
        username = "18691303202"   # 修改1 账号 一般是手机号 作者QQ 3330900358 有疑问欢迎随时交流
        password = "zhanghanbing"   # 修改2 密码
        header = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us,en",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",   # 修改3 抓包获取/从旧版代码复制
            "Content-Length": "360",
        }
        loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        data = "{}"
        session = requests.session()
        url = loginUrl + "?username=" + username + "&password=" + password
        respt = session.post(url, data=data, headers=header)
        res = json.loads(respt.text)
        if res["code"] == 0:
            print("Login success.")
            jwsession = respt.headers['JWSESSION']
        else:
            print(res)
            print('Login failed.')

        self.my_Name = "everr"  # 修改4 姓名
        self.my_sender = '1943608139@qq.com'  # 修改5 填写发信人的邮箱账号
        self.my_pass = 'iyiwppldeneocgdi'  # 修改6 发件人邮箱授权码
        self.my_user = '1943608139@qq.com'  # 修改7 收件人邮箱账号

        self.api = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",  # 修改8 抓包获取/从旧版代码复制
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/182/page-frame.html",  # 修改9 抓包获取/从旧版代码复制
            "Content-Length": "360",
            "JWSESSION": str(jwsession),
        }
        self.data = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),

            "longitude": "108.941603",  # 修改10 经度
            "latitude": "34.120783",  # 修改11 纬度
            "country": "中国",   # 修改12 地址
            "province": "陕西省",
            "city": "西安市",
            "district": "长安区",
        }

    # 获取随机体温
    def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.2, 36.7))

    # seq的1,2,3代表早，中，晚
    def get_seq(self):
        current_hour = datetime.datetime.now()
        current_hour = current_hour.hour + 8
        if 7 <= current_hour <= 9:
            return "1"
        elif 12 <= current_hour < 14:
            return "2"
        elif 22 <= current_hour < 23:
            return "3"
        else:
            return 1

    def run(self):
        print(datetime.datetime.now())
        res = requests.post(self.api, headers=self.headers, data=self.data, ).json()  # 打卡提交
        print(res)
        try:
            msg = MIMEText(self.my_Name+"  "+get_status(res), 'plain', 'utf-8')  # 填写邮件内容
            msg['From'] = formataddr(["我在校园", self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["xxxxx", self.my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号，此处xxx可选择性修改
            msg['Subject'] = get_status(res)  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
            server.login(self.my_sender, self.my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
            server.sendmail(self.my_sender, [self.my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(res)
            res = False
            print(res)
        return True

if __name__ == "__main__":
    answer().run()


def main_handler(event, context):
    logger.info('got event{}'.format(event))
    return answer().run()
