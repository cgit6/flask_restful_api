
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 # 哈希客戶端發送給我們的密碼
from db import db
from models import UserModel
from schemas import UserSchema
blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        # 在這裡，我們可以跳過這一點，稍後在插入資料庫時捕獲 IntegrityError。這可能是個更簡潔的解決方案。
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        # 獲取數據
        user = UserModel(
            username=user_data["username"], # username
            password=pbkdf2_sha256.hash(user_data["password"]) # 加密後的密碼
        )

        db.session.add(user) # 加入數據庫
        db.session.commit() # 更新數據庫
        return {"message": "User created successfully."}, 201 # 返回訊息


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
        return {"message": "User deleted."}, 200
