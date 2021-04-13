
class LineConstant:
    CHANNEL_ACCESS_TOKEN = "qipp53w9dsKIjaDG3D5eYswChigJUmYdgD6ilha3BCHjF4rJmG8dVjj3kMqpBy4TvTnYODobZelFc5bsSz9ycEx09y/XU3aZO42Bp2o0+9f9TRJBFMeUih6Oi2YB77ET4+u5z/miOF5FRihh5ubRTgdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET_TOKEN = "6fd6a21c86d311aaf115d9588cc5fc46"

    # CHANNEL_NOTIFY_TOKEN = "r2LutziDSljYNL2O0rq3kiBNn90lQCiQC7CATPZRP5n" # Roy測試用機器人 對 Roy專屬的token
    CHANNEL_NOTIFY_TOKEN = "z0bvCgU80dpOwxCRt6EGlKVnuChzDEnE3rQeTLEcydZ"  # Roy_Notify_測試機器人 對 Roy專屬的token

    OFFICIAL_PUSH_API = "https://api.line.me/v2/bot/message/push"
    OFFICIAL_NOTIFY_API = "https://notify-api.line.me/api/notify"

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
        URI="https://linebot-kuochuwon.herokuapp.com/api/v1/linebot/callback"
    )


class Constant:
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
