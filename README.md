
# IOT

This project consists of valuing the amount of temperature CO2 and humidity for the greenhouses is analysed.
Technologies: python, Kafka, influxdb, grafana, teflage, flutter and a raspberry Pi3 board.

## Installation

Clone the project

```bash
  cd my-project
  pip install requirements.txt 
```
    
## Documentation

[Prerequisites]

APT must be up to date. If in doubt, type the following command:
```bash
    sudo apt-get update
    sudo apt-get install 
```
[Docker installation]

1.Download Docker
```bash
    sudo apt-get install -y docker.io
```
2.To check that Docker is correctly installed with the command :
```bash
    docker -v
    Docker version 20.10.7, build 20.10.7-0ubuntu5~20.04.2
```
[Installing Docker Compose]

1.Download the version with the latest release from the official Docker repository :https://github.com/docker/compose/releases

Exemple:
```bash
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
2.Apply executable permissions to the binary
```bash
sudo chmod +x /usr/local/bin/docker-compose
```
3.To check that Docker is correctly installed with the command :
```bash
    docker-compose -v
    Docker Compose version v2.2.3
```
[Make another user]

It is recommended, for security reasons, to create a dedicated user for managing Docker volumes and not to run it as your superuser.
And you can work in your superuser.

1.Let's create a user  with the name grafana: 
```bash
    sudo adduser grafana
```
2.Add it to the docker group:
```bash
    sudo adduser grafana docker
```
[Creation of Telegraf, InfluxDB and Grafana volumes]
1.Log in as user grafana :
```bash
    su grafana
```
2.Move to this user's home directory:
```bash
    cd
```
3.Create the file /home/grafana/docker-compose.yml and change the highlighted lines to the desired configuration:
```bash
    vim /home/grafana/docker-compose.yml
```

## docker-compose.yml

```javascript
version: "3"
services:
  influxdb:
    image: influxdb:latest
    container_name: influxdb
    restart: always
    hostname: influxdb
    networks:
      - lan
    ports:
      - 8086:8086
    environment:
      INFLUX_DB: "telegraf"
      INFLUXDB_USER: "admin"             // you can change this value
      INFLUXDB_USER_PASSWORD: "admin"    // you can change this value
    volumes:
      - influxdb-data:/var/lib/influxdb
 
  telegraf:
    image: telegraf:latest
    depends_on:
      - influxdb
    container_name: telegraf
    restart: always
    networks:
      - lan
    links:
      - influxdb:influxdb
    tty: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/grafana/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf
    privileged: true
 
  grafana:
    image: grafana/grafana:latest
    depends_on:
      - influxdb
    container_name: grafana
    restart: always
    networks:
      - lan
    ports:
      - 3000:3000
    links:
      - influxdb:influxdb
    environment:
      GF_INSTALL_PLUGINS: "grafana-clock-panel,\
                          grafana-influxdb-08-datasource,\
                          grafana-kairosdb-datasource,\
                          grafana-piechart-panel,\
                          grafana-simple-json-datasource,\
                          grafana-worldmap-panel"
      GF_SECURITY_ADMIN_USER: "admin"                         // you can change this value
      GF_SECURITY_ADMIN_PASSWORD: "admin"                     // you can change this value
    volumes:
      - grafana-data:/var/lib/grafana
volumes:
  influxdb-data:
  grafana-data:
networks:
  lan: 
}
```


REMARQUE

INFLUXDB_USER: user created with read/write rights on the INFLUX_DB database.

INFLUXDB_USER_PASSWORD: password of the user INFLUXDB_USER.

GF_SECURITY_ADMIN_USER : administrator of the Grafana interface.

GF_SECURITY_ADMIN_PASSWORD: password of the Grafana administrator.

4.Create the Telegraf configuration directory and generate an updated configuration file with the following command:

```bash
    mkdir telegraf
    docker run --rm telegraf telegraf config > telegraf/telegraf.conf
```
5.Replace this lines in the configuration file /home/grafana/telegraf/telegraf.conf :

## telegraf.conf

```javascript
# Configuration for telegraf agent
[agent]
  
  interval = "10s"
 
  round_interval = true


  metric_batch_size = 1000
 

  metric_buffer_limit = 10000
 
 
  collection_jitter = "0s"
 
  
  flush_interval = "10s"
 

  flush_jitter = "0s"
 

  precision = ""
 

  hostname = ""
 
  omit_hostname = false
 
[[outputs.influxdb_v2]]
 

  urls = ["http://192.168.1.9:8086"]    ##address of your machine
 
  ## Token for authentication.
  token = ""                            ##get the token from influxDb
 
  ## Organization is the name of the organization you wish to write to; must exist.
  organization = ""                     ##name your organization
 
  ## Destination bucket to write into.
  bucket = ""                           ##give the name of your bucket
 

[[inputs.kafka_consumer]]
  brokers = ["192.168.1.9:9092"]
  topics = [""]                         ##name of your topic
  data_format = "json_v2"
  [[inputs.kafka_consumer.json_v2]]
        [[inputs.kafka_consumer.json_v2.field]]
            path = "CO2" 
  [[inputs.kafka_consumer.json_v2]]
        [[inputs.kafka_consumer.json_v2.field]]
            path = "TVOC" 
  [[inputs.kafka_consumer.json_v2]]
        [[inputs.kafka_consumer.json_v2.field]]
            path = "Temp" 
```

6.Start the containers:
```bash
    docker-compose up -d
```

