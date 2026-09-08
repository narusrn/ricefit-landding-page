# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Streamlit landing/docs site for the RiceFit API (NECTEC), deployed on Streamlit Community Cloud at `ricefit-landding-page-wcbsvzpxrxwy5atzdeuxdf.streamlit.app`. Lets developers read API docs and register for API access; registration provisions a real API key from an external NECTEC endpoint and emails it to the applicant.

## Running it

```
pip install -r requirements.txt
streamlit run app.py
```

`requirements.txt` lists `streamlit`, `oauth2client`, `google-api-python-client`, `python-dotenv` — `pandas` and `requests` are also imported directly (in the API-doc pages and `register.py`) but arrive only as transitive deps of `streamlit`/`altair`, not pinned explicitly; if a page ever fails to import one of them on a fresh install, that's why.

No test suite or linter is configured. `.github/workflows/codeql.yml` runs GitHub's CodeQL scan on push/PR; `.github/workflows/keep_awake.yml` pushes an empty commit every 5 hours purely to stop the Streamlit Cloud app from sleeping — don't mistake that commit history for real changes.

Secrets (`st.secrets[...]`) aren't in this repo — `GOOGLE_APPLICATION_CREDENTIALS` and the `EMAIL` block (see below) must be configured via Streamlit Cloud's secrets manager, or a local `.streamlit/secrets.toml` (gitignored) for local runs. `ricefit-bot-google.json` (a real service-account key) and `.env` also live at the repo root and are gitignored — never add them to a commit.

## Navigation is fully manual — not Streamlit's auto-nav

`.streamlit/config.toml` sets `showSidebarNavigation = false`, so Streamlit's automatic page list is off. The entire sidebar is built by `utils.sidebar_options()`, which every page calls near the top (right after `st.set_page_config(...)`):

```python
from utils import sidebar_options
st.set_page_config(...)
sidebar_options()
```

**Adding a new page means adding a `st.sidebar.page_link(...)` entry in `utils.py` — a new file under `pages/` alone will not appear anywhere.**

`app.py` itself is not a real landing page: it sets minimal config and immediately does `st.switch_page("pages/getting_started.py")`, so `getting_started.py` is the actual home page.

Pages:
- `pages/getting_started.py` — static walkthrough (OAuth flow, links to `/register`).
- `pages/register.py` — the registration form + confirm dialog.
- `pages/apidocs.py` — just links out to NECTEC's own hosted Swagger UI; it does not contain docs itself, which is a little confusing alongside the pages below that *do*.
- `pages/rice_phenotype_api_docs.py`, `pages/ricefit_api_docs.py`, `pages/ricefit_forecast_api_docs.py` — the actual embedded API reference pages, one per RiceFit endpoint (`/rice/phenotype`, `/ricefit`, `/ricefit_forecast`). These three share one visual theme (see below) and are the ones to copy when documenting a new endpoint.
- `pages/apidocs/getting_started.py` is leftover local dead code, not part of the deployed app (Streamlit doesn't recurse into `pages/` subdirectories, and it isn't referenced from `utils.py` either) — untracked in git, safe to ignore or delete.

## API doc page theme

Each of the three `*_api_docs.py` pages follows the same layout — reuse this structure for any future endpoint:
1. `st.set_page_config(page_title="RiceFit API – <Name>", layout="wide")` → `sidebar_options()` → header + one-paragraph description.
2. "API Overview": two columns — Name/Endpoint | Method/Description.
3. `---`, then two columns (~1.2–1.3 : 1):
   - Left: Request Headers table (`accept`, `apikey`) → Query Parameters table → any reference data (e.g. rice-variety list) → Response Codes table (400/401/404/500).
   - Right: Example Request (`curl`, base URL varies by environment) → Example JSON Response.
4. `---`, then "Response Reference": a field/type/description data-dictionary table, plus a legend/note block for anything with a non-obvious scale or counter semantics.

## Registration flow (`pages/register.py`)

`st.form` → validation → `register_confirm()` (`@st.dialog`) → on confirm, in order:
1. `recording_submission(data)` — audit log only: appends a row to a hardcoded Google Sheet via a service-account (`st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]`).
2. `get_api_key(client_name)` — calls NECTEC's real key-issuance endpoint (`.../digital-agri-api/apikeys/store`) to provision the actual API key.
3. `send_api_key_email(...)` — emails that key via SMTP\_SSL using `st.secrets["EMAIL"]` (`SENDER_EMAIL`, `SENDER_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT`).

Step 1 failing is swallowed (logged to stderr only) and doesn't block key issuance/email — the Sheet is just a log, not the source of truth for who has a key.
