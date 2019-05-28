from django.shortcuts import render, get_object_or_404
from .models import CustomUser

def list_researchers(request):
    reseachers = CustomUser.researchers.all()
    return render(request, 'users/researchers.html', {'researchers': reseachers})


def show_profile(request, pk):
    researcher = CustomUser.objects.get(pk=pk)
    publications = researcher.pubs.all()
    return render(request, 'users/profile.html',
                {'researcher': researcher, 'publications': publications})