Travel Mood Planner - 起動と終了方法
起動方法
初回起動（セットアップ含む）
bash./start.sh
2回目以降の起動（高速）
bashdocker compose up -d
または
bash./quickstart.sh
終了方法
通常の終了（データは保持）
bash./stop.sh
または
bashdocker compose down
完全に削除（データも削除）
bashdocker compose down -v
その他便利なコマンド
ログを見る
bash./logs.sh
状態確認
bashdocker compose ps
再起動
bashdocker compose restart
