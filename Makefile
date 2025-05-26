.PHONY: help setup build up down logs shell test clean

help:
	@echo "使用可能なコマンド:"
	@echo "  make setup    - 初期セットアップ"
	@echo "  make build    - Dockerイメージのビルド"
	@echo "  make up       - サービスの起動"
	@echo "  make down     - サービスの停止"
	@echo "  make logs     - ログの表示"
	@echo "  make shell    - バックエンドのシェルに入る"
	@echo "  make test     - テストの実行"
	@echo "  make clean    - すべてをクリーンアップ"

setup:
	@echo "初期セットアップを開始します..."
	@cp .env.example .env
	@echo "✅ .envファイルを作成しました"
	@make build
	@make up

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "サービスが起動するまで待機中..."
	@sleep 10
	@echo "データベースマイグレーションを実行中..."
	@docker-compose exec backend alembic upgrade head || echo "マイグレーションをスキップ"
	@echo "初期データを投入中..."
	@docker-compose exec backend python scripts/seed_data.py || echo "シードデータ投入をスキップ"
	@echo ""
	@echo "✅ すべてのサービスが起動しました！"
	@echo ""
	@echo "🌐 フロントエンド: http://localhost:3000"
	@echo "📚 API ドキュメント: http://localhost:8000/docs"
	@echo ""
	@echo "停止するには: make down"

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec backend bash

test:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/.next
	rm -rf frontend/node_modules
