import os, sys, time, json
from selenium import common
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode
from urllib.request import urlretrieve
import requests
import random

# I was lazy to make it OOP

driver = None

# headless doesn't work yet (--headless)
def launch_browser(*arguments : str):
	global driver

	options = Options()

	''' Use this if you want your current chrome profile (works only on windows)  
		
	# add existing profile to the chrome for cookies etc.
	profile_dir = f"{os.getenv('LOCALAPPDATA')}/Google/Chrome/User Data"
	options.add_argument(f"user-data-dir={profile_dir}")
	'''

	options.add_argument(f'--user-data-dir={DIR}/profile')

	# add aditionals arguments
	for argument in arguments:
		options.add_argument(argument)

	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

	return driver

currentIndex = -1
launched = False

def upload_video(path, description, tags): 
	global currentIndex
	global launched

	if not launched:
		launched = True
		launch_browser()

	upload_url = "https://www.tiktok.com/upload"
	currentIndex += 1

	driver.get(upload_url)

	def web_loaded(driver):
		return driver.execute_script("return document.readyState") == "complete"

	print("Preparing to upload a video..")

	# WebDriverWait(driver, 100).until(web_loaded)
	time.sleep(3)

	# switch to correct iframe
	frame = driver.find_element(By.TAG_NAME, "iframe")
	driver.switch_to.frame(frame)

	# set upload path
	upload_input = driver.find_element(By.TAG_NAME, "input")
	upload_input.send_keys(path)

	tags_input = driver.find_element(By.CLASS_NAME, "DraftEditor-editorContainer")

	# focus input
	ActionChains(driver).move_to_element(tags_input).click(tags_input).perform()

	# send description
	ActionChains(driver).send_keys(description + " ").perform()

	# send keys
	for tag in tags:
		ActionChains(driver).send_keys(("#" if not tag.startswith("#") else "") + tag).perform()
		time.sleep(1)
		ActionChains(driver).send_keys(Keys.RETURN).perform()

	time.sleep(0.5)

	driver.switch_to.default_content()
	driver.execute_script("window.scrollTo(150, 300);")
	driver.switch_to.frame(frame)

	upload_btn = driver.find_element(By.CLASS_NAME, "css-n99h88")

	def not_busy(driver):
		try:
			upload_status = driver.find_element(By.CLASS_NAME, "tiktok-progress-inner")
			print("\rUploading state: " + upload_status.text, end="\r")
		except (common.exceptions.StaleElementReferenceException, common.exceptions.NoSuchElementException):
			pass

		return upload_btn.get_attribute("disabled") != "true"

	WebDriverWait(driver, 100).until(not_busy)
	upload_btn.click()

	# wait a little
	time.sleep(1)

# @deprecated - doesn't work
def get_trendings(count=10) -> list:

	query = {
	            "aid": 1988,
	            "app_name": "tiktok_web",
	            "device_platform": "web",
	            "referer": "https://www.tiktok.com/",
	            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
	            "cookie_enabled": "true",
	            "browser_online": "true",
	            "ac": "4g",
	            "appId": 1233,
	            "appType": "m",
	            "isAndroid": False,
	            "isMobile": False,
	            "isIOS": False,
	            "OS": "windows",
	            "page_referer": "https://www.tiktok.com/",
	            "count": count,
	            "id": 1,
	            "secUid": "",
	            "maxCursor": 0,
	            "minCursor": 0,
	            "sourceType": 12,
	            "appId": 1233,
	            "region": "US",
	            "priority_region": "US",
	            "language": "US"
	 }

	url = f"https://m.tiktok.com/api/recommend/item_list?{urlencode(query)}"
	resp = requests.get(url, headers={
		"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
		"cookie" : open("cookies.txt", "r").read()
	})

	return resp.json()['itemList']

# doesn't work as well..
def get_video(video_id) -> dict:
	query = {
				"itemId": video_id,
	            "aid": 1988,
	            "app_name": "tiktok_web",
	            "device_platform": "web_mobile",
	            "region": "US",
	            "priority_region": "",
	            "os": "ios",
	            "referer": "",
	            "cookie_enabled": "true",
	            "browser_platform": "iPhone",
	            "browser_name": "Mozilla",
	            "browser_online": "true",
	            "timezone_name": "US",
	            "is_page_visible": "true",
	            "focus_state": "true",
	            "is_fullscreen": "false",
	            "history_len": random.randint(1, 5),
	            "language": "US",
	}

	url = f"https://m.tiktok.com/api/item/detail/?{urlencode(query)}"

	resp = requests.get(url, headers={
		"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
		"cookie" : open("cookies.txt", "r").read()
	})

	return resp.json()

# current directory of the file
DIR = os.path.dirname(os.path.realpath(__file__))

# download tiktok video
def download_video(video_info) -> str:
	url = video_info['downloadAddr']

	if not os.path.exists("videos"):
		os.mkdir("videos")

	name = f"videos/{video_info['id']}.{video_info['format']}"

	# download video
	urlretrieve(url, name)

	# return absolute path
	return f"{DIR}/{name}"

# pretty trash way of doing this
def get_tags_from_desc(desc : str) -> list:
	tags = []

	for x in desc.split(" "):
		if x.startswith("#"):
			tags.append(x[1:])

	return tags