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

    @staticmethod
    def add(name, date, task):
        obj = sdTask()  # TODO 看起來每個obj都是獨立的儲存物件，插入幾筆資料，就要產生幾筆物件
        obj.name = name
        obj.date = date
        obj.task = task
        return obj

    @staticmethod
    def delete_by_date(start_date, end_date):
        sdTask.query.filter(sdTask.date >= start_date,
                            sdTask.date <= end_date).delete(synchronize_session=False)

    @staticmethod
    def get_all():
        result = sdTask.query.filter().all()
        return result

    @staticmethod
    def get_by_time(start_date, end_date):
        result = sdTask.query.filter(sdTask.date >= start_date,
                                     sdTask.date <= end_date).all()
        return result
