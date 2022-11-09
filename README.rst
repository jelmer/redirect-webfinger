Simple redirecting webfinger implementation
===========================================

This simple webfinger implementation just redirects
a single webfinger address to another server. I use it to
allow people to find my mastodon profile via my
personal server.

Example usage::

   $ redirect-webfinger --acct=jelmer@jelmer.uk \
        --mastodon-server=mastodon.cloud \
        --mastodon-user=jelmer

The only URL it exposes is /.well-known/webfinger, which
you would probably want to expose via your reverse HTTP proxy.

Or using docker/podman::

   $ podman run ghcr.io/jelmer/redirect-webfinger \
        -e ACCT=jelmer@jelmer.uk \
        -e MASTODON_SERVER=mastodon.cloud \
        -e MASTODON_USER=jelmer

