from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    projects = Project.ongoing.all()
    return render(request,
                  'research/project/list.html',
                  {'projects': projects})


def project_detail(request, year, month, day, project):
    project = get_object_or_404(Project, slug=project,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    return render(request,
                  'research/project/detail.html',
                  {'project': project})
