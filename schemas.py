from marshmallow import Schema, fields

# 定義 item 的資料格式
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) #🤔 什麼意思?
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    # store_id = fields.Str(required=True)

# Store 資料格式
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) # 這個不用填資料庫會自己生成
    name = fields.Str(required=True) # 創建時填 name

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

# =======================================================================
# 創建 store
# 期望格式
# {
#     "name": "test_store_2"
# }
class StoreSchema(PlainStoreSchema):
    # items = fields.List(fields.Nested(lambda: ItemSchema()), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

# 新增 item
# 期望的格式
# {
#     "name":"chair2",
#     "price":334,
#     "store_id":2
# }
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    # store = fields.Nested(lambda: StoreSchema(), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


# 更新的 item 資料格式
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

# =======================================================================

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

# 用於tag和item, 當我們希望返回有關相關item和tag的信息時
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

# 當你在 `marshmallow` 的 `Schema` 定義中使用 `dump_only=True` 這個選項時，這意味著指定的字段只在序列化（即將數據對象轉換為可傳遞或存儲的格式，如 JSON）時包括，並不在反序列化（即將接收到的數據如 JSON 轉換回 Python 對象）時處理。

# ### 理解 `dump_only=True`
# - **序列化**是指將應用程序的內部數據（例如來自數據庫的數據）轉換為一種格式（通常是 JSON），以便可以輕鬆地通過網絡發送或存儲。當你想要向用戶展示數據時，你會進行序列化。
# - **反序列化**是指將接收到的數據（如來自前端的 JSON 請求）轉換回應用程序能處理的內部數據格式（如 Python 對象）。這在用戶提交數據到後端時常見。
# 使用 `dump_only=True` 的常見場景是對於那些由系統生成或控制的數據字段，比如數據庫的主鍵 `id`。在這種情況下，`id` 字段在創建對象時通常是由數據庫自動產生的，你不希望用戶能夠在創建新紀錄時提交自定義的 `id`，因此在從前端接收數據時，你不處理 `id` 字段。但是，在向用戶顯示數據時，`id` 是需要被包含在內的。
# ### 示例解釋
# 在你的 `PlainItemSchema` 中，`id` 字段被標記為 `dump_only=True`，意味著：
# - 當從數據庫中提取物品信息並需要將其發送給前端（例如，作為 API 響應的一部分）時，`id` 字段會被包括在內。
# - 當從前端接收 JSON 數據並將其轉換為後端的 Python 對象時，`id` 字段將被忽略，防止用戶覆蓋或提供自定義的 `id` 值。
# 這種做法幫助保護數據的完整性，確保重要的數據（如數據庫生成的唯一標識符）不會被外部用戶非法修改。