from django.shortcuts import render

from . import util

import os

import random

from markdown2 import Markdown

def index(request):
    if request.method == "POST":
        title = request.POST.get("q")
        print(title)
        entries = util.list_entries()
        if title in entries:
            contents = util.get_entry(title)
            return render(request, "encyclopedia/contents.html", {
                "title": title.lower(),
                "heading": title,
                "contents": contents
            })
        else:
            # list of all the entries with the subtring
            sub_entries = []
            for entry in entries:
                if title in entry:
                    sub_entries.append(entry)
            return render(request, "encyclopedia/matched.html", {

                "entries": sub_entries
            })

        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_title(request, title):
    contents = util.get_entry(title)
    markdowner = Markdown()
    contents = markdowner.convert(contents)
    if contents is None:
        return render(request, "encyclopedia/error.html",
                      {
                          "error_heading": "Error! ",
                          "error_message": "We couldn't find the page you are looking"
                      })
    return render(request, "encyclopedia/contents.html", {
        "title": title,
        "contents": contents
    })

def create(request):
    if request.method == "POST":
        all_entries = util.list_entries()
        title = request.POST.get("title")
        contents = request.POST.get("contents")
        if title is None:
            return render(request, "encyclopedia/error.html",
                          {
                              "error_heading": "Error!",
                              "error_message": "Please provide a title."
                          })
        elif title in all_entries:
            return render(request, "encyclopedia/error.html",
                          {
                              "error_heading": "Error!",
                              "error_message": "This page already exists."
                          })
        else:
            filepath = os.path.join('entries/' , f'{title}.md')
            with open(filepath, 'w') as f:
                f.write(contents)
            return view_title(None, title)
        
    
    return render(request, "encyclopedia/create.html")

def edit(request, title):

    if request.method == "POST":
        title = request.POST.get("title")
        contents = request.POST.get("contents")
        if title is None:
            return render(request, "encyclopedia/error.html",
                          {
                              "error_heading": "Error!",
                              "error_message": "Please provide a title."
                          })
        else:
            filepath = os.path.join('entries/' , f'{title}.md')
            with open(filepath, 'w') as f:
                f.write(contents)
            return view_title(request, title)
        
    print(title)
    contents = util.get_entry(title)
    print(contents)
    return render(request, "encyclopedia/edit.html",
                  {
                      "title": title,
                      "contents": contents
                  })
    
def get_random(request):
    entries = util.list_entries()
    return view_title(request, random.choice(entries))
