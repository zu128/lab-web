from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone, dateformat
from ..models import Question
from ..forms import QuestionForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def question_create(request):
    """
    board 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 계정에  로그인 계정 저장
            question.create_date = timezone.now()
            print(dateformat.format(timezone.now(),'Y-m-d'))
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


def category_list(request, category_name):
    """
    카테고리
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    _question_list = Question.objects.filter(category__icontains=category_name)

    if kw:
        _question_list = _question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__content__icontains=kw) |  # 답변내용검색
            Q(answer__author__username__icontains=kw)  # 답글 글쓴이검색
        ).distinct()
    _question_list = _question_list.order_by('-create_date')
    paginator = Paginator(_question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'so': so, 'kw': kw, 'category': category_name}
    return render(request, 'board/question_list.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    board 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')