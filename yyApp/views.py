from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from yyApp.models import Member, Board, Pet
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.template import context
from django.views.generic import ListView
from yyApp.chartData import state, city
import datetime


# Create your views here.

def check_session(request):
    get_session = request.session.get('user')
    if get_session:
        login_member = Member.objects.get(memberID=get_session)
    else:
        login_member = ''
    return login_member


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
        if not (memberID and memberPW and memberName and memberEmail):
            res_data['error'] = '모든 값을 입력해주세요'
        else:
            if memberPW == request.POST['memberPW_check']:
                member = Member(memberID=memberID, memberPW=make_password(memberPW), memberName=memberName,
                                memberEmail=memberEmail, memberAge=memberAge, adopterHouse=adopterHouse,
                                adopterAddress=adopterAddress, adopterFamily=adopterFamily, authority=False)
                member.save()
            else:
                res_data['error'] = '비밀번호와 비밀번호 확인이 일치하지 않아요'
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
            if memberPW == request.POST['memberPW_check']:
                member = Member(memberID=memberID, memberPW=make_password(memberPW), memberName=memberName,
                                memberEmail=memberEmail, memberAge=memberAge, authority=True)
                member.save()
            else:
                res_data['error'] = '비밀번호와 비밀번호 확인이 일치하지 않아요'

        return render(request, 'yyApp/guardian.html', res_data)


def choose_authority(request):
    if request.method == "GET":
        return render(request, 'yyApp/jointype.html')


def login(request):
    if request.method == "GET":
        return render(request, 'yyApp/login.html')
    elif request.method == "POST":
        login_id = request.POST.get('username', None)
        login_pw = request.POST.get('password', None)
        res_data = {}

        if not (login_id and login_pw):
            res_data['error'] = '아이디와 비밀번호 모두 입력해주세요.'
        else:
            try:
                member = Member.objects.get(memberID=login_id)
                if check_password(login_pw, member.memberPW):
                    request.session['user'] = member.memberID
                    return redirect('/yyApp')
                else:
                    res_data['error'] = '잘못된 비밀번호입니다.'
            except Member.DoesNotExist:
                res_data['error'] = '존재하지 않는 아이디입니다.'
        return render(request, 'yyApp/login.html', res_data)


def logout(request):
    a = check_session(request)
    print(a.memberID)
    if request.session['user']:
        del (request.session['user'])
    return redirect('/yyApp')


def home(request):
    return render(request, 'yyApp/index_haedong.html', {'login_member': check_session(request)})


def save_pet(pet):
    pet.save()


def write_post(request):
    # if request.method == "GET":
    # return render(request, 'yyApp/writepost.html')
    errors = []
    if request.method == 'POST':
        member = check_session(request)
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        date = datetime.date.today().isoformat()
        petName = request.POST.get('petName', '')
        petBirth = request.POST.get('petBirth', '')
        petSex = request.POST.get('petSex', '')
        if petSex == 'Male':
            petSex = True
        elif petSex == 'Female':
            petSex = False
        else:
            petSex = None
        petSize = request.POST.get('petSize', '')
        petLoc = request.POST.get('petLoc', None)
        petSpecies = request.POST.get('petSpecies', '')
        petWeight = float(request.POST.get('petWeight', 0))
        petNeuter = request.POST.get('petNeuter', '')
        if petNeuter == 'yes':
            petNeuter = True
        elif petNeuter == 'no':
            petNeuter = False
        else:
            petNeuter = None
        petColor = request.POST.get('petColor', '')
        petImage = request.FILES['petImage']
        if not petImage:
            petImage = None
        hashtag = request.POST.get('hashtag', '').split('#')

        if not title:
            errors.append('제목을 입력하세요.')
        if not content:
            errors.append('내용을 입력하세요.')
        if not errors:
            pet = Pet(petName=petName, petBirth=petBirth, petSex=petSex, petSize=petSize, petLoc=petLoc, petSpecies=petSpecies,
                      petWeight=petWeight, petImage=petImage, petNeuter=petNeuter, petColor=petColor,
                      memberID=Member.objects.get(memberID=member.memberID))

            save_pet(pet)
            saved_pet = Pet.objects.order_by('-id').first()

            post = Board(memberID=Member.objects.get(memberID=member.memberID), title=title, content=content,
                         date=date, hashtag=hashtag, petID=Pet.objects.get(id=saved_pet.id))

            post.save()

            # for hashtag in hashtag:
            #     hashtag = hashtag.strip()
            #     post.hashtag.add(hashtag)
    return render(request, 'yyApp/writepost.html', {'user': request.user, 'errors': errors, 'login_member': check_session(request)})


def post_detail(request, postID):
    post = get_object_or_404(Board, pk=postID)
    pet = get_object_or_404(Pet, pk=post.petID_id)
    is_check = False
    try:
        if str(post.memberID) == request.session['user']:
            is_check = True
    except KeyError:
        is_check = False
    return render(request, 'yyApp/postdetail.html', {'post': post, 'is_check': is_check, 'pet': pet, 'login_member': check_session(request)})


def post_delete(request):
    id = int(request.GET.get('id'))
    if 'id' in request.GET:
        post = get_object_or_404(Board, id=id)
        post.delete()
    return render(request, "yyApp/finish_delete.html")


class BoardListView(ListView):
    model = Board
    paginate_by = 9
    template_name = 'yyApp/board_list.html'  # DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'board_list'  # DEFAULT : <model_name>_list

    def get_queryset(self):
        board_list = Board.objects.order_by('-id')

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_board_list = board_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_board_list = board_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'title':
                    search_board_list = board_list.filter(title__icontains=search_keyword)
                elif search_type == 'content':
                    search_board_list = board_list.filter(content__icontains=search_keyword)
                return search_board_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return board_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        board_fixed = Board.objects.order_by('-id')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        context['board_fixed'] = board_fixed

        return context


def chart(request):

    pie_labels = list(state['상태'])
    pie_data = list(state['견 수'])
    bar_labels = list(city['지역'])
    bar_data = list(city['견 수'])

    return JsonResponse(data={
        'labelsPie': pie_labels,
        'dataPie': pie_data,
        'labelsBar': bar_labels,
        'dataBar': bar_data
    })