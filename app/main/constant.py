
class LineConstant:  # 應重構，使得每個變數去吃環境變數檔，靈活應對不同的line機器人
    CHANNEL_ACCESS_TOKEN = "qipp53w9dsKIjaDG3D5eYswChigJUmYdgD6ilha3BCHjF4rJmG8dVjj3kMqpBy4TvTnYODobZelFc5bsSz9ycEx09y/XU3aZO42Bp2o0+9f9TRJBFMeUih6Oi2YB77ET4+u5z/miOF5FRihh5ubRTgdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET_TOKEN = "6fd6a21c86d311aaf115d9588cc5fc46"

    # CHANNEL_NOTIFY_TOKEN = "r2LutziDSljYNL2O0rq3kiBNn90lQCiQC7CATPZRP5n" # Roy測試用機器人 對 Roy專屬的token
    # CHANNEL_NOTIFY_TOKEN = "z0bvCgU80dpOwxCRt6EGlKVnuChzDEnE3rQeTLEcydZ"  # Roy_Notify_測試機器人 對 Roy專屬的token
    CHANNEL_NOTIFY_TOKEN = "6INohLojGIHD6GOo44Clpk6zHNzjS3s8ABWY2VgeKZG"  # Roy_Notify_測試機器人 對 lihket專屬的token，可以有多個
    OFFICIAL_PUSH_API = "https://api.line.me/v2/bot/message/push"
    OFFICIAL_NOTIFY_API = "https://notify-api.line.me/api/notify"
    OFFICIAL_OAUTH_API = "https://notify-bot.line.me/oauth/token"
    OFFICIAL_REPLY_API = "https://api.line.me/v2/bot/message/reply"
    OFFICIAL_CONTENT_API = "https://api-data.line.me/v2/bot/message/<file_id>/content"

    user_id = dict(
        roykuo="U9afa5683614c2f30296a92eb07984d57",
        lihket="Ud2480636ce54bc7b98dfa1a51071c961"
    )
    push_header = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'}

    notify_header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization': f'Bearer {CHANNEL_NOTIFY_TOKEN}'}
    NOTIFY = dict(
        CLIENT_ID="UulwSUMmf5M9zY1HSTR8xy",
        SECRET="MDuIohlUsEsPRKP2VXq0weJAW3cYwbb24gfeixTDmVC",
        remote_URI="https://linebot-kuochuwon.herokuapp.com/api/v1/linebot/callback",
        local_URI="http://127.0.0.1:5000/api/v1/linebot/callback"
    )


class SundayWorship:
    # HINT key is time, value is subject
    slot_time = {
        "slot1": "0900~0930",  # value到時候可做為說明文字來取用
        "slot2": "0930~1000",
        "slot3": "1000~1030",
        "slot4": "1030~1100",
        "slot5": "1100~1130"
    }
    subject_slot = {
        "台語司會": ["slot1", "slot2", "slot3", "slot4"],
        "台語司琴": ["slot1", "slot2", "slot3", "slot4"],
        "台語PPT": ["slot1", "slot2", "slot3", "slot4"],
        "台語敬拜讚美": ["slot1", "slot2"],
        "主日學詩歌": ["slot1", "slot2"],
        "台語讀經": ["slot1", "slot2"],
        "台語證道": ["slot2", "slot3", "slot4"],
        "主日學分班": ["slot3", "slot4"],
        "青少年團契": ["slot3", "slot4"],
        "台語司獻": ["slot3", "slot4"],
        "華語司會": ["slot5"],
        "華語司琴": ["slot5"],
        "華語敬拜讚美": ["slot5"],
        "華語讀經": ["slot5"],
        "華語證道": ["slot5"]
    }

    chinese_subject = {
        "證道": "華語證道",
        "敬拜讚美": "華語敬拜讚美",
        "讀經": "華語讀經",
        "詩歌": "主日學詩歌",
        "分班": "主日學分班",
        "主理": "青少年團契",
        "司會": "華語司會",
        "司琴": "華語司琴",
        "PPT": "台語PPT"
    }

    taiwan_subject = {
        "證道": "台語證道",
        "敬拜讚美": "台語敬拜讚美",
        "讀經": "台語讀經",
        "司會": "台語司會",
        "司琴": "台語司琴",
        "司獻": "台語司獻",
        "PPT": "台語PPT"
    }


class Constant:  # 先不要刪除，因為目前@api_exception_handler有依賴這裡的參數
    CODE_TYPE_ISSUE_STATUS = 0
    CODE_TYPE_ISSUE_ERRORCODE = 1
    CODE_TYPE_REPORT_FROM = 2
    CODE_TYPE_DEVICE_STATUS = 3
    CODE_TYPE_DEVICE_COMPONENT = 4
    CODE_TYPE_EVENT_CATEGORY = 5
    CODE_TYPE_ISSUE_PRIORITY = 6

    COMMAND_DIMMING = 0
    COMMAND_POWER = 1
    COMMAND_DEVICE_TYPE_DEVICE = 0
    COMMAND_DEVICE_TYPE_GROUP = 1
    COMMAND_STATUS_RECEIVED = 0
    COMMAND_STATUS_QUEUE = 1

    CODE_EVENT_COMPONENT = {0: "CONTROLLER",
                            1: "LED"}

    CODE_EVENT_CATEGORY = {0: "溫度",
                           1: "濕度",
                           2: "電壓",
                           3: "亮度",
                           4: "電流",
                           5: "功率因數",
                           6: "功率",
                           7: "流明",
                           8: "資訊(開關機、排程、dimming)",
                           9: "dimming",
                           10: "開關機"}

    CODE_STATUS = {"NORMAL": 0,
                   "DEBUG": 1,
                   "INFO": 2,
                   "WARNING": 4,
                   "ERROR": 8,
                   "CRITICAL": 16}
    # User Role code
    SYSTEM_ADMIN = 1
    CUSTOMER_ADMIN = 2
    VENDOR_ADMIN = 3
    VENDOR_USER = 4

    ADMIN = "admin"
    REPORT_FROM_PEOPLE = "people"
    ISSUE_CHANGE_DESC = "status changed"
    DEFAULT_ISSUE_STATUS = "new"

    ACCESS_PRIVILEGES = {
        SYSTEM_ADMIN: [
            "new", "assigned", "in-progress", "resolved", "closed"
        ],
        CUSTOMER_ADMIN: [
            "new", "assigned", "in-progress", "resolved", "closed"
        ],
        VENDOR_ADMIN: [
            "assigned", "in-progress", "resolved", "closed"
        ],
        VENDOR_USER: [
            "in-progress"
        ]
    }

    PRIORITY_DUE_DAY = {
        "normal": 7,
        "high": 5,
        "urgent": 3
    }

    # for batch inset database in command view
    BATCH_COUNT_EXECUTE = 100

    # Redis related constants
    REDIS_EXPIRE_TIMES = 604800  # 60*60*24*7 == 604800 secs == 7 days


__code_table_name = {
    Constant.CODE_TYPE_ISSUE_STATUS: "issue_status",
    Constant.CODE_TYPE_ISSUE_ERRORCODE: "issue_errorcode",
    Constant.CODE_TYPE_REPORT_FROM: "report_from",
    Constant.CODE_TYPE_DEVICE_STATUS: "device_status",
    Constant.CODE_TYPE_DEVICE_COMPONENT: "device_component",
    Constant.CODE_TYPE_EVENT_CATEGORY: "event_category",
    Constant.CODE_TYPE_ISSUE_PRIORITY: "issue_priority"
}


def map_component(code):
    return Constant.CODE_EVENT_COMPONENT[code]


def map_category(code):
    return Constant.CODE_EVENT_CATEGORY[code]


def map_status(code_name):
    return Constant.CODE_STATUS[code_name]


def get_codes_name(code_type):
    return __code_table_name[code_type]
