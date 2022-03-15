from django.http import HttpResponse
import stats as stats


def index(request):
    return HttpResponse(stats)
