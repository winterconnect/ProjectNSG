from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from yyApp.models import Member


# Create your views here.
def join_adopter(request):
    if request.method == "GET":
        return render(request, 'yyApp/adopter.html')
    elif request.method == "POST":
        memberID = request.POST.get('memberID', None)
        memberPW = request.POST.get('memberPW', None)
        memberName = request.POST.get('memberName', None)
        memberEmail = request.POST.get('memberEmail', None)
        memberAge = request.POST.get('memberAge', None)
        adopterHouse = request.POST.get('adopterHouse', None)
        adopterAddress = request.POST.get('adopterAddress', None)
        adopterFamily = request.POST.get('adopterFamily', None)
        res_data = {}
        if not (memberID and memberPW and memberName and memberEmail): #and 수정
            res_data['error'] = '모든 값을 입력해주세요'
        else:
            member = Member(memberID=memberID, memberPW=make_password(memberPW), memberName=memberName,
                            memberEmail=memberEmail, memberAge=memberAge, adopterHouse=adopterHouse,
                            adopterAddress=adopterAddress, adopterFamily=adopterFamily, authority=False)
            member.save()
        return render(request, 'yyApp/adopter.html', res_data)


def join_guardian(request):
    if request.method == "GET":
        return render(request, 'yyApp/guardian.html')
    elif request.method == "POST":
        memberID = request.POST.get('memberID', None)
        memberPW = request.POST.get('memberPW', None)
        memberName = request.POST.get('memberName', None)
        memberEmail = request.POST.get('memberEmail', None)
        memberAge = request.POST.get('memberAge', None)

        res_data = {}
        if not (memberID and memberPW and memberName and memberEmail):
            res_data['error'] = '모든 값을 입력해주세요'
        else:
            member = Member(memberID=memberID, memberPW=make_password(memberPW), memberName=memberName,
                            memberEmail=memberEmail, memberAge=memberAge, authority=True)
            member.save()
        return render(request, 'yyApp/guardian.html', res_data)


def choose_authority(request):
    if request.method == "GET":
        return render(request, 'yyApp/jointype.html')

def board(request):
    if request.method == "GET":
        return render(request, 'yyApp/board.html')        
