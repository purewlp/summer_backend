from project.models import Project
from team.models import Team,Membership
from document.models import Document,DocumentVersion
from user.models import User
from Platform import settings
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

def create(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        id=request.POST.get('id') 
        name=request.POST.get('name')
        project=Project.objects.get(id=projectID)
        user=User.objects.get(id=id)
        document=Document(project=project,creator=user,name=name)
        document.save()
        DocumentVersion.objects.create(document=document,name=document.name,
        content=document.content)
        return JsonResponse({'errno':0,'msg':"新建文档成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def save(request):
    if request.method=='POST':
        documentID=request.POST.get('document_id')
        name=request.POST.get('name')
        content=request.POST.get('content')
        document=Document.objects.get(id=documentID)
        document.name=name
        document.content=content
        document.edited_time=timezone.now()
        document.save()
        DocumentVersion.objects.create(document=document,name=document.name,
        content=document.content)
        return JsonResponse({'errno':0,'msg':"保存成功"})
    else :
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def delete(request):
    if request.method == 'POST':
        documentID=request.POST.get('document_id')
        document=Document.objects.get(id=documentID)
        document.delete()
        return JsonResponse({'errno':0,'msg':"已成功删除文档"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def list(request):
    if request.method == 'GET':
        projectID=request.GET.get('project_id')
        project=Project.objects.get(id=projectID)
        documents=Document.objects.filter(project_id=projectID)
        document_list=[]
        for document in documents:
            document_data={
                'document_id':document.id,
                'name':document.name,
                'created_time':document.created_time,
                'creator_id':document.creator_id,
                'edited_time':document.edited_time,
            }
            document_list.append(document_data)
        return JsonResponse({'errno':0,'document_list':document_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

# def detail(request):
#     if request.method == 'GET':
#         documentID=request.GET.get('document_id')
#         document=Document.objects.get(id=documentID)
#         document_info={
#             'name':document.name,
#             'content':document.content,
#         }
#         projectID=document.project_id
#         teamID=Project.objects.get(projectID).team_id
#         member_list=[]
#         members=Membership.objects.filter(team_id=teamID)
