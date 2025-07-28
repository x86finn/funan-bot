import requests
import threading
import time
import os
from colorama import Fore, init

init(autoreset=True)

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

print(Fore.RED + "     FUNAN PAGE REPORT TOOL (MT)      ")

# User input
fb_url = input(Fore.YELLOW + "[+] Enter Facebook post/profile URL to report: ").strip()
total_reports = input(Fore.CYAN + "[+] Total reports to send (e.g. 10): ").strip()
threads = input(Fore.CYAN + "[+] Number of threads (e.g. 5): ").strip()
delay = input(Fore.CYAN + "[+] Delay between batches in seconds (default 5): ").strip()

# Validate inputs
total_reports = int(total_reports) if total_reports.isdigit() and int(total_reports) > 0 else 1
threads = int(threads) if threads.isdigit() and int(threads) > 0 else 1
delay = float(delay) if delay.replace('.', '').isdigit() else 5.0

# Facebook report endpoint
url = 'https://m.facebook.com/help/contact/209046679279097'

# Data to send
def send_report(report_id):
    data = {
        'crt-url': fb_url,
        'cf_age': "less than 9 years",
        'submit': 'submit'
    }
    try:
        res = requests.post(url, data=data, timeout=10)
        if res.status_code == 200:
            print(Fore.GREEN + f"[✓] Report #{report_id} sent successfully.")
        else:
            print(Fore.RED + f"[✗] Report #{report_id} failed. Status: {res.status_code}")
    except Exception as e:
        print(Fore.RED + f"[!] Error on report #{report_id}: {e}")

# Main logic with batches
def batch_runner():
    report_id = 1
    while report_id <= total_reports:
        current_batch = min(threads, total_reports - report_id + 1)
        thread_list = []
        for i in range(current_batch):
            t = threading.Thread(target=send_report, args=(report_id,))
            t.start()
            thread_list.append(t)
            report_id += 1

        # Wait for all threads in this batch
        for t in thread_list:
            t.join()

        if report_id <= total_reports:
            print(Fore.YELLOW + f"\n[~] Waiting {delay}s before next batch...\n")
            time.sleep(delay)

# Start
print(Fore.MAGENTA + f"\n[+] Sending {total_reports} reports using {threads} threads...\n")
batch_runner()
print("Successfully reported")
