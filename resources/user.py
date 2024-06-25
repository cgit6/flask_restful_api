
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 # 哈希客戶端發送給我們的密碼
# create_access_token:生成jwt token
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema
blp = Blueprint("Users", "users", description="Operations on users")

# 註冊
# 期望看到的格式
# {
# "username":"name",
# "password":"1234"
# }
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # 鑒察 username 是否有重複
        # 在這裡，我們可以跳過這一點，稍後在插入資料庫時捕獲 IntegrityError。這可能是個更簡潔的解決方案。
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="使用該用戶名的用戶已存在")

        # 獲取數據
        user = UserModel(
            username=user_data["username"], # username
            password=pbkdf2_sha256.hash(user_data["password"]) # 加密後的密碼
        )

        db.session.add(user) # 加入數據庫
        db.session.commit() # 更新數據庫
        return {"message": "用戶創建成功"}, 201 # 返回訊息

# 登入
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        # server 檢查收到的請求是否與資料庫一致
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # 建立 jwt token
            access_token = create_access_token(identity=user.id, fresh=True)
            # refresh: 用途是為了授權安全級別更高的操作
            refresh_token = create_refresh_token(identity=user.id)
            # 返回 token 到 client
            return {"access_token":access_token, "refresh_token":refresh_token}
        
        abort(401, message="無效驗證")

# 刷新 token
# 每次access_token過期時, 用戶端都可以使用/refresh端點產生新的access_token｡
# 如果您希望設定refresh token 的使用次數限制, 或希望refresh token到期後不能再次使用,
# 則可以設定刷新令牌的到期時間, 也可以將刷新令牌加入到BLOCKLIST中｡
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) 
        return {"access_token":new_token}


# 登出
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required() # 檢查
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) # 加入封鎖名單中
        return {"message": "成功退出"}



# 這個在實際部屬時要刪除
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "用戶已刪除"}, 200
