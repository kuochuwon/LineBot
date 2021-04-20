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


def parsing_church_schedule(input_file):
    # input_file = "季表格式調整.docx"
    # input_file = "季表格式調整 - 複製.docx"  # HINT for Debug

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

# TODO 需要重構


def _generate_message(msg_collection: dict) -> str:
    msg_content = ""
    if msg_collection:
        for name, v in msg_collection.items():
            task_msg = ""
            slot_msg = ""
            for tasks, time_slots in v.items():
                task_msg += tasks
                for slot in time_slots:
                    slot_msg += f"{SundayWorship.slot_time.get(slot)} "
            msg_content += (f"{name}的服事分配有潛在問題， {task_msg}的時間重疊了: {slot_msg}\n"
                            f"▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️\n")
    else:
        msg_content = "檢查完畢，服事內容未發現潛在問題。"
    return msg_content


def check_conflict(member_duties: dict):
    # member_duties['四月份04']['郭超立'].append("台語證道") # HINT 用於Debug
    msg_collection = dict()
    for date, value in member_duties.items():
        for name, tasks in value.items():
            time_slots = []
            for task in tasks:
                time_slots += SundayWorship.subject_slot.get(task)

            # temp.append("slot1")  # HINT 用於Debug
            seen = set()
            repeat = set()
            for x in time_slots:
                if x not in seen:
                    seen.add(x)
                else:
                    repeat.add(x)

            if repeat:
                summary = dict()
                time_slots = sorted(list(repeat))
                for elem in time_slots:
                    summary.update({elem: []})
                    for task in tasks:
                        if elem in SundayWorship.subject_slot.get(task):
                            summary[elem].append(task)

                # if name == '郭超立':  # HINT for debug
                #     summary['slot3'] = ['測試流程1', '測試流程2']
                #     summary['slot4'] = ['測試流程1', '測試流程2']

                task_timeslot = {}
                for slot, tasks in summary.items():
                    string = ""
                    for task in tasks:
                        string += f"{task} "  # HINT 每個task後面加上空白，用於顯示到Line畫面時可明顯區隔
                    task_timeslot.setdefault(string, []).append(slot)
                msg_collection.update({name: task_timeslot})
                # a = "temp"

    msg_content = _generate_message(msg_collection)

    return msg_content
