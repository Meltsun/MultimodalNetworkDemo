#!/bin/bash

# 根据传入的是c还是s删除特定的容器
flag=$1
if [ ! -z "$flag" ]; then 
  if [ "$flag" == "c" ];then 
    # 获取特定名称模式的容器列表
    all_containers=$(docker ps -aq --filter "name=c") # 容器名字中有c 即可匹配到，这里直接就是写的正则了
  elif [ "$flag" == "s" ];then 
    # 获取特定名称模式的容器列表
    all_containers=$(docker ps -aq --filter "name=s") # 容器名字中有c 即可匹配到
  else
    echo "传入 c 或者 s删除对应容器。不传入表示删除所有容器"
  fi
else
  all_containers=$(docker ps -aq)
fi

# 将all_containers 中的容器删除
if [ -z "$all_containers" ]; then
  echo "没有Docker容器需要被删除。"
else
  # 逐个检查容器状态
  for container_id in $all_containers; do
    container_status=$(docker inspect -f '{{.State.Status}}' $container_id)
    if [ $container_status == "running" ]; then
      echo "正在停止容器：$container_id..."
      docker kill $container_id
    fi
    echo "正在删除容器：$container_id..."
    docker rm $container_id
  done
  echo "所有指定的Docker容器已被成功删除。"
fi
