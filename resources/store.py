import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort # Blueprint一種
from sqlalchemy.exc import SQLAlchemyError, IntegrityError # 錯誤處理

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

# 把一個路徑的方法寫在一個物件中
@blp.route("/store")
class StoreList(MethodView):
    # 顯示所有的 store
    @blp.response(200, StoreSchema(many=True)) # 🤔裝飾函數?
    def get(self):
        return StoreModel.query.all()
    
    # 創建新的 store
    @blp.arguments(StoreSchema) # 檢查資料格式
    @blp.response(201, StoreSchema) # 定義返回的格式
    # store_data是 client 端送來的資料
    def post(self, store_data):
        # 被 Schema 取代
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(400,message="Bad request. Ensure 'name' is included in the JSON payload")
        
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists.")
        # store_id = uuid.uuid4() .hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        # return store

        store = StoreModel(**store_data)
        try:
            db.session.add (store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="已經存在同名商店。")
        except SQLAlchemyError:
            abort(500, message="創建商店時出錯。")
        return store



# 
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema) 
    def get(self, store_id):
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")
        
        store = StoreModel.query.get_or_404(store_id)
        return store # 返回物件
    
    # 獲得特定 store_id 的所有訊息包括name,item

    # 刪除 store
    # 因為 delete 只會返回 文字所以不用使用 @...
    def delete(self, store_id):
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")

        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}