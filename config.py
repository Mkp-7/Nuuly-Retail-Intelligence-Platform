"""
Configuration - edit this file to target any app.

To switch to a different company:
1. Update APP_STORE_ID with the Apple App Store app ID
2. Update APP_NAME, PLATFORM_TITLE, PLATFORM_SUBTITLE, PLATFORM_ICON
3. Commit and push - GitHub Actions runs the scraper automatically
4. Streamlit Cloud redeploys automatically

How to find APP_STORE_ID:
  Go to apps.apple.com, search the app, look at the URL:
  apps.apple.com/us/app/nuuly/id1511548818
  The number after 'id' is the APP_STORE_ID → 1511548818
"""

# ── Target App ────────────────────────────────────────────────────────────────
APP_STORE_ID   = "1511548818"       # Apple App Store numeric ID
APP_NAME       = "Nuuly"            # Human readable name for AI prompts
APP_COUNTRY    = "us"               # Country code for App Store

# ── Platform Branding ─────────────────────────────────────────────────────────
PLATFORM_TITLE    = "Retail Intelligence Platform"
PLATFORM_SUBTITLE = "Customer Insights & Operations"
PLATFORM_ICON     = "🏪"

# ── AI Model ─────────────────────────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Scraper Settings ──────────────────────────────────────────────────────────
MAX_REVIEW_PAGES = 10          # iTunes RSS gives 50 reviews/page, max 10 pages = 500 reviews

# ── Data Paths ────────────────────────────────────────────────────────────────
DATA_DIR      = "data"
REVIEWS_CSV   = "data/reviews.csv"
BUSINESSES_CSV = "data/businesses.csv"   # not used for App Store mode

# ── Analytics Settings ────────────────────────────────────────────────────────
ANOMALY_THRESHOLD_STARS  = 0.4
SIGNIFICANT_DELTA_STARS  = 0.3
