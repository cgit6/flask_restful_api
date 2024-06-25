from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # 🤔# lazy="dynamic"它不會在你加載 StoreModel 對象時自動加載所有相關的 ItemModel 對象。
    # 相反，它提供了一個查詢生成器，讓你可以按需執行更複雜的查詢，例如篩選特定條件的商品。
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete") 
    # 加入 tag 標籤，如果不使用 lazy="dynamic" 它將向資料庫中進行查詢以獲取所有標記資訊
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")

# 如果刪除已經存在的 store 那 store 中的item 會出現 name 中的 nullable=False 被違反
# 解決方案是如果刪除了 store 時，裡面的item 也會一併刪除 => 用 cascade="all, delete, delete-orphan" 處理


# 如果沒有  lazy="dynamic" 則每次 fetch 時 items、tags 都會返回