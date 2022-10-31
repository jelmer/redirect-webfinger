#!/usr/bin/python3

from aiohttp import web
import logging

logging.basicConfig()

app = web.Application()

RESP = {
  "subject": "acct:jelmer@jelmer.uk",
  "aliases": [
    "https://mastodon.cloud/@jelmer",
    "https://mastodon.cloud/users/jelmer"
  ],
  "links": [
    {
      "rel": "http://webfinger.net/rel/profile-page",
      "type": "text/html",
      "href": "https://mastodon.cloud/@jelmer"
    },
    {
      "rel": "self",
      "type": "application/activity+json",
      "href": "https://mastodon.cloud/users/jelmer"
    },
    {
      "rel": "http://ostatus.org/schema/1.0/subscribe",
      "template": "https://mastodon.cloud/authorize_interaction?uri={uri}"
    }
  ]
}

async def handle_webfinger(request):
    resource = request.query.get('resource')
    if resource != 'acct:jelmer@jelmer.uk':
        logging.warning('Unknown resource: %r', resource)
        raise web.HTTPNotFound(text='no such resource')
    return web.json_response(RESP)


app.router.add_get('/.well-known/webfinger', handle_webfinger,
                   name='webfinger')

web.run_app(app, host='0.0.0.0', port=8080)
