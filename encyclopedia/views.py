import markdown2
import random

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

# A form class whose instance is used in layout.html to enter the query (the Wiki page you want to view)
class QueryForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    # This condition is satisfied when yhe user submits a query for a Wiki page
    if request.method == "POST":
        entries = util.list_entries()
        form = QueryForm(request.POST)

        if form.is_valid():
            # Getting the query of the user
            query = form.cleaned_data["query"]
            # Getting all the entries that have the query as a substring. Ignores case
            matching_queries = []
            for entry in entries:
                if query.lower() in entry.lower():
                    matching_queries.append(entry)
            # If the Wiki page exists, redirects the user to the Wiki page
            if query in entries:
                return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
            # Else, renders a page that shows a list of queries similar to the user's query
            else:
                return render(request, "encyclopedia/results.html", {
                    "entries": matching_queries
                })
    
    # This is triggered when the request is of GET method,i.e,when we just want to view the page
    query_form = QueryForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": query_form,
    })

"""
This function gets called when we want to render a page that displays the contents of a particular entry. Renders an error 
page if the page does not exist.
"""
def entry(request, title):
    content = util.get_entry(title)
    # Checks if the entry exists
    if content != None:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(f"{content}"),
            "title": title
        })
    # If entry does not exist, shows an error page.
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

"""
This function renders the html page where you enter the content to create a new Wiki page. 
"""
def newpage(request):
    # This contains the title of all Wiki entries in lowercase.
    entries = [entry.lower() for entry in util.list_entries()]

    # This clause is triggered if the user submits a new Wiki entry
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        # Shows an error if no tite is provided
        if len(title) == 0:
            return render(request, "encyclopedia/newpage.html", {
                "content": content,
                "message": "Enter a title!"
            })
        # Shows an error as Wiki entry for this title already exists
        elif title.lower() in entries:
            return HttpResponse(f"Entry for {title} already exists.")
        # Saves the new Wiki entry and redirects the user to its page
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    # This clause is triggered when the request method is GET
    return render(request, "encyclopedia/newpage.html", {
        "content": None,
        "message": None
    })

"""
This function is called when the user clicks on the link to edit an entry
"""
def editpage(request, title):
    content = util.get_entry(title)

    # This clause is triggered when the user makes an edit. 
    if request.method == "POST":
        content = request.POST["content"]
        # Makes the edit and redirects the user to the edit entry's Wiki page
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    # This clause is the default,i.e,when the request method is GET
    return render(request, "encyclopedia/editpage.html", {
        "content": content,
        "title": title
    })

"""
This function is called when the user want's to view a random wiki page.
"""
def randompage(request):
    entries = util.list_entries()
    # Choosing a random Wiki entry
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': random_entry}))

"""
This function is called when we want to delete a Wiki entry
"""
def deletepage(request, title):
    util.delete_entry(title)
    return HttpResponseRedirect(reverse("index"))