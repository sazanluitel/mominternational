from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
# from core.models import Post
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
# from core.models import STATUS
from django.db.models import Q
from events.models import Events

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@method_decorator(csrf_exempt, name='dispatch')

# Create your views here.
class EventView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/events/list.html')
    

class AddEventView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/events/add.html')
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        entry_charge = request.POST.get('entry_charge')
        description = request.POST.get('description')
        
        try:
            if not title:
                raise Exception("Event title is required")
            
            event = Events(
                title=title,
                slug=slug,
                user=request.user,
                start_date=start_date,
                end_date=end_date,
                location=location,
                entry_charge=entry_charge,
                description=description,

            )

            event.clean_fields()
            event.save()
            
            messages.success(request, "Event added successfully")
            return redirect('dashboard:editpost', id=event.id)
        except Exception as e:
            messages.error(request, str(e))

        return render(request, 'dashboard/events/add.html', context={
            "eventid" : None,
            "title" : title,
            "slug" : slug,
            "description" : description,
            "start_date" : start_date,
            "end_date" : end_date,
            "location" : location,
            "entry_charge" : entry_charge,
        })
    
class EventAjaxView(View):
    
    def get_title(self, title, event_id, username):
        return f'''
            <div class="course_group">
                <div class="content">
                    <div class="title">{title}</div>
                </div>
            </div>
        '''
    
    
    def get_action(self, event_id):
        edit_url = reverse('dashboard:editpost', kwargs={'id': event_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('dashboard:posts')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <a href="" class="btn btn-warning btn-sm">View</a>

                <input type="hidden" name="_selected_id" value="{event_id}" />
                <input type="hidden" name="_selected_type" value="post" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', None)
        page_number = (start // length) + 1

        posts = Events.objects.filter(post_type="page")
        if search_value:
            posts = posts.filter(Q(title__icontains=search_value) | Q(description__icontains=search_value) | Q(slug__icontains=search_value))
        posts = posts.order_by('date')

        paginator = Paginator(posts, length)
        page_posts = paginator.page(page_number)

        data = []
        for post in page_posts:
            data.append([
                self.get_title(post.title, post.id, post.user.username),
                self.get_status(post.status, post.id),
                self.get_action(post.id)
            ])

        return JsonResponse({
            "draw" : draw,
            "recordsTotal" : paginator.count,
            "recordsFiltered" : paginator.count,
            "data" : data
        }, status=200)
    

class EditEventView(View):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        
        try:
            event = get_object_or_404(Events, id=event_id)
            return render(request, 'dashboard/events/add.html', context={

            "eventid" : event.id,
            "title" : event.title,
            "slug" : event.slug,
            "description" : event.description,
            "start_date" : event.start_date,
            "end_date" : event.end_date,
            "location" : event.location,
            "entry_charge" : event.entry_charge,
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:posts')
    

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        entry_charge = request.POST.get('entry_charge')
        description = request.POST.get('description')
        eventid = kwargs.get('id')
        
        try:
            event= get_object_or_404(Events, id=eventid)
            if not title:
                raise Exception("Event title is required")
            
            event.title = title
            event.slug = slug
            event.start_date = start_date
            event.end_date = end_date
            event.location = location
            event.entry_charge = entry_charge
            event.description = description
    
            event.save()
            messages.success(request, "Event updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:editevent', id=eventid)