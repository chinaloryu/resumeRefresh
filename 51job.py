#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author loryu@4yutech.com
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os, sys
import time, platform
import requests, json
import random,base64,os
import numpy,cv2


def sendMsg(msg, phone_num):
	json_text = {
		"msgtype": "markdown",
		"at": {
			"atMobiles": [
			phone_num
			],
			"isAtAll": False
		},
		"markdown": {
			"title": 'resume refresh',
			"text": "![](http://img.mp.sohu.com/upload/20170807/7ccbb02232ce42a79a2cd05d2fe3d95f_th.png)"+msg+" @"+phone_num
		}
	}
	print(requests.post(api_url, json.dumps(json_text), headers=headers).content)


def refresh(loginname, password, system_os):
	# executable binary of chromedriver
	if system_os == 'Windows':
		chrome_driver = './bin/chromedriver.exe'
	elif system_os == 'Linux':
		chrome_driver = './bin/chromedriver'
	elif system_os == 'Darwin':
		chrome_driver = './bin/chromedriver_darwin'
	else:
		print('Not surpported OS!')
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument('start-maximized')
	options.add_argument('no-sandbox')
	options.add_argument('disable-dev-shm-usage')
	# chrome_driver = './chromedriver'
	driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
	# driver = webdriver.Chrome()
	print('[', time.ctime(), ']', 'start refresh resume......')
	try:
		driver.get('https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url=')
		sleep(random.uniform(0.5, 2.0))
	except:
		print('>>>>>>>>>>>>>\nlogin page failed!')
	try:
		driver.find_element_by_id('loginname').send_keys(loginname)
		sleep(random.uniform(0.5,2.0))
	except:
		print('>>>>>>>>>>>>>\nfind login name text frame failed!')
	try:
		driver.find_element_by_id('password').send_keys(password)
		sleep(random.uniform(0.5,2.0))
	except:
		print('>>>>>>>>>>>>>\nfind password text frame failed!')
	try:
		driver.find_element_by_id('isread_em').click()
		sleep(random.uniform(0.5,2.0))
	except:
		print('>>>>>>>>>>>>>\nagrement check failed!')
	try:
		driver.find_element_by_id('login_btn_withPwd').click()
		sleep(random.uniform(0.5,2.0))
	#passthrough geetest verification using opencv
	#save backgroud image as local image file
	bg_img = driver.find_element_by_xpath("//canvas[@class='geetest_canvas_bg geetest_absolute']")
	JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
	bg_img_info = driver.execute_script(JS)
	bg_img_base64 = bg_img_info.split(',')[1]
	bg_img_bytes = base64.b64decode(bg_img_base64)
	with open ('./img/geetest_bg.png','wb') as f:
		f.write(bg_img_bytes)

	fg_img = driver.find_element_by_xpath("//canvas[@class='geetest_canvas_slice geetest_absolute']")
	JS = 'return document.getElementsByClassName("geetest_canvas_slice geetest_absolute")[0].toDataURL("image/png");'
	fg_img_info = driver.execute_script(JS)
	fg_img_base64 = fg_img_info.split(',')[1]
	fg_img_bytes = base64.b64decode(fg_img_base64)
	with open('./img/geetest_fg.png', 'wb') as f:
		f.write(fg_img_bytes)

	bg = cv2.cvtColor(cv2.imread('./img/geetest_bg.png'), cv2.COLOR_BGR2GRAY)
	fg = cv2.cvtColor(cv2.imread('./img/geetest_fg.png'), cv2.COLOR_BGR2GRAY)
	fg = fg[fg.any(1)]
	result = cv2.matchTemplate(bg, fg, cv2.TM_CCOEFF_NORMED)
	x, y = numpy.unravel_index(numpy.argmax(result), result.shape)
	btn = driver.find_element_by_xpath("//div[@class='geetest_slider_button']")
	ActionChains(driver).drag_and_drop_by_offset(btn, xoffset=x * 1.4, yoffset=0).perform()
	#clean up
	os.remove('./img/geetest_bg.png')
	os.remove('./img/geetest_fg.png')

	except:
		print('>>>>>>>>>>>>>\nfind login button failed!')
	try:
		driver.refresh()
	except:
		print('>>>>>>>>>>>>>\nbrowser refresh failed!')
	try:
		driver.get('http://i.51job.com/userset/my_51job.php')
		sleep(random.uniform(0.5, 2.0))
	except:
		print('>>>>>>>>>>>>>\nlogin to user profile failed!')
	try:
		print('>>>>>>>>>>>>>refresh button')
		driver.find_elements_by_xpath("//span[text()='刷新']")[0].click()
		print('[', time.ctime(), ']', 'refresh success.')
		return 0
	except:
		print('[', time.ctime(), ']', 'refresh failed.')
		return 1
	driver.close()

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print('insufficient arguments, need 4, actually {}'.format(len(sys.argv) - 1))
		print('Usage:python ' + sys.argv[0] + ' <login name> <password> <phone number> <access token>')
	else:
		sys_os = platform.system()
		rtn = refresh(sys.argv[1], sys.argv[2], sys_os)
		headers = {'Content-Type': 'application/json;charset=utf-8'}
		api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % sys.argv[4]
		if 0 < rtn:
			sendMsg('[' + time.ctime() + '] ' + str(sys.argv[1]) +' refresh failed.', sys.argv[3])
		else:
			sendMsg('[' + time.ctime() + '] ' + str(sys.argv[1]) +' refresh success.', sys.argv[3])
