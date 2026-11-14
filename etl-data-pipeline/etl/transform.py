"""Validate and normalize raw API records."""


def transform_posts(records: list[dict]) -> tuple[list[dict], int]:
    """Return cleaned records and the number of rejected records.

    A valid post must have integer id/userId values and non-empty title/body
    strings. Text is stripped and internal whitespace is normalized.
    """
    cleaned = []
    rejected = 0
    seen_ids = set()

    for record in records:
        if not isinstance(record, dict):
            rejected += 1
            continue

        post_id = record.get("id")
        user_id = record.get("userId")
        title = record.get("title")
        body = record.get("body")

        # bool is a subclass of int in Python, so explicitly reject booleans.
        valid_ids = (
            isinstance(post_id, int) and not isinstance(post_id, bool)
            and isinstance(user_id, int) and not isinstance(user_id, bool)
        )
        valid_text = (
            isinstance(title, str) and bool(title.strip())
            and isinstance(body, str) and bool(body.strip())
        )

        if not valid_ids or not valid_text or post_id in seen_ids:
            rejected += 1
            continue

        seen_ids.add(post_id)
        cleaned.append({
            "id": post_id,
            "user_id": user_id,
            "title": " ".join(title.split()),
            "body": " ".join(body.split()),
        })

    return cleaned, rejected
