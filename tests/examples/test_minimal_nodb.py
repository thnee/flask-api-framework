import pytest


@pytest.mark.parametrize("examples_client", [["minimal_nodb", "app"]], indirect=True)
def test_index(examples_client):
    r = examples_client.get("/")
    assert r.json["value"] == "minimal"
