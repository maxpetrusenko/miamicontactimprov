"""The three-plan card grid shared by /pricing and /membership: Drop-in $20, Monthly $40
(the highlighted plan), Yearly $260. One place for the plan facts so the two pages cannot
drift. Cards only carry plan facts; the buy buttons are passed in by the page, because
/pricing links the memberships to /membership while /membership checks out in place.
"""

MONTHLY_ITEMS = [
    "4 classes each billing month",
    "Unused classes don't carry over",
    "Credit returns if we cancel a class",
    "Cancel any time from your confirmation email",
]
YEARLY_ITEMS = [
    "One class every week, 52 in the year",
    "Credit returns if we cancel a class",
    "Cancel any time from your confirmation email",
]
DROP_IN_ITEMS = [
    "$20, $30 after 3pm on Friday",
    "Friday class, 7:00 to 7:45",
    "Promotion codes apply online",
    "Online sales close 2 hours before class",
    "At the door: $30 to $50, pay what you can",
    "Full refund if we cancel",
]


def _card(name, amount, per, tag, cta, items, featured=False, save=""):
    top = (
        '<div class="plan-top">Most popular</div>'
        if featured
        else '<div class="plan-top empty" aria-hidden="true">&nbsp;</div>'
    )
    save_html = f'<span class="plan-save">{save}</span>' if save else ""
    lis = "".join(f"<li>{i}</li>" for i in items)
    cls = "plan hi" if featured else "plan"
    return (
        f'<section class="{cls}">{top}<div class="plan-body">'
        f'<h2 class="plan-name">{name}</h2>'
        f'<div class="plan-price"><b>{amount}</b><span>/{per}</span></div>'
        f'<p class="plan-tag">{tag}{save_html}</p>'
        f'<div class="plan-cta">{cta}</div>'
        f"<ul>{lis}</ul></div></section>"
    )


def drop_in(cta):
    return _card("Drop-in", "$20", "class", "Try one Friday class.", cta, DROP_IN_ITEMS)


def monthly(cta):
    return _card("Monthly", "$40", "month", "Four classes a month.", cta, MONTHLY_ITEMS, featured=True)


def yearly(cta):
    return _card(
        "Yearly", "$260", "year", "A class every week.", cta, YEARLY_ITEMS,
        save="$260 vs $480 paying monthly",
    )


def grid(*cards):
    return f'<div class="plans plans-{len(cards)}">{"".join(cards)}</div>'
