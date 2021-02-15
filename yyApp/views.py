from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from yyApp.models import Member, Board, Pet, Comment
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.template import context
from django.views.generic import ListView
from yyApp.chartData import state, city
import datetime
from django.db import connection
from .form import CommentForm


# Create your views here.

def check_session(request):
    get_session = request.session.get('user')
    if get_session:
        login_member = Member.objects.get(memberID=get_session)
    else:
        login_member = None
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
    cursor = connection.cursor()
    strSql = '''
    SELECT yyApp_Board.id, petImage FROM yyApp_Board JOIN yyApp_Pet ON yyApp_Board.petID_id = yyApp_Pet.id \
        ORDER BY yyApp_Board.id DESC LIMIT 4;
    '''  # Board tbl에서 id와 petimg 가져옴/ petID에 근거하여 Pet tbl를 조인/Board tbl의 id를 내림차순으로 4개만 정렬
    cursor.execute(strSql)
    result = cursor.fetchall()  # 튜플 형태로 가져옴(board_id, petImage) 
    print(result)
    connection.commit()
    connection.close()

    return render(request, 'yyApp/index_haedong.html', {'login_member': check_session(request), 'pets': result})


def save_pet(pet):
    pet.save()


def write_post(request):
    if request.method == "GET":
        return render(request, 'yyApp/writepost.html', {'login_member': check_session(request)})
    elif request.method == 'POST':
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

        try:
            petImage = request.FILES['petImage']
        except:
            petImage = None

        hashtag = request.POST.get('hashtag', '')
        hashtag.replace(" ", "")

        errors = []

        if not title:
            errors.append('제목을 입력하세요.')
        if not content:
            errors.append('내용을 입력하세요.')
        if not errors:
            pet = Pet(petName=petName, petBirth=petBirth, petSex=petSex, petSize=petSize, petLoc=petLoc,
                      petSpecies=petSpecies,
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
    return render(request, 'yyApp/finish_write.html',
                  {'user': request.user, 'errors': errors, 'login_member': check_session(request)})


def post_detail(request, postID):
    post = get_object_or_404(Board, pk=postID)
    pet = get_object_or_404(Pet, pk=post.petID_id)
    comments = Comment.objects.filter(postID=postID)
    print(comments)
    is_check = False
    try:
        if str(post.memberID) == request.session['user']:
            is_check = True
    except KeyError:
        is_check = False
    return render(request, 'yyApp/postdetail.html',
                  {'post': post, 'is_check': is_check, 'pet': pet, 'comments': comments, 'login_member': check_session(request)})


def post_delete(request):
    id = int(request.GET.get('id'))
    if 'id' in request.GET:
        post = get_object_or_404(Board, id=id)
        post.delete()
    return render(request, "yyApp/finish_delete.html")


class BoardListView(ListView):
    model = Pet
    paginate_by = 9
    template_name = 'yyApp/board_list.html'  # DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'board_pet'  # DEFAULT : <model_name>_list

    def get_queryset(self):
        board_pet = Pet.objects.select_related('board').order_by('-id').exclude(board__id=None)
        search_keyword_bar = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        search_keyword_box_sex = self.request.GET.get('pet_sex', None)
        search_keyword_box_size = self.request.GET.get('pet_size', '')
        search_keyword_box_species = self.request.GET.get('pet_species', '')

        if search_keyword_bar:
            if len(search_keyword_bar) > 1:
                if search_type == 'all':
                    search_board_list = board_pet.filter(
                        Q(board__title__icontains=search_keyword_bar) | Q(board__content__icontains=search_keyword_bar))
                elif search_type == 'title_content':
                    search_board_list = board_pet.filter(
                        Q(board__title__icontains=search_keyword_bar) | Q(board__content__icontains=search_keyword_bar))
                elif search_type == 'title':
                    search_board_list = board_pet.filter(board__title__icontains=search_keyword_bar)
                elif search_type == 'content':
                    search_board_list = board_pet.filter(board__content__icontains=search_keyword_bar)

                return search_board_list

            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')

        # 검색박스 구현
        if search_keyword_box_sex and search_keyword_box_size and search_keyword_box_species:
            search_board_list = board_pet.filter(
                Q(petSex=search_keyword_box_sex) &
                Q(petSpecies__icontains=search_keyword_box_species) &
                Q(petSize__icontains=search_keyword_box_size))
            return search_board_list

        elif search_keyword_box_sex and search_keyword_box_size:
            search_board_list = board_pet.filter(
                Q(petSex=search_keyword_box_sex) &
                Q(petSize__icontains=search_keyword_box_size))
            return search_board_list

        elif search_keyword_box_sex and search_keyword_box_species:
            search_board_list = board_pet.filter(
                Q(petSex=search_keyword_box_sex) &
                Q(petSpecies__icontains=search_keyword_box_species))
            return search_board_list

        elif search_keyword_box_size and search_keyword_box_species:
            search_board_list = board_pet.filter(
                Q(petSpecies__icontains=search_keyword_box_species) &
                Q(petSize__icontains=search_keyword_box_size))
            return search_board_list

        elif search_keyword_box_sex:
            search_board_list = board_pet.filter(Q(petSex=search_keyword_box_sex))
            return search_board_list

        elif search_keyword_box_size:
            search_board_list = board_pet.filter(Q(petSize__icontains=search_keyword_box_size))
            return search_board_list

        elif search_keyword_box_species:
            search_board_list = board_pet.filter(Q(petSpecies__icontains=search_keyword_box_species))
            return search_board_list

        else:
            messages.error(self.request, '옵션을 선택해주세요')

        return board_pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 페이지
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
        board_fixed = Board.objects.order_by('-id')

        # 검색필터, 검색바
        search_keyword_bar = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        search_keyword_box_sex = self.request.GET.get('pet_sex', None)
        search_keyword_box_size = self.request.GET.get('pet_size', '')
        search_keyword_box_species = self.request.GET.get('pet_species', '')

        if len(search_keyword_bar) > 1:
            context['q'] = search_keyword_bar

        context['type'] = search_type
        context['board_fixed'] = board_fixed
        context['pet_sex'] = search_keyword_box_sex
        context['pet_size'] = search_keyword_box_size
        context['pet_species'] = search_keyword_box_species

        # 글쓰기 버튼 구현
        login_member = check_session(self.request)
        if login_member and login_member.authority:
            is_check = True
        else:
            is_check = False
        context['is_check'] = is_check
        context['login_member'] = login_member

        # pet_list = Pet.objects.order_by('-id')
        # for pet in pet_list:
        #     board_list = Board.objects.filter(petID_id=pet.id)
        #     for board in board_list:
        #         print("board: ", board.petID_id)
        #         print("pet: ", pet.id)
        #         if pet.id == board.petID_id:
        #             is_same = True
        #         else :
        #             is_same = False
        #         print(is_same)

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


def mypage(request):
    login_member = check_session(request)
    posts = Board.objects.filter(memberID=login_member.memberID)
    pets = Pet.objects.filter(memberID=login_member.memberID)

    return render(request, "yyApp/mypage.html", {'login_member': login_member, 'posts': posts, 'pets': pets})


def modify_adoption(request):
    id = int(request.GET.get('id'))
    pet = Pet.objects.get(id=id)
    if 'id' in request.GET:
        if not pet.petAdoption:
            pet.petAdoption = True
            pet.save()
        else:
            pet.petAdoption = False
            pet.save()
    return render(request, "yyApp/finish_mod_adoption.html")


def add_comment_to_post(request, postID):
    post = get_object_or_404(Board, id=postID)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postID = post
            comment.save()
            return redirect('yyApp:post_detail', postID=post.id)
    else:
        form = CommentForm()
        return render(request, 'yyApp/add_comment_to_post.html', {'form': form})
