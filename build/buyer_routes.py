"""Routes and sitemap rows for the H006 buyer-intent pages. No imports, so locales.py can read it."""

ROUTES = {
    "buy-class-tickets": "/contact-improv-class-tickets-miami",
    "buy-jam-cost": "/contact-improv-jam-cost-miami",
}

# slug -> (sitemap priority, changefreq)
SITEMAP = {"buy-class-tickets": ("0.8", "weekly"), "buy-jam-cost": ("0.7", "weekly")}
