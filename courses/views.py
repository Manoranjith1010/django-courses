from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Topic, Course, Lecture, Enroll
from django.contrib import messages
from django.contrib.auth.decorators import login_required # for Access Control
from django.core.paginator import Paginator



# Create your views here.

def index(request):
    courses = (
        Course.objects.filter(course_is_active='Yes', course_is_featured="Yes")
        .prefetch_related('course_topic')
    )
    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)
    context = {
        'courses': courses_page,
        'page_obj': courses_page,
    }
    return render(request, 'courses/index.html', context)


def courses(request):
    courses = Course.objects.filter(course_is_active='Yes').prefetch_related('course_topic')
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)
    context = {
        'courses': courses_page,
        'page_obj': courses_page,
    }
    return render(request, 'courses/courses.html', context)


def topic_courses(request, topic_slug):
    topic = get_object_or_404(Topic, topic_slug=topic_slug)
    courses = (
        Course.objects.filter(course_is_active='Yes', course_topic=topic)
        .prefetch_related('course_topic')
    )
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)
    context = {
        'courses': courses_page,
        'page_obj': courses_page,
        'topic': topic,
    }
    return render(request, 'courses/topic_courses.html', context)


def search_courses(request):
    if request.method == "GET":
        keyword = request.GET.get('q')
        courses = Course.objects.filter(course_is_active='Yes').prefetch_related('course_topic')
        searched_courses = courses.filter(course_title__icontains=keyword) | courses.filter(course_description__icontains=keyword)
        paginator = Paginator(searched_courses, 9)
        page_number = request.GET.get('page')
        courses_page = paginator.get_page(page_number)
        
        context = {
            'courses': courses_page,
            'page_obj': courses_page,
            'keyword': keyword,
        }
        return render(request, 'courses/search_courses.html', context)


def course_detail(request, course_slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('course_topic'),
        course_slug=course_slug,
    )
    lectures = Lecture.objects.filter(course=course).select_related('course')

    # Check
    if request.user.is_authenticated:
        enrolled = Enroll.objects.filter(course=course, user=request.user)
    else:
        enrolled = None
    

    context = {
        'course': course,
        'lectures': lectures,
        'enrolled': enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required(login_url='account_login')
def lecture(request, course_slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('course_topic'),
        course_slug=course_slug,
    )
    lectures = Lecture.objects.filter(course=course).select_related('course')
    first_lecture = Lecture.objects.filter(course=course).select_related('course')[:1]
    #Check User Enrolled
    enrolled = Enroll.objects.filter(course=course, user=request.user)

    context = {
        'course': course,
        'lectures': lectures,
        'first_lecture': first_lecture,
        'enrolled': enrolled,
    }
    # return render(request, 'courses/lecture.html', context)
    #Check User Enrolled
    if enrolled:
        return render(request, 'courses/lecture.html', context)
    else:
        #User Logged In but Not Enrolled
        messages.error(request, "Enroll Now to access this course.")
        return render(request, 'courses/course_detail.html', context)


@login_required(login_url='account_login')
def lecture_selected(request, course_slug, lecture_slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('course_topic'),
        course_slug=course_slug,
    )
    lectures = Lecture.objects.filter(course=course).select_related('course')
    lecture_selected = get_object_or_404(
        Lecture.objects.select_related('course'),
        lecture_slug=lecture_slug,
        course=course,
    )
    #Check User Enrolled
    enrolled = Enroll.objects.filter(course=course, user=request.user)

    context = {
        'course': course,
        'lectures': lectures,
        'lecture_selected': lecture_selected,
        'enrolled': enrolled,
    }
    # return render(request, 'courses/lecture_selected.html', context)
    #Check User Enrolled
    if enrolled:
        return render(request, 'courses/lecture_selected.html', context)
    else:
        #User Logged In but Not Enrolled
        messages.error(request, "Enroll Now to access this course.")
        return render(request, 'courses/course_detail.html', context)


@login_required(login_url='account_login')
def enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    try:
        Enroll.objects.create(user=user, course=course)
        messages.success(request, "Successfully enrolled to the Course.")
        return redirect(index)

    except IntegrityError:
        messages.error(request, "Couldn't Enroll to the course. Please try again later.")
        return redirect(index)


@login_required(login_url='account_login')
def enrolled_courses(request):
    courses = Enroll.objects.filter(user=request.user).select_related('course')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/enrolled_courses.html', context)
    

        

