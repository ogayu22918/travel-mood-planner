#!/bin/bash

# Docker Composeコマンドの検出
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "エラー: Docker Composeが見つかりません。"
    exit 1
fi

echo "ログを表示します (Ctrl+Cで終了)"
echo ""
$DOCKER_COMPOSE logs -f
