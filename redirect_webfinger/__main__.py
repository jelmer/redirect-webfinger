#!/usr/bin/python3

import logging
import os
import sys

from aiohttp import web

from . import format_response


async def handle_webfinger(request: web.Request) -> web.Response:
    try:
        resource = request.query['resource']
    except KeyError:
        raise web.HTTPBadRequest(text='missing resource param')
    if resource not in request.app['resources']:
        logging.warning('Unknown resource: %r', resource)
        raise web.HTTPNotFound(text='no such resource')
    return web.json_response(format_response(
        resource=resource,
        mastodon_server=request.app['mastodon_server'],
        mastodon_user=request.app['mastodon_user']),
        content_type='application/jrd+json')


def create_app(accts: list[str], mastodon_server: str, mastodon_user: str) -> web.Application:
    app = web.Application()
    app['resources'] = [f'acct:{acct}' for acct in accts]
    app['mastodon_server'] = mastodon_server
    app['mastodon_user'] = mastodon_user

    app.router.add_get('/.well-known/webfinger', handle_webfinger,
                       name='webfinger')
    return app


def parse_args(argv=None, environ=os.environ):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--acct', type=str, help='Example: jelmer@jelmer.uk', nargs='*',
        default=environ['ACCT'].split(',') if 'ACCT' in environ else None)
    parser.add_argument(
        '--mastodon-server', type=str, help='Example: mastodon.cloud',
        default=environ.get('MASTODON_SERVER'))
    parser.add_argument(
        '--mastodon-user', type=str, help='Example: jelmer',
        default=environ.get('MASTODON_USER'))

    args = parser.parse_args(argv)
    if not args.acct or not args.mastodon_server or not args.mastodon_user:
        parser.print_usage()
        sys.exit(1)
    return args


def main(argv=None):
    logging.basicConfig()

    args = parse_args(argv)

    app = create_app(args.acct, mastodon_server=args.mastodon_server,
                     mastodon_user=args.mastodon_user)
    web.run_app(app, host='0.0.0.0', port=8080)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
