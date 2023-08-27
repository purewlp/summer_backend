from user.models import User
from team.models import Team
from project.models import Project,ProjectRecycleBin,Collection
from Platform import settings
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import F,Q
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
        new_project=Project(creator=user,team=team,name=name,finished=False)
        new_project.save()
        return JsonResponse({'errno':0,'msg':"创建项目成功",'id':new_project.id})
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
        creator_id=creator.id,team=team,project_id=projectID,created_time=project.created_time,
        finished=project.finished,finished_time=project.finished_time)
        project.deleted=True
        project.save()
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

        # Project.objects.create(creator=creator,team=team,name=name,id=projectID,
        # created_time=project.created_time,finished=project.finished,finished_time=project.finished_time)
        project.delete()
        project=Project.objects.get(id=projectID)
        project.deleted = False
        project.save()
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
            if project.finished is True:
                finished='已归档'
                finished_time=project.finished_time.strftime("%Y-%m-%d %H:%M:%S")
            else :
                finished='未归档'
                finished_time=''
            if project.deleted is False:
                project_data={
                    'project_id':project.id,
                    'project_name':project.name,
                    'user_id':user.id,
                    'user_nickname':user.nickname,
                    'created_time':project.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'finished':finished,
                    'finished_time':finished_time,
                    'isEditing':False,
                    'newName':'',
                }
                project_list.append(project_data)
        return JsonResponse({'errno':0,'project_list':project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def binList(request):
    if request.method == 'GET':
        teamID=request.GET.get('team_id')
        projects=ProjectRecycleBin.objects.filter(team_id=teamID)
        project_list=[]
        for project in projects:
            creator=User.objects.get(id=project.creator_id)
            deleter=User.objects.get(id=project.deleter_id)
            if project.finished is True:
                finished='已归档'
                finished_time=project.finished_time.strftime("%Y-%m-%d %H:%M:%S")
            else :
                finished='未归档'
                finished_time=''
            project_data={
                'project_id':project.project_id,
                'project_name':project.name,
                'creator_id':creator.id,
                'creator_nickname':creator.nickname,
                'created_time':project.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                'deleter_id':deleter.id,
                'deleted_time':project.deleted_time.strftime("%Y-%m-%d %H:%M:%S"),
                'expiration_time':project.expiration_time.strftime("%Y-%m-%d %H:%M:%S"),
                'deleter_nickname':deleter.nickname,
                'finished':finished,
                'finished_time':finished_time,
                'isEditing':False,
                'newName':'',
            }
            project_list.append(project_data)
        return JsonResponse({'errno':0,'project_list':project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def ownList(request):
    if request.method == 'GET':
        teamID=request.GET.get('team_id')
        id=request.GET.get('id')
        projects=Project.objects.filter(team_id=teamID,creator_id=id)
        project_list=[]
        for project in projects:
            user=User.objects.get(id=project.creator_id)
            if project.finished is True:
                finished='已归档'
                finished_time=project.finished_time.strftime("%Y-%m-%d %H:%M:%S")
            else :
                finished='未归档'
                finished_time=''
            if project.deleted is False:
                project_data={
                    'project_id':project.id,
                    'project_name':project.name,
                    'created_time':project.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'finished':finished,
                    'finished_time':finished_time,
                    'isEditing':False,
                    'newName':'',
                }
                project_list.append(project_data)
        return JsonResponse({'errno':0,'project_list':project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def deleteAgain(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        project=ProjectRecycleBin.objects.get(project_id=projectID)
        project.delete()
        project=Project.objects.get(project_id=projectID)
        project.delete()
        return JsonResponse({'errno':0,'msg':"项目已彻底删除"})
    else :
        return JsonResponse({'errno':0,'msg':"请求方式错误"})

def finish(request):
    if request.method == 'POST':
        # teamID=request.POST.get('team_id')
        projectID=request.POST.get('project_id')
        project=Project.objects.get(id=projectID)
        project.finished=True
        project.finished_time=timezone.now()
        project.save()
        return JsonResponse({'errno':0,'msg':"该项目已成功归档"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def collect(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        projectID=request.POST.get('project_id')
        info=Collection.objects.filter(user_id=id,project_id=projectID)
        if info:
            return JsonResponse({'errno':1002,'msg':"您已收藏该项目"})
        user=User.objects.get(id=id)
        team=Team.objects.get(id=teamID)
        Collection.objects.create(team=team,user=user,project_id=projectID)
        return JsonResponse({'errno':0,'msg':"收藏成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def discollect(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        projectID=request.POST.get('project_id')
        collection=Collection.objects.get(project_id=projectID)
        collection.delete()
        return JsonResponse({'errno':0,'msg':"取消收藏成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def collectList(request):
    if request.method == 'GET':
        teamID=request.GET.get('team_id')
        id=request.GET.get('id')
        collections=Collection.objects.filter(team_id=teamID,user_id=id)
        project_list=[]
        for collection in collections:
            project=Project.objects.get(id=collection.project_id)
            user=User.objects.get(id=project.creator_id)
            if project.finished is True:
                finished='已归档'
                finished_time=project.finished_time.strftime("%Y-%m-%d %H:%M:%S")
            else :
                finished='未归档'
                finished_time=''
            if project.deleted is False:
                project_data={
                    'project_id':project.id,
                    'project_name':project.name,
                    'user_id':user.id,
                    'user_nickname':user.nickname,
                    'created_time':project.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'finished':finished,
                    'finished_time':finished_time,
                    'isEditing':False,
                    'newName':'',
                }
                project_list.append(project_data)
        return JsonResponse({'errno':0,'project_list':project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def search(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user= User.objects.get(id=id)
        team_id = request.GET.get('team_id')
        team = Team.objects.get(id=team_id)
        search_str = request.GET.get('search_str')
        rank = request.GET.get('rank')
        rank = int(rank)
        if rank == 1 :
            projects=Project.objects.filter(Q(name__icontains=search_str))
            project_list = []
            for project in projects:
                if project.deleted is False:
                    project_data = {
                        'project_id': project.id,
                        'project_name': project.name,
                        'user_id': user.id,
                        'user_nickname': user.nickname,
                        'created_time': project.created_time,
                        'finished': project.finished,
                        'finished_time': project.finished_time,
                        'isEditing': False,
                        'newName': '',
                    }
                    project_list.append(project_data)
            return JsonResponse({'errno': 0, 'project_list': project_list})
        elif rank == 2 :
            projects = Project.objects.filter(Q(name__icontains=search_str))
            project_list = []
            for project in projects:
                if project.creator is user and project.deleted is False:
                    project_data = {
                        'project_id': project.id,
                        'project_name': project.name,
                        'user_id': user.id,
                        'user_nickname': user.nickname,
                        'created_time': project.created_time,
                        'finished': project.finished,
                        'finished_time': project.finished_time,
                        'isEditing': False,
                        'newName': '',
                    }
                    project_list.append(project_data)
            return JsonResponse({'errno': 0, 'project_list': project_list})
        elif rank == 3 :
            projects = Project.objects.filter(Q(name__icontains=search_str))
            project_list = []
            for project in projects:
                if project.deleted is False and Collection.objects.filter(user=user,team=team,project_id = project.id):
                    project_data = {
                        'project_id': project.id,
                        'project_name': project.name,
                        'user_id': user.id,
                        'user_nickname': user.nickname,
                        'created_time': project.created_time,
                        'finished': project.finished,
                        'finished_time': project.finished_time,
                        'isEditing': False,
                        'newName': '',
                    }
                    project_list.append(project_data)
            return JsonResponse({'errno': 0, 'project_list': project_list})
        elif rank ==4 :
            projects = ProjectRecycleBin.objects.filter(Q(name__icontains=search_str))
            project_list = []
            for project in projects:
                if project.team == team:
                    project_data = {
                        'project_id': project.id,
                        'project_name': project.name,
                        'user_id': user.id,
                        'user_nickname': user.nickname,
                        'created_time': project.created_time,
                        'finished': project.finished,
                        'finished_time': project.finished_time,
                        'isEditing': False,
                        'newName': '',
                    }
                    project_list.append(project_data)
            return JsonResponse({'errno': 0, 'project_list': project_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})