#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitHub Actions のワークフロー実行履歴を削除するスクリプト

使用方法:
1. GitHub Personal Access Token を取得して環境変数 GITHUB_TOKEN に設定
2. スクリプトを実行: python cleanup_workflow_runs.py

オプション:
--keep-latest N: 最新のN件のワークフロー実行を残す（デフォルト: 10）
--keep-successful: 成功したワークフロー実行を残す
--branch BRANCH: 特定のブランチのワークフロー実行のみを削除
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
import time

# GitHub APIのベースURL
API_BASE = "https://api.github.com"

def get_github_token():
    """環境変数からGitHub Tokenを取得"""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("エラー: 環境変数 GITHUB_TOKEN が設定されていません。")
        print("GitHub Personal Access Token を取得して設定してください。")
        sys.exit(1)
    return token

def get_workflow_runs(owner, repo, token, branch=None, status=None):
    """ワークフロー実行の一覧を取得"""
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {}
    if branch:
        params["branch"] = branch
    if status:
        params["status"] = status
    
    all_runs = []
    page = 1
    
    while True:
        params["page"] = page
        params["per_page"] = 100
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"エラー: ワークフロー実行の取得に失敗しました。ステータスコード: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        data = response.json()
        runs = data.get("workflow_runs", [])
        if not runs:
            break
        
        all_runs.extend(runs)
        page += 1
        
        # GitHubのAPI制限に引っかからないよう少し待機
        time.sleep(0.5)
    
    return all_runs

def delete_workflow_run(owner, repo, run_id, token):
    """ワークフロー実行を削除"""
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

def main():
    parser = argparse.ArgumentParser(description="GitHub Actionsのワークフロー実行履歴を削除します")
    parser.add_argument("--owner", help="リポジトリのオーナー名", default="tkykszk")
    parser.add_argument("--repo", help="リポジトリ名", default="logkiss")
    parser.add_argument("--keep-latest", type=int, help="残す最新のワークフロー実行数", default=10)
    parser.add_argument("--keep-successful", action="store_true", help="成功したワークフロー実行を残す")
    parser.add_argument("--branch", help="特定のブランチのワークフロー実行のみを削除")
    parser.add_argument("--dry-run", action="store_true", help="実際に削除せずに何が削除されるかを表示")
    args = parser.parse_args()
    
    token = get_github_token()
    
    print(f"リポジトリ {args.owner}/{args.repo} のワークフロー実行を取得中...")
    runs = get_workflow_runs(args.owner, args.repo, token, branch=args.branch)
    
    print(f"合計 {len(runs)} 件のワークフロー実行が見つかりました。")
    
    # 最新のN件を除外
    runs_to_keep = runs[:args.keep_latest]
    runs_to_delete = runs[args.keep_latest:]
    
    # 成功したワークフロー実行を除外（オプション）
    if args.keep_successful:
        runs_to_delete = [run for run in runs_to_delete if run["conclusion"] != "success"]
    
    print(f"削除対象: {len(runs_to_delete)} 件")
    
    if args.dry_run:
        print("ドライラン: 以下のワークフロー実行が削除対象です")
        for run in runs_to_delete:
            created_at = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            print(f"ID: {run['id']}, 名前: {run['name']}, ブランチ: {run['head_branch']}, "
                  f"ステータス: {run['conclusion']}, 作成日時: {created_at}")
        return
    
    # 削除実行
    deleted_count = 0
    for run in runs_to_delete:
        run_id = run["id"]
        if delete_workflow_run(args.owner, args.repo, run_id, token):
            deleted_count += 1
            print(f"ワークフロー実行 ID: {run_id} を削除しました。")
        else:
            print(f"ワークフロー実行 ID: {run_id} の削除に失敗しました。")
        
        # GitHubのAPI制限に引っかからないよう少し待機
        time.sleep(1)
    
    print(f"合計 {deleted_count} 件のワークフロー実行を削除しました。")

if __name__ == "__main__":
    main()
