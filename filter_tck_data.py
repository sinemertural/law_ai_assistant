# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 15:37:45 2025
@author: Asus
"""

import pandas as pd
import json

# -----------------------------------------------------
# 1. PC'DEKİ CSV DOSYASINI YÜKLE
# -----------------------------------------------------

file_path = r"C:\Users\Asus\Desktop\turkish_law_dataset.csv"

df = pd.read_csv(file_path, encoding="utf-8")

print("Dataset ilk 5 kayıt:")
print(df.head())
print("\nToplam kayıt:", len(df))

# -----------------------------------------------------
# 2. TCK İLE İLGİLİ SATIRLARI FİLTRELE
# -----------------------------------------------------

pattern = r"TCK|Türk Ceza Kanunu|Ceza Kanunu|TCK\s*\d+"

tck_df = df[
    df['soru'].astype(str).str.contains(pattern, case=False, na=False) |
    df['cevap'].astype(str).str.contains(pattern, case=False, na=False) |
    df['context'].astype(str).str.contains(pattern, case=False, na=False)
]

print("\nTCK ile ilgili toplam kayıt:", len(tck_df))
print(tck_df.head())

# -----------------------------------------------------
# 3. FİLTRELENEN VERİYİ CSV OLARAK MASAÜSTÜNE KAYDET
# -----------------------------------------------------

csv_out = r"C:\Users\Asus\Desktop\tck_filtered.csv"
tck_df.to_csv(csv_out, index=False, encoding="utf-8")

print(f"\nCSV kaydedildi: {csv_out}")

# -----------------------------------------------------
# 4. JSON FORMATINA DÖNÜŞTÜR VE MASAÜSTÜNE KAYDET
# -----------------------------------------------------

json_records = []

for _, row in tck_df.iterrows():
    record = {
        "soru": row.get("soru", None),
        "cevap": row.get("cevap", None),
        "cevaplayan_unvan": row.get("kaynak", None),
        "tarih": row.get("tarih", None) if "tarih" in row else None
    }
    json_records.append(record)

json_out = r"C:\Users\Asus\Desktop\tck_filtered.json"

with open(json_out, "w", encoding="utf-8") as f:
    json.dump(json_records, f, ensure_ascii=False, indent=4)

print(f"JSON kaydedildi: {json_out}")
