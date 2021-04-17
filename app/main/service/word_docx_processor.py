import re
from pathlib import Path

from app.main.constant import SundayWorship
from docx import Document


def regex(s):
    return re.sub(r"[ \n\t]", "", s)


def parse_docx(word):
    data = []
    # keys = None
    # table = word.tables[0]
    for table in word.tables:
        for i, row in enumerate(table.rows[1:]):
            text = (cell.text for cell in row.cells)
            row_data = row_data = tuple(text)
            data.append(row_data)
    return data


def parsing_church_schedule(input_file=None):
    input_file = "季表格式調整.docx"

    # HINT link: https://stackoverflow.com/questions/27861732/parsing-of-table-from-docx-file/27862205
    word = Document(Path.cwd() / "downloads/" / input_file)
    data = parse_docx(word)
    month_duties1 = dict()
    month_duties2 = dict()
    chi_names = set()
    tai_names = set()
    # chi_index = {k: v.replace(" ", "") for k, v in enumerate(data[1])}  # 原始值含有空白
    chi_index = {k: regex(v) for k, v in enumerate(data[1])}  # 原始值含有空白
    tai_index = {k: regex(v) for k, v in enumerate(data[21])}  # 原始值含有空白
    subject1 = SundayWorship.chinese_subject
    subject2 = SundayWorship.taiwan_subject

    for row in data[2:14]:  # chinese
        people_duties = dict()
        date = regex(row[0]) + regex(row[1])
        for index, name in enumerate(row):
            if index in (2, 3, 4, 5, 6, 11):
                name = regex(name)
                chi_names.add(name)
                people_duties.setdefault(name, []).append(subject1.get(chi_index.get(index)))
        month_duties1.update({date: people_duties})
    try:
        for row in data[22:34]:
            people_duties = dict()
            date = regex(row[0]) + regex(row[2])
            for index, name in enumerate(row):
                if index in (3, 4, 5, 7):
                    name = regex(name)
                    tai_names.add(name)
                    people_duties.setdefault(name, []).append(subject2.get(tai_index.get(index)))
                elif index == 8:
                    money_getters = name.split(" ")
                    people_duties.setdefault(regex(money_getters[0]), []).append(subject2.get(tai_index.get(index)))
                    people_duties.setdefault(regex(money_getters[1]), []).append(subject2.get(tai_index.get(index)))
                    tai_names.add(regex(money_getters[0]))
                    tai_names.add(regex(money_getters[1]))
            month_duties2.update({date: people_duties})

        chi_date = list(month_duties1.keys())
        tai_date = list(month_duties2.keys())
    except Exception as e:
        print(f"error, {e}")
        raise

    # # TODO 應修改以增加效率
    # # 若有人在台語禮拜及華語禮拜都有服事，進行更新
    # for date, value in month_duties1.items():
    #     for name, duties_list in value.items():
    #         if month_duties2.get(date):
    #             if month_duties2[date].get(name):
    #                 duties_list += month_duties2[date].get(name)

    # # TODO 應修改以增加效率
    # # 將只有台語禮拜的服事人選，加到month_duties1，以確保month_duties1有國台語的服事'聯集'
    # for date, value in month_duties2.items():
    #     for name, duties_list in value.items():
    #         if month_duties1.get(date):
    #             if month_duties1[date].get(name) is None:
    #                 month_duties1[date] = {**value, **month_duties1[date]}
    #         else:
    #             month_duties1.update(value)

    a = "temp"
