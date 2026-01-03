#!/usr/bin/env python3
import json

new_tools = [
    {
        "nom": "Cobalt Strike",
        "description": "Plateforme commerciale de simulation d'adversaires et red teaming",
        "categorie": "Red Team",
        "type": "Commercial",
        "installation": "License commerciale requise, installation via package Java",
        "documentation": "https://www.cobaltstrike.com/",
        "prix": "Commercial ($3500+/an)",
        "plateforme": json.dumps(["Windows", "Linux", "macOS"]),
        "commandes_courantes": json.dumps([
            "beacon > shell command",
            "beacon > screenshot",
            "beacon > hashdump",
            "beacon > mimikatz"
        ]),
        "alternatives": json.dumps(["Sliver", "Covenant", "Mythic"])
    },
    {
        "nom": "Empire/Starkiller",
        "description": "Framework PowerShell post-exploitation avec GUI",
        "categorie": "Post-Exploitation",
        "type": "Open Source",
        "installation": "pip3 install powershell-empire",
        "documentation": "https://github.com/BC-SECURITY/Empire",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "uselistener http",
            "usestager multi/launcher",
            "usemodule credentials/mimikatz/logonpasswords",
            "usemodule privesc/powerup/allchecks"
        ]),
        "alternatives": json.dumps(["Covenant", "Metasploit", "Cobalt Strike"])
    },
    {
        "nom": "Covenant",
        "description": "Framework C2 .NET avec interface web moderne",
        "categorie": "Command & Control",
        "type": "Open Source",
        "installation": "Docker ou compilation depuis source .NET",
        "documentation": "https://github.com/cobbr/Covenant",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Windows", "Linux"]),
        "commandes_courantes": json.dumps([
            "Créer un listener",
            "Générer un launcher",
            "Exécuter des tasks",
            "Pivoting entre grunts"
        ]),
        "alternatives": json.dumps(["Empire", "Sliver", "Cobalt Strike"])
    },
    {
        "nom": "Sliver",
        "description": "Framework C2 moderne écrit en Go par BishopFox",
        "categorie": "Command & Control",
        "type": "Open Source",
        "installation": "curl https://sliver.sh/install | sudo bash",
        "documentation": "https://github.com/BishopFox/sliver",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "generate --mtls target.com",
            "mtls",
            "use [session-id]",
            "ps",
            "screenshot"
        ]),
        "alternatives": json.dumps(["Cobalt Strike", "Covenant", "Merlin"])
    },
    {
        "nom": "Havoc C2",
        "description": "Framework C2 moderne et modulaire",
        "categorie": "Command & Control",
        "type": "Open Source",
        "installation": "Compilation depuis source (C++/Qt)",
        "documentation": "https://github.com/HavocFramework/Havoc",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows"]),
        "commandes_courantes": json.dumps([
            "Créer un listener",
            "Générer un demon agent",
            "Post-exploitation modules",
            "Lateral movement"
        ]),
        "alternatives": json.dumps(["Sliver", "Brute Ratel", "Cobalt Strike"])
    },
    {
        "nom": "Nessus",
        "description": "Scanner de vulnérabilités professionnel",
        "categorie": "Vulnerability Scanning",
        "type": "Commercial/Freemium",
        "installation": "Package DEB/RPM ou installer Windows",
        "documentation": "https://www.tenable.com/products/nessus",
        "prix": "Essentials (gratuit 16 IPs), Professional ($3990/an)",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Interface web sur port 8834",
            "Créer une scan policy",
            "Lancer un scan",
            "Exporter les résultats"
        ]),
        "alternatives": json.dumps(["OpenVAS", "Qualys", "Rapid7 Nexpose"])
    },
    {
        "nom": "OpenVAS",
        "description": "Scanner de vulnérabilités open-source (Greenbone)",
        "categorie": "Vulnerability Scanning",
        "type": "Open Source",
        "installation": "Docker: docker pull greenbone/community-edition",
        "documentation": "https://www.greenbone.net/en/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux"]),
        "commandes_courantes": json.dumps([
            "gvm-start",
            "Interface web Greenbone Security Assistant",
            "Créer une tâche de scan",
            "Consulter les rapports"
        ]),
        "alternatives": json.dumps(["Nessus", "Qualys", "Nuclei"])
    },
    {
        "nom": "Acunetix",
        "description": "Scanner de vulnérabilités d'applications web",
        "categorie": "Web Application Security",
        "type": "Commercial",
        "installation": "Installation via package ou appliance",
        "documentation": "https://www.acunetix.com/",
        "prix": "Commercial (~$4500+/an)",
        "plateforme": json.dumps(["Windows", "Linux"]),
        "commandes_courantes": json.dumps([
            "Définir une cible web",
            "Configurer le scan",
            "Lancer le crawling",
            "Analyser les vulnérabilités"
        ]),
        "alternatives": json.dumps(["Burp Suite Pro", "OWASP ZAP", "Netsparker"])
    },
    {
        "nom": "OWASP ZAP",
        "description": "Proxy de sécurité web open-source",
        "categorie": "Web Application Security",
        "type": "Open Source",
        "installation": "Download JAR ou package",
        "documentation": "https://www.zaproxy.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "zap.sh -daemon -port 8080",
            "Spider une application",
            "Active scan",
            "Fuzzer des paramètres"
        ]),
        "alternatives": json.dumps(["Burp Suite", "Acunetix", "AppSpider"])
    },
    {
        "nom": "Wireshark",
        "description": "Analyseur de protocoles réseau graphique",
        "categorie": "Network Analysis",
        "type": "Open Source",
        "installation": "apt install wireshark / Package Windows",
        "documentation": "https://www.wireshark.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Capturer le trafic",
            "Filtres: http, tcp.port==443, ip.addr==X",
            "Follow TCP Stream",
            "Export Objects"
        ]),
        "alternatives": json.dumps(["tcpdump", "tshark", "NetworkMiner"])
    },
    {
        "nom": "Snort",
        "description": "Système de détection/prévention d'intrusions (IDS/IPS)",
        "categorie": "Network Security",
        "type": "Open Source",
        "installation": "apt install snort",
        "documentation": "https://www.snort.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows"]),
        "commandes_courantes": json.dumps([
            "snort -A console -q -c /etc/snort/snort.conf -i eth0",
            "Créer des règles personnalisées",
            "Analyser les alertes",
            "Mode IPS inline"
        ]),
        "alternatives": json.dumps(["Suricata", "Zeek", "OSSEC"])
    },
    {
        "nom": "Suricata",
        "description": "Moteur IDS/IPS/NSM multi-thread haute performance",
        "categorie": "Network Security",
        "type": "Open Source",
        "installation": "apt install suricata",
        "documentation": "https://suricata.io/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows"]),
        "commandes_courantes": json.dumps([
            "suricata -c /etc/suricata/suricata.yaml -i eth0",
            "Gestion des règles",
            "Intégration avec ELK",
            "Eve JSON output"
        ]),
        "alternatives": json.dumps(["Snort", "Zeek", "Security Onion"])
    },
    {
        "nom": "Zeek (Bro)",
        "description": "Framework d'analyse de trafic réseau et NSM",
        "categorie": "Network Security Monitoring",
        "type": "Open Source",
        "installation": "apt install zeek",
        "documentation": "https://zeek.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "macOS"]),
        "commandes_courantes": json.dumps([
            "zeek -i eth0",
            "Analyser des PCAP",
            "Scripts personnalisés",
            "Génération de logs structurés"
        ]),
        "alternatives": json.dumps(["Suricata", "Snort", "Moloch"])
    },
    {
        "nom": "Security Onion",
        "description": "Distribution Linux pour NSM, IDS et hunt de menaces",
        "categorie": "Network Security Monitoring",
        "type": "Open Source",
        "installation": "ISO bootable ou installation réseau",
        "documentation": "https://securityonionsolutions.com/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux"]),
        "commandes_courantes": json.dumps([
            "Stack complet: Suricata + Zeek + Elastic",
            "Interface Kibana",
            "PCAP analysis",
            "Alert triage"
        ]),
        "alternatives": json.dumps(["SELKS", "RockNSM", "Custom ELK stack"])
    },
    {
        "nom": "CyberChef",
        "description": "Application web de manipulation de données",
        "categorie": "Data Analysis",
        "type": "Open Source",
        "installation": "https://gchq.github.io/CyberChef/ ou selfhosted",
        "documentation": "https://github.com/gchq/CyberChef",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Web", "Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Encodage/Décodage Base64, Hex, etc.",
            "Cryptographie",
            "Compression/Décompression",
            "Analyse de format"
        ]),
        "alternatives": json.dumps(["BurpSuite Decoder", "CLI tools"])
    },
    {
        "nom": "Yara",
        "description": "Outil d'identification et classification de malware",
        "categorie": "Malware Analysis",
        "type": "Open Source",
        "installation": "apt install yara / pip install yara-python",
        "documentation": "https://virustotal.github.io/yara/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "yara rules.yar suspicious_file",
            "yara -s rule.yar /path/to/scan",
            "Créer des règles personnalisées",
            "Integration with sandbox"
        ]),
        "alternatives": json.dumps(["ClamAV", "Custom IOC matching"])
    },
    {
        "nom": "Cuckoo Sandbox",
        "description": "Système d'analyse automatisée de malware",
        "categorie": "Malware Analysis",
        "type": "Open Source",
        "installation": "pip install cuckoo ou Docker",
        "documentation": "https://cuckoosandbox.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux"]),
        "commandes_courantes": json.dumps([
            "cuckoo submit malware.exe",
            "cuckoo web",
            "Analyse de comportement",
            "Network capture"
        ]),
        "alternatives": json.dumps(["ANY.RUN", "Joe Sandbox", "Hybrid Analysis"])
    },
    {
        "nom": "IDA Pro",
        "description": "Désassembleur et débogueur professionnel",
        "categorie": "Reverse Engineering",
        "type": "Commercial",
        "installation": "Installation via license commerciale",
        "documentation": "https://hex-rays.com/ida-pro/",
        "prix": "Commercial ($589-$3840+)",
        "plateforme": json.dumps(["Windows", "Linux", "macOS"]),
        "commandes_courantes": json.dumps([
            "Désassemblage multi-architecture",
            "Decompiler (Hex-Rays)",
            "Debugging",
            "Plugin development"
        ]),
        "alternatives": json.dumps(["Ghidra", "Binary Ninja", "radare2"])
    },
    {
        "nom": "Binary Ninja",
        "description": "Plateforme de reverse engineering moderne",
        "categorie": "Reverse Engineering",
        "type": "Commercial",
        "installation": "License commerciale",
        "documentation": "https://binary.ninja/",
        "prix": "Commercial ($399 Personal)",
        "plateforme": json.dumps(["Windows", "Linux", "macOS"]),
        "commandes_courantes": json.dumps([
            "Analysis et désassemblage",
            "IL (Intermediate Language)",
            "Python API",
            "Plugin ecosystem"
        ]),
        "alternatives": json.dumps(["IDA Pro", "Ghidra", "Cutter"])
    },
    {
        "nom": "Frida",
        "description": "Framework de dynamic instrumentation",
        "categorie": "Dynamic Analysis",
        "type": "Open Source",
        "installation": "pip install frida-tools",
        "documentation": "https://frida.re/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS", "iOS", "Android"]),
        "commandes_courantes": json.dumps([
            "frida -U -f com.app.name -l script.js",
            "Hook functions",
            "Modifier behavior at runtime",
            "Dump memory"
        ]),
        "alternatives": json.dumps(["Xposed", "Cydia Substrate", "Pin"])
    },
    {
        "nom": "Apktool",
        "description": "Outil de reverse engineering d'applications Android",
        "categorie": "Mobile Security",
        "type": "Open Source",
        "installation": "apt install apktool",
        "documentation": "https://ibotpeaches.github.io/Apktool/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "apktool d app.apk",
            "Modifier smali/resources",
            "apktool b app/",
            "Re-sign APK"
        ]),
        "alternatives": json.dumps(["jadx", "dex2jar", "Bytecode Viewer"])
    },
    {
        "nom": "MobSF",
        "description": "Framework automatisé d'analyse de sécurité mobile",
        "categorie": "Mobile Security",
        "type": "Open Source",
        "installation": "Docker ou pip install",
        "documentation": "https://github.com/MobSF/Mobile-Security-Framework-MobSF",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Interface web automatisée",
            "Static analysis Android/iOS",
            "Dynamic analysis",
            "Scan de vulnérabilités"
        ]),
        "alternatives": json.dumps(["Drozer", "qark", "Objection"])
    },
    {
        "nom": "Burp Suite Professional",
        "description": "Suite complète de test d'applications web (version Pro)",
        "categorie": "Web Application Security",
        "type": "Commercial",
        "installation": "JAR avec license",
        "documentation": "https://portswigger.net/burp/pro",
        "prix": "Commercial ($449/an)",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Scanner automatisé",
            "Intruder avec payloads",
            "Extensions BApp Store",
            "Collaboration"
        ]),
        "alternatives": json.dumps(["OWASP ZAP", "Acunetix", "AppSpider"])
    },
    {
        "nom": "Postman",
        "description": "Plateforme de test et développement d'API",
        "categorie": "API Testing",
        "type": "Freemium",
        "installation": "Package natif ou snap",
        "documentation": "https://www.postman.com/",
        "prix": "Gratuit / Pro ($12/user/mois)",
        "plateforme": json.dumps(["Linux", "Windows", "macOS"]),
        "commandes_courantes": json.dumps([
            "Créer des requêtes",
            "Collections",
            "Tests automatisés",
            "Mock servers"
        ]),
        "alternatives": json.dumps(["Insomnia", "curl", "HTTPie"])
    },
    {
        "nom": "Kali Linux",
        "description": "Distribution Linux spécialisée en pentest",
        "categorie": "Operating System",
        "type": "Open Source",
        "installation": "ISO bootable, VM, WSL2, Docker",
        "documentation": "https://www.kali.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "VM", "ARM"]),
        "commandes_courantes": json.dumps([
            "600+ outils préinstallés",
            "apt update && apt upgrade",
            "Toolsets par catégorie",
            "Custom builds"
        ]),
        "alternatives": json.dumps(["Parrot OS", "BlackArch", "Pentoo"])
    },
    {
        "nom": "Parrot OS",
        "description": "Distribution Linux pour sécurité et vie privée",
        "categorie": "Operating System",
        "type": "Open Source",
        "installation": "ISO bootable, VM",
        "documentation": "https://www.parrotsec.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "ARM"]),
        "commandes_courantes": json.dumps([
            "Outils de pentest",
            "Focus sur la privacy",
            "AnonSurf pour anonymat",
            "Forensics tools"
        ]),
        "alternatives": json.dumps(["Kali Linux", "BlackArch", "BackBox"])
    },
    {
        "nom": "Aircrack-ng",
        "description": "Suite d'outils pour audit de réseaux WiFi",
        "categorie": "Wireless Security",
        "type": "Open Source",
        "installation": "apt install aircrack-ng",
        "documentation": "https://www.aircrack-ng.org/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux"]),
        "commandes_courantes": json.dumps([
            "airmon-ng start wlan0",
            "airodump-ng wlan0mon",
            "aireplay-ng --deauth",
            "aircrack-ng -w wordlist capture.cap"
        ]),
        "alternatives": json.dumps(["Wifite", "Kismet", "Fern WiFi Cracker"])
    },
    {
        "nom": "Hashcat",
        "description": "Cracker de hash GPU-acceleré (version complète)",
        "categorie": "Password Cracking",
        "type": "Open Source",
        "installation": "apt install hashcat / Binary download",
        "documentation": "https://hashcat.net/hashcat/",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows"]),
        "commandes_courantes": json.dumps([
            "hashcat -m 1000 -a 3 hash.txt ?a?a?a?a?a?a",
            "hashcat -m 0 -a 0 hash.txt rockyou.txt",
            "Support 350+ hash types",
            "Multi-GPU support"
        ]),
        "alternatives": json.dumps(["John the Ripper", "oclHashcat"])
    },
    {
        "nom": "Responder",
        "description": "Outil de poisoning LLMNR, NBT-NS et MDNS",
        "categorie": "Network Attack",
        "type": "Open Source",
        "installation": "git clone https://github.com/lgandx/Responder",
        "documentation": "https://github.com/lgandx/Responder",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux"]),
        "commandes_courantes": json.dumps([
            "responder -I eth0 -wrf",
            "Capture NTLM hashes",
            "HTTP/SMB/SQL poisoning",
            "WPAD attacks"
        ]),
        "alternatives": json.dumps(["Inveigh", "mitm6"])
    },
    {
        "nom": "Covenant Framework",
        "description": "Alternative .NET à Cobalt Strike",
        "categorie": "Command & Control",
        "type": "Open Source",
        "installation": "Docker ou build depuis source",
        "documentation": "https://github.com/cobbr/Covenant",
        "prix": "Gratuit",
        "plateforme": json.dumps(["Linux", "Windows"]),
        "commandes_courantes": json.dumps([
            "Interface web moderne",
            "Grunts (agents) C#",
            "Post-exploitation tasks",
            "Credential harvesting"
        ]),
        "alternatives": json.dumps(["Cobalt Strike", "Empire", "Sliver"])
    }
]

print(f"📊 Préparation de {len(new_tools)} nouveaux outils...")

tools_file = "app/data/tools.json"
with open(tools_file, 'r', encoding='utf-8') as f:
    existing_tools = json.load(f)

print(f"✅ {len(existing_tools)} outils existants trouvés")

existing_names = {tool['nom'].lower() for tool in existing_tools}
new_unique_tools = [tool for tool in new_tools if tool['nom'].lower() not in existing_names]

print(f"✅ {len(new_unique_tools)} nouveaux outils uniques à ajouter")
print(f"⚠️  {len(new_tools) - len(new_unique_tools)} doublons ignorés")

existing_tools.extend(new_unique_tools)

with open(tools_file, 'w', encoding='utf-8') as f:
    json.dump(existing_tools, f, ensure_ascii=False, indent=2)

print(f"✅ Fichier mis à jour: {len(existing_tools)} outils au total")
print(f"📈 Gain: +{len(new_unique_tools)} outils ({len(new_unique_tools)/len(existing_tools)*100:.1f}% d'augmentation)")
