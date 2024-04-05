## Langchain API 开发模板
采用conda管理包和环境，工程内的包的import采取绝对路径方式。（以project root目录开始的路径）

### 准备工作
 - Clone 代码
 - 修改文件`environment`中环境的名字，默认是`langchain`； 
 - 安装依赖 `conda env create -f environment.yml`
 - 配置环境变量，项目根目录下创建.env 文件

##### 需要配置的环境变量如下：
```properties
PROJECT_NAME=app
BACKEND_CORS_ORIGINS=["*"]
OPENAI_API_KEY=replace with your real key

UNSPLASH_API_KEY=replace with your real key
SERP_API_KEY=replace with your real key
```

### 运行程序
在根目录运行`./start.sh`; 运行后有两个可以playground的：
- Restful API `/docs`
- 同OpenAI聊天 `/chat`
