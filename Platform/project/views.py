from user.models import User
from team.models import Team
from project.models import Project
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
        # project=Project.objects.filter(name=name)
        # if project:
        #     return JsonResponse({'errno':1002,'msg':"项目名称重复，请重新命名"})
        new_project=Project(creator=user,team=team,name=name)
        new_project.save()
        return JsonResponse({'errno':0,'msg':"创建项目成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})