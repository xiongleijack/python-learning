"""Review 通知（钉钉 / 企微 / Slack webhook）。"""

from __future__ import annotations

import json
import urllib.request

from .config import NOTIFY_WEBHOOK_URL


def notify_review(title: str, detail: str) -> None:
    if not NOTIFY_WEBHOOK_URL:
        print(f"[notify mock] {title}\n{detail}")
        return

    payload = json.dumps({"text": f"{title}\n{detail}"}).encode("utf-8")
    req = urllib.request.Request(
        NOTIFY_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"通知已发送: {resp.status}")
