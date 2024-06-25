from flask.views import MethodView
from flask_smorest import Blueprint, abort # Blueprint一種
from flask_jwt_extended import jwt_required, get_jwt #
from sqlalchemy.exc import SQLAlchemyError # 錯誤處理


from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True)) # 🤔 這句話再說什麼?以 JSON 列表的形式返回。
    def get(self):
        return ItemModel.query.all()
    
    # 任務 :向特定 id 添加(post)新的 item
    # 期望的資料格式是什麼?
    @jwt_required()
    @blp.arguments(ItemSchema) # 用於檢查資料格式
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json() # 取得 POST 的內容，不過因為用schemas 傳回來的已經是 dict 了不用轉換
        
        # 👽 這部分被schema 取代
        # # 先檢查傳入的內容是否完整
        # if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
        #     abort(400,message="Bad request. Ensure 'price', 'store_id', and 'name' are included")
        # # 檢查唯一性
        # for item in items.values():
        #     if(item_data["name"] == item["Fhame"] and item_data["store_id"] == item["store_id"]):
        #         abort(400, message=f"Item already exists.")
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item

        item = ItemModel(**item_data)
        try:
            db.session.add(item) # 更新數據
            db.session.commit() # 上傳到資料庫
        except SQLAlchemyError:
            abort(500, message="插入 item 時發生錯誤。")
        return item

# 對特定物品做什麼?
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    # 取得
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found.")

        item = ItemModel.query_get_or_404(item_id)
        return item
    
    # 刪除 item
    # 比如說 url/item/1 然後就會 item_id 為 1 的資料
    @jwt_required()
    def delete(self, item_id):
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     abort(404, message="Item not found.")
        
        # admin方法2:
        jwt = get_jwt() # 應該會返回 bool
        if not jwt.get("is_admin"):
            abort(401, messsage="需要管理員權限")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item) # 刪除資料
        db.session.commit() # 更新資料庫
        return {"message": "Item deleted."}


    # 更新
    @blp.arguments(ItemUpdateSchema) # 用於檢查資料格式
    @blp.response(200, ItemSchema) # 路由被成功處理並返回結果時，應該返回什麼樣的數據結構和 HTTP 狀態碼。
    def put(self,item_data, item_id):

        # 這邊被 Schema 取代
        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
        # try:
        #     item = items[item_id]
        #     # https://blog.teclado.com/python-dictionary-merge-update-operators/
        #     item |= item_data # 🤔 |= 是什麼?
        #     return item
        # except KeyError:
        #     abort(404, message="Item not found.")

        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not implemented.")
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
