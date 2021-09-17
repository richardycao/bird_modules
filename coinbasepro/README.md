### Create image

`cd ./coinbasepro`
`docker build -f Dockerfile.server -t coinbasepro_server_image .`

### Run container locally

`docker run -t --rm --name coinbasepro_server coinbasepro_server_image`