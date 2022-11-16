#!/usr/bin/python3

from redirect_webfinger.__main__ import create_app


def create_test_app():
    return create_app(
        ['jelmer@jelmer.uk'],
        mastodon_server='mastodon.cloud', mastodon_user='jelmer')


async def test_no_param(aiohttp_client):
    client = await aiohttp_client(create_test_app())

    resp = await client.get('/.well-known/webfinger')
    assert resp.status == 400


async def test_unknown(aiohttp_client):
    client = await aiohttp_client(create_test_app())

    resp = await client.get('/.well-known/webfinger?resource=unknown-resource')
    assert resp.status == 404


async def test_valid(aiohttp_client):
    client = await aiohttp_client(create_test_app())

    resp = await client.get(
        '/.well-known/webfinger?resource=acct:jelmer@jelmer.uk')
    assert resp.status == 200

    json = await resp.json()

    assert json == {
        'aliases': ['https://mastodon.cloud/@jelmer', 'https://mastodon.cloud/users/jelmer'],
        'links': [{'href': 'https://mastodon.cloud/@jelmer', 'rel': 'http://webfinger.net/rel/profile-page', 'type': 'text/html'},
                  {'href': 'https://mastodon.cloud/users/jelmer', 'rel': 'self', 'type': 'application/activity+json'},
                  {'rel': 'http://ostatus.org/schema/1.0/subscribe', 'template': 'https://mastodon.cloud/authorize_interaction?uri={uri}'}],
        'subject': 'acct:jelmer@jelmer.uk'}
