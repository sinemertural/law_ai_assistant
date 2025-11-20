# Önce gerekli kütüphaneleri kurmalısın (Terminal veya hücreye yaz):
# !pip install datasets pandas

from datasets import load_dataset
import pandas as pd

def veri_setini_hazirla():
    print("1. Veri seti Hugging Face'den indiriliyor...")
    try:
        # Veri setini yükle
        dataset = load_dataset("alibayram/hukuk_soru_cevap", split="train")
        df = dataset.to_pandas()
        print(f"   -> Toplam veri sayısı: {len(df)}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return

    # 2. Anahtar Kelimeleri Tanımla
    # Bu kelimeler soruda veya cevapta geçiyorsa "Ceza Hukuku" kabul edeceğiz.
    ceza_kelimeleri = [
        "ceza", "suç", "hapis", "tutuklama", "gözaltı", "ifade", 
        "savcı", "sanık", "mağdur", "şüpheli", "TCK", "ağır ceza",
        "asliye ceza", "denetimli serbestlik", "sabıka", "infaz",
        "yaralama", "tehdit", "hakaret", "hırsızlık", "dolandırıcılık",
        "öldürme", "yağma", "cinsel", "uyuşturucu", "kaçakçılık"
    ]

    # Bu kelimeler geçiyorsa eleyeceğiz (Hukuk ama Ceza değil)
    yasakli_kelimeler = [
        "boşanma", "nafaka", "velayet", "mal paylaşımı", "aile mahkemesi",
        "kira", "tahliye", "depozito", "işçi", "işveren", "kıdem", "ihbar",
        "tazminat", "senet", "çek", "icra", "borç", "tapu", "kadastro",
        "tüketici hakem heyeti", "ayıplı mal"
    ]

    print("2. Ceza Hukuku verileri ayıklanıyor...")
    
    filtered_data = []

    for index, row in df.iterrows():
        # Metni küçük harfe çevir ki büyük/küçük harf sorunu olmasın
        metin = (str(row['soru']) + " " + str(row['cevap'])).lower()
        
        # Yasaklı kelime var mı? Varsa atla.
        if any(kelime in metin for kelime in yasakli_kelimeler):
            continue
            
        # Ceza kelimesi var mı? Varsa listeye ekle.
        if any(kelime in metin for kelime in ceza_kelimeleri):
            filtered_data.append(row)

    # Yeni DataFrame oluştur
    df_ceza = pd.DataFrame(filtered_data)
    
    print(f"3. İşlem tamamlandı!")
    print(f"   -> Toplam veri: {len(df)}")
    print(f"   -> Ceza Hukuku verisi: {len(df_ceza)}")
    print(f"   -> Elenen (Diğer hukuk dalları): {len(df) - len(df_ceza)}")

    # 4. Dosyaları Kaydet
    df_ceza.to_csv("ceza_hukuku_soru_cevap.csv", index=False, encoding='utf-8-sig') # Excel için
    df_ceza.to_json("ceza_hukuku_soru_cevap.json", orient='records', force_ascii=False, indent=4) # Model eğitimi için
    
    print("\nDosyalar kaydedildi: 'ceza_hukuku_soru_cevap.json' ve .csv")
    print("Şimdi bu dosyalara göz atabilirsin.")

# Fonksiyonu çalıştır
veri_setini_hazirla()