"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: View functions for the mini_insta app. Handles ProfileListView 
    and ProfileDetailView functions with corressponding attributes 
"""
from django.shortcuts import render

# Create your views here.
from .models import Profile, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
class CreatePostView(CreateView):
    '''Create a new post.'''
    
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)
 
 
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
    
class UpdateProfileView(UpdateView):
    '''Update an existing profile.'''

    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    
class DeletePostView(DeleteView):
    '''Delete an existing post.'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        context['profile'] = profile

        return context
    
    def get_success_url(self) -> str:
        '''Provide a URL to redirect to after deleting the Post.'''
        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':self.object.profile.pk})
    
class UpdatePostView(UpdateView):
    '''Update an existing post.'''

    model = Post
    template_name = "mini_insta/update_post_form.html"
    form_class = UpdatePostForm
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        context['profile'] = profile

        return context
    def get_success_url(self) -> str:
        '''Provide a URL to redirect to after updating the Post.'''
        # call reverse to generate the URL for this Post
        return reverse('show_post', kwargs={'pk':self.object.pk})
    
class ShowFollowersDetailView(DetailView):
    '''Show the followers for one user.'''
    
    model = Profile
    template_name="mini_insta/show_followers.html"
    context_object_name = 'profile'
    
class ShowFollowingDetailView(DetailView):
    '''Show the following for one user.'''
    
    model = Profile
    template_name="mini_insta/show_following.html"
    context_object_name = 'profile'
    
class ShowFeedView(DetailView):
    '''Show the feed for one user.'''
    
    model = Profile
    template_name="mini_insta/show_feed.html"
    context_object_name = 'profile'
    
class SearchView(ListView):
    '''Show the search results for a query.'''
    
    template_name="mini_insta/search_results.html"
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to get the search query from the request.'''
        if "query" not in self.request.GET:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Override the get_queryset method to filter the profiles based on the search query.'''
        queryset = self.request.GET.get("query", "")
        return Post.objects.filter(caption__contains=queryset)
    
    def get_context_data(self, **kwargs):
        '''Override the get_context_data method to add the search query to the context.'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
       
       # Get the profile and posts for the current user
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        posts = self.get_queryset()

        # Filter profiles based on the search query
        from_username = Profile.objects.filter(username__contains=query)
        from_bio = Profile.objects.filter(bio_text__contains=query)
        from_display_name = Profile.objects.filter(display_name__contains=query)
        profiles = from_username | from_bio | from_display_name 
        
        # Add the search query and profiles to the context
        context['query'] = query
        context['profile'] = profile
        context['posts'] = posts
        context['profiles'] = profiles
        return context