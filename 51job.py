#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author loryu
from selenium import webdriver
from time import sleep
import os, sys
import time, platform
import requests, json
import random


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
		chrome_driver = './chromedriver.exe'
	elif system_os == 'Linux':
		chrome_driver = './chromedriver'
	elif system_os == 'Darwin':
		chrome_driver = './chromedriver_darwin'
	else:
		print('Not surpported OS!')
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
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
		driver.find_element_by_id('login_btn_withPwd').click()
		sleep(random.uniform(0.5,2.0))
	except:
		print('>>>>>>>>>>>>>\nfind login button failed!')
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
