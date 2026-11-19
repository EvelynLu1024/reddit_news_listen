# news-reader

A private, read-only script. It reads the public hot listing of [r/news](https://www.reddit.com/r/news/) and keeps posts whose titles match a local politics or finance list. The result is printed for a private page that only I use.

This is not a moderator bot, not a subreddit app, and not a service for other people.

## Why this is not a Devvit app

Devvit apps run inside a subreddit, in JavaScript. They cannot export a listing to an external private page, and they have no Python runtime. This script has to run outside Reddit, so Devvit does not fit.

## What it requests

One request when the script is run:

`GET https://oauth.reddit.com/r/news/hot?limit=25`

OAuth scope: `read`.

From each post it keeps only:

| Field | Use |
| --- | --- |
| `title` | local politics / finance match |
| `url` | the outbound article link |
| `score` | shown on the private page |
| `num_comments` | shown on the private page |
| `created_utc` | shown on the private page |
| `permalink` | link back to the Reddit thread |

No other subreddit is requested. The script is meant to be run by hand, or on a timer of about 30 minutes. That is one listing request, not a crawl.

The `User-Agent` is `python:news-reader:0.1 (by /u/<reddit username>)`.

## What it does not do

- No submit, comment, vote, save, subscribe, message, or moderator action.
- No account data, no private messages, no user profiles.
- The filtered lines stay on a private page. They are not republished on a public or monetized site.
- The text is not used to train a model.
- The token and username come from environment variables. They are not committed.

## Layout

```text
news_reader.py    one GET, then print the matches
filter_rules.py   title words for politics and finance
```

Matching is local. Words such as `senate`, `sanction`, `inflation`, and `interest rate` are in `filter_rules.py`. A title that matches none of them is discarded.

## Run

Python 3.9 or newer. No third-party packages.

```text
set REDDIT_TOKEN=the-oauth-token
set REDDIT_USERNAME=your-reddit-username
python news_reader.py
```

Example of the local printout:

```text
r/news hot: 25 posts, 2 matched politics or finance
2026-11-19 06:37 UTC  politics          120 pts  14 comments  Example headline about a senate vote
2026-11-19 04:10 UTC  finance           80 pts  9 comments  Example headline about an interest rate
```

The two titles above are format examples, not posts fetched by this repository.
