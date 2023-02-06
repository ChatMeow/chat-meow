<!--
 * @Author: MeowKJ
 * @Date: 2021-11-22 01:41:22
 * @LastEditors: MeowKJ ijink@qq.com
 * @LastEditTime: 2023-02-02 16:37:44
 * @FilePath: /ChatMeow/README.md
-->

## 百度语言识别说明

### 食用方法

使用python 脚本方式测试rest api 识别接口

根目录下创建**key.yml**文件

从网页中申请的应用获取appKey和appSecret
同时设置设置 CUID字段， 这是用户唯一标识，用来区分用户，计算 UV 值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为 60 字符以内。

```yaml
BAIDU_KEY:
  - "4E1BG9lTnlSeIf1NQFlrxxxx"           # 填写网页上申请的appkey 如 API_KEY="g8eBUMSokVB1BHGmgxxxxxx"
  - "544ca4657ba8002e3dea3ac2f5fxxxxx"   # 填写网页上申请的APP SECRET 如 SECRET_KEY="94dc99566550d87f8fa8ece112xxxxx"
  - "123456PYTHON"                       # 填写一个CUID

OPENAI_API_KEY: "sk-xxxxxxxxxxxxxxxxxxxxx" # 这里是openai的apikey

```

[百度短语音识别标准版文档](https://ai.baidu.com/ai-doc/SPEECH/ek38lxj1u)
