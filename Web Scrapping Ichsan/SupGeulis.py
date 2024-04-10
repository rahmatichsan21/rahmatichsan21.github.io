from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

# URL target
url = "https://www.republika.co.id/"

# Mengambil halaman web
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Mendapatkan waktu scraping
scraping_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Mendapatkan semua data yang diperlukan
data = []
captions = soup.select('div.col-md-9 div.caption')
for caption in captions:
    category_elem = caption.select_one('span.kanal-info')
    title_elem = caption.select_one('h3 span')
    time_elem = caption.select_one('div.date')
    
    category = category_elem.text.strip() if category_elem else "Tidak ditemukan"
    title = title_elem.text.strip() if title_elem else "Tidak ditemukan"
    time_ago = time_elem.text.strip().split("-")[-1].strip() if time_elem else "Tidak ditemukan"
    
    data.append({
        "kategori": category,
        "judul": title,
        "waktu_publish": time_ago
    })

# Menyimpan data dalam file JSON
output_file = "data_republika.json"
output_data = {
    "waktu_scraping": scraping_time,
    "data": data
}
with open(output_file, "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("Data telah disimpan dalam file", output_file)
