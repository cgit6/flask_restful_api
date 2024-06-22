from db import db

class ItemModel(db.Model):

    # __tablename__ 是什麼意思?
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True) # 每一筆資料的 id
    name = db.Column(db.String(80), nullable=False) # 如果這邊加上 unique=True 則可以有多個同名的 item
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    
    # foreign key
    # 如果沒有對應的 store_id 則無法成功創建 item
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items") # 🤔 解釋一下這是什麼意思
    # 沒有一個模型添加了tag id或item id, 這兩個模型都將通過item_tags
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

# db.Column：
# 這是 SQLAlchemy 用來定義一個數據庫表中的列的構造函數。這裡，它被用來創建 price 這個列。
# db.Float(precision=2)：
# db.Float 是指定列類型為浮點數，這在存儲如價格這樣的小數時非常常見。
# precision=2 參數指定了浮點數的精度，這裡設為 2 位小數。這意味著數據庫會嘗試按照這種精度來存儲數據，但實際的存儲和精度保證取決於使用的具體數據庫系統。
# unique=False：
# 這個參數指定該列的值是否必須是唯一的。unique=False 表示不需要 price 的值是唯一的，多個項目可以有相同的價格。
# nullable=False：
# 這個參數決定這個列的值是否可以為空（NULL）。nullable=False 意味著這個列必須有值，不能為 NULL。這是數據庫完整性的一種保證，確保每個項目都必須有一個價格。