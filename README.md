
[![Tests](https://github.com/ahmetkagankk/ecommerce-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetkagankk/ecommerce-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/ahmetkagankk/ecommerce-api/branch/main/graph/badge.svg)](https://codecov.io/gh/ahmetkagankk/ecommerce-api)


# E-Commerce REST API

## Proje Açıklama
5 farklı kaynak içeren REST API projesi:
- users
- products
- orders
- categories
- reviews

İlişkiler:
- User → Order (one-to-many)
- Order → Product (many-to-many)
- Product → Category (many-to-one)
- Product → Review (one-to-many)

Teknolojiler
- Backend: Python + FastAPI
- Veritabanı: SQLite + SQLAlchemy
- Test: Pytest
- Dokümantasyon: FastAPI Swagger UI (OpenAPI 3.0)

## Kurulum Talimatları
1. Repo'yu klonla:
git clone https://github.com/ahmetkagankk/ecommerce-api.git
cd ecommerce-api
text2. Sanal ortam oluştur ve aktif et:
python -m venv venv
venv\Scripts\activate
text3. Bağımlılıkları kur:
pip install -r requirements.txt
text4. Uygulamayı çalıştır:
uvicorn main:app --reload
text## API Dokümantasyon
Uygulama çalıştığında şu adrese git:
http://localhost:8000/docs

Swagger UI üzerinden tüm endpoint'leri test edebilirsin.

## API Endpoint Listesi ve Örnekler
- **Users**
- GET /users/ → Tüm kullanıcılar
- GET /users/{id} → Tek kullanıcı
- POST /users/ → Yeni kullanıcı (örnek: {"username": "ali", "email": "ali@example.com"})
- PATCH /users/{id} → Güncelle
- DELETE /users/{id} → Sil

- **Categories**
- GET /categories/
- POST /categories/ → {"name": "Elektronik"}

- **Products**
- GET /products/
- POST /products/ → {"name": "Telefon", "price": 10000, "category_id": 1}

- **Reviews**
- POST /reviews/ → {"text": "Harika!", "product_id": 1}

- **Orders**
- POST /orders/ → {"user_id": 1, "product_ids": [1, 2]}

## Test Çalıştırma
- pytest -q


## CI/CD
[![Tests](https://github.com/ahmetkagankk/ecommerce-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetkagankk/ecommerce-api/actions)
[![Coverage](https://codecov.io/gh/ahmetkagankk/ecommerce-api/graph/badge.svg)](https://codecov.io/gh/ahmetkagankk/ecommerce-api)
