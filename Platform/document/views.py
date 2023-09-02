from project.models import Project
from team.models import Team,Membership
from document.models import Document,DocumentVersion,Folder
from user.models import User
from message.models import Message,UserMessage
from Platform import settings
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

def create(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        folderID=request.POST.get('folder_id')
        id=request.POST.get('id') 
        name=request.POST.get('name')
        if not name:
            name='新建文档'
        # document=Document.objects.filter(name=name,project_id=projectID)
        # if document:
        #     return JsonResponse({'errno':1002,'msg':"名称重复，请重新输入"})
        project=Project.objects.get(id=projectID)
        user=User.objects.get(id=id)
        if not folderID:
            document=Document(project=project,creator=user,name=name)
        else:
            document=Document(project=project,creator=user,name=name,folder_id=folderID)
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
        # document=Document.objects.filter(name=name)
        # if document:
        #     return JsonResponse({'errno':1002,'msg':"名称重复，请重新输入"})
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
        folderID=request.GET.get('folder_id')
        project=Project.objects.get(id=projectID)
        folder_list=[]
        document_list=[]
        if folderID:
            documents=Document.objects.filter(project_id=projectID,folder_id=folderID)
        else:
            documents=Document.objects.filter(project_id=projectID)
            folders=Folder.objects.filter(project_id=projectID)
            for folder in folders:
                folder_data={
                    'folder_id':folder.id,
                    'name':folder.name,
                }
                folder_list.append(folder_data)
  
        for document in documents:
            if folderID:
                document_data={
                    'document_id':document.id,
                    'name':document.name,
                    'created_time':document.created_time,
                    'creator_id':document.creator_id,
                    'edited_time':document.edited_time,
                }
                document_list.append(document_data)
            else:
                if document.folder is None:
                    document_data={
                        'document_id':document.id,
                        'name':document.name,
                        'created_time':document.created_time,
                        'creator_id':document.creator_id,
                        'edited_time':document.edited_time,
                    }
                    document_list.append(document_data)
        return JsonResponse({'errno':0,'document_list':document_list,'folder_list':folder_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def detail(request):
    if request.method == 'GET':
        documentID=request.GET.get('document_id')
        ID=request.GET.get('ID')
        document=Document.objects.get(id=documentID)
        document_info={
            'name':document.name,
            'content':document.content,
        }
        projectID=document.project_id
        teamID=Project.objects.get(id=projectID).team_id
        member_list=[]
        members=Membership.objects.filter(team_id=teamID)
        for member in members:
            user=User.objects.get(id=member.user_id)
            if ID!=str(user.id):
                member_data={
                    'user_id':user.id,
                    'nickname':user.nickname,
                }
                member_list.append(member_data)
        return JsonResponse({'errno':0,'document_info':document_info,'member_list':member_list})
    else :
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def remind(request):
    if request.method == 'POST':
        sendID=request.POST.get('send_id')
        receiveID=request.POST.get('receive_id')
        projectID=request.POST.get('project_id')
        documentID=request.POST.get('document_id')
        send=User.objects.get(id=sendID)
        receive=User.objects.get(id=receiveID)
        project=Project.objects.get(id=projectID)
        document=Document.objects.get(id=documentID)
        content=send.nickname+"在项目"+project.name+"的"+document.name+"文档中提到了你"
        message=Message(content=content,publisher=send.nickname)
        message.save()
        user_message=UserMessage(user=receive,message=message)
        user_message.save()
        return JsonResponse({'errno':0,'msg':"@成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def createFolder(request):
    if request.method == 'POST':
        projectID=request.POST.get('project_id')
        project=Project.objects.get(id=projectID)
        folder=Folder(project=project)
        folder.save()
        return JsonResponse({'errno':0,'msg':"成功新建文件夹"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def deleteFolder(request):
    if request.method == 'POST':
        folderID=request.POST.get('folder_id')
        # projectID=request.POST.get('project_id')
        # project=Project.objects.get(id=projectID)
        folder=Folder.objects.get(id=folderID)
        folder.delete()
        return JsonResponse({'errno':0,'msg':"成功删除文件夹"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def rename(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        folderID=request.POST.get('folder_id')
        folder=Folder.objects.get(id=folderID)
        folder.name=name
        folder.save()
        return JsonResponse({'errno':0,'msg':"重命名成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def versionList(request):
    if request.method == 'GET':
        documentID=request.GET.get('document_id')
        versions=DocumentVersion.objects.filter(document_id=documentID)
        version_list=[]
        for version in versions:
            version_data={
                'version_id':version.id,
                'name':version.name,
                'content':version.content,
                'edited_time':version.edited_time.strftime("%Y-%m-%d %H:%M:%S"),
                'version':version.version
            }
            version_list.append(version_data)
        return JsonResponse({'errno':0,'version_list':version_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def recover(request):
    if request.method == 'POST':
        versionID=request.POST.get('version_id')
        documentID=request.POST.get('document_id')
        version=DocumentVersion.objects.get(id=versionID)
        document=Document.objects.get(id=documentID)
        document.name=version.name
        document.content=version.content
        document.edited_time=timezone.now()
        document.save()
        # DocumentVersion.objects.create(document=document,name=document.name,
        # content=document.content)
        return JsonResponse({'errno':0,'msg':"保存成功"})
    else :
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})