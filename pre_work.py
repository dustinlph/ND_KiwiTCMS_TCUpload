# coding=utf-8
"""
@Project: KiwiTCMS_TCUpload
@File: /pre_work.py
@Author: Dustin Lin
@Created on: 2023/5/18 15:52:16
"""
import os
required_file_path: str = os.path.expanduser('~/.tcms.conf')
if not os.path.isfile(required_file_path):
    print("Not exist")
    url: str = input("URL: ")
    username: str = input("Username: ")
    password: str = input("Password: ")
    with open(required_file_path, "w") as f:
        f.write(f"[tcms]\nurl = {url}/xml-rpc/\nusername = {username}\npassword = {password}")
    f.close()
else:
    print("File already exist")
