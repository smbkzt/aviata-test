import json
from datetime import timedelta

import celery
import requests
from django.utils import timezone

from directions.models import DirectionSearchIds, MinPrice
from utils.constants import (GET_SEARCH_PRICES_ID, GET_SEARCH_PRICES_RESULT, API_DATE_FORMAT,
                             QUERY, DAYS_COUNT, HEADER, HUMAN_READABLE_DATE_FORMAT, )


def get_months_keys(key: str) -> tuple:
    """
    Turns flight direction key into 30-days keys.
    :param key: Search key - {ALA-TSE}
    :return: Tuple of datetime format and search-keys.
    """
    moths_keys = []
    months = []
    for day in range(1, DAYS_COUNT):
        date = timezone.now() + timedelta(day)
        formatted_date = date.strftime(API_DATE_FORMAT)

        months.append(date.strftime(HUMAN_READABLE_DATE_FORMAT))
        moths_keys.append(QUERY.format(key + formatted_date))
    return months, moths_keys


def make_search(query: str):
    search_id = get_search_id_key(query)
    price = get_and_set_cheapest_price(query, search_id)
    return price


def get_search_id_key(query: str) -> str:
    """
    Gets search id from Aviata API using specific queryset.
    :param query: Queryset in `DirectionDate1000E` format.
    :return: Returns search id.
    """

    direction_id: str = DirectionSearchIds.get(key=query)
    if direction_id:
        return direction_id

    data = json.dumps({'query': query})
    response = requests.post(headers=HEADER, data=data, url=GET_SEARCH_PRICES_ID)
    if response.status_code == 201:
        search_id = response.json()['id']
        DirectionSearchIds.set(key=query, value=search_id)
        return search_id
    return ""


@celery.task(default_retry_delay=2 * 10, max_retries=2)
def get_and_set_cheapest_price(query: str, search_id: str, update=False):
    """
    Searches for the cheapest price using search id.
    :param query: Queryset in `DirectionDate1000E` format.
    :param search_id: Special id for Aviata API.
    :param update: Update the cache data or not.
    :return: The minimum price of the direction.
    """
    price = MinPrice.get(key=query)

    if price and not update:
        return price

    response = requests.get(url=GET_SEARCH_PRICES_RESULT.format(search_id), headers=HEADER)
    if response.status_code == 200:
        response_json = response.json()
        if response_json['status'] != 'done':
            get_and_set_cheapest_price.apply_async(args=(query, search_id, True), countdown=20)
        prices = [int(i['price']['amount']) for i in response_json['items']]
        if prices:
            price = min(prices)
            MinPrice.set(key=query, value=price)
            return price
        elif not prices and response_json['status'] == 'done':
            MinPrice.set(key=query, value='Нет доступных рейсов')
    return 0
