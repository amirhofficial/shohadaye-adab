from django.http import Http404
from django.shortcuts import render
import json
from .data import get_data, field_by_id, major_by_id, job_by_id


def index(request):
    data = get_data()
    return render(request, "career/index.html", {"fields": data["FIELDS"], "roadmap": data["ROADMAP"], "skills": data["SKILLS"], "note": data["GENERAL_NOTE"], "quiz_count": len(data["QUIZ"]), "quiz_json": json.dumps(data["QUIZ"], ensure_ascii=False), "fields_json": json.dumps(data["FIELDS"], ensure_ascii=False), "majors": data["MAJORS"], "jobs": data["JOBS"]})


def field_detail(request, field_id):
    data = get_data()
    field = field_by_id(field_id)
    if not field:
        raise Http404("رشته پیدا نشد")
    majors = [x for x in data["MAJORS"] if x["field"] == field_id]
    jobs = [x for x in data["JOBS"] if field_id in x["fields"]]
    return render(request, "career/field.html", {"field": field, "majors": majors, "jobs": jobs, "note": data["GENERAL_NOTE"]})


def major_detail(request, major_id):
    data = get_data()
    major = major_by_id(major_id)
    if not major:
        raise Http404("رشته دانشگاهی پیدا نشد")
    field = field_by_id(major["field"])
    jobs = [x for x in data["JOBS"] if major_id in x["majors"]]
    return render(request, "career/detail.html", {"kind": "major", "item": major, "field": field, "jobs": jobs, "note": data["GENERAL_NOTE"]})


def job_detail(request, job_id):
    data = get_data()
    job = job_by_id(job_id)
    if not job:
        raise Http404("شغل پیدا نشد")
    fields = [field_by_id(x) for x in job["fields"]]
    majors = [x for x in data["MAJORS"] if x["id"] in job["majors"]]
    return render(request, "career/detail.html", {"kind": "job", "item": job, "fields": fields, "majors": majors, "note": data["GENERAL_NOTE"]})
