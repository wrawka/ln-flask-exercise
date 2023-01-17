from urlshort import create_app


def test_index(client):
    response = client.get('/')
    assert b'SHORTEN' in response.data
