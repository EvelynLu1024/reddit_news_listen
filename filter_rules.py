"""Local title filter. Applied only after a listing response is received."""

import re

# Six topics. A title must match at least one.
TOPICS = {
    "election": (
        "election",
        "elections",
        "electoral",
        "ballot",
        "referendum",
        "candidate",
        "campaign",
        "polling",
    ),
    "diplomacy": (
        "diplomat",
        "diplomacy",
        "embassy",
        "ambassador",
        "sanction",
        "sanctions",
        "treaty",
        "summit",
        "ceasefire",
        "foreign minister",
    ),
    "central-bank": (
        "central bank",
        "federal reserve",
        "interest rate",
        "rate hike",
        "rate cut",
        "monetary policy",
        "ecb",
        "inflation",
    ),
    "trade": (
        "tariff",
        "tariffs",
        "trade deal",
        "trade war",
        "export ban",
        "import ban",
        "wto",
        "customs",
    ),
    "energy": (
        "oil price",
        "crude",
        "opec",
        "lng",
        "natural gas",
        "pipeline",
        "refinery",
        "energy price",
    ),
    "markets": (
        "stock market",
        "bond market",
        "financial market",
        "treasury",
        "bond yield",
        "wall street",
        "sell-off",
        "selloff",
        "recession",
    ),
}


def _hit(title, phrase):
    if " " in phrase or "-" in phrase:
        return phrase in title
    return re.search(rf"\b{re.escape(phrase)}\b", title) is not None


def tags_for(title):
    """Return the topic names that match, or an empty list."""
    text = title.casefold()
    return [name for name, phrases in TOPICS.items() if any(_hit(text, phrase) for phrase in phrases)]
