# docker-rotating-proxy

Inspired by [https://github.com/mattes/rotating-proxy](https://github.com/mattes/rotating-proxy)


## Create the application
Start a proxy server using http proxy

### start the application

1. run the proxy

     ```bash
        docker build -t ha-proxy .
        docker run -d -p 11111:11111 -p 4444:4444 --name=rotating-proxy ha-proxy  --log-driver json-file --log-opt max-size=10m
     ```

1. access the proxy stats at

        [http://localhost:4444/haproxy?stats](http://localhost:4444/haproxy?stats)

1. set you client to use

        - http proxy: http://localhost:11111
        - https proxy: http://localhost:11111
