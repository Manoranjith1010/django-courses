from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import Topic, Course, Lecture, Enroll, LectureProgress, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# ===== Helper function for pagination =====
def paginate_queryset(queryset, request, per_page=9):
    """Reusable pagination helper to reduce code duplication."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


# ===== Course listing fields to optimize queries =====
COURSE_LIST_FIELDS = [
    'id', 'course_title', 'course_slug', 'course_description',
    'course_image', 'course_created_at', 'course_is_active', 'course_is_featured'
]


def index(request):
    """Homepage with featured courses."""
    courses = (
        Course.objects
        .filter(course_is_active=True, course_is_featured=True)
        .only(*COURSE_LIST_FIELDS)
        .prefetch_related('course_topic')
    )
    courses_page = paginate_queryset(courses, request, per_page=6)
    
    return render(request, 'courses/index.html', {
        'courses': courses_page,
        'page_obj': courses_page,
    })


def courses(request):
    """All courses listing page."""
    courses = (
        Course.objects
        .filter(course_is_active=True)
        .only(*COURSE_LIST_FIELDS)
        .prefetch_related('course_topic')
    )
    courses_page = paginate_queryset(courses, request)
    
    return render(request, 'courses/courses.html', {
        'courses': courses_page,
        'page_obj': courses_page,
    })


def topic_courses(request, topic_slug):
    """Courses filtered by topic."""
    topic = get_object_or_404(Topic, topic_slug=topic_slug)
    courses = (
        Course.objects
        .filter(course_is_active=True, course_topic=topic)
        .only(*COURSE_LIST_FIELDS)
        .prefetch_related('course_topic')
    )
    courses_page = paginate_queryset(courses, request)
    
    return render(request, 'courses/topic_courses.html', {
        'courses': courses_page,
        'page_obj': courses_page,
        'topic': topic,
    })


def search_courses(request):
    """Search courses by keyword using optimized Q objects."""
    keyword = request.GET.get('q', '').strip()
    
    if keyword:
        # Optimized search using Q objects - single query
        courses = (
            Course.objects
            .filter(
                Q(course_title__icontains=keyword) | 
                Q(course_description__icontains=keyword),
                course_is_active=True
            )
            .only(*COURSE_LIST_FIELDS)
            .prefetch_related('course_topic')
            .distinct()
        )
    else:
        courses = Course.objects.none()
    
    courses_page = paginate_queryset(courses, request)
    
    return render(request, 'courses/search_courses.html', {
        'courses': courses_page,
        'page_obj': courses_page,
        'keyword': keyword,
    })


def course_detail(request, course_slug):
    """Course detail page with lecture list and reviews."""
    course = get_object_or_404(
        Course.objects.prefetch_related('course_topic'),
        course_slug=course_slug,
    )
    lectures = (
        Lecture.objects
        .filter(course=course)
        .only('id', 'lecture_title', 'lecture_slug', 'lecture_file', 'course_id')
        .order_by('id')
    )
    
    # Get reviews for this course
    reviews = (
        Review.objects
        .filter(course=course)
        .select_related('user')
        .order_by('-created_at')[:10]
    )
    avg_rating = Review.objects.filter(course=course).aggregate(avg=Avg('rating'))['avg']
    review_count = Review.objects.filter(course=course).count()
    
    # Use .exists() for boolean check - more efficient than fetching objects
    enrolled = False
    user_review = None
    user_progress = 0
    completed_count = 0
    
    if request.user.is_authenticated:
        enrolled = Enroll.objects.filter(course=course, user=request.user).exists()
        user_review = Review.objects.filter(course=course, user=request.user).first()
        
        # Get user's progress on this course
        if enrolled:
            total = lectures.count()
            completed_count = LectureProgress.objects.filter(
                user=request.user,
                lecture__course=course,
                completed=True
            ).count()
            user_progress = int((completed_count / total) * 100) if total > 0 else 0
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lectures': lectures,
        'enrolled': enrolled,
        'lecture_count': lectures.count(),
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'user_review': user_review,
        'user_progress': user_progress,
        'completed_count': completed_count,
    })


def _get_lecture_context(course, lectures, current_lecture, user=None):
    """Helper to build lecture navigation context with real progress tracking."""
    lecture_list = list(lectures)
    current_index = None
    
    for i, lec in enumerate(lecture_list):
        if lec.id == current_lecture.id:
            current_index = i
            break
    
    previous_lecture = lecture_list[current_index - 1] if current_index and current_index > 0 else None
    next_lecture = lecture_list[current_index + 1] if current_index is not None and current_index < len(lecture_list) - 1 else None
    
    # Calculate real progress based on completed lectures
    total_lectures = len(lecture_list)
    completed_count = 0
    completed_lecture_ids = set()
    
    if user and user.is_authenticated:
        completed_lecture_ids = set(
            LectureProgress.objects.filter(
                user=user,
                lecture__course=course,
                completed=True
            ).values_list('lecture_id', flat=True)
        )
        completed_count = len(completed_lecture_ids)
    
    progress_percent = int((completed_count / total_lectures) * 100) if total_lectures > 0 else 0
    
    # Check if course is just completed (100% and current lecture was the last uncompleted)
    just_completed = (progress_percent == 100 and 
                      current_lecture.id not in completed_lecture_ids.difference({current_lecture.id}))
    
    return {
        'previous_lecture': previous_lecture,
        'next_lecture': next_lecture,
        'progress_percent': progress_percent,
        'current_position': current_index + 1 if current_index is not None else 1,
        'total_lectures': total_lectures,
        'completed_count': completed_count,
        'completed_lecture_ids': completed_lecture_ids,
        'just_completed_course': progress_percent == 100,
    }


@login_required(login_url='account_login')
def lecture(request, course_slug):
    """Lecture page - shows first lecture of the course."""
    course = get_object_or_404(
        Course.objects.only('id', 'course_title', 'course_slug', 'seo_course_description', 'seo_course_keywords'),
        course_slug=course_slug,
    )
    lectures = (
        Lecture.objects
        .filter(course=course)
        .only('id', 'lecture_title', 'lecture_slug', 'lecture_file', 'lecture_description', 'course_id')
        .order_by('id')
    )
    
    # Use .exists() for efficient boolean check
    enrolled = Enroll.objects.filter(course=course, user=request.user).exists()
    
    if not enrolled:
        messages.error(request, "Enroll Now to access this course.")
        return redirect('course-detail', course_slug=course_slug)
    
    first_lecture = lectures.first()
    
    # Mark lecture as completed when accessed
    if first_lecture:
        progress, created = LectureProgress.objects.get_or_create(
            user=request.user,
            lecture=first_lecture,
            defaults={'completed': True, 'completed_at': timezone.now()}
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
    
    # Build navigation context with real progress
    nav_context = {}
    if first_lecture:
        nav_context = _get_lecture_context(course, lectures, first_lecture, request.user)
    
    context = {
        'course': course,
        'lectures': lectures,
        'first_lecture': [first_lecture] if first_lecture else [],
        'lecture_selected': first_lecture,
        'enrolled': enrolled,
        **nav_context,
    }
    
    return render(request, 'courses/lecture.html', context)


@login_required(login_url='account_login')
def lecture_selected(request, course_slug, lecture_slug):
    """Specific lecture page with navigation and progress tracking."""
    course = get_object_or_404(
        Course.objects.only('id', 'course_title', 'course_slug', 'seo_course_description', 'seo_course_keywords'),
        course_slug=course_slug,
    )
    lectures = (
        Lecture.objects
        .filter(course=course)
        .only('id', 'lecture_title', 'lecture_slug', 'lecture_file', 'lecture_description', 'course_id')
        .order_by('id')
    )
    lecture_selected = get_object_or_404(
        Lecture.objects.select_related('course'),
        lecture_slug=lecture_slug,
        course=course,
    )
    
    # Use .exists() for efficient boolean check
    enrolled = Enroll.objects.filter(course=course, user=request.user).exists()
    
    if not enrolled:
        messages.error(request, "Enroll Now to access this course.")
        return redirect('course-detail', course_slug=course_slug)
    
    # Mark lecture as completed when accessed
    progress, created = LectureProgress.objects.get_or_create(
        user=request.user,
        lecture=lecture_selected,
        defaults={'completed': True, 'completed_at': timezone.now()}
    )
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
    
    # Build navigation context with real progress
    nav_context = _get_lecture_context(course, lectures, lecture_selected, request.user)
    
    context = {
        'course': course,
        'lectures': lectures,
        'lecture_selected': lecture_selected,
        'enrolled': enrolled,
        **nav_context,
    }
    
    return render(request, 'courses/lecture_selected.html', context)


@login_required(login_url='account_login')
def enroll(request, course_id):
    """Enroll user in a course."""
    course = get_object_or_404(Course.objects.only('id', 'course_slug'), id=course_id)

    try:
        Enroll.objects.create(user=request.user, course=course)
        messages.success(request, "Successfully enrolled! Start learning now.")
        return redirect('lecture', course_slug=course.course_slug)
    except IntegrityError:
        messages.error(request, "You are already enrolled in this course.")
        return redirect('course-detail', course_slug=course.course_slug)


@login_required(login_url='account_login')
def enrolled_courses(request):
    """List of user's enrolled courses with progress - optimized to avoid N+1."""
    # Get all enrolled course IDs for the user
    enrolled_course_ids = Enroll.objects.filter(
        user=request.user
    ).values_list('course_id', flat=True)
    
    # Get courses with lecture counts in a single query
    courses_with_counts = Course.objects.filter(
        id__in=enrolled_course_ids
    ).annotate(
        total_lectures=Count('lectures'),
        completed_lectures=Count(
            'lectures__progress',
            filter=Q(
                lectures__progress__user=request.user,
                lectures__progress__completed=True
            )
        )
    ).only('id', 'course_title', 'course_slug', 'course_image', 'course_description')
    
    # Calculate progress for each course
    courses_with_progress = []
    for course in courses_with_counts:
        total = course.total_lectures
        completed = course.completed_lectures
        progress = int((completed / total) * 100) if total > 0 else 0
        
        courses_with_progress.append({
            'course': course,
            'progress': progress,
            'completed': completed,
            'total': total,
        })
    
    return render(request, 'courses/enrolled_courses.html', {
        'courses': courses_with_progress,
    })


@login_required(login_url='account_login')
def submit_review(request, course_slug):
    """Submit or update a course review."""
    if request.method != 'POST':
        return redirect('course-detail', course_slug=course_slug)
    
    course = get_object_or_404(Course, course_slug=course_slug)
    
    # Check if user is enrolled
    if not Enroll.objects.filter(course=course, user=request.user).exists():
        messages.error(request, "You must be enrolled to leave a review.")
        return redirect('course-detail', course_slug=course_slug)
    
    rating = request.POST.get('rating', 5)
    comment = request.POST.get('comment', '').strip()
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            rating = 5
    except (ValueError, TypeError):
        rating = 5
    
    # Create or update review
    review, created = Review.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={'rating': rating, 'comment': comment}
    )
    
    if created:
        messages.success(request, "Thank you for your review!")
    else:
        messages.success(request, "Your review has been updated.")
    
    return redirect('course-detail', course_slug=course_slug)