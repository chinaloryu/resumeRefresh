#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Author loryu
from selenium import webdriver
from time import sleep
import os,sys
import time

def grab(loginname,password):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(options = options)
	# driver = webdriver.Chrome()
	print('[',time.ctime(),']','start refresh resume......')
	try:
	    driver.get('http://login.51job.com')
	    driver.find_element_by_id('loginname').send_keys(loginname)
	    driver.find_element_by_id('password').send_keys(password)
	    test=driver.find_element_by_id('login_btn').click()
	    driver.get('http://i.51job.com/userset/my_51job.php')
	    driver.find_element_by_xpath("//span[text()=\"刷新\"]").click()
	    print('[',time.ctime(),']','refresh success.')
	except:
	    print('[',time.ctime(),']','refresh failed.')
	driver.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('insufficient arguments, need 2, actually {}'.format(len(sys.argv) - 1))
		print('Usage:python ' + sys.argv[0] + ' <loginname> <password>')
	else:
		grab(sys.argv[1],sys.argv[2])
