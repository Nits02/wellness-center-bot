"""Supabase client initialization for the Wellness Center POC."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from supabase import Client, create_client


def _first_non_empty(*values: str | None) -> str | None:
    """Return the first non-empty string value from a list of candidates."""
    for value in values:
        if value and value.strip():
            return value.strip()
    return None


def get_supabase_client() -> Client:
    """Create and return a Supabase client using environment variables.

    Expected variables:
    - SUPABASE_URL
    - One of: SUPABASE_SECRET_KEY, SUPABASE_SERVICE_ROLE_KEY,
      SUPABASE_ANON_KEY, SUPABASE_PUBLISHABLE_KEY
    """
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = _first_non_empty(
        os.getenv("SUPABASE_SECRET_KEY"),
        os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        os.getenv("SUPABASE_ANON_KEY"),
        os.getenv("SUPABASE_PUBLISHABLE_KEY"),
    )

    if not supabase_url:
        raise ValueError("Missing required environment variable: SUPABASE_URL")
    if not supabase_key:
        raise ValueError(
            "Missing Supabase key. Set one of SUPABASE_SECRET_KEY, "
            "SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ANON_KEY, or SUPABASE_PUBLISHABLE_KEY"
        )

    return create_client(supabase_url, supabase_key)
