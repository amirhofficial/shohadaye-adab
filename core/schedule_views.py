from django.shortcuts import render
from .schedule_data import CLASS_CHOICES, DAYS, PERIODS, SCHEDULES

def schedule(request):
    selected = request.GET.get("class", CLASS_CHOICES[0][0])
    valid = {slug for slug, _ in CLASS_CHOICES}
    if selected not in valid:
        selected = CLASS_CHOICES[0][0]
    day_rows = []
    for key, title in DAYS:
        lessons = SCHEDULES[selected].get(key, [])
        lessons = (lessons + ["نیازمند تکمیل"] * 4)[:4]
        day_rows.append({"title": title, "lessons": lessons})
    return render(request, "schedule.html", {
        "schedule_classes": CLASS_CHOICES, "selected_class_slug": selected,
        "selected_class": dict(CLASS_CHOICES)[selected], "periods": PERIODS, "day_rows": day_rows,
    })
