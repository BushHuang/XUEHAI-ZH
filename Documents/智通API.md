# 智通API详解
## 注意事项
- 该文档计划收录ZTY/ZTP的API，即[ztp.yunzuoye.net](ztp.yunzuoye.net)
- 除非特别标注，均需[签名](https://github.com/BushHuang/XUEHAI-ZH/blob/main/Documents/%E5%AD%A6%E6%B5%B7%E7%AD%BE%E5%90%8D.md)
- 请求头中的User-Agent应设为`<应用包名>/<应用版本号> (<设备型号>; android; <安卓系统版本号>; <你的设备号>)`，示例：`com.xuehai.launcher/v1.21.06.20251212hwS (SM-P200; android; 9; FUCXUEHAI)`
- 
## 检查动态码（checkBrushCode）
- 介绍：这是一个用于检查动态码的API。它接收一个动态码和设备ID
- 类型：RESTful
- URL：`https://ztp.yunzuoye.net/api/v2/pub/platform/brushCode`
- 方法：PATCH
- 入参：
  - `code`: 输入的动态码。
  - `deviceId`: 设备ID
- 返回内容：动态码是否正确

## 请求平台APK（requestPlatformApk）
- 介绍：该API用于请求下载智通平台的APK
- 类型：REST
- URL：`https://ztp.yunzuoye.net/api/v2/platform/apk`
- 方法：GET
- 入参：
  - `appId`: 智通平台类型，ToC版为`mdm_stu_to_c`,学生版为`mdm_stu`,教师版为`mdm_tea`
  - `versionCode`: ZTY版本号，截至20260210时为1021006，可从com.xuehai.launcher.common.base.BaseApplication.getVersionCode()得到
- 返回内容：智通平台下载URL

## 检查设备（checkDevice）
- 介绍：该API用于远程校验设备ID
- 类型：REST
- URL：`https://ztp.yunzuoye.net/api/v1/pub/platform/check/device`
- 方法：GET
- 入参：
  - `deviceId`: 设备ID。
- 返回内容：未知

## 请求服务器时间戳（requestServerTimestamp）
- 介绍：该API用于请求服务器的当前时间戳，并使用该时间戳更新本地系统时间。
- 类型：REST
- URL：`https://ztp.yunzuoye.net/api/v1/platform/dateTime` 
- 方法：GET
- 入参：无
- 返回内容：服务器时间
