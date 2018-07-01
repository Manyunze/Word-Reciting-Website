# coding:utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm, SettingsForm, NoteForm
from .models import User, UserAttrib, Vocabulary, UserWord, Task, Word, Note
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def page_not_found(request):
    return render_to_response('404.html')


def indexview(request):
    if request.user.is_authenticated():
        usermore = get_object_or_404(UserAttrib, user=request.user)
        context = {'usermore': usermore}
        return render(request, "wordrecite/index.html", context=context)
    else:
        return render(request, "wordrecite/index.html")

def about(request):
    if request.user.is_authenticated():
        usermore = get_object_or_404(UserAttrib, user=request.user)
        context = {'usermore': usermore}
        return render(request, "wordrecite/about.html", context=context)
    else:
        return render(request, "wordrecite/about.html")

def registerview(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("wordrecite:indexview"))
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                daily_words = form.cleaned_data['daily_words']
                vocabulary_id = form.cleaned_data['vocabulary']
                vocabulary = Vocabulary.objects.get(id=vocabulary_id)
                user = User.objects.create_user(username=username,
                                                password=password1)
                user.save()
                usermore = UserAttrib.objects.create(user=user)
                usermore.vocabulary = vocabulary
                add_list = []
                for word in vocabulary.words.all():
                    add_list.append(UserWord(word=word,
                                             user=usermore,
                                             vocabulary=vocabulary))
                UserWord.objects.bulk_create(add_list)
                usermore.daily_words = daily_words
                task = Task.objects.create(
                    user=usermore,
                    date=datetime.today().date())
                task.newtask()
                usermore.save()  
                login(request, user)
                return HttpResponseRedirect(reverse("wordrecite:indexview"))
        else:
            form = UserForm()
        return render(request, 'wordrecite/register.html', context={
            'form': form
        })


def loginview(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("wordrecite:indexview"))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('wordrecite:indexview'))
                else:
                    error_message = '无效的用户名或密码'
                    return render(request, 'wordrecite/login.html', context={
                        'error_message': error_message,
                        'form': form
                    })
        else:
            form = LoginForm()
        return render(request, 'wordrecite/login.html', context={
            'form': form
        })

@login_required
def statusview(request):
    usermore = UserAttrib.objects.get(user=request.user)
    task = usermore.task
    task.updatetask()
    message = ""
    if task.userallcount() == 0:
        message = '当前词库已经背完，点击更换词库'
    if task.todaytaskcount() == 0:
        message = '本日学习任务已完成，再来一组请点击这里'
    context = {'usermore': usermore,
               'message': message}
    return render(request, "wordrecite/status.html", context=context)


@login_required
def logoutview(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse("wordrecite:indexview"))


@login_required
def vocabularyview(request):
    if request.user.is_authenticated():
        usermore = get_object_or_404(UserAttrib, user=request.user)
        context = {'usermore': usermore}
        return render(request, "wordrecite/vocabulary.html", context=context)
    else:
        form = LoginForm()
    return render(request, 'wordrecite/login.html', context={'form': form})

@login_required
def settingsview(request):
    usermore = get_object_or_404(UserAttrib, user=request.user)
    data = {
        'vocabulary': usermore.vocabulary.id,
        'daily_words': usermore.daily_words
    }
    form = SettingsForm(initial=data)
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            daily_words = form.cleaned_data['daily_words']
            vocabulary_id = form.cleaned_data['vocabulary']
            vocabulary = Vocabulary.objects.get(id=vocabulary_id)
            if usermore.vocabulary == vocabulary and \
                    usermore.daily_words == daily_words:
                pass
            elif usermore.vocabulary == vocabulary:
                usermore.daily_words = daily_words
                usermore.save()
            else:
                usermore.vocabulary = vocabulary
                add_list = []
                word = vocabulary.words.all()[0]
                if not UserWord.objects.filter(word=word,
                                               user=usermore,
                                               vocabulary=vocabulary).exists():
                    for word in vocabulary.words.all():
                        add_list.append(UserWord(word=word,
                                                 user=usermore,
                                                 vocabulary=vocabulary))
                    UserWord.objects.bulk_create(add_list)
                usermore.daily_words = daily_words
                usermore.task.updatetask()
                usermore.save() 
            return HttpResponseRedirect(reverse("wordrecite:vocabularyview"))
        else:
            return HttpResponseRedirect(reverse("wordrecite:settingsview"))
    else:
        return render(request, 'wordrecite/settings.html', context={
            'form': form
        })


@login_required
def taskview(request):
    usermore = UserAttrib.objects.get(user=request.user)
    task = usermore.task
    task.updatetask()
    if task.userallcount() == 0:
        message = '当前词库已经背完，点击更换词库'
        context = {'usermore': usermore,
                   'message': message}
        return render(request, "wordrecite/settings.html", context=context)
    if task.todaytaskcount() == 0:
        message = '本日学习任务已完成，再来一组请点击这里'
        context = {'usermore': usermore,
                   'message': message}
        return render(request, "wordrecite/status.html", context=context)
    taskword = task.taskwords.all().order_by('date')[0]
    if request.method == 'GET':
        # 此处一开始写成了[:0]这样会一只返回有个单独的Queryset
        return render(request, 'wordrecite/task.html', context={
            'taskword': taskword,
            'usermore': usermore,
            'todaytaskcount': task.todaytaskcount()
        })
    if request.method == 'POST':
        word_id = taskword.word.id
        if request.POST.get('know', False):
            taskword.know()
            task.taskwords.remove(taskword)
            task.save()
            return HttpResponseRedirect(reverse("wordrecite:detailview", args=[word_id]))
        if request.POST.get('master', False):
            taskword.master()
            task.taskwords.remove(taskword)
            task.save()
            return HttpResponseRedirect(reverse("wordrecite:detailview", args=[word_id]))
        if request.POST.get('unknow', False):
            taskword.unknow()
            task.save()
            return HttpResponseRedirect(reverse("wordrecite:detailview", args=[word_id]))
        return HttpResponseRedirect(reverse("wordrecite:indexview"))
    else:
        # 此处一开始写成了[:0]这样会一只返回有个单独的Queryset
        return render(request, 'wordrecite/task.html', context={
            'taskword': taskword,
            'usermore': usermore,
            'todaytaskcount': task.todaytaskcount()
        })


@login_required
def mynotesview(request):
    usermore = UserAttrib.objects.get(user=request.user)
    mynotes = usermore.notes.all().order_by('-date')
    context = {'mynotes': mynotes, 'usermore': usermore}
    if not mynotes.exists():
        message = '你还没有笔记呢'
        context['message'] = message
        return render(request, "wordrecite/mynotespage.html", context=context)
    paginator = Paginator(mynotes, 4)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        # 页码不是整数，返回第一页。
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    context = {'notes': notes, 'usermore': usermore}
    return render(request, 'wordrecite/mynotespage.html', context=context)


@login_required
def detailview(request, word_id):
    usermore = UserAttrib.objects.get(user=request.user)
    word = get_object_or_404(Word, id=word_id)
    if request.method == 'POST':
        if request.POST.get('go', False):
            return HttpResponseRedirect(reverse('wordrecite:taskview'))
        if request.POST.get('note', False):
            return HttpResponseRedirect(reverse('wordrecite:notesview', args=[word_id]))
    return render(request, 'wordrecite/word.html', context={'word': word, 'usermore': usermore})


@login_required
def notesview(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    notes = Note.objects.filter(word=word).filter()
    usermore = UserAttrib.objects.get(user=request.user)
    try:
        note = Note.objects.filter(user=usermore, word=word)[0]
        data = {
            'content': note.content,
        }
        form = NoteForm(initial=data)
        if request.method == 'POST':
            form = NoteForm(request.POST)
            if form.is_valid():
                note.content = form.cleaned_data['content']
                note.update()
                note.save()
                return HttpResponseRedirect(reverse("wordrecite:detailview", args=[word_id]))
    except:
        form = NoteForm()
    if request.method == 'POST':
        if request.POST.get('note', False):
            form = NoteForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                Note.objects.create(
                    content=content,
                    word=word,
                    user=usermore)
                return HttpResponseRedirect(reverse("wordrecite:detailview", args=[word_id]))
    context = {
        'notes': notes,
        'word': word,
        'form': form,
        'usermore': usermore
    }
    return render(request, 'wordrecite/notes.html', context=context)


@login_required
def editnoteview(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    usermore = UserAttrib.objects.get(user=request.user)
    notes = Note.objects.filter(word=word).filter()
    note = Note.objects.filter(user=usermore, word=word)[0]
    data = {
        'content': note.content,
    }
    form = NoteForm(initial=data)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note.content = form.cleaned_data['content']
            note.update()
            note.save()
            return HttpResponseRedirect(reverse('wordrecite:mynotesview'))
    else:
        context = {
            'notes': notes,
            'form': form,
            'word': word,
            'usermore': usermore
        }
        return render(request, 'wordrecite/editnote.html', context=context)


@login_required
def moretaskview(request):
    usermore = UserAttrib.objects.get(user=request.user)
    task = usermore.task
    task.newtask()
    return HttpResponseRedirect(reverse('wordrecite:taskview'))


@login_required
def deletenoteview(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    usermore = UserAttrib.objects.get(user=request.user)
    note = Note.objects.filter(user=usermore, word=word)[0]
    note.delete()
    return HttpResponseRedirect(reverse('wordrecite:mynotesview'))
