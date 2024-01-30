# -*- coding: utf-8 -*-

import requests
import unittest

class AbuseIPDBChecker():
    def __init__(self, api_key):
        """
        AbuseIPDBChecker sınıfı, AbuseIPDB API ile IP adreslerini kontrol etmek için kullanılır.

        Args:
            api_key (str): AbuseIPDB API anahtarı.

        Usage:
            checker = AbuseIPDBChecker(api_key)
            result = checker.check_ip("test_malicuous.txt")
        """
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2/check"

    def check_ip(self, ip_address):
        """
        Verilen IP adresini AbuseIPDB API kullanarak kontrol eder.

        Args:
            ip_address (str): Kontrol edilecek IP adresi.

        Returns:
            dict or None: API'den alınan yanıtın sözlük temsilini döndürür. Hata durumunda None.

        Usage:
            result = checker.check_ip("test_malicuous.txt")
        """
        url = self.base_url
        headers = {'Key': self.api_key}
        params = {'ipAddress': ip_address, 'maxAgeInDays': 90}
    
        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"Error: {response.status_code}")
                print(response.text)  # Hata durumunda API'nin döndüğü cevabı yazdırır
                return None
        except requests.Timeout:
            print("İstek zaman aşımına uğradı.")
            return None
        except requests.RequestException as e:
            print(f"Hata: {e}")
            return None

# AbuseIPDB API anahtarını buraya yerleştirin
api_key = "6952ce29629c909dc1ed108e0ac89f2105205cf6ea92783062c9122bef48fe664434f8eb50ce1ae8"

# AbuseIPDBChecker sınıfından bir örnek oluşturur
abuseipdb_checker = AbuseIPDBChecker(api_key)

# Kontrol etmek istenilen IP adreslerini içeren bir txt dosyası oluşturur
ip_address_file_path = "test_malicious.txt"

# Dosya içindeki ip adreslerini alır
with open(ip_address_file_path, 'r') as file:
    for line in file:
        # Satırda boşluklar varsa temizleyip IP adresini alır
        ip_address = line.strip()

        # IP adresini kontrol eder
        result = abuseipdb_checker.check_ip(ip_address)

        # JSON formatındaki çıktı üretir
        print(result)


class TestAbuseIPDBChecker(unittest.TestCase):
    """
    "setUp" metodu, her bir test çalışmadan önce API anahtarını ve AbuseIPDBChecker'ı oluşturur.
    """
    def setUp(self):
        self.api_key = api_key
        self.checker = AbuseIPDBChecker(self.api_key)

    def test_check_malicious_ip(self):
        ip_address_file_path = "test_malicious.txt"
        ip_address = "1.0.210.101"

        # Read all IP addresses from the file
        with open(ip_address_file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file]

        # Check if IP address is in the list
        is_malicious = ip_address in ip_addresses

        result = self.checker.check_ip(ip_address)
        self.assertIsNotNone(result)

        if is_malicious:
            self.assertTrue(result)
        else:
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()