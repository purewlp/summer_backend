import random

from django.http import JsonResponse
from django.shortcuts import render

from project.models import Project
from prototype.models import Prototype, ProjectPrototype


# Create your views here.


def savePrototype(request):
    if request.method == 'POST':
        id = request.POST.get('prototypeID')
        componentData = request.POST.get('componentData')
        canvasStyleData = request.POST.get('canvasStyleData')

        try:
            prototype = Prototype(id=id, componentData=componentData,
                                  canvasStyleData=canvasStyleData)
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
            return JsonResponse({'errno': 0, 'componentData': prototype.componentData,
                                 'canvasStyleData': prototype.canvasStyleData})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def setPrototype(request):
    if request.method == 'POST':
        projectID = request.POST.get('projectID')
        title = request.POST.get('title')
        canvasStyleData = request.POST.get('canvasStyleData')
        id = projectID + '-' + str(random.randint(0, 100))
        while(True):
            try:
                Prototype.objects.get(id=id)
            except:
                break
            id = projectID + '-' + str(random.randint(0, 100))

        try:
            prototype = Prototype(id=id, title=title, canvasStyleData=canvasStyleData)
            prototype.save()
            ProjectPrototype(project=Project.objects.get(id=projectID), prototype=prototype).save()
            return JsonResponse({'errno': 0, 'prototypeID': id})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def deletePrototype(request):
    if request.method == 'POST':
        prototypeID = request.POST.get('prototypeID')
        try:
            prototype = Prototype.objects.get(id=prototypeID)
            prototype.delete()
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def getDesign(request):
    if request.method == 'POST':
        projectID = request.POST.get('projectID')
        try:
            project = Project(id=projectID)
            prototypes = ProjectPrototype.objects.filter(project=project)
        except:
            return JsonResponse({'errno': 1001})














