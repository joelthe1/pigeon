# pigeon

Pigeon is a UDP based message forwarding service that sits between your service and other external services and takes care of:   
1) Sending your messages (assumed to be via UDP) through the appropriate channel for it to reach another external service (e.g. kafka).
2) Receiving your messages (or those you are interested in listening to) from differen channels (e.g. Kafka) and forwarding them to your service via UDP

## But why? (aka Motivations)
The main motivation in creating Pigeon is help service developers not worry about the actual transport layer used to communicate across services in the ASED system. Service developers need only concern themselves with sending and receiving UDP messages and add a flavor of Pigeon, like Kafka based Pigeon, which would then forward all messages it receives on a specific Kafka topic to your service via UDP and send all your outgoing UDP traffic to external services via the pre-configured Kafka topics.

## Features
Currently `pigeon` is able to:
1) Listen for UDP Datagrams and send a Kafka message on multiple Kafka topics  
   UDP --> Kafka  
   
2) Listen for Kafka messages on a specified topic and send them as UDP Datagrams  
   Kafka --> UDP  

## Setup
To run locally, create a `virtualenv` with `Python 3.8.3` and install from `requirements.txt`:

```
# Clone repo
% git clone git@github.com:joelthe1/pigeon.git
% cd pigeon
 
# Setup virtualenv
# Change path to Python according to your system's configuration
% virtualenv -p /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8 .venv
% source .venv/bin/activate

# Install dependencies
% pip install -r requirements.txt

# Peek at `Makefile` if you desire to change configurations
# Start pigeon (ensure you have a running instance of Kafka 
# and that it is correctly setup in the `Makefile`
% make

# You can follow along logs from the `logs` directory
```

## Testing
1) Sending Multiple UDP Messages
For sending multiple UDP messages try using [nping](https://nmap.org/nping/):
```
# Needs `sudo` to work without errors/warnings
sudo nping --data-string="Test message" --delay=1ms --count=10 -H -N --udp --dest-port 9089 127.0.0.1
```
`nping` also has a few optinos for specifying payload. (Try `nping -h` and look for `PAYLOAD OPTIONS`)

2) Run and Port Forward Kafka
You also need to have Kafka running on your system (usually in `minikube`) and port forwarded on another terminal. Something like:
```
kubectl port-forward statefulset/ii-kafka 19092:19092
```

3) Read Kafka Messages
To read Kafka messages sent by `pigeon` try using [kafkacat](https://github.com/edenhill/kafkacat):
```
# Read topic pigeon.test.outbound
# Run on a separate terminal window
kafkacat -C -o end -b localhost:19092 -t pigeon.test.outbound
```

4) Send Kafka Messages
You can use `kafkacat` to send small Kafka messages too:
```
# Send stdin to pigeon.test.inbound topic. Sends on `enter`.
# Run on a separate terminal window
kafkacat -P -b localhost:19092 -t pigeon.test.inbound
```
