"""One read of the public r/news hot listing.

The script does not post, comment, vote, message, or moderate.
Run it by hand, or at most about every 30 minutes.
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from filter_rules import tags_for

APP = "news-reader"
VERSION = "0.1"
LISTING = "https://oauth.reddit.com/r/news/hot?limit=25"
KEPT_FIELDS = ("title", "url", "score", "num_comments", "created_utc", "permalink")


def _headers(token, username):
    return {
        "Authorization": f"bearer {token}",
        "User-Agent": f"python:{APP}:{VERSION} (by /u/{username})",
        "Accept": "application/json",
    }


def fetch_hot(token, username):
    request = Request(LISTING, headers=_headers(token, username), method="GET")
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    posts = []
    for child in payload["data"]["children"]:
        data = child["data"]
        posts.append({field: data.get(field) for field in KEPT_FIELDS})
    return posts


def select(posts):
    chosen = []
    for post in posts:
        tags = tags_for(post.get("title") or "")
        if not tags:
            continue
        post = dict(post)
        post["tags"] = tags
        chosen.append(post)
    return chosen


def _line(post):
    when = datetime.fromtimestamp(post["created_utc"], timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tags = ",".join(post["tags"])
    title = " ".join((post.get("title") or "").split())
    return f"{when}  {tags:<16}  {post.get('score')} pts  {post.get('num_comments')} comments  {title}"


def main():
    try:
        token = os.environ["REDDIT_TOKEN"]
        username = os.environ["REDDIT_USERNAME"]
    except KeyError as missing:
        print(f"Set {missing.args[0]} in the environment. Do not put it in this repository.", file=sys.stderr)
        return 1
    try:
        posts = fetch_hot(token, username)
    except HTTPError as exc:
        print(f"Reddit returned HTTP {exc.code}.", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        print(f"Could not read the listing: {exc.__class__.__name__}.", file=sys.stderr)
        return 1
    chosen = select(posts)
    print(f"r/news hot: {len(posts)} posts, {len(chosen)} matched politics or finance")
    for post in chosen:
        print(_line(post))
    return 0


if __name__ == "__main__":
    sys.exit(main())
