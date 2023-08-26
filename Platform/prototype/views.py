from django.http import JsonResponse
from django.shortcuts import render

from prototype.models import Prototype


# Create your views here.


def savePrototype(request):
    if request.method == 'POST':
        id = request.POST.get('prototypeID')
        componentData = request.POST.get('componentData')
        canvasStyleData = request.POST.get('canvasStyleData')

        # try:
        prototype = Prototype(id=id, componentData=componentData,
                              canvasStyleData=canvasStyleData)
        prototype.save()
        return JsonResponse({'errno': 0})
        # except:
        #     return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def getPrototype(request):
    if request.method == 'GET':
        id = request.GET.get('prototypeID')
        try:
            prototype = Prototype.objects.get(id=id)
            return JsonResponse({'errno': 0, 'componentData': prototype.componentData,
                                 'canvasStyleData': prototype.canvasStyleData})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})















