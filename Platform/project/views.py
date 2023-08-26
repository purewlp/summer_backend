from user.models import User
from team.models import Team
from project.models import Project,ProjectRecycleBin
from Platform import settings
from django.http import JsonResponse

# Create your views here.
def createProject(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        name=request.POST.get('project_name')
        user=User.objects.get(id=id)
        team=Team.objects.get(id=teamID)
        project=Project.objects.filter(name=name)
        if project:
            return JsonResponse({'errno':1002,'msg':"项目名称重复，请重新命名"})
        new_project=Project(creator=user,team=team,name=name)
        new_project.save()
        return JsonResponse({'errno':0,'msg':"创建项目成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def deleteProject(request):
    if request.method=='POST':
        id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        projectID=request.POST.get('project_id')
        deleter=User.objects.get(id=id)
        team=Team.objects.get(id=teamID)
        project=Project.objects.get(id=projectID)
        id=project.creator_id
        creator=User.objects.get(id=id)
        ProjectRecycleBin.objects.create(name=project.name,deleter_id=deleter.id,
        creator_id=creator.id,team=team,project_id=projectID)
        project.delete()
        return JsonResponse({'errno':0,'msg':"成功删除项目"})
    else :
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def recoverProject(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        project=ProjectRecycleBin.objects.get(project_id=projectID)
        id=project.creator_id
        name=project.name
        teamID=project.team_id
        creator=User.objects.get(id=id)
        team=Team.objects.get(id=teamID)
        Project.objects.create(creator=creator,team=team,name=name,id=projectID)
        project.delete()
        return JsonResponse({'errno':0,'msg':"恢复成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def renameProject(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        name=request.POST.get('name')
        project=Project.objects.get(id=projectID)
        project.name=name
        project.save()
        return JsonResponse({'errno':0,'msg':"重命名成功"})
    else :
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def list(request):
    if request.method == 'GET':
        teamID=request.GET.get('team_id')
        projects=Project.objects.filter(team_id=teamID)
        project_list=[]
        for project in projects:
            user=User.objects.get(id=project.creator_id)
            project_data={
                'project_id':project.id,
                'project_name':project.name,
                'user_id':user.id,
                'user_nickname':user.nickname,
            }
            project_list.append(project_data)
        return JsonResponse({'errno':0,'project_list':project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})