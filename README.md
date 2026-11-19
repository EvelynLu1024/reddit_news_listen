# news-reader

A private, read-only script. Each run reads the public hot listing of three communities and keeps posts whose titles match a local topic list. The result is printed for a private page that only I use.

| Community | What it is for |
| --- | --- |
| [r/worldnews](https://www.reddit.com/r/worldnews/) | international news |
| [r/geopolitics](https://www.reddit.com/r/geopolitics/) | geopolitics |
| [r/Economics](https://www.reddit.com/r/Economics/) | macroeconomics |

Topics kept: elections, diplomacy, central banks, trade, energy, and financial markets. Everything else is discarded.

This is not a moderator bot, not a subreddit app, and not a service for other people.

## Why this is not a Devvit app

Devvit apps run inside a subreddit, in JavaScript. They cannot export listings from these three communities to an external private page, and they have no Python runtime. This script has to run outside Reddit, so Devvit does not fit.

## What it requests

Three requests when the script is run, one listing each:

```text
GET https://oauth.reddit.com/r/worldnews/hot?limit=25
GET https://oauth.reddit.com/r/geopolitics/hot?limit=25
GET https://oauth.reddit.com/r/Economics/hot?limit=25
```

OAuth scope: `read`.

From each post it keeps only:

| Field | Use |
| --- | --- |
| `title` | local topic match |
| `url` | the outbound article link |
| `score` | shown on the private page |
| `num_comments` | shown on the private page |
| `created_utc` | shown on the private page |
| `permalink` | link back to the Reddit thread |

No other subreddit is requested. The script is meant to be run by hand, or on a timer of about 30 minutes. That is three listing requests per run, not a crawl.

The `User-Agent` is `python:news-reader:0.2 (by /u/<reddit username>)`.

## What it does not do

- No submit, comment, vote, save, subscribe, message, or moderator action.
- No account data, no private messages, no user profiles.
- The filtered lines stay on a private page. They are not republished on a public or monetized site.
- The text is not used to train a model.
- The token and username come from environment variables. They are not committed.

## Layout

```text
news_reader.py    three GETs, then print the matches
filter_rules.py   title words for the six topics
```

Matching is local, in `filter_rules.py`. Examples: `election` and `referendum`; `sanction`, `embassy`, and `ceasefire`; `central bank` and `interest rate`; `tariff` and `trade deal`; `crude`, `opec`, and `natural gas`; `stock market`, `treasury`, and `bond yield`. A title that matches none of them is discarded.

## Run

Python 3.9 or newer. No third-party packages.

```text
set REDDIT_TOKEN=the-oauth-token
set REDDIT_USERNAME=your-reddit-username
python news_reader.py
```

Example of the local printout:

```text
r/worldnews hot: 25 posts, 1 matched
2026-11-19 06:37 UTC  r/worldnews  [diplomacy]  120 pts  14 comments  Example headline about a ceasefire
r/geopolitics hot: 25 posts, 1 matched
2026-11-19 05:10 UTC  r/geopolitics  [trade]  40 pts  6 comments  Example headline about a tariff
r/Economics hot: 25 posts, 1 matched
2026-11-19 04:10 UTC  r/Economics  [central-bank,markets]  80 pts  9 comments  Example headline about an interest rate
```

The titles above are format examples, not posts fetched by this repository.
