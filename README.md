# FastlaneUsage
To introduce the `fastlane` usage.
Blog: http://devhy.com/2018/01/23/26-fastlane-usage/


- Update 2018-04-03
	
	增加打包后续支持的python脚本，具体用法可执行`python iOS_test_pgy.py --help`查看说明
	建议在`jenkins + fastlane`下使用，构建完成时调用脚本即可实现后续上传ipa到蒲公英并通过钉钉机器人发送消息到群组。
	
	```shell
		# ${WORKSPACE}是jenkins自带环境变量，其他变量是在jenkins中自定义环境变量
		/usr/bin/python ~/Desktop/iOS_test_pgy.py -p ${WORKSPACE}/build -n ${AppName} -k ${PgyToken} -d ${DingToken} -m 说明:${DingMsg}
	```


