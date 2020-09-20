import requests
from bs4 import BeautifulSoup
import json
import shutil
import os
import re

class insta_site():
	def __init__(self, name):
		self.name = name
		req = requests.get(f"https://www.instagram.com/{name}/")
		self.status_code = req.ok
		self.soup = BeautifulSoup(req.text, 'html.parser')
		self.followers = '0 Followers'
		self.following = '0 Following'
		self.posts = '0 Posts'
		self.img_path = '/'
		
	def get_info(self):
		if self.status_code:
			data = self.soup.find_all(property="og:description")[0]['content']
			self.description = data
			data = re.search(r'(.*) Followers,(.*) Following,(.*) Posts -', data)
			if data is not None:
				self.followers = data.group(1).strip() + ' Followers'
				self.following = data.group(2).strip() + ' Following'
				self.posts = data.group(3).strip() + ' Posts'
			else:
				return 'Name not found!', 'Name not found!', 'Name not found!', 'Name not found'
			return self.followers, self.following, self.posts, self.description
		else:
			return 'Name not found!', 'Name not found!', 'Name not found!', 'Name not found'
	
	def get_img(self):
		if self.status_code:
			img_path = f"static/insta_{self.name}.jpg"
			
			img_url = self.soup.find_all(property="og:image")[0]['content']
			req_img = requests.get(img_url)
			
			if not os.path.exists(img_path):
				with open(img_path, 'wb+') as file_img:
					file_img.write(req_img.content)
			else:
				os.remove(img_path)
				with open(img_path, 'wb+') as file_img:
					file_img.write(req_img.content)
				#with open(img_path, 'rb') as current_img:
				#	if current_img.read() != req_img.raw.read():
				#		os.remove(img_path)
				#		with open(img_path, 'wb+') as file_img:
				#			shutil.copyfileobj(req_img.raw, file_img)
				
			del req_img
			self.img_path = img_path
			return self.img_path
		else:
			return 'Image not found!'


