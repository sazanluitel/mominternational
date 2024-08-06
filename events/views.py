from django.shortcuts import render
from django.views import View
from events.models import Events
from django.contrib import messages


class FrontPage(View):
    def get(self, request, *args, **kwargs):
     return render(request, 'index.html')
    
    

def AddEvent(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        no_of_people = request.POST.get('no_of_people')
        locations = request.POST.get('locations')
        budget = request.POST.get('budget')

        errors = []

        if not title:
            errors.append("Title is required.")
        if not start_date:
            errors.append("Start date is required.")
        if not end_date:
            errors.append("End date is required.")
        if not no_of_people:
            errors.append("No of people is required.")
        if not locations:
            errors.append("Location is required.")
        if not budget:
            errors.append("Budget is required.")

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            event = Events(
                title=title,
                start_date=start_date,
                end_date=end_date,
                no_of_people=no_of_people,
                locations=locations,
                budget=budget
            )
            event.save()
            messages.success(request, "Event enquiry is sent successfully! We will get back to you with the event details and budget.")

    return render(request, 'index.html')

class AboutPage(View):
    def get(self, request):
        return render(request, 'website/pages/about.html')

class ContactPage(View):
    def get(self, request):
        return render(request, 'website/pages/contact.html')