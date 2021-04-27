from app.main import db
from sqlalchemy.sql.expression import func


class Bible(db.Model):
    __tablename__ = "sd21_Bible"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locate = db.Column(db.String(50), comment="經文位置")
    sentence = db.Column(db.Text, nullable=False, comment="經文內容")
    comment = db.Column(db.Text, comment="Comment")
    # 資料來自現代中文譯本2019版

    def __repr__(self):
        return f"<sd21_Bible locate={self.locate}/sentence={self.sentence}>"

    @staticmethod
    def get_all():
        result = Bible.query.all()
        return result

    @staticmethod
    def get_by_id(id):
        result = Bible.query.filter(Bible.id == id).first()
        return result

    @staticmethod
    def get_by_random():
        result = Bible.query.order_by(func.random()).first()
        return result
