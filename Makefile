all: container-image

container-image:
	buildah build -t ghcr.io/jelmer/redirect-webfinger:latest .
	buildah push ghcr.io/jelmer/redirect-webfinger:latest
