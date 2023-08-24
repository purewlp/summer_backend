from user.models import User
from team.models import Team,Membership,RoleEnum
from Platform import settings
from django.http import JsonResponse
# Create your views here.

def test(request):
    if request.method=='POST':
        user1=User.objects.get(username='test1')
        user2=User.objects.get(username='test2')

        team1=Team.objects.create(name='Team A',creator=user1)
        team2 = Team.objects.create(name='Team B', creator=user2)

        Membership.objects.create(user=user2, team=team1, role=RoleEnum.ADMIN.value)
        Membership.objects.create(user=user1, team=team2, role=RoleEnum.ADMIN.value)
        Membership.objects.create(user=user2, team=team2, role=RoleEnum.MEMBER.value)
        
        return JsonResponse({'errno':0})
    else:
        return JsonResponse({'errno':1001})

