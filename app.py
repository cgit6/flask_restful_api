from flask import Flask, request
from flask_smorest import Api
import os
# 新的需求
from db import db
import models

# 路徑管理
from resources.item import blp as ItemBlueprint 
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

def create_app(db_url =None):

    app = Flask(__name__)

    # 整個服務的基礎設定
    app.config["PROPACATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/" # 根節點
    # 告訴flasks更多的我們使用swagger的API文件
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # 使用 sqllite3 作為開發時的資料庫
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    db.init_app(app) # 初始化 Flask SQLAlchemy

    # 創建資料庫
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint (StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    
    return app






# ============================================================= #

# import uuid
# from flask_smorest import abort # 利用 abort 返回錯誤訊息
# from db import items, stores # 資料庫
# # 測試一下能不能用
# @app.get("/test")
# def test():
#     return "運作正常2"

# @app.get("/store")
# def get_stores():
#     # 🤔為什麼這邊要用 list()?
#     return {"stores": list(stores.values())}

# # 獲得特定 store_id 的所有訊息包括name,item
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         # 找到對應的 store_id
#         return stores[store_id] # 返回

#     except KeyError:
#         # 如果找不到
#         abort(404, message="Store not found")

# # POST 方法
# # 從 client 送出 name
# @app.post("/store")
# def create_store():
#     store_data = request.get_json() # 將收到得json 格式轉換為 dict
#     # 檢查內容是否完整
#     if "name" not in store_data:
#         abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
#     # 檢查創建的 name 是否已經存在(確保唯一性)
#     for store in stores.values():
#         if storre_data["name"] == store["name"]:
#             abort(400, message=f"Store already exists.")

#     store_id = uuid.uuid4().hex # 生成一個唯一的id(還是有可能產生碰撞)
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store # 加入到 stores 中
#     return store, 201 # 返回當前數據狀態，狀態碼

# # 刪除 store
# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         abort(404, message="Store not found.")


# # 返回所有的 items
# @app.get("/item")
# def get_all_items():
#     # 🤔為什麼這邊要用 list()?
#     return {"item": list(items.values())}

# # 指返回匹配的 name 的 item 訊息
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     # 如果存在
#     try:
#         return items[item_id] # 
#     except KeyError:
#         abort(404, message="Item not found")

# # 任務 :向特定 id 添加(post)新的 item
# @app.post("/item")
# def create_item():
#     item_data = request.get_json() # 取得 POST 的內容
#     # 先檢查傳入的內容是否完整
#     if("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
#         abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
#     # 對每個 item 檢查是否重複，如果 物品可以重複的情況下呢?
#     for item in items.values():  
#         if(item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
#             abort(400, message=f"Item already exists.")

#     # 這是什麼?
#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found")
    
#     item_id = uuid.uuid4().hex # 生成一個唯一的id(還是有可能產生碰撞)
#     item = {**item_id,"id": item_id}
#     items[item_id] = item # 加入到 stores 中
    
#     return item, 201
# # 如果兩筆資料名稱重複怎麼處理?
# # 如果name 不正確怎麼辦?

# # 更新 item
# # 輸入: name,price
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     # 
#     if "price" not in item_data or "name" not in item_data:
#         abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
#     try:
#         item = items[item_id]
#         item |= item_data # 🤔 |= 是什麼?
#         return item
#     except KeyError:
#         abort(404, message="Item not found.")

# # 刪除 item
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id] # 執行刪除 item 的操作
#         return {"message": "Item deleted."}
#     except KeyError:
#         abort(404, message="Item not found.")









