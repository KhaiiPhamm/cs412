"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: View functions for the mini_insta app. Handles ProfileListView 
    and ProfileDetailView functions with corressponding attributes 
"""
from django.shortcuts import render

# Create your views here.
from .models import Profile, Post
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm
from django.urls import reverse
from .models import Photo

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all users.'''

    model = Profile 
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Show the details for one user.'''
    
    model = Profile
    template_name="mini_insta/show_profile.html"
    context_object_name = 'profile'
    
class PostDetailView(DetailView):
    '''Show the details for one post.'''
    
    model = Post
    template_name="mini_insta/show_post.html"
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''Create a new post.'''
    
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add the foreign key to the form instance before saving
        form.instance.profile = profile

        # delegate the work to the superclass method form_valid:
        response = super().form_valid(form)
        
        # read the image URL from the raw form submission
        # image_url = self.request.POST.get('image_url')
        files = self.request.FILES.getlist('image_file')
        
        # print("FILES:", self.request.FILES)
        # create the Photo, with the Post as its foreign key
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)
        for image_file in files:
            Photo.objects.create(post=self.object, image_file=image_file)
        
        return response
    
    def get_success_url(self) -> str:
        '''Provide a URL to redirect to after creating a new Post.'''
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Profile
        return reverse('show_post', kwargs={'pk':self.object.pk})
    
    