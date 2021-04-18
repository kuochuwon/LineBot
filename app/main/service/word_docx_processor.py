from app.main.service import ret
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
    # input_file = "季表格式調整.docx"
    input_file = "季表格式調整 - 複製.docx"  # HINT for Debug

    # HINT link: https://stackoverflow.com/questions/27861732/parsing-of-table-from-docx-file/27862205
    word = Document(Path.cwd() / "downloads/" / input_file)
    data = parse_docx(word)
    chi_duties = dict()
    tai_duties = dict()
    sum_names = set()
    chi_index = {k: regex(v) for k, v in enumerate(data[1])}  # 原始值含有空白
    tai_index = {k: regex(v) for k, v in enumerate(data[21])}  # 原始值含有空白
    chi_subject = SundayWorship.chinese_subject
    tai_subject = SundayWorship.taiwan_subject

    for row in data[2:14]:  # chinese
        people_duties = dict()
        date = regex(row[0]) + regex(row[1])
        for index, name in enumerate(row):
            if index in (2, 3, 4, 5, 6, 11):
                name = regex(name)
                if name is not None and (name != ''):  # 有None就不要收
                    sum_names.add(name)
                    people_duties.setdefault(name, []).append(chi_subject.get(chi_index.get(index)))
        chi_duties.update({date: people_duties})
    for row in data[22:34]:
        people_duties = dict()
        date = regex(row[0]) + regex(row[2])
        for index, name in enumerate(row):
            if index in (3, 4, 5, 7):
                name = regex(name)
                sum_names.add(name)
                people_duties.setdefault(name, []).append(tai_subject.get(tai_index.get(index)))
            elif index == 8:
                money_getters = name.split(" ")
                people_duties.setdefault(regex(money_getters[0]), []).append(tai_subject.get(tai_index.get(index)))
                people_duties.setdefault(regex(money_getters[1]), []).append(tai_subject.get(tai_index.get(index)))
                sum_names.add(regex(money_getters[0]))
                sum_names.add(regex(money_getters[1]))
        tai_duties.update({date: people_duties})

    chi_date = list(chi_duties.keys())
    tai_date = list(tai_duties.keys())
    sum_date = set(chi_date + tai_date)

    # HINT 將taiduties整併到chiduties，並return出去
    for each_date in sum_date:
        if chi_duties.get(each_date) is None:
            chi_duties.update({each_date: dict()})
        for each_name in sum_names:
            # print(each_name)
            lis1 = chi_duties[each_date].get(each_name)
            lis2 = tai_duties[each_date].get(each_name)
            if lis1 is None and lis2 is not None:
                chi_duties[each_date][each_name] = tai_duties[each_date][each_name]
            elif lis1 is None and lis2 is None:
                continue
            elif lis1 is not None and lis2 is None:
                continue
            else:
                chi_duties[each_date][each_name] = lis1 + lis2

    return chi_duties


def check_conflict(member_duties):
    # member_duties['四月份04']['郭超立'].append("台語證道") # HINT 用於Debug
    for date, value in member_duties.items():
        for name, tasks in value.items():
            temp = []
            for task in tasks:
                temp += SundayWorship.subject_slot.get(task)

            # temp.append("slot1")  # HINT 用於Debug
            seen = set()
            repeat = set()
            for x in temp:
                if x not in seen:
                    seen.add(x)
                else:
                    repeat.add(x)
            temp2 = []
            for elem in repeat:
                for task in tasks:
                    if elem in SundayWorship.subject_slot.get(task):
                        temp2.append((task, SundayWorship.slot_time.get(elem)))
            for elem2 in temp2:
                print(f"{name} 兄弟/姊妹 的服事有衝突， 衝突的項目為 {elem2[0]} 時間點為: {elem2[1]} ")

            a = "temp"
