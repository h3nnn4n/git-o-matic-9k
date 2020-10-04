from django.http import HttpResponse


def index(_request):
    """
    Always returns `ok` with status code 200. Used as a heart beat. If this
    endpoint doesnt return `ok` then something is very wrong.
    """
    return HttpResponse('ok')
