from django.shortcuts import render
from .models import Member
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, UpdateView

from users.models import Member
from .forms import MemberActivationForm, MemberCreationForm, EditProfileForm


class MemberActivationView(FormView):
    form_class = MemberActivationForm
    success_url = '/'
    template_name = 'activation.html'

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), **{'user': self.get_object()}}

    def get_object(self):
        return get_object_or_404(Member, user__username=self.kwargs['username'])


class MemberCreationView(CreateView):
    form_class = MemberCreationForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:edit_profile')

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('users:activation', args=[self.request.POST['username']])


class EditProfileView(UpdateView):
    model = Member
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        if not hasattr(self.request.user, 'member'):
            self.request.user.member = Member(user=self.request.user)
        return self.request.user.member
