from datetime import datetime as dt
from datetime import timedelta
from typing import Any, TypeAlias

from motor.core import AgnosticCollection

Response: TypeAlias = dict[str, Any]

FORMATS = {
    'month': '%Y-%m',
    'day': '%Y-%m-%d',
    'hour': '%Y-%m-%dT%H',
    'full': '%Y-%m-%dT%H:%M:%S',
}


async def calc(collection: AgnosticCollection, data: dict[str, str]) -> Response:
    dt_from = dt.fromisoformat(data['dt_from'])
    dt_upto = dt.fromisoformat(data['dt_upto'])
    stage_match = {'$match': {'dt': {'$gte': dt_from, '$lte': dt_upto}}},
    stage_densify_dates = {'$densify': {
        'field': 'dt',
        'range': {
            'step': 1,
            'unit': 'minute',
            'bounds': [dt_from, dt_upto + timedelta(minutes=1)],
        },
    }}
    stage_group_and_sum = {'$group': {
        '_id': {'$dateToString': {'date': '$dt', 'format': FORMATS[data['group_type']]}},
        'date': {'$min': '$dt'},
        'total': {'$sum': '$value'},
    }}
    pipeline = [
        stage_match,
        stage_densify_dates,
        stage_match,
        stage_group_and_sum,
        {'$sort': {'date': 1}},
        {'$project': {'total': 1, 'date': {'$dateToString': {'date': '$date', 'format': FORMATS['full']}}}},
    ]
    response: Response = {'dataset': [], 'labels': []}
    async for item in collection.aggregate(pipeline):
        response['dataset'].append(item['total'])
        response['labels'].append(item['date'])

    return response
