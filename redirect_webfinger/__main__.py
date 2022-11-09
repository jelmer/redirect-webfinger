#!/usr/bin/python3

import logging
import os

from aiohttp import web

from . import format_response


async def handle_webfinger(request):
    resource = request.query.get('resource')
    supported_resource = 'acct:%s' % request.app['acct']
    if resource != supported_resource:
        logging.warning('Unknown resource: %r', resource)
        raise web.HTTPNotFound(text='no such resource')
    return web.json_response(format_response(
        resource=supported_resource,
        mastodon_server=request.app['mastodon_server'],
        mastodon_user=request.app['mastodon_user']))


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--acct', type=str, help='Example: jelmer@jelmer.uk', nargs=1,
        default=os.environ.get('ACCT'))
    parser.add_argument(
        '--mastodon-server', type=str, help='Example: mastodon.cloud', nargs=1,
        default=os.environ.get('MASTODON_SERVER'))
    parser.add_argument(
        '--mastodon-user', type=str, help='Example: jelmer', nargs=1,
        default=os.environ.get('MASTODON_USER'))
    args = parser.parse_args(argv)

    if not args.acct or not args.mastodon_server or not args.mastodon_user:
        parser.print_usage()
        return 1

    logging.basicConfig()

    app = web.Application()
    app['acct'] = args.acct
    app['mastodon_server'] = args.mastodon_server
    app['mastodon_user'] = args.mastodon_user

    app.router.add_get('/.well-known/webfinger', handle_webfinger,
                       name='webfinger')

    web.run_app(app, host='0.0.0.0', port=8080)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
