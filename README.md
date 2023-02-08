<!--
 * @Author: MeowKJ
 * @Date: 2021-11-22 01:41:22
 * @LastEditors: MeowKJ ijink@qq.com
 * @LastEditTime: 2023-02-08 14:13:36
 * @FilePath: /chat-meow/README.md
-->
# ChatMeow

## 开始

### 1.克隆本项目到OrangePi (使用Unbuntu20.04系统为例)，并安装依赖喵

`git clone https://github.com/meowkj/chat-meow.git && cd chat-meow`

安装必备依赖

```sh
apt-get update -y && RUN apt-get install -y python3-dev portaudio19-dev python3-pyaudio
pip install Flask openai PyAudio PyYAML requests
```

或者使用准备好的Docker镜像(beta)

```sh
docker pull kjqaq/chatmeow
```

#### 2.获取百度和openai的key喵

#### 百度

获取百度云KEY，需要有短文字识别，语音合成权限
百度官方文档地址

- 语音识别：<http://ai.baidu.com/docs#/ASR-API/top>
- 语音合成：<http://ai.baidu.com/docs#/TTS-API/top>

#### openai

openai apikey 查看链接
<https://platform.openai.com/account/api-keys>

根目录下创建**key.yml**文件，按照如下格式填入

```yaml
BAIDU_KEY:
  - "4E1BG9lTnlSeIf1NQFlrxxxx"           # 填写网页上申请的appkey
  - "544ca4657ba8002e3dea3ac2f5fxxxxx"   # 填写网页上申请的APP SECRET
  - "123456PYTHON"                       # 填写一个CUID 只是用来区分不同应用 随意填写

OPENAI_API_KEY: "sk-xxxxxxxxxxxxxxxxxxxxx" # openai的apikey
```

### 3.运行喵

在根目录下
使用自己的python环境
`python3 mian.py &`

使用docker提供的环境(beta)
`docker run --itd -v .:/chat --privileged -itd kjqaq/chatmeow`
