"""Basic Supabase connectivity test for the Wellness Center POC."""

from __future__ import annotations

from datetime import datetime, timezone

from supabase_client import get_supabase_client


def main() -> None:
    client = get_supabase_client()

    unique_suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    dummy_user = {
        "name": f"Dummy User {unique_suffix}",
        "phone": f"99999{unique_suffix[-5:]}",
    }

    insert_response = client.table("users").insert(dummy_user).execute()
    if not insert_response.data:
        raise RuntimeError("Insert failed: no data returned from Supabase.")

    inserted_user = insert_response.data[0]
    inserted_id = inserted_user["id"]

    read_response = (
        client.table("users")
        .select("id, name, phone")
        .eq("id", inserted_id)
        .single()
        .execute()
    )
    if not read_response.data:
        raise RuntimeError("Read-back failed: inserted row was not found.")

    print("Connection test successful.")
    print(f"Inserted and fetched user id: {read_response.data['id']}")
    print(f"Name: {read_response.data['name']}")
    print(f"Phone: {read_response.data['phone']}")


if __name__ == "__main__":
    main()
