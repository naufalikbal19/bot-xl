import requests
import ftplib
import os
import schedule
import time

# Konfigurasi FTP
ftp_host = 'ftpupload.net'  # Ganti dengan host FTP Anda
ftp_username = 'if0_37474190'     # Ganti dengan username FTP Anda
ftp_password = 'mgEovM0mYD0O'    # Ganti dengan password FTP Anda
file_path = 'htdocs/admin/list.txt'  # Path ke file list.txt di server FTP
output_file_path = 'htdocs/admin/output.php'  # Path untuk upload output HTML

# Fungsi untuk melakukan pemeriksaan domain
def cek_domain(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=15)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

# Fungsi untuk mengambil daftar domain dari FTP
def get_domain_list():
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_username, ftp_password)
        with open('list.txt', 'wb') as f:
            ftp.retrbinary(f'RETR {file_path}', f.write)
    with open('list.txt', 'r') as f:
        return f.read().splitlines()

# Fungsi untuk menyimpan output ke file PHP
def save_output_to_php(results):
    with open('output.php', 'w') as f:
        f.write("<?php\n")
        # Inisialisasi counter untuk status
        status_counter = 1
        
        for domain, status in results:
            f.write(f"$status[{status_counter}] = '{status}';\n")  # Simpan status dengan penambahan angka
            status_counter += 1  # Tambah counter
        f.write("?>\n")
# Fungsi untuk mengupload file ke FTP
def upload_to_ftp(file_name, remote_path):
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_username, ftp_password)
        with open(file_name, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)

# Fungsi utama
def main():
    domains = get_domain_list()
    results = []
    for domain in domains:
        if cek_domain(domain):
            status = 'aman'
        else:
            status = 'blocked'
        results.append((domain, status))
        print(f"Bot Sedang Berjalan....")
    
    save_output_to_php(results)  # Ganti pemanggilan fungsi untuk menyimpan output
    upload_to_ftp('output.php', output_file_path)  # Upload file output.php ke FTP

def run_script():
    main()

schedule.every(1).minutes.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)
