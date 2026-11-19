"""Local title filter. Applied only after a listing response is received."""

import re

_POLITICS = (
    "election",
    "senate",
    "congress",
    "parliament",
    "president",
    "white house",
    "sanction",
    "ceasefire",
    "diplomat",
    "military",
    "ukraine",
    "tariff",
)

_FINANCE = (
    "interest rate",
    "inflation",
    "federal reserve",
    "central bank",
    "stock",
    "bond",
    "treasury",
    "recession",
    "oil price",
    "bank",
    "tariff",
)


def _hit(title, phrase):
    if " " in phrase:
        return phrase in title
    return re.search(rf"\b{re.escape(phrase)}\b", title) is not None


def tags_for(title):
    """Return politics and/or finance, or an empty list when the title is neither."""
    text = title.casefold()
    tags = []
    if any(_hit(text, phrase) for phrase in _POLITICS):
        tags.append("politics")
    if any(_hit(text, phrase) for phrase in _FINANCE):
        tags.append("finance")
    return tags
