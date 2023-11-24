# Proxy Checker

Pyhton script using **threading** to find working proxies from a big list of proxies. The script supports HTTP, SOCKS4, SOCKS5 proxies.
```
127.0.0.1:1234
127.0.0.2:80
127.0.0.3:8008
```

## Usage
```
python3 proxycheck.py -i proxylist.txt -p socks5 -t 32 -o ./output
```
Option `-i` is for the input list of proxies. 

Option `-p` is for the proxies type.

Option `-t` is for the number of threads. It is recommended to use the number of threads based on you pc specs.

Option `-o` is for the output directory. The script is writing the output to multiple files and puts together the proxies from the same country. The script checks the proxies by making a request to the ipinfo.io and this way it will receive their country location.

