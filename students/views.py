from collections import OrderedDict

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets

from students.models import User
from students.serializers import UserSerializer
from courses.models import Course
from courses.views import calculate_score


User = get_user_model()


def get_all_scores_for_user(user):
    scores = []
    for course in Course.objects.all():
        course_scores = []
        for section in course.section_set.order_by('number'):
            course_scores.append((section, calculate_score(user, section),))
        scores.append((course, course_scores),)
    return scores


def student_detail(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    student = request.user
    return render(request, 'students/student_detail.html', {
        'scores': get_all_scores_for_user(student),
        'student': student,
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer
