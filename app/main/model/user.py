from sqlalchemy.sql import func
# from sqlalchemy.sql.functions import user

from app.main import db
from app.main.constant import Constant


class sdUser(db.Model):
    __tablename__ = "sd11_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_unique_id = db.Column(db.String(64), comment="使用者在Line上的unique ID")
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    display_name = db.Column(db.String(50), comment="暱稱")
    access_token = db.Column(db.String(64), comment="用於Line Notify的Token")
    comment = db.Column(db.Text, comment="Comment")
    status = db.Column(db.Integer, server_default="0", comment="0=停用，1=啟用")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    email = db.Column(db.String(100), comment="Email")
    telephone = db.Column(db.String(30), comment="Telephone number")
    line_id = db.Column(db.String(30), comment="LINE id")

    def __repr__(self):
        return f"<sdUser user_unique_id={self.user_unique_id}/name={self.name}/display_name={self.display_name}>"

    # @property
    # def password(self):
    #     raise AttributeError("password field cannot be read")

    # @password.setter
    # def password(self, new_password):
    #     self.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

    # def check_password(self, password):
    #     return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def search(user_id):
        return db.session.query(sdUser).filter(sdUser.user_unique_id == user_id).first()

    @staticmethod
    def getall(cust_id):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id).all()
        return users

    @staticmethod
    def getdetail(cust_id, user_list):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).all()
        return users

    @staticmethod
    def add(name, user_unique_id):
        obj = sdUser()
        obj.name = name
        obj.display_name = name
        obj.user_unique_id = user_unique_id
        return obj

    # delete_all_user_groups: delete all user groups record corresponding to the user from m2m table
    @staticmethod
    def delete_all_user_groups(cust_id, user_list):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).all()
        for user in users:
            ug_rels = user.user_groups
            ug_rels.clear()

    @staticmethod
    def delete(cust_id, user_list):
        sdUser.query.filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).delete(synchronize_session=False)

    @staticmethod
    def update(user_id, access_token):
        try:
            obj = db.session.query(sdUser).filter(sdUser.user_unique_id == user_id).first()
            obj.access_token = access_token
        except Exception as e:
            print(f"failed to update user: {e}")
        finally:
            return obj

    @staticmethod
    def get_admin(cust_id):
        admin = db.session.query(sdUser).filter(sdUser.cust_id.in_(cust_id), sdUser.name == Constant.ADMIN).all()
        return admin
