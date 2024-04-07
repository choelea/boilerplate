#!/bin/bash

# 配置部分
APP_MODULE="app.main:app" # 你的FastAPI应用，格式为module:instance
HOST="0.0.0.0"
PORT=8000
LOGFILE="logs/uvicorn.log"

git pull

# 使用lsof命令找到指定端口的进程PID并杀死该进程
PID=$(lsof -ti:$PORT)
if [ ! -z "$PID" ]; then
  echo "Stopping Uvicorn process on port $PORT..."
  kill -9 $PID
fi

# 等待一小段时间确保进程已经完全停止
sleep 2

# 重新启动Uvicorn
echo "Starting Uvicorn..."

nohup uvicorn $APP_MODULE --host $HOST --port $PORT > $LOGFILE 2>&1 &

echo "Uvicorn restarted successfully."%  