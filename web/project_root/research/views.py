from django.shortcuts import render

# Create your views here.
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404
from .models import Project
from .forms import ProjectSearchForm


def project_list(request):
    form = ProjectSearchForm()
    query = None
    if 'query' in request.GET:
        form = ProjectSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            projects = Project.objects.annotate(
                search=SearchVector('en_title', 'th_title', 'th_abstract')).filter(search=query)
    else:
        projects = Project.ongoing.all()
    return render(request,
                  'research/project/list.html',
                  {'projects': projects, 'form': form, 'query': query})


def project_detail(request, year, month, day, project):
    project = get_object_or_404(Project, slug=project,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    thai_status = {'began': 'เริ่มดำเนินการแล้ว',
                   'drafted': 'ร่างโครงการ'}
    return render(request,
                  'research/project/detail.html',
                  {'project': project, 'thai_status': thai_status})
