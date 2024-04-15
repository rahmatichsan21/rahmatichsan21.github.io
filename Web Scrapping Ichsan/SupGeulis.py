from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import os
import time

def scrape_and_append():
    # URL target
    url = "https://www.republika.co.id/"

    # Mengambil halaman web
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Mendapatkan waktu scraping
    scraping_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Mendapatkan data berita terbaru
    data = []
    captions = soup.select('div.col-md-9 div.caption')
    if captions:
        for caption in captions:
            category_elem = caption.select_one('span.kanal-info')
            title_elem = caption.select_one('h3 span')
            time_elem = caption.select_one('div.date')

            category = category_elem.text.strip() if category_elem else "Tidak ditemukan"
            title = title_elem.text.strip() if title_elem else "Tidak ditemukan"
            time_ago = time_elem.text.strip().split("-")[-1].strip() if time_elem else "Tidak ditemukan"

            data.append({
                "waktu_scraping": scraping_time,
                "kategori": category,
                "judul": title,
                "waktu_publish": time_ago
            })

    # Menyimpan data dalam file JSON
    output_file = "data_republika.json"
    if os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, "r") as json_file:
            existing_data = json.load(json_file)
            existing_data.extend(data)
            data_to_write = existing_data
    else:
        data_to_write = data

    with open(output_file, "w") as json_file:
        json.dump(data_to_write, json_file, indent=4)
        json_file.write('\n')

    print("Data telah disimpan dalam file", output_file)

# Menjadwalkan scraping setiap 10 menit
while True:
    scrape_and_append()
    time.sleep(600)  # Delay 10 menit
