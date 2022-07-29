from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def recipes_api_list(request):
    return Response('ok')
