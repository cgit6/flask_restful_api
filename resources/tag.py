from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")

# 取得某個 store_id 的 tag
@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    # 
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id) # 找到 store 的所有 tag
        return store.tags.all()

    # 新增 tag(一對多)
    @blp.arguments (TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        tag = TagModel(**tag_data, store_id=store_id)
        print(tag)

        try:
            db. session.add(tag) # 加入 tag 
            db.session.commit() # 更新資料庫
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db. session.commit()
        except SQLAlchemyError:
            abort(500, message="插入tag時發生錯誤")
        return tag

    # 移除 item 的 tag
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="插入tag時發生錯誤")
        return {"message": "item已從tag中刪除", "item": item, "tag": tag}


# 
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    # 
    @blp.response(202,description="Deletes a tag if no item is tagged with it.",example={"message": "tag 已刪除"})
    @blp.alt_response(404, description="找不到 Tag")
    @blp.alt_response(400,description="如果 tag 指派給一或多個item，則傳回。在這種情況下，tag不會被刪除")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        # 如果有 tag.items
        if not tag.items:
            db.session.delete(tag) # 刪除
            db.session.commit()
            return {"message": "tag 已刪除"}
        abort(400, message="無法刪除 tag。請確保 tag 未與任何 item 關聯，然後重試",)


