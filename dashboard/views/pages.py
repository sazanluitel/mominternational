from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from events.models import Events

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/index.html')

class Adduser(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/user/add.html')
    
class UserList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/user/list.html')

class UsersAjax(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/user/list.html')
    
class Settings(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/settings/general.html')

# Create your views here.
class PagesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/page/list.html')
    

class AddPagesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/page/add.html')
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        status = request.POST.get('status')
        
        try:
            if not title:
                raise Exception("Page title is required")
            
            page = Events(
                title=title,
                slug=slug,
                description=description,
                status=status,
                user=request.user,
                post_type="page"
            )
            page.clean_fields()
            page.save()
            
            messages.success(request, "Page added successfully")
            return redirect('dashboard:editpage', id=page.id)
        except Exception as e:
            messages.error(request, str(e))

        return render(request, 'dashboard/page/add.html', context={
            "postid" : None,
            "title" : title,
            "slug" : slug,
            "description" : description,
            "status" : status
        })
    
class PagesAjaxView(View):
    
    def get_title(self, title, post_id, username):
        return f'''
            <div class="course_group">
                <div class="content">
                    <div class="title">{title}</div>
                </div>
            </div>
        '''
    
    def get_action(self, post_id):
        edit_url = reverse('dashboard:editpage', kwargs={'id': post_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('dashboard:pages')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <a href="" class="btn btn-warning btn-sm">View</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="page" />
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
        posts = posts.order_by('-date')

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
    

class EditPagesView(View):
    def get(self, request, *args, **kwargs):
        pageid = kwargs.get('id')
        
        try:
            page = get_object_or_404(Events, id=pageid)
            return render(request, 'dashboard/page/add.html', context={
                "postid" : page.id,
                "title" : page.title,
                "slug" : page.slug,
                "description" : page.description,
                "status" : page.status
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:pages')
    

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        status = request.POST.get('status')
        postid = kwargs.get('id')
        
        try:
            page = get_object_or_404(Events, id=postid)
            if not title:
                raise Exception("Page title is required")
            
            page.title = title
            page.slug = slug
            page.description = description
            page.status = status
            page.save()
            
            messages.success(request, "Page updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:editpage', id=postid)


