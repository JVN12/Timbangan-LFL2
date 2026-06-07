from machine import Pin
from hx711 import HX711
import time
import network
import urequests
# Dijalanin di laptop cia
'''
Link untuk mencatat hasil : 
https://docs.google.com/forms/d/e/1FAIpQLSco-g8zMMxvO8S1zijWbG9DrzryIpD7krykcKbMbkNYuHsUWg/
formResponse?usp=pp_url&entry.937330527=angka_berat
'''
# Ini hasil kalibrasi
OFFSET = 952370
SCALE = 1121

# Jalanin load cell
if __name__ == '__main__':
    hx = HX711(d_out=22, pd_sck=23)
    hx.channel = HX711.CHANNEL_A_128
    hx.power_on()
    
    # Persiapan filter
    N = 12
    data = []
    sum_data = 0
    alpha = 0.5
    filter_lama = 0
    filter_value = 0
    error = 0.0001
    Terkirim = False
    
    # Sambung wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("FisikaMesh","fisikaunpar")

    while not wifi.isconnected():
        print(".",end="")
        time.sleep(0.1)
    print("Terhubung dengan WiFi!")
    
    # Loop utama load cell
    while True:
        weight = (hx.read() - OFFSET)/SCALE
      
        # Filter IIR dengan Bobot
        if filter_lama == 0:
            filter_value = weight
        else:
            filter_value = alpha * weight + (1 - alpha) * filter_lama
      
        print(f"Filtered: {filter_value:.2f} g")
          
        # Kirim data ke Gform (saat data stabil)
        if abs(filter_value - filter_lama) < error and filter_value > 2 and not Terkirim: 
            url = f"https://docs.google.com/forms/d/e/1FAIpQLSco-g8zMMxvO8S1zijWbG9DrzryIpD7krykcKbMbkNYuHsUWg/formResponse?entry.937330527={filter_value:.2f}"
            urequests.get(url)
            Terkirim = True
        elif filter_value < 2 :
            Terkirim = False
        filter_lama = filter_value
