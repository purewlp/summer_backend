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
            prototype = Prototype.objects.get(id=id)
            prototype.componentData = componentData
            prototype.canvasStyleData = canvasStyleData
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


def newId(projectID):
    id = projectID + '-' + str(random.randint(0, 100))
    while(True):
        try:
            Prototype.objects.get(id=id)
        except:
            break
        id = projectID + '-' + str(random.randint(0, 100))
    return id

def newPrototype(projectID, modeltype, title, canvasStyleData):
    # id = projectID + '-' + str(random.randint(0, 100))
    # while(True):
    #     try:
    #         Prototype.objects.get(id=id)
    #     except:
    #         break
    #     id = projectID + '-' + str(random.randint(0, 100))

    models = []
    rid = newId(projectID)
    project = Project.objects.get(id=projectID)

    if modeltype == '2':
        # models.append(Prototype.objects.get(id='10004-11'))
        main = Prototype.objects.get(id='10004-11')
        models.append(Prototype.objects.get(id='10004-22'))
        models.append(Prototype.objects.get(id='10004-43'))
        models.append(Prototype.objects.get(id='10004-95'))

    elif modeltype == '3':
        # models.append(Prototype.objects.get(id='10005-11'))
        main = Prototype.objects.get(id='10005-11')
        models.append(Prototype.objects.get(id='10005-22'))
        models.append(Prototype.objects.get(id='10005-43'))
        models.append(Prototype.objects.get(id='10005-95'))

    else:
        prototype = Prototype(id=rid, title=title, canvasStyleData=canvasStyleData)
        prototype.save()
        ProjectPrototype(project=project, prototype=prototype).save()
        return rid

    for model in models:
        # print(model.title)
        prototype = Prototype(id=newId(projectID), title=title+'-'+model.title, canvasStyleData=model.canvasStyleData, componentData=model.componentData)
        prototype.save()
        ProjectPrototype(project=project, prototype=prototype).save()

    prototype = Prototype(id=rid, title=title+'-'+main.title, canvasStyleData=main.canvasStyleData, componentData=main.componentData)
    prototype.save()
    ProjectPrototype(project=project, prototype=prototype).save()
    return rid


def setPrototype(request):
    if request.method == 'POST':
        projectID = request.POST.get('projectID')
        title = request.POST.get('title')
        canvasStyleData = request.POST.get('canvasStyleData')
        model = request.POST.get('model')   #空白 1  商城 2  学术 3
        # id = projectID + '-' + str(random.randint(0, 100))
        # while(True):
        #     try:
        #         Prototype.objects.get(id=id)
        #     except:
        #         break
        #     id = projectID + '-' + str(random.randint(0, 100))

        # try:
        # componentData = ''
        # if model == '2':
        #     componentData = Prototype.objects.get(id='10004-11').componentData
        #     canvasStyleData = Prototype.objects.get(id='10004-11').canvasStyleData
        # if model == '3':
        #     componentData = Prototype.objects.get(id='10005-11').componentData
        #     canvasStyleData = Prototype.objects.get(id='10005-11').canvasStyleData
        id = newPrototype(projectID, model, title, canvasStyleData)


        # prototype = Prototype(id=id, title=title, canvasStyleData=canvasStyleData)
        # prototype.save()
        return JsonResponse({'errno': 0, 'prototypeID': id})
        # except:
        #     return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def deletePrototype(request):
    if request.method == 'POST':
        prototypeID = request.POST.get('prototypeID')
        try:
            prototype = Prototype.objects.get(id=prototypeID)
            prototype.delete()
            return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})


def getDesign(request):
    if request.method == 'GET':
        projectID = request.GET.get('projectID')
        try:
            project = Project(id=projectID)
            project_prototypes = ProjectPrototype.objects.filter(project=project)
            prototypes = []
            for project_prototype in project_prototypes:
                prototype = project_prototype.prototype
                prototypes.append({
                    'prototypeID': prototype.id,
                    'title': prototype.title,
                    'isEditing': False,
                    'newName': '',
                    'hover': False
                })
            return JsonResponse({'errno': 0, 'prototypes': prototypes})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})

def rename(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        id = request.POST.get('prototypeID')
        try:
            prototype = Prototype.objects.get(id=id)
            prototype.title = title
            prototype.save()
            return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})












