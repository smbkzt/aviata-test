from concurrent.futures.thread import ThreadPoolExecutor

from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from directions.models import MinPrice
from utils.constants import AVAILABLE_DIRECTIONS, DIRECTIONS
from utils.requests_lib import get_months_keys, make_search


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
            return JsonResponse({'message': "Direction not found."}, status=404)

        months, keys = get_months_keys(direction)

        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(make_search, keys)

        for m, k in zip(months, keys):
            result.update({
                str(m): MinPrice.get(key=k) if MinPrice.get(key=k) else "Поиск..."
            })

        return JsonResponse(result)
