import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from news.newsv3 import search_news, save_to_csv


@ensure_csrf_cookie
def news(request):
    return render(request, 'search.html')


@ensure_csrf_cookie
def search_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            query = data.get("query")

            result = search_news(query)
            # print(f"result done")
            save_to_csv(result)
            # print(f"save_to_csv done")
            return JsonResponse({"message": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@ensure_csrf_cookie
def result_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            results = data.get("message", [])
        except json.JSONDecodeError:
            results = []
        return render(request, 'result.html', {'articles': results})
    return render(request, 'result.html', {'results': []})
