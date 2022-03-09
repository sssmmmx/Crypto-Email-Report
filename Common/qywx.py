import time
import requests
import json



class WeChatSMS:
    def __init__(self):
        self.CORPID = '123'                                                 # 企业ID， 登陆企业微信，在我的企业-->企业信息里查看
        self.CORPSECRET = '123'                                             # 自建应用，每个自建应用里都有单独的secret
        self.AGENTID = '1000004'                                            # 应用代码
        self.TOUSER = "123"                                                 # 接收者用户名,  @all 全体成员 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
#        print (data)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except():
            with open('access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:                      # token的有效时间7200s
                return access_token
            else:
                with open('access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, msg):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": msg
                },
            "safe": "0"
            }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()                                # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]

    def get_media_ID(self, image):  #上传到临时素材  图片ID
        img_url ="https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token="+ self.get_access_token() +"&type=image"
        # file_abs_path = "C:/Users/surgarman/Desktop/frame/auto_report/12345.png"
        # files = {'image': (path, open(file_abs_path, 'rb'), 'image/png', {})}
        path = "/auto_report/png/" + image
        data = {'media': open(path, 'rb')}  # post jason
        response = requests.post(url=img_url, files=data)  # post 请求上传文件
        json_res = response.json()  # 返回转为json

        return json_res['media_id']

    def send_image(self, image):

        img_id = self.get_media_ID(image)
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()

        send_values = {
            "touser": self.TOUSER,
            "msgtype": "image",
            "agentid": self.AGENTID,
            "image": {
                "media_id": img_id
            },
            "safe": "0"
        }

        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]



if __name__ == '__main__':
    wx = WeChatSMS()
    wx.send_data(msg="消息通知测试")
    wx.send_image(image="12345.PNG")
