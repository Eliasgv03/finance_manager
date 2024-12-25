# tags/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tag
from .forms import TagForm

@login_required
def list_tags(request):
    query = request.GET.get('search', '')
    tags = Tag.objects.filter(user=request.user, name__icontains=query)
    return render(request, 'tags/list_tags.html', {'tags': tags, 'query': query})

@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('tags:list_tags')
    else:
        form = TagForm()
    return render(request, 'tags/form_tag.html', {'form': form})

@login_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tags:list_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tags/form_tag.html', {'form': form})

@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'POST':
        tag.delete()
        return redirect('tags:list_tags')
    return render(request, 'tags/confirm_delete_tag.html', {'tag': tag})
