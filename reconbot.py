import subprocess
import os
import datetime
import requests
from config import DISCORD_WEBHOOK, NUCLEI_SEVERITY, NUCLEI_THREADS, REPORT_DIR

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def notify_discord(message):
    requests.post(DISCORD_WEBHOOK, json={"content": message})

def recon(domain):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs(f"{REPORT_DIR}/{domain}", exist_ok=True)

    print(f"[+] Starting recon for {domain}")

    # Subdomain discovery
    subs = run_cmd(f"subfinder -d {domain} -silent")
    with open(f"{REPORT_DIR}/{domain}/subdomains.txt", "w") as f:
        f.write(subs)

    # HTTPx
    run_cmd(f"cat {REPORT_DIR}/{domain}/subdomains.txt | httpx -silent > {REPORT_DIR}/{domain}/httpx.txt")

    # Waybackurls
    with open(f"{REPORT_DIR}/{domain}/httpx.txt", "r") as f:
        urls = f.read().splitlines()
        all_urls = ""
        for u in urls:
            all_urls += run_cmd(f"waybackurls {u}") + "\n"
    with open(f"{REPORT_DIR}/{domain}/waybackurls.txt", "w") as f:
        f.write(all_urls)

    # Nuclei scan
    run_cmd(f"cat {REPORT_DIR}/{domain}/httpx.txt | nuclei -severity {NUCLEI_SEVERITY} -c {NUCLEI_THREADS} -silent -o {REPORT_DIR}/{domain}/nuclei.txt")

    notify_discord(f"✅ Recon completed for `{domain}`.\nReports saved in `{REPORT_DIR}/{domain}/`")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 reconbot.py <domain>")
        exit(1)
    recon(sys.argv[1])
