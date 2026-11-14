from etl.transform import transform_posts


def test_transform_cleans_whitespace_and_maps_fields():
    records = [{
        "id": 1,
        "userId": 7,
        "title": "  Hello   data ",
        "body": " first line\n second   line ",
    }]

    cleaned, rejected = transform_posts(records)

    assert rejected == 0
    assert cleaned == [{
        "id": 1,
        "user_id": 7,
        "title": "Hello data",
        "body": "first line second line",
    }]


def test_transform_rejects_missing_fields_and_empty_text():
    records = [
        {"id": 1, "userId": 1, "title": "", "body": "body"},
        {"id": 2, "userId": 1, "title": "title"},
        {"userId": 1, "title": "title", "body": "body"},
    ]

    cleaned, rejected = transform_posts(records)

    assert cleaned == []
    assert rejected == 3


def test_transform_rejects_duplicate_ids():
    record = {"id": 1, "userId": 1, "title": "title", "body": "body"}

    cleaned, rejected = transform_posts([record, record])

    assert len(cleaned) == 1
    assert rejected == 1


def test_transform_rejects_boolean_ids():
    records = [{"id": True, "userId": 1, "title": "title", "body": "body"}]

    cleaned, rejected = transform_posts(records)

    assert cleaned == []
    assert rejected == 1
