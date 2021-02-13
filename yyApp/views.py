from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from yyApp.models import Member, Board, Pet
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.template import context
from django.views.generic import ListView


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



class BoardListView(ListView):
    model = Pet
    paginate_by = 9
    template_name = 'yyApp/board_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'pet_list'        #DEFAULT : <model_name>_list

    def get_queryset(self):
        pet_list = Pet.objects.order_by('-id')
        board_pet = Pet.objects.select_related('board')

        search_keyword_bar = self.request.GET.get('q', '')


        
        search_keyword_box_sex = self.request.GET.get('pet_sex', '')
        search_keyword_box_size = self.request.GET.get('pet_size', '')        
        search_keyword_box_species = self.request.GET.get('pet_species', '')


        print(search_keyword_box_sex)
        print(search_keyword_box_size)
        print(search_keyword_box_species)           
        search_type = self.request.GET.get('type', '')
        
        if search_keyword_bar :
            if len(search_keyword_bar) > 1 :
                if search_type == 'all':
                    search_board_list = board_pet.filter(Q (board__title__icontains=search_keyword_bar) | Q (board__content__icontains=search_keyword_bar))
                elif search_type == 'title_content':
                    search_board_list = board_pet.filter(Q (board__title__icontains=search_keyword_bar) | Q (board__content__icontains=search_keyword_bar))
                elif search_type == 'title':
                    search_board_list = board_pet.filter(board__title__icontains=search_keyword_bar)    
                elif search_type == 'content':
                    search_board_list = board_pet.filter(board__content__icontains=search_keyword_bar)

                return search_board_list    

            else:

                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')   
            
        # 검색박스 구현
        if search_keyword_box_sex and search_keyword_box_size and search_keyword_box_species :
            search_board_list = pet_list.filter(Q (petSex__icontains=search_keyword_box_sex) & Q (petSpecies__icontains=search_keyword_box_species) & Q (petSize__icontains=search_keyword_box_size) )
            return search_board_list

        elif search_keyword_box_sex and search_keyword_box_size:
            search_board_list = pet_list.filter(Q (petSex__icontains=search_keyword_box_sex) & Q (petSize__icontains=search_keyword_box_size) )
            return search_board_list

        elif search_keyword_box_sex and search_keyword_box_species :
            search_board_list = pet_list.filter(Q (petSex__icontains=search_keyword_box_sex) & Q (petSpecies__icontains=search_keyword_box_species) )
            return search_board_list

        elif search_keyword_box_size and search_keyword_box_species :
            search_board_list = pet_list.filter(Q (petSpecies__icontains=search_keyword_box_species) & Q (petSize__icontains=search_keyword_box_size) )
            return search_board_list

        elif search_keyword_box_sex :
            search_board_list = pet_list.filter(Q (petSex__icontains=search_keyword_box_sex) )
            return search_board_list

        elif search_keyword_box_size :
            search_board_list = pet_list.filter(Q (petSize__icontains=search_keyword_box_size) )
            return search_board_list

        elif search_keyword_box_species :
            search_board_list = pet_list.filter(Q (petSpecies__icontains=search_keyword_box_species) )          
            return search_board_list

        else:
            messages.error(self.request, '옵션을 선택해주세요')

        return pet_list


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
        board_fixed = Board.objects.order_by('-id')

        search_keyword_bar = self.request.GET.get('q', '')      
        search_type = self.request.GET.get('type', '')

        search_keyword_box_sex = self.request.GET.get('pet_sex', '')
        search_keyword_box_size = self.request.GET.get('pet_size', '')        
        search_keyword_box_species = self.request.GET.get('pet_species', '')

        if len(search_keyword_bar) > 1 :
            context['q'] = search_keyword_bar

        context['type'] = search_type
        context['board_fixed'] = board_fixed
        context['pet_sex'] = search_keyword_box_sex
        context['pet_size'] = search_keyword_box_size
        context['pet_species'] = search_keyword_box_species
                        

        return context

