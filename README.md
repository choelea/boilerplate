## Langchain API 开发模板
采用conda管理包和环境，工程内的包的import采取绝对路径方式。（以project root目录开始的路径）

### 准备工作
 - Clone 代码
 - 修改文件`environment`中环境的名字，默认是`langchain`； 
 - 安装依赖 `conda env create -f environment.yml`; 这步如果不能科学上网可能会失败，参考下面备注
 - 配置环境变量，项目根目录下创建.env 文件

> 可以选择先创建虚机环境`conda  create -n backend-api python=3.11`, 然后再安装依赖 `pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com`。 

##### 需要配置的环境变量如下：
```properties
PROJECT_NAME=app
BACKEND_CORS_ORIGINS=["*"]

OPENAI_API_KEY=replace with your real key
UNSPLASH_API_KEY=replace with your real key
SERP_API_KEY=replace with your real key
AZURE_OPENAI_API_KEY=replace with your real key#微软Azure OpenAI Key
ZHIPUAI_API_KEY = replace with your real key #智谱


APP_AK = replace with your real key #问学
APP_SK = replace with your real key #问学
APP_APP_ID = replace with your real key #问学
```

### 运行程序
在运行之前需要设置conda的环境：`conda activate backend-api`； 然后在工程根目录运行`./start-dev.sh`; 运行后有两个可以playground的：
- Restful API `/docs`
- 同OpenAI聊天 `/chat`
Linux部署可以尝试`conda activate backend-api`然后使用`./start.sh`，这个脚本会在后台运行程序, 在`logs/app.log` 跟踪日志。

### 更新代码
更新代码后导出环境 `conda env export > environment.yml`，然后提交代码。也可以导出依赖 `pip freeze > requirements.txt`，但是这个文件不会被conda管理。不过requirements.txt可以用pip命令来在虚机环境中安装依赖。
```
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple        #清华源安装
  pip install -r requirements.txt -i https://pypi.douban.com/simple/        #豆瓣源安装
  pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```
