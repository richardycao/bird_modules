### Create image

`cd ./logger`

`docker build -f Dockerfile.client -t logger_client_image .`

### Run container locally

`docker run -t --rm --name logger_client --link coinbasepro_server --env "INPUT_ENDPOINT=coinbasepro_server:50051" logger_client_image`