import os
import tempfile

import pytest

import webapp

@pytest.fixture
def client():
    db_fd, webapp.app.config['DATABASE'] = tempfile.mkstemp()
    webapp.app.config['TESTING'] = True
    client = webapp.app.test_client()

    """with webapp.app.app_context():
        webapp.init_db()"""

    yield client

    os.close(db_fd)
    os.unlink(webapp.app.config['DATABASE'])



def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Hello' in rv.data
