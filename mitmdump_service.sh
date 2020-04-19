#!/bin/bash

export MITMPROXY_CACHEDIR=/home/pi/rpi-mitmproxy_images_cache

export PATH=/home/pi/.local/bin:/home/pi/rpi-mitmproxy:$PATH
export PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages:/home/pi/rpi-mitmproxy:$PYTHONPATH

date &>> /var/log/mitmdump.log
echo "MITMPROXY_CACHEDIR=$MITMPROXY_CACHEDIR"  &>> /var/log/mitmdump.log
# mitmdump --showhost --ssl-insecure --set upstream_cert=false --listen-host=0.0.0.0 --listen-port=8080 -s examples/hans/cache_files.py &>> /var/log/mitmdump.log
cd /home/pi/rpi-mitmproxy
python3 mitmdump_main.py --showhost --ssl-insecure --set upstream_cert=false --listen-host=0.0.0.0 --listen-port=8080 -s examples/hans/cache_files.py &>> /var/log/mitmdump.log
