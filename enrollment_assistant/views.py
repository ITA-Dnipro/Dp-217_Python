from django.shortcuts import render


def index_view(request):
    return render(request, "index.html")


def handler404(request, exception, template_name="404.html"):
    return render(request, template_name, status=404)
