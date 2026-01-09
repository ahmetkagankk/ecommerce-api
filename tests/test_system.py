from fastapi import status

# ====================== SYSTEM / E2E TESTS ======================
def test_full_user_to_order_flow(client):
    """Senaryo 1: Kullanıcı kaydı → Ürün ekleme → Sipariş oluşturma"""
    # Kullanıcı oluştur
    user_resp = client.post("/users/", json={"username": "e2e_buyer", "email": "buyer@example.com"})
    assert user_resp.status_code == status.HTTP_201_CREATED
    user_id = user_resp.json()["id"]

    # Kategori oluştur
    cat_resp = client.post("/categories/", json={"name": "E2E Category"})
    assert cat_resp.status_code == 201
    cat_id = cat_resp.json()["id"]

    # Ürün oluştur
    prod_resp = client.post("/products/", json={"name": "E2E Laptop", "price": 5000, "category_id": cat_id})
    assert prod_resp.status_code == 201
    prod_id = prod_resp.json()["id"]

    # Sipariş ver
    order_resp = client.post("/orders/", json={"user_id": user_id, "product_ids": [prod_id]})
    assert order_resp.status_code == 201
    order_id = order_resp.json()["id"]

    # Siparişi kontrol et
    get_order = client.get(f"/orders/{order_id}")
    assert get_order.status_code == 200
    order_data = get_order.json()
    assert order_data["user_id"] == user_id
    assert len(order_data["products"]) == 1
    assert order_data["products"][0]["name"] == "E2E Laptop"

def test_product_full_crud_cycle(client):
    """Senaryo 2: Ürün listeleme → Detay → Güncelleme → Silme"""
    # Kategori
    cat = client.post("/categories/", json={"name": "CRUD Cat"}).json()["id"]

    # Create
    create = client.post("/products/", json={"name": "Old Name", "price": 100, "category_id": cat})
    assert create.status_code == 201
    prod_id = create.json()["id"]

    # Listeleme (en az 1 ürün olsun)
    list_resp = client.get("/products/")
    assert list_resp.status_code == 200
    assert any(p["id"] == prod_id for p in list_resp.json())

    # Detay görüntüleme
    detail = client.get(f"/products/{prod_id}")
    assert detail.status_code == 200
    assert detail.json()["name"] == "Old Name"

    # Güncelleme
    update = client.patch(f"/products/{prod_id}", json={"name": "New Name", "price": 200})
    assert update.status_code == 200
    assert update.json()["name"] == "New Name"

    # Silme
    delete = client.delete(f"/products/{prod_id}")
    assert delete.status_code == 204

    # Tekrar detay → 404
    deleted = client.get(f"/products/{prod_id}")
    assert deleted.status_code == 404

def test_review_and_product_flow(client):
    """Senaryo 3: Ürün oluştur → Yorum ekle → Yorumları listele"""
    cat = client.post("/categories/", json={"name": "Review Cat"}).json()["id"]
    prod = client.post("/products/", json={"name": "Reviewed Item", "price": 300, "category_id": cat}).json()["id"]

    # Yorum ekle
    review = client.post("/reviews/", json={"text": "Çok beğendim!", "product_id": prod})
    assert review.status_code == 201

    # Yorumları listele
    reviews = client.get("/reviews/")
    assert reviews.status_code == 200
    review_list = reviews.json()
    assert any(r["product_id"] == prod and r["text"] == "Çok beğendim!" for r in review_list)

def test_multiple_products_in_order(client):
    """Senaryo 4: Bir siparişte birden fazla ürün"""
    user = client.post("/users/", json={"username": "multi_buyer", "email": "multi@example.com"}).json()["id"]
    cat = client.post("/categories/", json={"name": "Multi Cat"}).json()["id"]

    prod1 = client.post("/products/", json={"name": "Item1", "price": 100, "category_id": cat}).json()["id"]
    prod2 = client.post("/products/", json={"name": "Item2", "price": 200, "category_id": cat}).json()["id"]
    prod3 = client.post("/products/", json={"name": "Item3", "price": 300, "category_id": cat}).json()["id"]

    order = client.post("/orders/", json={"user_id": user, "product_ids": [prod1, prod2, prod3]})
    assert order.status_code == 201
    data = order.json()
    assert len(data["products"]) == 3
    product_names = {p["name"] for p in data["products"]}
    assert product_names == {"Item1", "Item2", "Item3"}

def test_complex_interaction_all_resources(client):
    """Senaryo 5: Tüm kaynaklarla kompleks akış"""
    # Kullanıcı + Kategori + Ürün + Yorum + Sipariş
    user = client.post("/users/", json={"username": "complex_user", "email": "complex@example.com"}).json()["id"]
    cat = client.post("/categories/", json={"name": "Complex Cat"}).json()["id"]
    prod = client.post("/products/", json={"name": "Ultimate Product", "price": 9999, "category_id": cat}).json()["id"]

    # Yorum ekle
    client.post("/reviews/", json={"text": "Hayatımın ürünü!", "product_id": prod})

    # Sipariş ver
    order = client.post("/orders/", json={"user_id": user, "product_ids": [prod]})
    assert order.status_code == 201

    # Tüm listeleri kontrol et
    assert client.get("/users/").json()  # boş değil
    assert client.get("/categories/").json()
    assert client.get("/products/").json()
    assert client.get("/reviews/").json()
    assert client.get("/orders/").json()