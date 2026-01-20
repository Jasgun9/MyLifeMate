from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Sleep

# Create your views here.
def index(request):
    return render(request, 'mysleepmate/index.html')

def insights(request):
    user = request.user

    # ---- Last 7 days total sleep ----
    # last_week = timezone.now().date() - timedelta(days=6)

    # daily_sleep_qs = Sleep.objects.filter(
    #     user=user,
    #     created_at__gte=last_week
    # ).values('created_at').annotate(
    #     total=Sum('duration')
    # ).order_by('created_at')

    # daily_labels = []
    # daily_hours = []

    # for row in daily_sleep_qs:
    #     daily_labels.append(row['created_at'].strftime("%d %b"))
    #     # Convert duration to hours float
    #     # hours = row['total'].total_seconds() / 3600
    #     # daily_hours.append(round(hours, 2))
    #     daily_hours.append(round(row['total'].total_seconds() / 3600, 2))

    # # ---- Bedtime trend ----
    # bedtime_qs = Sleep.objects.filter(user=user).order_by('created_at')

    # bed_labels = []
    # bed_times = []

    # for s in bedtime_qs:
    #     bed_labels.append(s.created_at.strftime("%d %b"))
    #     bed_times.append(s.start_time.hour + s.start_time.minute / 60)

    # # ---- Sleep distribution ----
    # short = Sleep.objects.filter(user=user, duration__lt=timedelta(hours=6)).count()
    # normal = Sleep.objects.filter(user=user, duration__range=(timedelta(hours=6), timedelta(hours=8))).count()
    # long = Sleep.objects.filter(user=user, duration__gt=timedelta(hours=8)).count()

    # context = {
    #     "daily_labels": daily_labels,
    #     "daily_hours": daily_hours,
    #     "bed_labels": bed_labels,
    #     "bed_times": bed_times,
    #     "sleep_dist": [short, normal, long]
    # }
    start_date = timezone.now().date() - timedelta(days=13)
    short = Sleep.objects.filter(user=request.user, duration__lt=timedelta(hours=6)).count()
    healthy = Sleep.objects.filter(user=request.user, duration__range=(timedelta(hours=6), timedelta(hours=8))).count()
    long = Sleep.objects.filter(user=request.user, duration__gt=timedelta(hours=8)).count()

    sleep_dist = [short, healthy, long]

    qs = Sleep.objects.filter(
        user=user,
        created_at__gte=start_date
    ).values('start_time__date').annotate(
        total=Sum('duration')
    ).order_by('created_at')

    labels = []
    hours = []

    for row in qs:
        labels.append(row['start_time__date'].strftime("%d %b"))
        hours.append(
            round(row['total'].total_seconds() / 3600, 2)
        )


    bed_labels = []
    bed_hours = []

    qs = Sleep.objects.filter(user=request.user).order_by('start_time')[:14]

    for s in qs:
        bed_labels.append(s.start_time.date().strftime("%d %b"))
        bed_hours.append(
            s.start_time.hour + s.start_time.minute / 60
        )
    context = {
        "labels": labels,
        "hours": hours,
        "sleep_dist": sleep_dist,
        "bed_labels": bed_labels,
        "bed_hours": bed_hours,
    }
    return render(request, 'mysleepmate/insights.html', context)