#coding=utf-8
# __author__: lin9e
# 2020-10-4

import requests
import random
import json
import threading
import queue
import re
import time
import execjs
import urllib.parse
#创建AipOcr
from aip import AipOcr
# 修改变量内容区
#ouidVal = 42740552
#ouidVal = 46064289
listid = 446476
sid = 'e5c4c0fc575e4fac'
# 本次运行脚本所投票计数参数
this_votes = 0

# 计算rnd参数值
def getrnd(ouidVal, listid):
	idnum = ouidVal + listid
	idnumlen = int(len(str(idnum)))
	#print(idnumlen)
	idlength = 20 - idnumlen
	zheng = ''
	for i in range(idlength):
		zheng = zheng + str(random.randint(1,10))
	rndNum = str(idnum) + zheng
	return rndNum

# 利用百度ocr sdk 识别在线验证码
def baiduocr(url_content):
	# url_content: 在线验证码图片内容 r.content
	# res: 识别结果
	""" 你的 APPID AK SK """
	APP_ID = '22784655'
	API_KEY = 'CleOfcAV8tAxEBhPDmq6r6Kg'
	SECRET_KEY = '8j7oASZDKaXcneYP4ZqBhA7GujiqjRWb'
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	# APP_ID = '22795779'
	# API_KEY = 'MoCY5BDnNhMlheBzgQqN6kd3'
	# SECRET_KEY = 'RnsppGvUnn8KabnoeZmLAlAoysM4R3dL'
	# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	# 网络图片文字识别 限额每日500次
	#ocr_res = client.webImage(url_content)
	# 通用文字识别 限额每日50000次
	ocr_res = client.basicGeneral(url_content)
	# 通用文字识别 高进度版 限额每日500次
	#ocr_res = client.basicAccurate(url_content)
	# 通用文字识别 含位置信息 限额每日500次
	#ocr_res = client.general(url_content)
	# 通用文字识别 含位置信息 限额每日500次
	#ocr_res = client.accurate(url_content)
	
	js = json.dumps(ocr_res)
	js1 = json.loads(js)
	res = js1['words_result'][0]['words']
	return res
# 加密验证码
def getData(yzm):
	with open('crypto_with_env.js','r') as f:
		ctx = execjs.compile(f.read())
		return ctx.call('getData', yzm)
# 判断字符串是否为纯数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

ua = [
	"Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.15(0x17000f31) NetType/WIFI Language/zh_CN",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_2 like Mac OS X) > AppleWebKit/637.51.2 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.15(0x17000f31) NetType/WIFI Language/zh_CN",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/4G Language/zh_CN",
	"Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045416 Mobile Safari/537.36 MMWEBID/9098 MicroMessenger/7.0.12.1620(0x27000C50) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
	"Mozilla/5.0 (iPad; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN",
	"Mozilla/5.0 (Linux; Android 10; YAL-AL50 Build/HUAWEIYAL-AL50; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045410 Mobile Safari/537.36 MMWEBID/6614 MicroMessenger/7.0.16.1700(0x2700103E) Process/tools WeChat/arm32 NetType/4G Language/zh_CN ABI/arm64",
	"Mozilla/5.0 (Linux; Android 8.1.0; V1818CA Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2469 MMWEBSDK/200701 Mobile Safari/537.36 MMWEBID/8290 MicroMessenger/7.0.17.1701(0x27001141) Process/tools WeChat/arm64 GPVersion/1 NetType/WIFI Language/zh_CN ABI/arm64",
	"Mozilla/5.0 (Linux; Android 7.1.2; vivo X9 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045409 Mobile Safari/537.36 MMWEBID/7808 MicroMessenger/7.0.20.1781(0x2700143D) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64"
]
# 每次运行脚本换个不同ua
user_agent = random.choice(ua)

headers = {
	"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
	"Origin":"https://h5.cxhdong.cn",
	"Accept-Encoding":"gzip, deflate",
	"Connection":"close",
	"Accept":"application/json, text/javascript, */*; q=0.01",
	"User-Agent":user_agent,
	"Referer":"https://h5.cxhdong.cn/m.php?v=e5c4c0fc575e4fac&b=1905107&id=140&sign=friend"
}

# 获取实时用户tokenVal
def getTokenVal(ouidVal):
	url = "https://h5.cxhdong.cn/m.php?v=e5c4c0fc575e4fac&b=1905107&id=140&sign=friend"
	cookie = "D5O_advice_brandid_42740552=1905107; D5O_back_sid_42740552=e5c4c0fc575e4fac; D5O_uphit_1905107=315027; CNZZDATA1278886474=253815611-1601343509-%7C1601883571; D5O_openinfos=%257B%2522uid%2522%253A%2522{ouid}%2522%252C%2522token%2522%253A%2522%2522%257D; D5O_42740552_1905107=4464476; D5O_enter=1905107;".format(ouid=ouidVal)
	headers_get_token = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"User-Agent":user_agent,
		"Accept-Encoding":"gzip, deflate",
		"Connection":"close",
		"Cookie":cookie
	}
	try:
		r = requests.get(url, headers=headers_get_token)
		#print(r.content)
		pattern = re.compile(r"var tokenVal=\'(.*?)\';\r\n        var")
		token = pattern.findall(str(r.text))
		return token[0].strip()
	except Exception as e:
		#print(e)
		return ''

# 定义多线程类 @getVotes
class getVotes(threading.Thread):
	def __init__(self, queue1):
		threading.Thread.__init__(self)
		self._queue = queue1

	def run(self):
		while not self._queue.empty():
			ouidVal = self._queue.get_nowait()
			try:
				self.vote(ouidVal)
			except Exception as e:
				print(e)
	def vote(self, ouidVal):
		tokenVal = getTokenVal(ouidVal)
		global this_votes
		if tokenVal != '':
			print("获取实时token: " + ouidVal + "|" + tokenVal)
			rnd = getrnd(int(ouidVal),listid)
			s = requests.Session()
			try:
				#def first():
				#first: 获取验证码、识别验证码、加密识别后的验证码
				print("[*] Starting 获取验证码、识别验证码、加密识别后的验证码...")
				url1 = "https://v.tiantianvote.com/api/c2/captchas.png.php?rnd=%s&type=2&id=4464476"%(rnd)
				#print(url1)
				r1 = s.get(url=url1, headers=headers, timeout=5)
				# #保存验证码图片 以供参考
				# yzm_name = "yzm_"+str(random.randint(1, 999))+".png"
				# with open(yzm_name,'wb') as f:
				# 	f.write(r1.content)
				#验证码识别结果
				time.sleep(2)
				yzm = baiduocr(r1.content)
				# # 循环获取正确验证码 {bug:百度OCR接口同一张验证码多次识别结果一致，故循环暂时无用}
				# while_count = 0
				# while True:
				# 	while_count = while_count + 1
				# 	yzm = baiduocr(r1.content)
				# 	print(yzm)
				# 	if "加载" in yzm: # 验证码加载 or 待加载 的情况
				# 		break
				# 	if len(yzm) == 4 and is_number(yzm):
				# 		break
				# 	if while_count > 5:
				# 		break
				print("[+] OCR识别验证码结果为"+yzm)
				if len(yzm) == 4 and is_number(yzm):
					#验证码加密结果
					captcha_ = getData(yzm)
					captcha = urllib.parse.quote(captcha_)
					#print(captcha)
					#print("[*] Finish 获取验证码、识别验证码、加密识别后的验证码...")
					#second: 校验验证码是否正确
					#print("[*] 开始校验验证码是否正确...")
					url2 = "https://v.tiantianvote.com/api/c2/captchas.check1.php"
					data2 = "captcha={}&rnd={}&type=2&id=4464476".format(captcha, rnd)
					#print(data2)
					r2 = s.post(url=url2, headers=headers, data=data2)
					#print(r2.content)
					r2_res = r2.content.decode('utf8')
					js2 = json.loads(r2.content)
					#print(r2_res)
					if r2_res.find("200") != -1:
						print("[+] 验证码校验成功，开始投票...")
						url3 = "https://v.tiantianvote.com/v.php"
						data3 = "brandid=1905107&itemid=4464476&yqm={}&rnd={}&token={}&ouid={}&sid=e5c4c0fc575e4fac".format(captcha, rnd, tokenVal, ouidVal)
						#print(data3)
						time.sleep(2)
						r3 = s.post(url=url3, headers=headers, data=data3)
						r3_res = r3.content.decode('utf8')
						#print(r3_res)
						js = json.loads(r3.content)
						if r3_res.find("votes") != -1 and js['votes'] != 0:
							print("[+] !!!!!!!!!!!!!!!!!!!!!!投票成功！!!!!!!!!!!!!!!!!!!!!!!!当前票数为：%s"%str(js['votes']))
							this_votes = this_votes + 1
						else:
							print("[-] 投票失败！原因：%s"%(js['msg']))
							# print(r3_res)
						time.sleep(1)
					else:
						print("[-] 验证码验证失败! 原因：%s"%(js2['msg']))

			except Exception as e:
				print(e)

def main():
	domains = []
	queue1 = queue.Queue()
	for _ in range(10000,99999):
		ouidVal = "460" + str(_)
		queue1.put(ouidVal)
	threads = []
	# 线程数
	thread_count = 33

	for i in range(thread_count):
		threads.append(getVotes(queue1))
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	
	# print("[+++]Over!本次运行脚本共计投票{votes}次".format(votes=str(this_votes)))

if __name__ == '__main__':
	main()











