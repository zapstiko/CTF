#!/usr/bin/python3
import hashlib
import os
import requests
print("Enter full url with port eg http://test.com:80/")
url=input("=>")
get=False
l=0
letter=""
ifs=True
r=requests.get(url)
first=True
def run(get,l,letter,ifs,r,url,rcookie,rfirst):
	for a in r.text:
		if get:
			if not a=="<":
				letter +=a
			else:
				get=False
				m=hashlib.md5()
				m.update(letter.encode())
				dts={'hash':m.hexdigest()}
				if rfirst:
					rfirst=False
					rcookie=r.cookies
				x=requests.post(url,data=dts,cookies=rcookie)
				if "HTB" in x.text:
					print(x.text)
					os.system("echo 'RG8gbm90IGJlICBhZnJhaWQgeW91IGFyZSBub3QgaGFja2VkLi4uIFRoaXMgaXMgdG8gc2hvdyB5b3Ugd2hhdCBoYXBwZW5zIHdoZW4geW91IGJlY29tZSBzY3JpcHQga2lkZHkuLi4K' | base64 -d >> ~/Desktop/YOu_h4cked.txt")
					exit()
				l=0
				letter=''
				ifs=True
				run(get,l,letter,ifs,x,url,rcookie,rfirst)
				break
		elif (a==">" and l<=7 and ifs):
			l +=1
		elif (a==">" and l==8 and ifs ):
			get=True
			ifs=False
if first:
	first=False
	run(get,l,letter,ifs,r,url,"","True")
exit()
