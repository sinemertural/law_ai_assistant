import json
import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- AYARLAR ---
KANUN_DOSYASI = "/Users/sinemertural/Desktop/law_ai_assistant/json/kanunlar.json" 
VERITABANI_KLASORU = "/Users/sinemertural/Desktop/hukuk_db"

documents = []

# --- 1. KANUNLARI YÜKLEME ---
print(f"{KANUN_DOSYASI} okunuyor...")
try:
    with open(KANUN_DOSYASI, 'r', encoding='utf-8') as f:
        kanun_verisi = json.load(f)
        
    for veri in kanun_verisi:
        # JSON'dan alanları çekiyoruz
        madde = veri.get('madde_no', '')
        baslik = veri.get('baslik', '')
        icerik = veri.get('icerik', '')
        kategori = veri.get('kategori', '')
        
        # Anahtar kelimeler bir liste (['a', 'b']) olduğu için onları virgüle ayırarak metne çeviriyoruz
        anahtar_kelimeler_liste = veri.get('anahtar_kelimeler', [])
        anahtar_kelimeler_str = ", ".join(anahtar_kelimeler_liste) if isinstance(anahtar_kelimeler_liste, list) else str(anahtar_kelimeler_liste)
        
        # Yapay zekanın okuyacağı "Tek Parça Metin" (Chunk)
        # Burası ne kadar açıklayıcı olursa arama o kadar iyi sonuç verir.
        text = (
            f"Kanun Maddesi: {madde}\n"
            f"Başlık: {baslik}\n"
            f"İçerik: {icerik}\n"
            f"Kategori: {kategori}\n"
            f"İlgili Anahtar Kelimeler: {anahtar_kelimeler_str}"
        )
        
        # Metadata (Filtreleme yapmak istersek diye saklıyoruz)
        metadata = {
            "kaynak": "Kanun",
            "baslik": baslik,
            "kategori": kategori,
            "madde_no": madde
        }
        documents.append(Document(page_content=text, metadata=metadata))
    print(f"-> {len(kanun_verisi)} kanun maddesi başarıyla işlendi.")

except FileNotFoundError:
    print(f"HATA: {KANUN_DOSYASI} dosyası bulunamadı. Lütfen klasörde olduğundan emin ol.")
except json.JSONDecodeError:
    print(f"HATA: {KANUN_DOSYASI} formatı bozuk. Köşeli parantezlere [] ve virgüllere dikkat et.")
except Exception as e:
    print(f"HATA: Kanun dosyası okunurken beklenmedik hata: {e}")

# --- 3. VERITABANI OLUŞTURMA ---
if documents:
    print(f"\nToplam {len(documents)} veri parçacığı vektörleştiriliyor...")
    print("Embedding modeli yükleniyor... (Bu işlem işlemci hızına göre sürer)")
    
    # Türkçe desteği güçlü, ücretsiz model
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    print("Vektör veritabanı kaydediliyor...")
    db = Chroma.from_documents(
        documents=documents, 
        embedding=embedding_function, 
        persist_directory=VERITABANI_KLASORU
    )
    
    print(f"✅ HARİKA! Veritabanı '{VERITABANI_KLASORU}' klasörüne kaydedildi.")
    print("Şimdi chatbot yapma aşamasına geçebiliriz.")
else:
    print("❌ Hiç veri bulunamadı. JSON dosyalarını kontrol et.")