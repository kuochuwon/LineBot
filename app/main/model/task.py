from sqlalchemy.sql import func

from app.main import db


class sdTask(db.Model):
    __tablename__ = "sd20_tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, comment="日期")
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    task = db.Column(db.String(50), comment="服事項目")
    comment = db.Column(db.Text, comment="Comment")

    def __repr__(self):
        return f"<sdTask date={self.date}/name={self.name}/task={self.task}>"

    def add(name, date, task):
        obj = sdTask()  # TODO 如果for loop很多次，會不會浪費效能生成物件?
        obj.name = name
        obj.date = date
        obj.task = task
        return obj
