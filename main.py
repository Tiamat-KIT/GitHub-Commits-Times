import requests
import datetime
from collections import defaultdict
import os

# GitHubのAPIエンドポイント
API_URL = "https://api.github.com/repos/{owner}/{repo}/commits"

# あなたのGitHubユーザー名とリポジトリ名に置き換えてください
owner = "Tiamat-KIT"
repo = "yumemi-homework-app-retry"

# 個人アクセストークン
token = os.environ['GITHUB_TOKEN']

# ヘッダーにトークンを追加
headers = {
    "Authorization": f"token {token}"
}

# ブランチごとの時間の割合と開発時間を計算
branch_times = defaultdict(int)

# ページネーションを使用して全てのコミットを取得
page = 1
while True:
    response = requests.get(API_URL.format(owner=owner, repo=repo), headers=headers, params={"page": page})
    commits = response.json()
    if not commits:
        break

    # 最初のコミットの日時を開始日として設定
    if page == 1:
        start_date = datetime.datetime.strptime(commits[0]['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")

    # 最後のコミットの日時を終了日として設定
    end_date = datetime.datetime.strptime(commits[-1]['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")

    # ブランチごとの時間の割合と開発時間を計算
    for commit in commits:
        # ここでは、コミットメッセージの最初の行をブランチ名として扱っています。
        # 実際のコミットメッセージの形式に応じてパターンを調整してください。
        branch = commit['commit']['message'].split('\n')[0]
        branch_times[branch] += 1

    page += 1

# 開発にかかった時間を計算
total_time = end_date - start_date

# 結果の表示
print(f"Start date: {start_date}")
print(f"End date: {end_date}")
print(f"Total development time: {total_time}")
print("Branch times and development times:")
for branch, time in branch_times.items():
    print(f"{branch}: {time}")
