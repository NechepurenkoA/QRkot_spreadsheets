from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

SPREADSHEET_BODY = {
        'properties': {'title': 'Отчет на {}',
                       'locale': 'ru_RU'},
        'sheets': [
            {
                'properties':
                {
                     'sheetType': 'GRID',
                     'sheetId': 0,
                     'title': 'Лист1',
                     'gridProperties':
                     {
                         'rowCount': 100,
                         'columnCount': 11
                     }
                }
            }
        ]
    }


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body['properties']['title'] = (
        spreadsheet_body['properties']['title'].format(now_date_time)
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for proj in projects:
        new_row = [
            str(proj['name']),
            (proj['closed_date'] - proj['created_date']).strftime('%d, %H:%M:%S.%f'),
            str(proj['description'])
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:С30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
