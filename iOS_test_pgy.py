# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 打包后续脚本，蒲公英版本, 蒲公英的二维码是唯一的
import optparse
import os
import sys
import json
import re
from datetime import date, time, datetime, timedelta
import urllib
import urllib2
import json
import getopt
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

#----定义一些全局变量
#编译好的ipa文件目录
build_path   = ""
#ipa名称(不包含.ipa)
file_name    = ""

#蒲公英上传的token
key_token    = ""
#钉钉机器人key
dingtalk_key = ""

#钉钉消息附加说明
dingtalk_msg = ""

#----具体方法
#提示用法
def usage():
    print(u"""
        iOS 打包后续脚本，上传ipa文件到蒲公英，发送钉钉消息
        -h / --help   :使用帮助
        -n / --name=  :ipa文件名称
        -k / --key=   :包管理平台（蒲公英）api token
        -d / --ding=  :钉钉机器人key
        -p / --path=  :build目录的路径
        -m / --msg=   :钉钉消息附加说明
        
        如：python iOS_test_pgy.py -p ipa所在目录路径 -n ipa文件名 -k 蒲公英token -d 钉钉token -m 钉钉附加说明
        """)

#判断字符串是否为空
def isNone(para):
    if para == None or len(para) == 0:
        return True
    else:
        return False

#上传
def uploadToPgy():
    file_path = ("%s/%s.ipa"%(build_path, file_name))
    print file_path
    
    if os.path.exists(file_path):
        url   = "https://www.pgyer.com/apiv2/app/upload"
        datas = {"_api_key" : key_token, "buildUpdateDescription" : dingtalk_msg}
        files = {"file" : open(file_path, "rb")}
        response = requests.post(url, data=datas, files=files)
        resObj = json.loads(response.text)
        
        return resObj['data']
    else:
        print '----没有找到ipa文件----'
    return {}

#发送钉钉机器人
def dingTalkRobot(uploadInfo):
    title   = uploadInfo['buildName'] + uploadInfo['buildVersion'] + "(" + uploadInfo['buildVersionNo'] + ")"
    qr_url  = uploadInfo['buildQRCodeURL']
    timeStr = uploadInfo['buildCreated']

    url  = "https://oapi.dingtalk.com/robot/send?access_token=" + dingtalk_key
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":"iOS-打包-" + title ,
            "text": "![QRcode]("+ qr_url +") \n\n"  +
                    "iOS-打包-" + title + "\n\n"
                    "**" + dingtalk_msg + "** \n\n" +
                    "*" + timeStr + "*发布"
        }
    }
    headers = {'Content-Type' : 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resObj = json.loads(response.text)
    print resObj
    return

#主函数
def main():
    # 上传包
    print '----开始上传包----'
    uploadInfo = uploadToPgy()
    print uploadInfo
    
    if isNone(uploadInfo) or not uploadInfo.has_key('buildQRCodeURL'):
        print '-----上传失败-----'
    else:
        print '-----上传成功-----'
        print '----发送钉钉消息----'
        dingTalkRobot(uploadInfo)
    return

#命令行输入参控制
try:
    options,args = getopt.getopt(sys.argv[1:],"hn:k:d:p:m:",["help","name=","key=","ding=","path=","msg="])
except getopt.GetoptError:
    print "入参错误，请参考"
    usage()
    sys.exit()

if __name__ == '__main__':
    
    #检查入参
    if isNone(options):
        usage()
        sys.exit()

    #检查入参
    for key,value in options:
        if key in ("-h","--help"):
            usage()
            sys.exit()

    print "-----准备工作-----"
    print "  输入参数如下: "
    for key, value in options:
        if key in ("-n","--name"):
            file_name = value
        if key in ("-k","--key"):
            key_token = value
        if key in ("-d","--ding"):
            dingtalk_key = value
        if key in ("-p","--path"):
            build_path = value
        if key in ("-m","--msg"):
            dingtalk_msg = value
        print("    " + key + " --> " + value)

    print "-----开始工作------"
    main()
