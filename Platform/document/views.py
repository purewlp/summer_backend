from project.models import Project
from document.models import Document
from Platform import settings
from django.http import JsonResponse

# Create your views here.

def create(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        project=Project.objects.get(id=projectID)
        name=request.POST.get('name')
        Document.objects.create(project=project)
        return JsonResponse({'errno':0})
    else:
        return JsonResponse({'errno':1001})
