from django.http import JsonResponse
from django.shortcuts import render

from prototype.models import Prototype


# Create your views here.


def savePrototype(request):
    if request.method == 'POST':
        id = request.POST.get('prototypeID')
        componentData = request.POST.get('componentData')
        canvasStyleData = request.POST.get('canvasStyleData')
        all = request.POST.get('all')

        try:
            prototype = Prototype(id=id, componentData=componentData,
                                  canvasStyleData=canvasStyleData, all=all)
            prototype.save()
            return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def getPrototype(request):
    if request.method == 'GET':
        id = request.GET.get('prototypeID')
        try:
            prototype = Prototype.objects.get(id=id)
            info = {
                'componentData': prototype.componentData,
                'canvasStyleData': prototype.canvasStyleData,
                'all': prototype.all
            }
            return JsonResponse({'errno': 0, 'info': info})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})















