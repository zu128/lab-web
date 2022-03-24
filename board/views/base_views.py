from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer
from django.core.paginator import Paginator
from django.db.models import Q, Count


def index(request):
    """
    board 목록 출력
    """
    #입력 파라미터
    page = request.GET.get('page', '1')  #   페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 한 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    board 내용 출력
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    question = get_object_or_404(Question, pk=question_id)
    if so == 'recommend':
        answer_list = question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = question.answer_set.annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:
        answer_list = question.answer_set.order_by('-create_date')

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__author__username__icontains=kw) |  # 댓글 글쓴이 검색
            Q(author__username__icontains=kw)  # 질문 글쓴이 검색
        ).distinct()
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'page': page, 'kw': kw, 'so': so, 'answer_list': page_obj}
    return render(request, 'board/question_detail.html', context)
