CEH Diploma - Session 3 (Scanning & Enumeration)
Packet captures - open each in Wireshark

These are REAL captures taken from a live lab. Attacker = 10.10.10.1 (Kali role),
target = 10.10.10.10 (FILE01, a Linux host running FTP/SSH/SMTP/HTTP/POP3/IMAP/
rpcbind/NetBIOS/SNMP/LDAP/Samba/MySQL, with TCP 3389 and 8080 dropped by a firewall
and TCP 9999 closed).

  01-arp-host-discovery      nmap -sn 10.10.10.0/28
  02-icmp-ping-sweep         nmap -sn -PE --send-ip (one live host, one dead)
  03-tcp-syn-scan            nmap -sS   (open / closed / filtered in one file)
  04-tcp-connect-scan        nmap -sT   (compare with 03 - handshake completes)
  05-udp-scan                nmap -sU -p 53,111,161,137
  06-fin-null-xmas-scan      nmap -sF then -sN then -sX
  07-ack-scan                nmap -sA   (firewall mapping, not port state)
  08-version-detection       nmap -sV
  09-os-detection            nmap -O    (2231 packets - the noise lesson)
  10-evasion-decoy-fragment  nmap -sS -f -D decoy1,decoy2,ME,decoy3
  11-smb-enumeration         smbclient -L + nmap smb-* NSE scripts
  12-ldap-enumeration        ldapsearch anonymous bind + subtree search
  13-snmp-walk               snmpwalk -v2c -c public
  14-ftp-anonymous           anonymous login transcript
  15-smtp-user-enum          VRFY valid vs invalid user
  16-rpc-nfs-showmount       rpcinfo -p + showmount -e
  17-http-banner-grab        HEAD / request and server headers
  18-full-portscan-noise     nmap -sS -p 1-1000 -T4 (2015 packets)
  19-nse-default-scripts     nmap -sC (933 packets)

No real-world traffic, no credentials, no personal data. Lab addresses only.
