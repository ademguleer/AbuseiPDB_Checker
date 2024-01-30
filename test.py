# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 22:28:56 2024

@author: AdemGuler
"""

import requests

class AbuseIPDBChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2/check"

    def check_ip(self, ip_address):
        params = {'ipAddress': ip_address, 'maxAgeInDays': 90}
        headers = {'Key': self.api_key}
        # response = requests.get(self.base_url, params=params, headers=headers)

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"Error: {response.status_code}")
                print(response.text)  # Hata durumunda API'nin döndüğü cevabı yazdırın
                return None
        except requests.Timeout:
            print("Request is timeout.")
            return None
        except requests.RequestException as e:
            print(f"Hata: {e}")
            return None

# AbuseIPDB API anahtarını buraya yerleştirin
api_key = "6952ce29629c909dc1ed108e0ac89f2105205cf6ea92783062c9122bef48fe664434f8eb50ce1ae8"

# AbuseIPDBChecker sınıfından bir örnek oluşturun
abuseipdb_checker = AbuseIPDBChecker(api_key)

# Kontrol etmek istediğiniz IP adreslerini içeren bir txt dosyası oluşturun
# Her satır bir IP adresini içermelidir
ip_address_file_path = "test_malicuous.txt"

# Dosyayı açıp her bir IP adresini işleyin
with open(ip_address_file_path, 'r') as malicious_file:
    for line in malicious_file:
        # Satırdaki boşlukları temizleyip IP adresini alın
        ip_address = line.strip()

        # IP adresini kontrol et
        result = abuseipdb_checker.check_ip(ip_address)

        # JSON formatındaki çıktıyı kullanabilirsiniz
        print(result)
