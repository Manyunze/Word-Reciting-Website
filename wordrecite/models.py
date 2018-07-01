from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.


class Word(models.Model):
    '''单词'''
    name = models.CharField(max_length=100)
    explanation = models.TextField(default='')
    example = models.TextField(default='')
    vocabularys = models.ManyToManyField('Vocabulary', related_name='words')

    def __str__(self):
        return self.name


class UserAttrib(models.Model):
    '''用户'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_words = models.IntegerField(default=50)
    vocabulary = models.ForeignKey('Vocabulary', null=True)

    def __str__(self):
        return self.user.username

    def unfinishedcount(self):
        '''用户未学过的单词数'''
        return self.words.filter(learntimes__lt=1, vocabulary=self.vocabulary).count()

    def finishedcount(self):
        '''用户已经掌握的单词数'''
        return self.words.filter(learntimes__gte=5, vocabulary=self.vocabulary).count()

    def knowcount(self):
        '''用户学过但是还没掌握的单词数'''
        return self.words.filter(learntimes__gte=1, vocabulary=self.vocabulary).count()


class Note(models.Model):
    ''' 笔记 '''
    content = models.TextField()
    shared = models.BooleanField(default=True)
    user = models.ForeignKey('UserAttrib', related_name='notes', null=True)
    word = models.ForeignKey('Word', related_name='wordnotes', null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    def update(self):
        self.date = timezone.now()


class Vocabulary(models.Model):
    ''' 背诵的范围 '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserWord(models.Model):
    '''
    用户单词库中的每个单词的背诵及其状态
    背诵的次数去衡量每个单词掌握程度
    '''
    word = models.ForeignKey('Word')
    user = models.ForeignKey('UserAttrib', related_name='words')
    vocabulary = models.ForeignKey(
        'Vocabulary', related_name='vocabularywords')
    learntimes = models.IntegerField(default=0)  # 模仿扇贝一个单词背诵5遍
    task = models.ForeignKey(
        'Task',
        related_name='taskwords',
        null=True,
        on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word.name

    def update(self):
        self.date = timezone.now()

    def name(self):
        return self.word.name

    def explanation(self):
        return self.word.explanation

    def example(self):
        return self.word.example

    def know(self):
        self.learntimes += 1
        self.update()
        self.save()

    def unknow(self):
        self.learntimes = 0
        self.update()
        self.save()

    def master(self):
        self.learntimes = 5
        self.update()
        self.save()


class Task(models.Model):
    '''用户每天的任务'''
    user = models.OneToOneField(
        'UserAttrib',
        on_delete=models.CASCADE,
        related_name='task')
    date = models.DateField(null=True)

    def userallcount(self):
        '''用户在该词库中未掌握的单词数'''
        return self.user.words.filter(learntimes__lt=5, vocabulary=self.user.vocabulary).count()

    def todaytaskcount(self):
        '''用户每天任务的单词数'''
        return self.taskwords.count()

    def newtask(self):
        '''创建每天任务'''
        self.date = datetime.today().date()
        count = self.user.words.filter(
            learntimes__lt=5, vocabulary=self.user.vocabulary).count()
        if count < self.user.daily_words:
            words = self.user.words.filter(
                learntimes__lt=5, vocabulary=self.user.vocabulary).order_by('?')[:count]  # 此处一开始忘记过滤掉<5这个条件
            for word in words:
                word.task = self
                word.save()  # 超级重要
        else:
            words = self.user.words.filter(learntimes__lt=5,
                                           vocabulary=self.user.vocabulary)\
                .order_by('?')[:self.user.daily_words]  # 此处一开始忘记过滤掉<5这个条件
            for word in words:
                word.task = self
                word.save()  # 超级重要

    def updatetask(self):
        '''更新每天任务'''
        if self.date < datetime.today().date():
            self.newtask()
            self.save()
