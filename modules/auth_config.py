"""
Removix Supabase Authentication Configuration
--------------------------------------------
Loads and validates Supabase credentials from .env or environment variables.
"""

import os
from pathlib import Path

# Load .env if present
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
except Exception:
    pass


def get_supabase_config() -> dict:
    """Returns the current Supabase public URL and publishable/anon key."""
    # Re-read in case .env was modified at runtime
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k in ("SUPABASE_URL", "SUPABASE_ANON_KEY"):
                            os.environ[k] = v
        except Exception:
            pass

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_ANON_KEY", "").strip()

    is_configured = bool(
        url
        and key
        and "your-project-id" not in url
        and "your-anon" not in key
        and url.startswith("http")
    )

    return {
        "supabase_url": url,
        "supabase_anon_key": key,
        "configured": is_configured,
    }
