from concurrent.futures.thread import ThreadPoolExecutor

from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from directions.models import MinPrice
from utils.constants import AVAILABLE_DIRECTIONS, DIRECTIONS
from utils.requests_lib import get_months_keys, get_and_set_min_price


class DirectionsView(View):
    def get(self, request):
        return JsonResponse(
            DIRECTIONS
        )


class DirectionDetailView(DetailView):
    def get(self, request, direction=None, *args, **kwargs):
        result = {}
        direction = str(direction).upper()

        if direction not in AVAILABLE_DIRECTIONS:
            return JsonResponse({'message': "Incorrect direction!"}, status=401)

        months, keys = get_months_keys(direction)

        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(get_and_set_min_price, keys)

        for m, k in zip(months, keys):
            result.update({str(m): MinPrice.get(key=k)})

        return JsonResponse(result)
