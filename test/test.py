import logging
from test.test_data import test_data

from src.calculation import calc

logging.basicConfig(level=logging.INFO)


async def test(collection):
    for input_data, expected_result in test_data:
        actual_result = await calc(collection, input_data)
        try:
            assert actual_result == expected_result
            logging.info('=== SUCCESS !!! ===')
        except AssertionError:
            logging.info('============START============')
            logging.info(expected_result)
            logging.info('--------------------------')
            logging.info(actual_result)
            logging.info('============END============')
            assert 0
