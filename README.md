# Load-Balancer-Store
Load Balancer using Round Robin algorithm. Distributed system, developed on Python using the ZeroMQ framework with the Pub/Sub pattern.

Store simulation with persistence in MYSQL database. n clients can make requests, which will be balanced by the load balancer and finally distributed to n servers, which will serve the clients requests.

## Instalation

```bash
pip3 install pyzmq
```

## Execution

```bash
python Server.py 1
python Server.py 2
python Server.py 3
python Server.py 4
python LoadBalancer.py
python Client.py
```

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)
