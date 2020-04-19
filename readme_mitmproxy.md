# 2020-04-14 Hans Maerki

* https://www.techcoil.com/blog/how-to-setup-raspbian-buster-lite-for-raspberry-pi-server-projects/
* https://www.tecchannel.de/a/wlan-access-point-unter-linux-erstellen,3286236,3
  Zu kompliziert
* https://hawksites.newpaltz.edu/myerse/2018/06/08/hostapd-on-raspberry-pi/
  gut

## Goal
  Allow access via WLAN to Internet
  Proxy all webaccess
  Cash files

## Installation

``` bash
microsd: touch ssh
```

``` bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install rpi-update python3-pip libjpeg-dev libopenjp2-7 libtiff5 git
sudo apt-get -y autoremove
sudo apt-get -y clean
# Upgrade the firmware
sudo rpi-update
# Config
sudo raspi-config
  4 -> I2, change Timezone: Europe/Zurich
  5 -> P2, SSH: Enable
# Hostname: rpi-mitmproxy
vi /etc/hostname
vi /etc/hosts
```

## Install Visual Studio Code

``` bash
sudo -s
. <( wget -O - https://code.headmelted.com/installers/apt.sh )
sudo apt-get install libx11-xcb1
```

## Clone `mitmproxy` repository

``` bash
git config --global user.email "buhtig.hans.maerki@ergoinfo.ch"
git config --global user.name "Hans Maerki"
git clone https://github.com/hmaerki/rpi-mitmproxy.git
```

pip3 install --upgrade pip
pip3 install -e ~rpi-mitmproxy/
pip3 install pillow

## Copy certificate

``` bash
openssl x509 -in ~/.mitmproxy/mitmproxy-ca.pem -inform PEM -out ~/.mitmproxy/mitmproxy-ca.crt
sudo mkdir /usr/share/ca-certificates/extra
sudo cp /home/pi/.mitmproxy/mitmproxy-ca.crt /usr/share/ca-certificates/extra/
sudo dpkg-reconfigure ca-certificates
```

## Register as a service

See: https://discourse.mitmproxy.org/t/mitm-proxy-on-ubuntu-startup/943/2

``` bash
sudo cp /home/pi/rpi-mitmproxy/mitmdump.service_template /lib/systemd/system/mitmdump.service

sudo systemctl daemon-reload
sudo systemctl enable mitmdump.service
sudo systemctl restart mitmdump.service
```

# Configure Browser

In Firefox

``` text
about:config
network.proxy.http 10.0.11.203
network.proxy.http_port 8080
network.proxy.share_proxy_settings true
network.proxy.ssl 10.0.11.203
network.proxy.ssl_port 8080
network.proxy.type 1
```

In Firefox - install certificate

``` text
http://mitm.it
-> click on 'other'
-> Check two boxes and add certificate
```

