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

echo "Travel Mood Planner クイックスタート"
echo ""

# .envファイルが存在しない場合はコピー
if [ ! -f .env ]; then
    echo ".envファイルを作成しています..."
    cp .env.example .env
fi

# Dockerコンテナの起動
$DOCKER_COMPOSE up -d

echo ""
echo "✅ 起動完了！"
echo "フロントエンド: http://localhost:3000"
echo "API: http://localhost:8000/docs"
