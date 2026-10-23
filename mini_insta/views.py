"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: View functions for the mini_insta app. Handles ProfileListView 
    and ProfileDetailView functions with corressponding attributes 
"""
from django.shortcuts import render

# Create your views here.
from .models import Profile, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from .models import Photo, Profile, Photo, Follow, Like 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Require login, and give views the logged-in user's Profile."""
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')    
    
    def get_logged_in_profile(self):
        return Profile.objects.filter(user=self.request.user).first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = None
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()
        context['me'] = me
        context['is_following'] = bool(me) and Follow.objects.filter(
            profile=self.object, follower_profile=me).exists()
        return context
    
class PostDetailView(DetailView):
    '''Show the details for one post.'''
    
    model = Post
    template_name="mini_insta/show_post.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = None
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()
        context['me'] = me
        context['has_liked'] = bool(me) and Like.objects.filter(
            post=self.object, profile=me).exists()
        context['profile'] = self.object.profile
        return context
    
class CreatePostView(MyLoginRequiredMixin, CreateView):
    '''Create a new post.'''
    
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        # add the foreign key to the form instance before saving
        form.instance.profile = self.get_logged_in_profile()

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
    
class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    '''Update an existing profile.'''

    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    
    def get_object(self):
        return self.get_logged_in_profile()
    
class DeletePostView(MyLoginRequiredMixin, DeleteView):
    '''Delete an existing post.'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_queryset(self):
        return Post.objects.filter(profile=self.get_logged_in_profile())
    
    def get_success_url(self) -> str:
        '''Provide a URL to redirect to after deleting the Post.'''
        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':self.object.profile.pk})
    
class UpdatePostView(MyLoginRequiredMixin, UpdateView):
    '''Update an existing post.'''

    model = Post
    template_name = "mini_insta/update_post_form.html"
    form_class = UpdatePostForm
    
    def get_queryset(self):
        return Post.objects.filter(profile=self.get_logged_in_profile())
    
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
    
class ShowFeedView(MyLoginRequiredMixin, DetailView):
    '''Show the feed for one user.'''
    
    model = Profile
    template_name="mini_insta/show_feed.html"
    context_object_name = 'profile'
    
    def get_object(self):
        return self.get_logged_in_profile()
    
class SearchView(MyLoginRequiredMixin, ListView):
    '''Show the search results for a query.'''
    
    template_name="mini_insta/search_results.html"
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to get the search query from the request.'''
        if request.user.is_authenticated and "query" not in request.GET:
            return render(request, "mini_insta/search.html", {"profile": self.get_logged_in_profile()})
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Override the get_queryset method to filter the profiles based on the search query.'''
        queryset = self.request.GET.get("query", "")
        return Post.objects.filter(caption__contains=queryset)
    
    def get_context_data(self, **kwargs):
        '''Override the get_context_data method to add the search query to the context.'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")

        # Filter profiles based on the search query
        from_username = Profile.objects.filter(username__contains=query)
        from_bio = Profile.objects.filter(bio_text__contains=query)
        from_display_name = Profile.objects.filter(display_name__contains=query)
        profiles = from_username | from_bio | from_display_name 
        
        # Add the search query and profiles to the context
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = profiles
        return context
    
class ShowMyProfileView(MyLoginRequiredMixin, DetailView):
    """Show the logged-in user;s own profile page"""
    
    template_name = "mini_insta/show_profile.html"
    context_object_name= 'profile'
    
    def get_object(self):
        return self.get_logged_in_profile()
    
class LogoutView(TemplateView):
    """Show the logged-out page"""
    
    template_name = "mini_insta/logout_confirmation.html"

class CreateProfileView(CreateView):
    """Create a new profile"""
    
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
            
        return context
        
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        # save() creates the User and returns it
        user = user_form.save()

        # log the new user in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # attach the User to the Profile before it is saved
        form.instance.user = user

        # delegate the rest to the superclass
        return super().form_valid(form)
    
class FollowView(MyLoginRequiredMixin, TemplateView):
    '''The logged-in user follows the profile with this pk.'''

    def get(self, request, *args, **kwargs):
        me = self.get_logged_in_profile()
        other = Profile.objects.get(pk=kwargs['pk'])

        # never follow yourself, and never follow twice
        if me != other and not Follow.objects.filter(
                profile=other, follower_profile=me).exists():
            Follow.objects.create(profile=other, follower_profile=me)

        return redirect('show_profile', pk=other.pk)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class DeleteFollowView(MyLoginRequiredMixin, TemplateView):
    '''The logged-in user stops following the profile with this pk.'''

    def get(self, request, *args, **kwargs):
        me = self.get_logged_in_profile()
        other = Profile.objects.get(pk=kwargs['pk'])

        Follow.objects.filter(profile=other, follower_profile=me).delete()

        return redirect('show_profile', pk=other.pk)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class LikePostView(MyLoginRequiredMixin, TemplateView):
    '''The logged-in user likes the post with this pk.'''

    def get(self, request, *args, **kwargs):
        me = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        # never like your own post, and never like twice
        if post.profile != me and not Like.objects.filter(
                post=post, profile=me).exists():
            Like.objects.create(post=post, profile=me)

        return redirect('show_post', pk=post.pk)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class DeleteLikePostView(MyLoginRequiredMixin, TemplateView):
    '''The logged-in user removes their like from the post with this pk.'''

    def get(self, request, *args, **kwargs):
        me = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        Like.objects.filter(post=post, profile=me).delete()

        return redirect('show_post', pk=post.pk)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)