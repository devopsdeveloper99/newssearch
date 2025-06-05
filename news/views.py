import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from news.newsv3 import search_news, save_to_csv


def news(request):
    template = loader.get_template('search.html')
    return HttpResponse(template.render())


def search_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            query = data.get("query")
            result = search_news(query)
            save_to_csv(result)
            return JsonResponse({"message": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def result_view(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            results = data.get("message", [])
        except json.JSONDecodeError:
            results = []
        return render(request, 'result.html', {'articles': results})
    return render(request, 'result.html', {'results': []})
