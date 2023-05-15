#!/bin/bash
sudo docker build . -f DockerfileApi -t api:03
sudo docker build . -f DockerfileFront -t front:64
sudo docker run -d -p 5000:5000 -p 8089:8089 api:03
sudo docker run -d -v /home/ubuntu/ATIVA/dB:/front/db -p 80:80 front:64