#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author loryu
from selenium import webdriver
from time import sleep
import os, sys
import time, platform
import requests, json


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
			"text": "![](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.theladders.com%2Fcareer-advice%2Fcareer-path-dream-job&psig=AOvVaw0IG7mop6c8gFKsqByKIjbE&ust=1612959173588000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKD3l63j3O4CFQAAAAAdAAAAABAF)"+msg+" @"+phone_num
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
	options.add_argument('no-sandbox')
	options.add_argument('disable-dev-shm-usage')
	# chrome_driver = './chromedriver'
	driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
	# driver = webdriver.Chrome()
	print('[', time.ctime(), ']', 'start refresh resume......')
	try:
		driver.get('http://login.51job.com')
		driver.find_element_by_id('loginname').send_keys(loginname)
		driver.find_element_by_id('password').send_keys(password)
		driver.find_element_by_id('login_btn').click()
		driver.get('http://i.51job.com/userset/my_51job.php')
		driver.find_element_by_xpath("//span[text()=\"刷新\"]").click()
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
