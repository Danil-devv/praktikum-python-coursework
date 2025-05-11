from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Poll, Question, Vote


def home(request):
    polls = Poll.objects.all()
    return render(request, 'home.html', {'polls': polls})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def create_poll(request):
    if request.method == 'POST':
        poll_title = request.POST.get('poll_title')
        poll = Poll.objects.create(title=poll_title, creator=request.user)

        question_indexes = set()
        for key in request.POST:
            if key.startswith('question_') and '_text' in key:
                index = key.split('_')[1]
                question_indexes.add(index)

        for index in sorted(question_indexes):
            text = request.POST.get(f'question_{index}_text')
            q_type = request.POST.get(f'question_{index}_type')
            question = Question.objects.create(poll=poll, text=text, question_type=q_type)

            i = 0
            while True:
                choice_key = f'question_{index}_choice_{i}'
                choice_text = request.POST.get(choice_key)
                if not choice_text:
                    break
                Choice.objects.create(question=question, text=choice_text)
                i += 1

        return redirect('home')
    return render(request, 'create_poll.html')


@login_required
def poll_detail(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return render(request, 'poll_not_found.html')

    questions = poll.questions.all()

    if request.method == 'POST':
        for question in questions:
            answer = request.POST.getlist(f'question_{question.id}')

            if Vote.objects.filter(user=request.user, question=question).exists():
                continue

            for choice_id in answer:
                choice = get_object_or_404(Choice, id=choice_id, question=question)
                Vote.objects.create(user=request.user, question=question, choice=choice)

        return render(request, 'poll_voted.html', {'poll': poll})

    return render(request, 'poll_detail.html', {
        'poll': poll,
        'questions': questions
    })


@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.prefetch_related('choices', 'choices__vote_set')

    results = []
    for question in questions:
        total_votes = question.vote_set.count()

        choices_data = []
        for choice in question.choices.all():
            vote_count = choice.vote_set.count()
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            choices_data.append({
                'text': choice.text,
                'count': vote_count,
                'percent': round(percentage, 1),
            })

        results.append({
            'question': question,
            'choices': choices_data,
        })

    return render(request, 'poll_results.html', {
        'poll': poll,
        'results': results,
    })


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.creator == request.user:
        poll.delete()

    polls = Poll.objects.filter(creator=request.user)
    return render(request, 'my_polls.html', {'polls': polls})


@login_required
def my_polls(request):
    polls = Poll.objects.filter(creator=request.user)
    return render(request, 'my_polls.html', {'polls': polls})
