from fastapi.testclient import TestClient
from app import schemas

# ====================== INTEGRATION TESTS ======================
def test_create_and_read_user(client):
    # POST
    response = client.post("/users/", json={"username": "intuser", "email": "int@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "intuser"
    user_id = data["id"]

    # GET single
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_list_users(client):
    client.post("/users/", json={"username": "user1", "email": "u1@example.com"})
    client.post("/users/", json={"username": "user2", "email": "u2@example.com"})
    
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_user(client):
    # Create
    post_resp = client.post("/users/", json={"username": "old", "email": "old@example.com"})
    user_id = post_resp.json()["id"]

    # PATCH – 
    response = client.patch(f"/users/{user_id}", json={"username": "newname", "email": "new@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newname"
    assert data["email"] == "new@example.com"

def test_delete_user(client):
    # Create
    post_resp = client.post("/users/", json={"username": "todel", "email": "del@example.com"})
    user_id = post_resp.json()["id"]
    
    # DELETE
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    # GET again → 404
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_create_category_and_product(client):
    # Category
    cat_resp = client.post("/categories/", json={"name": "Electronics"})
    assert cat_resp.status_code == 201
    cat_id = cat_resp.json()["id"]
    
    # Product
    prod_resp = client.post("/products/", json={"name": "Phone", "price": 1000, "category_id": cat_id})
    assert prod_resp.status_code == 201
    assert prod_resp.json()["category_id"] == cat_id

def test_create_order_with_products(client):
    # User
    user_resp = client.post("/users/", json={"username": "buyer", "email": "buy@example.com"})
    user_id = user_resp.json()["id"]
    
    # Category + Product
    cat_resp = client.post("/categories/", json={"name": "Tech"})
    cat_id = cat_resp.json()["id"]
    prod_resp = client.post("/products/", json={"name": "Laptop", "price": 2000, "category_id": cat_id})
    prod_id = prod_resp.json()["id"]
    
    # Order
    order_resp = client.post("/orders/", json={"user_id": user_id, "product_ids": [prod_id]})
    assert order_resp.status_code == 201
    order_data = order_resp.json()
    assert len(order_data["products"]) == 1
    assert order_data["products"][0]["id"] == prod_id

def test_get_order_not_found(client):
    response = client.get("/orders/99999")
    assert response.status_code == 404

def test_create_review(client):
    # Product oluştur
    cat_resp = client.post("/categories/", json={"name": "Games"})
    prod_resp = client.post("/products/", json={"name": "Game", "price": 60, "category_id": cat_resp.json()["id"]})
    prod_id = prod_resp.json()["id"]
    
    # Review
    review_resp = client.post("/reviews/", json={"text": "Awesome!", "product_id": prod_id})
    assert review_resp.status_code == 201

def test_delete_product(client):
    # Create product
    cat = client.post("/categories/", json={"name": "Tools"})
    prod = client.post("/products/", json={"name": "Hammer", "price": 50, "category_id": cat.json()["id"]})
    prod_id = prod.json()["id"]
    
    # Delete
    del_resp = client.delete(f"/products/{prod_id}")
    assert del_resp.status_code == 204
    
    # Get → 404
    get_resp = client.get(f"/products/{prod_id}")
    assert get_resp.status_code == 404

def test_invalid_request_bad_json(client):
    response = client.post("/users/", json={"username": "bad"})  # email eksik
    assert response.status_code == 422  # Validation error