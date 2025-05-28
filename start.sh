#!/bin/bash

echo "================================================"
echo "  Travel Mood Planner セットアップ"
echo "================================================"

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Docker Composeコマンドの検出
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo -e "${RED}エラー: Docker Composeが見つかりません。${NC}"
    exit 1
fi

echo "Docker Composeコマンド: $DOCKER_COMPOSE"

# Dockerが起動しているか確認
echo -n "Docker Desktopの状態を確認中... "
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗${NC}"
    echo ""
    echo -e "${RED}エラー: Docker Desktopが起動していません。${NC}"
    echo "Docker Desktopを起動してから再度実行してください。"
    exit 1
fi
echo -e "${GREEN}✓${NC}"

# 既存のコンテナをクリーンアップ
echo -n "既存のコンテナをクリーンアップ中... "
$DOCKER_COMPOSE down > /dev/null 2>&1
echo -e "${GREEN}✓${NC}"

# Dockerイメージのビルド
echo ""
echo "Dockerイメージをビルドしています..."
echo "（初回は10-15分程度かかる場合があります）"
$DOCKER_COMPOSE build

if [ $? -ne 0 ]; then
    echo -e "${RED}ビルドに失敗しました。${NC}"
    exit 1
fi

# サービスの起動
echo ""
echo "サービスを起動しています..."
$DOCKER_COMPOSE up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}サービスの起動に失敗しました。${NC}"
    exit 1
fi

# サービスが起動するまで待機
echo ""
echo "サービスが起動するまで待機中..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 1
done
echo ""

# データベースマイグレーション
echo ""
echo "データベースをセットアップ中..."
$DOCKER_COMPOSE exec -T backend alembic upgrade head 2>/dev/null || echo "マイグレーションをスキップ"

# 初期データの投入
echo "初期データを投入中..."
$DOCKER_COMPOSE exec -T backend python scripts/seed_data.py 2>/dev/null || echo "シードデータ投入をスキップ"

echo ""
echo "================================================"
echo -e "${GREEN}✅ セットアップが完了しました！${NC}"
echo "================================================"
echo ""
echo "🌐 アプリケーションURL:"
echo "   フロントエンド: http://localhost:3000"
echo "   API ドキュメント: http://localhost:8000/docs"
echo ""
