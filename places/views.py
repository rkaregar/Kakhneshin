from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from habitats.models import GeographicDivision
from places.models import Place, PlaceComment, PlaceCommentPhoto, PlaceCommentVideo
from places.forms import PlaceSearchForm


class PlaceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Place
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'places/create_place.html'
    success_url = '/places'
    success_message = 'مکان دیدنی %s با موفقیت ثبت شد!'

    def form_valid(self, form):
        if self.request.user.member:
            form.instance.owner = self.request.user.member
        return super(PlaceCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')


# noinspection PyAttributeOutsideInit
class PlaceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Place
    fields = ['name', 'address', 'town', 'photo']
    template_name = 'places/update_place.html'
    success_message = 'مکان دیدنی %s با موفقیت ویرایش شد!'

    def get_success_url(self):
        return '/places/%s/detail' % self.place_pk

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)
        return self.place

    def user_passed_test(self, request):
        return request.user.is_superuser or self.place.creator == self.request.user.member
        # return request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['town_name'] = self.place.town.name
        except Exception:
            context['town_name'] = ''
        return context

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceUpdateView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان ویرایش این مکان دیدنی را ندارید')


# noinspection PyAttributeOutsideInit
class PlaceDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = '/places/'
    success_message = 'مکان دیدنی %s با موفقیت حذف شد!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data.get('name')

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)
        return self.place

    def user_passed_test(self, request):
        return request.user.is_superuser or self.place.creator == self.request.user.member
        # return request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceDeleteView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  حذف این مکان دیدنی را ندارید')


class PlaceListView(ListView):
    model = Place

    def get_queryset(self):
        qs = super(PlaceListView, self).get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(creator=self.request.user.member)

        return qs


class PlaceTinyDetailView(DetailView):
    template_name = 'places/place_detail_tiny.html'
    context_object_name = 'place'

    def get_object(self, queryset=None):
        self.place_pk = self.kwargs.get('place_pk', None)
        self.place = get_object_or_404(Place, pk=self.place_pk)

        return self.place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[
            'user_has_edit_access'] = self.request.user.is_superuser or self.place.creator == self.request.user.member

        prev_url = self.request.META.get('HTTP_REFERER', None)
        if prev_url and 'search' in prev_url:
            context['prev_form'] = {}
            context['prev_form']['name'] = self.request.GET.get('name', None)
            context['prev_form']['division'] = self.request.GET.get('division', None)

        context['comments'] = PlaceComment.objects.filter(place_id=self.kwargs.get('place_pk', None)).order_by(
            '-created_at')

        return context

    def user_passed_test(self, request):
        return request.user.is_authenticated
        # return request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        if self.place is None:
            raise Http404
        if self.user_passed_test(request):
            return super(PlaceTinyDetailView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied('شما امکان  دیدن جزییات این مکان دیدنی را ندارید')

    def post(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        if request.POST.get('delete', None):
            comment_id = request.POST.get('comment_id', None)
            comment = PlaceComment.objects.get(pk=comment_id)
            if self.request.user == comment.writer.user:
                comment.delete()
                context['messages'] = ['نظر شما با موفقیت حذف شد.', ]
            else:
                context['errors'] = ['شما تنها مجاز به حذف نظرات ثبت شده توسط خود هستید.', ]
        else:
            rating = request.POST.get('rating', None)
            if rating == '':
                rating = None
            review = request.POST.get('review', None)

            if not rating and not review:
                context['errors'] = ['ثبت حداقل یکی از موارد امتیاز یا متن نظر الزامیست']
            else:
                place_comment = PlaceComment.objects.create(place_id=self.kwargs.get('place_pk', None),
                                                            writer=self.request.user.member, rating=rating,
                                                            review=review)

                if self.request.FILES:
                    for image in self.request.FILES.getlist('image'):
                        PlaceCommentPhoto.objects.create(place_comment=place_comment, photo=image)
                    for video in self.request.FILES.getlist('video'):
                        PlaceCommentVideo.objects.create(place_comment=place_comment, video=video)

        return self.render_to_response(context)


class PlaceSearchView(ListView):
    model = Place
    template_name = 'places/places_search.html'
    # paginate_by = 10 TODO
    context_object_name = 'places'

    def get_queryset(self, **kwargs):
        self.form = PlaceSearchForm(self.request.GET)
        if self.form.is_valid():
            name = self.form.cleaned_data.get('name', None)
            town_id = self.form.cleaned_data.get('division', None)

            places = Place.objects.all()

            if name:
                places = places.filter(name__icontains=name)
            if town_id:
                places = places.filter(town_id=town_id)

            return places
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        try:
            context['division_name'] = GeographicDivision.objects.get(
                pk=self.form.cleaned_data['division']).hierarchy_name
        except Exception:
            context['division_name'] = ''
        return context
