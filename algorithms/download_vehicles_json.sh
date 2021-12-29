#!/bin/bash

curl \
  -S -f -o "../data/vehicules-commercialises.json" \
  "https://public.opendatasoft.com/explore/dataset/vehicules-commercialises/download/?format=json&timezone=Europe/Berlin&lang=fr"
