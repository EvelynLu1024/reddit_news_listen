"""One read of three public hot listings.

The script does not post, comment, vote, message, or moderate.
Run it by hand, or at most about every 30 minutes.
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from filter_rules import tags_for

APP = "news-reader"
VERSION = "0.2"
# r/worldnews: international news. r/geopolitics: geopolitics. r/Economics: macroeconomics.
SUBREDDITS = ("worldnews", "geopolitics", "Economics")
KEPT_FIELDS = ("title", "url", "score", "num_comments", "created_utc", "permalink")


def _headers(token, username):
    return {
        "Authorization": f"bearer {token}",
        "User-Agent": f"python:{APP}:{VERSION} (by /u/{username})",
        "Accept": "application/json",
    }


def fetch_hot(token, username, subreddit):
    url = f"https://oauth.reddit.com/r/{quote(subreddit)}/hot?limit=25"
    request = Request(url, headers=_headers(token, username), method="GET")
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    posts = []
    for child in payload["data"]["children"]:
        data = child["data"]
        post = {field: data.get(field) for field in KEPT_FIELDS}
        post["subreddit"] = subreddit
        posts.append(post)
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
    return f"{when}  r/{post['subreddit']}  [{tags}]  {post.get('score')} pts  {post.get('num_comments')} comments  {title}"


def main():
    try:
        token = os.environ["REDDIT_TOKEN"]
        username = os.environ["REDDIT_USERNAME"]
    except KeyError as missing:
        print(f"Set {missing.args[0]} in the environment. Do not put it in this repository.", file=sys.stderr)
        return 1
    failures = 0
    for subreddit in SUBREDDITS:
        try:
            posts = fetch_hot(token, username, subreddit)
        except HTTPError as exc:
            failures += 1
            print(f"r/{subreddit}: Reddit returned HTTP {exc.code}.", file=sys.stderr)
            continue
        except (URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            failures += 1
            print(f"r/{subreddit}: could not read the listing ({exc.__class__.__name__}).", file=sys.stderr)
            continue
        chosen = select(posts)
        print(f"r/{subreddit} hot: {len(posts)} posts, {len(chosen)} matched")
        for post in chosen:
            print(_line(post))
    return 1 if failures == len(SUBREDDITS) else 0


if __name__ == "__main__":
    sys.exit(main())
