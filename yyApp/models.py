from django.db import models
from django_db_views.db_view import DBView


class Member(models.Model):
    memberID = models.CharField(max_length=50, primary_key=True)
    memberPW = models.CharField(max_length=200)
    memberName = models.CharField(max_length=20)
    memberAge = models.DateField()
    memberEmail = models.CharField(max_length=50)
    adopterHouse = models.CharField(max_length=200, blank=True)
    adopterAddress = models.CharField(max_length=200, blank=True)
    adopterFamily = models.CharField(max_length=200, blank=True)
    authority = models.BooleanField()


class Board(models.Model):
    memberID = models.ForeignKey('Member', on_delete=models.SET_DEFAULT, default=' ')
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200, blank=True)
    hashtag = models.CharField(max_length=200, blank=True)
    like = models.IntegerField(default=0, blank=True, null=False)
    petID = models.OneToOneField('Pet', on_delete=models.SET_DEFAULT, default=' ')    


class Comment(models.Model):
    memberID = models.ForeignKey('Member', on_delete=models.SET_DEFAULT, default=' ')
    date = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=4000)
    postID = models.ForeignKey('Board', on_delete=models.CASCADE)


class Pet(models.Model):
    petName = models.CharField(max_length=50, blank=True)
    petBirth = models.DateField(null=True, blank=True)  # 연도만 넣을지
    petSex = models.NullBooleanField()
    petSize = models.CharField(max_length=50, blank=True)
    petLoc = models.CharField(max_length=50, blank=True)  # 발견 장소
    petSpecies = models.CharField(max_length=50, blank=True)  # 견종 총 10개 (8개 종 + 믹스 + 기타)
    petWeight = models.FloatField(null=True, blank=True)
    petNeuter = models.NullBooleanField()  # 중성화
    petColor = models.CharField(max_length=50, blank=True)
    petImage = models.ImageField(upload_to='images/')  # 'image/': 업로드된 사진을 저장할 디렉토리를 임시로 지정
    petAdoption = models.BooleanField(default=False)  # 입양 완료 여부
    memberID = models.ForeignKey('Member', on_delete=models.SET_DEFAULT, default=' ')
    # postID = models.OneToOneField('Board', on_delete=models.SET_DEFAULT, default=' ')


# class BoardPet(DBView):
#     post = models.ForeignKey(Board,on_delete=models.DO_NOTHING)
#     title = models.CharField(max_length=200)
#     content = models.CharField(max_length=200, blank=True)
#     petName = models.CharField(max_length=50, blank=True)
#     petBirth = models.DateField(null=True, blank=True)
#     petSpecies = models.CharField(max_length=50, blank=True)
#     petColor = models.CharField(max_length=50, blank=True)
#     petAdoption = models.BooleanField(default=False)
#     petImage = models.ImageField(upload_to='images/')
#     view_definition = """
#         SELECT
#         row_number() over () as id,
#         Board.id as post_id,
#         Board.title as title,
#         Board.content as content,
#         Pet.petName as petName,
#         Pet.petBirth as 'petBirth',
#         Pet.petColor as 'petColor',
#         Pet.petAdoption as 'petAdoption',
#         Pet.petImage as 'petImage'
#         FROM Board LEFT JOIN Pet
#         ON Board.id = Pet.postID
#     """
#     class Meta:
#         managed = False
#         db_table = "BoardPet"