"""The eight chapters of the beginner's guide, in reading order.

The chapter list is the single source for: the index, the prev/next links, the print page,
the PDF, llms.txt and the routes in build/locales.py (which carries the slugs because a
route is defined once, there). `check_slugs_agree` stops the build if the two drift.
"""

import locales
from guide_chapters_a import CH1, CH2, CH3, CH4
from guide_chapters_b import CHAPTERS_B

CHAPTERS = [CH1, CH2, CH3, CH4] + CHAPTERS_B

# The credit used on the index, the print page and the PDF.
BOOK_TITLE = "Dancing Deeper Still: The Practice of Contact Improvisation"
BOOK_PUBLISHER = "Intimately Rooted Books"
BOOK_YEAR = "2018"
BOOK_URL = "https://martinkeogh.com/books"


def check_slugs_agree():
    declared = [c["slug"] for c in CHAPTERS]
    if tuple(declared) != tuple(locales.GUIDE_SLUGS):
        raise SystemExit(
            f"guide chapters drift: guide_chapters has {declared}, locales.GUIDE_SLUGS has {list(locales.GUIDE_SLUGS)}"
        )


check_slugs_agree()
