from flask import Flask, request

app = Flask(__name__) # 創建 flask app

# 當前數據，而且只存在於 memory 中
stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]

# 目標是讓使用者可以創建自己的 store(name)，item (name, price)資料

# 測試一下能不能用
@app.get("/test")
def test():
    return "運作正常2"

@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": stores}

# 創建一個新的 store
@app.post("/store")
def create_store():
    # 將接收到的內容轉換為 dict
    request_data = request.get_json()
    # 創建的內容格式=> {name:string, items:array}
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

# 創建 item
@app.post("/store/<string:name>/item")
# name 是上面<string:name> 的 store name
def create_item(name):
    # 將後端接收到的json訊息轉換成dict
    request_data = request.get_json()
    # 遍歷每個 store 如果有符合 name，則在原本的那個 store 中依照item 的格式新增 new_item
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201

    # 如果找不到則回傳失敗
    return {"message": "Store not found"}, 404
# 🤔 如果有兩個相同店家名稱怎麼辦?
# 如果接收到的 name 不正確怎麼辦? 可不可以用 ML 找到最接近的店家名稱詢問是不是這個

# 這是一查詢功能，查詢特定店家，返回訊息
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

# 取得特定店家的所有 item 訊息
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
