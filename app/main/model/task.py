from sqlalchemy.sql import func

from app.main import db
from app.main.constant import Constant


class sdTask(db.Model):
    __tablename__ = "sd20_tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, comment="日期")
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    task = db.Column(db.String(50), comment="服事項目")
    comment = db.Column(db.Text, comment="Comment")

    def __repr__(self):
        return f"<sdTask date={self.date}/name={self.name}/task={self.task}>"
