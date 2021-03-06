from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from base.views import login_required
from django.utils.decorators import method_decorator
# Create your views here.
class IndexView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'home.html')

class TrackView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'hangzhou-track.html')

class HeatMapView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'heatmap.html')

class CharacteristicView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'characteristic.html')

class TrendView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'trend.html')