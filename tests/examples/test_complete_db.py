import pytest


@pytest.mark.parametrize(
    "examples_client", [["complete_db", "create_app"]], indirect=True
)
def test_complete(examples_client):
    r = examples_client.post(
        "/v1/authors",
        json=dict(
            name="asdf",
        ),
    )
    assert r.status_code == 201
    assert r.json["name"] == "asdf"

    r = examples_client.post(
        "/v1/authors",
        json=dict(
            name="qwer",
        ),
    )
    assert r.status_code == 201
    assert r.json["name"] == "qwer"

    r = examples_client.get("/v1/authors")
    assert r.status_code == 200
    assert len(r.json["items"]) == 2

    r = examples_client.post(
        "/v1/books",
        json=dict(
            author_id=1,
            title="asdf 1",
            year=1982,
            description="asdf1 asdf1 asdf1",
        ),
    )
    assert r.status_code == 201

    r = examples_client.post(
        "/v1/books",
        json=dict(
            author_id=1,
            title="asdf 2",
            year=1982,
            description="asdf2 asdf2 asdf2",
        ),
    )
    assert r.status_code == 201

    r = examples_client.post(
        "/v1/books",
        json=dict(
            author_id=2,
            title="asdf 3",
            year=1982,
            description="asdf3 asdf3 asdf3",
        ),
    )
    assert r.status_code == 201

    r = examples_client.post(
        "/v1/books",
        json=dict(
            year=1982,
        ),
    )
    assert r.status_code == 400
    assert r.json["source"] == "body"

    r = examples_client.get("/v1/books")
    assert r.status_code == 200
    assert len(r.json["items"]) == 3

    r = examples_client.get("/v1/authors/1/books")
    assert r.status_code == 200
    assert len(r.json["items"]) == 2

    r = examples_client.get("/v1/books/1")
    assert r.status_code == 200
    assert r.json["id"] == 1
    assert r.json["title"] == "asdf 1"

    r = examples_client.get("/v1/books/asdf")
    assert r.status_code == 400
    assert r.json["source"] == "kwargs"

    r = examples_client.patch(
        "/v1/books/1",
        json=dict(
            title="something else",
        ),
    )
    assert r.status_code == 200
    assert r.json["title"] == "something else"

    r = examples_client.get("/v1/books/1")
    assert r.status_code == 200
    assert r.json["id"] == 1
    assert r.json["title"] == "something else"
    assert r.json["description"] == "asdf1 asdf1 asdf1"

    r = examples_client.put(
        "/v1/books/1",
        json=dict(
            title="zxcv",
        ),
    )
    assert r.status_code == 400

    r = examples_client.put(
        "/v1/books/1",
        json=dict(
            title="zxcv",
            year=1983,
            description="zxcv zxcv zxcv",
        ),
    )
    assert r.status_code == 200

    r = examples_client.get("/v1/books/1")
    assert r.status_code == 200
    assert r.json["id"] == 1
    assert r.json["title"] == "zxcv"
    assert r.json["year"] == 1983
    assert r.json["description"] == "zxcv zxcv zxcv"

    r = examples_client.delete("/v1/books/1")
    assert r.status_code == 200

    r = examples_client.get("/v1/books/1")
    assert r.status_code == 404
