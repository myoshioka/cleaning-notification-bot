import os
import datetime
import json
import requests
import jaconv

SPREADSHEET_API_BASE_URL = os.getenv('SPREADSHEET_API_BASE_URL')
SPREADSHEET_API_KEY = os.getenv('SPREADSHEET_API_KEY')
AUTH_ID = os.getenv('AUTH_ID')
AUTH_PASS = os.getenv('AUTH_PASS')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
G_SPREADSHEET = os.getenv('G_SPREADSHEET')


def notification(event, context):
    """
    eventはテスト用
      {
        "today": "20190101"
      }
    """
    if (event is not None) and ('today' in event):
        today_str = event['today']  # 20190101
        today = datetime.datetime.strptime(today_str, '%Y%m%d').date()
    else:
        today = datetime.date.today()

    today_year = today.year
    today_month = today.month
    today_weekday = today.weekday()

    next_date = None
    next_str = None

    # 金曜日の場合、次は月曜日
    if today_weekday == 4:
        next_date = today + datetime.timedelta(days=3)
        next_str = '来週月曜日'
    else:
        next_date = today + datetime.timedelta(days=1)
        next_str = '明日'

    # シート名は月の数字の全角
    zen_today_month = jaconv.h2z(str(today_month), digit=True)
    url = SPREADSHEET_API_BASE_URL + SPREADSHEET_API_KEY + '?sheet=' + zen_today_month
    # API call
    response = requests.get(url=url, auth=(AUTH_ID, AUTH_PASS))
    cleaning_duty_list = response.json()
    if 'error' in cleaning_duty_list:
        return False

    today_target_person = None
    next_target_person = None
    for cleaning_duty in cleaning_duty_list:

        if not '日付' in cleaning_duty and not '担当者' in cleaning_duty:
            print('Key not found error')
            continue

        # 日付の表記は[１月１日]
        ja_date = jaconv.z2h(cleaning_duty['日付'], digit=True)
        ja_date = str(today_year) + '年' + ja_date
        try:
            cleaning_date = datetime.datetime.strptime(
                ja_date, '%Y年%m月%d日').date()
        except ValueError:
            continue

        if cleaning_date == today:
            today_target_person = cleaning_duty['担当者']

        if cleaning_date == next_date:
            next_target_person = cleaning_duty['担当者']

    today_message = '*今日の掃除当番* \n {today_target_person}さんです'.format(
        today_target_person=today_target_person)

    next_message = '*{next_str}の掃除当番* \n {next_target_person}さんです'.format(
        next_str=next_str,
        next_target_person=next_target_person)

    if not today_target_person:
        today_message = '今日の掃除はお休みです'

    if not next_target_person:
        next_message = '{next_str}の掃除はお休みです'.format(next_str=next_str)

    # slack通知
    title_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":sparkles: *<{link_url}|お掃除当番のお知らせです>*".format(link_url=G_SPREADSHEET)
        }
    }

    today_target_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": today_message
        }
    }

    next_target_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": next_message
        }
    }
    divider = {
        "type": "divider"
    }

    rtn = requests.post(WEB_HOOK_URL, headers={'Content-Type': 'application/json'},
                        data=json.dumps(
                            {
                                "blocks": [
                                    title_section,
                                    divider,
                                    today_target_section,
                                    divider,
                                    next_target_section
                                ]
                            }))
    print(rtn)
