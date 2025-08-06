import requests
from datetime import datetime
import os

# === 需要配置 ===
GITHUB_OWNER = "luoboluoboHu61"
GITHUB_REPO = "ci-build-explorer"
GITHUB_TOKEN = "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"

# === API 核心函数 ===
def get_workflow_runs():
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "per_page": 10  # 最多获取10条构建记录
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ GitHub API Error: {response.status_code} – {response.text}")
        return []

    data = response.json()
    runs = data.get("workflow_runs", [])

    result = []
    for run in runs:
        result.append({
            "id": run["id"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "branch": run["head_branch"],
            "commit_msg": run["head_commit"]["message"] if run["head_commit"] else "N/A",
            "start_time": run["run_started_at"],
            "end_time": run["updated_at"] if run["status"] == "completed" else None
        })

    return result
