from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import random

from . import util
from markdown2 import markdown

# Create a form to fill title
class NewEntryTitle(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}))

# Create a form to fill content
class NewEntryContent(forms.Form):
    content = forms.CharField(label="Content", widget=forms.TextInput(attrs={'class' : 'form-control col-lg-5'}))

# Render home page with the list of all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Return the entry from "title" parameter
def title(request, title):
    if util.get_entry(title):
        name = ""
        for i in util.get_entry(title).split():
            if i == title:
                name = i
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
        "name": name,
        "content": content,
    })
    else:
        return HttpResponse("The page you are trying to find does not exist")

# Search entry
def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return title(request, value)
    else:
        subString = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subString.append(entry)

        return render(request, "encyclopedia/search.html", {
        "entries": subString,
        "value": value
    })

# Open "Create New Page"
def add(request):
    return render(request, "encyclopedia/add.html")

# Create New Page
def create(request):
    if request.method == 'POST':
        title = NewEntryTitle(request.POST)
        content = NewEntryContent(request.POST)
        if title.is_valid() and content.is_valid():
            title = title.cleaned_data["title"]
            content = content.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html", {
                "name": title,
                "content": content,
                "value": util.get_entry(title)
            })
            else:
                return render(request, "encyclopedia/add.html", {
                "title_form": title,
                "content_form": content,
                "existing": True
                })
        else:
            return render(request, "encyclopedia/add.html", {
            "title_form": title,
            "content_form": content,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/add.html", {
            "title_form": NewEntryTitle(),
            "content_form": NewEntryContent(),
            "existing": False
        })    

# Open "Edit"
def edit_page(request):
    return render(request,"encyclopedia/edit.html")

# Edit
def edit(request):
    if request.method == 'POST':
        title = NewEntryTitle(request.POST)
        content = NewEntryContent(request.POST)
        if title.is_valid() and content.is_valid():
            title = title.cleaned_data["title"]
            content = content.cleaned_data["content"]
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html", {
            "name": title,
            "content": content,
            "value": util.get_entry(title)
            })
        else:
            return render(request, "encyclopedia/edit.html", {
            "title_form": title,
            "content_form": content,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/edit.html", {
            "title_form": NewEntryTitle(),
            "content_form": NewEntryContent(),
        })    

# Random entry
def shuffle(request):
    list = util.list_entries()
    return title(request, random.choices(list)[0])



