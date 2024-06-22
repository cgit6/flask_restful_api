# 在 item 與 tag 之間的輔助 Schema
# 多對多連結
from db import db
class ItemTags(db.Model):
    __tablename__ = "items_tags" # schema name
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    # 連結 items 與 tags

