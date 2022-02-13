import pytest


@pytest.mark.parametrize("examples_client", [["minimal_db", "app"]], indirect=True)
def test_index(examples_client):
    r = examples_client.post("/books", json=dict(title="asdf"))
    assert r.json["title"] == "asdf"

    r = examples_client.get("/books")
    assert len(r.json["items"]) == 1
    assert r.json["items"][0]["id"] == 1
    assert r.json["items"][0]["title"] == "asdf"
