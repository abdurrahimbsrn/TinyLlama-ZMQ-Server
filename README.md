# TinyLlama-ZMQ-Server

TinyLlama modelini Docker container'ında ZeroMQ arayüzüyle sunan hafif bir sunucu uygulaması.

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![ZeroMQ](https://img.shields.io/badge/ZeroMQ-✓-green?logo=zeromq)
![TinyLlama](https://img.shields.io/badge/TinyLlama-1.1B-ff69b4)

## Özellikler

- 🐳 Docker container desteği
- ⚡ ZeroMQ ile yüksek performanslı mesajlaşma
- 🤖 TinyLlama-1.1B-Chat model entegrasyonu
- 🔌 JSON tabanlı API arayüzü
- 📊 Sistem kaynak kullanım optimizasyonu

## Kurulum

### 1. Docker ile Çalıştırma

```bash
docker build -t tinyllama-server .
docker run -p 5555:5555 --gpus all tinyllama-server
```

### 2. Manuel Kurulum

```bash
git clone https://github.com/sizin-kullanici-adi/tinyllama-zmq-server.git
cd tinyllama-zmq-server
pip install -r requirements.txt
python server.py
```

## Kullanım

### İstemci Örneği (Python)

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

messages = [
    {
        "role": "system",
        "content": "Sen eğlenceli bir korsan asistansın. Kısa ve net cevaplar ver."
    },
    {   
        "role": "user", 
        "content": "Deniz neden tuzludur?"
    }
]

payload = {
    "messages": messages,
    "max_tokens": 60
}

socket.send_string(json.dumps(payload))
response = json.loads(socket.recv_string())
print(response["response"])
```

### API Formatı

**İstek:**
```json
{
    "messages": [
        {"role": "system", "content": "Sistem mesajı"},
        {"role": "user", "content": "Kullanıcı sorusu"}
    ],
    "max_tokens": 60
}
```

**Yanıt:**
```json
{
    "response": "Model yanıtı",
    "tokens_used": 42,
    "status": "success"
}
```

## Yapılandırma

Çevre değişkenleri:

| Değişken       | Varsayılan Değer               | Açıklama                     |
|----------------|-------------------------------|-----------------------------|
| `MODEL_PATH`   | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | Model yolu                 |
| `ZMQ_PORT`     | `5555`                        | ZeroMQ bağlantı portu       |
| `MAX_TOKENS`   | `100`                         | Maksimum token sayısı       |

## Katkıda Bulunma

1. Forklayın (`https://github.com/sizin-kullanici-adi/tinyllama-zmq-server/fork`)
2. Yeni branch oluşturun (`git checkout -b feature/fooBar`)
3. Değişikliklerinizi commit edin (`git commit -am 'Add some fooBar'`)
4. Push yapın (`git push origin feature/fooBar`)
5. Pull Request oluşturun

## Lisans

Apache License 2.0 - Bkz. [LICENSE](LICENSE) dosyası

---

> **Not:** TinyLlama modeli bazen tutarsız cevaplar üretebilir. Daha stabil sonuçlar için sistem prompt'unuzu optimize edin.
