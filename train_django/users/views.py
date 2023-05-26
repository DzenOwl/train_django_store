from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
# from django.contrib import auth, messages
from django.views.generic.edit import CreateView, UpdateView

# from products.models import BasketItem
from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Log in'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    # передаём ссылку на класс
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    title = 'Store - Sign up'
    success_url = reverse_lazy('users:login')
    success_message = 'Registration successful!'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    # передаём ссылку на класс
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Verification'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'], username=kwargs['username'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Store - Log in',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     basket_items = BasketItem.objects.filter(user=user)
#
#     def sum_params(first, second):
#         return first.sum() + second.sum(), first.quantity + second.quantity
#
#     total_sum, total_quantity = reduce(sum_params, basket_items)
#
#     context = {
#         'title': 'Profile',
#         'form': form,
#         'basket_items': basket_items,
#         'total_quantity': total_quantity,
#         'total_sum': total_sum,
#     }
#     return render(request, 'users/profile.html', context)


# def register(request):
# #     if request.method == 'POST':
# #         form = UserRegistrationForm(data=request.POST)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, 'Registration successful!')
# #             return HttpResponseRedirect(reverse('users:login'))
# #         else:
# #             print(form.errors)
# #     else:
# #         form = UserRegistrationForm()
# #     context = {
# #         'title': 'Store - Sign up',
# #         'form': form
# #     }
# #     return render(request, 'users/register.html', context)
