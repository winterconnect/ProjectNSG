from django.db import models


class Member(models.Model):
    memberID = models.CharField(max_length=50, primary_key=True, default=' ')
    memberPW = models.CharField(max_length=200)
    memberName = models.CharField(max_length=20)
    memberAge = models.DateField()
    memberEmail = models.CharField(max_length=50)
    adopterHouse = models.CharField(max_length=200, blank=True)
    adopterAddress = models.CharField(max_length=200, blank=True)
    adopterFamily = models.CharField(max_length=200, blank=True)
    authority = models.BooleanField()

    def __str__(self):
        return self.memberID


class Board(models.Model):
    memberID = models.ForeignKey('Member', on_delete=models.SET_DEFAULT, default=' ')
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200, blank=True)
    hashtag = models.CharField(max_length=200, blank=True)
    like = models.IntegerField(default=0, blank=True, null=False)
    petID = models.OneToOneField('Pet', on_delete=models.SET_DEFAULT, default='')


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
    petSpecies = models.CharField(max_length=50, blank=True)  # 견종
    petWeight = models.FloatField(null=True, blank=True)
    petNeuter = models.NullBooleanField()  # 중성화
    petColor = models.CharField(max_length=50, blank=True)
    petImage = models.ImageField(upload_to='images/', blank=True, null=True)  # 'image/': 업로드된 사진을 저장할 디렉토리를 임시로 지정
    petAdoption = models.BooleanField(default=False)  # 입양 완료 여부
    memberID = models.ForeignKey('Member', on_delete=models.SET_DEFAULT, default='')

