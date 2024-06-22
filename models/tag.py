from db import db

class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    # unique=True 改成 unique=False，兩個標記都不能具有相同的名稱，現在希望把它改成
    # 如果 store_id 不同則 name 可以一樣
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    # 建立 store => items 的一對多關係
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")