from django.contrib import admin

from products.admin import BasketItemAdminInline
from users.models import EmailVerification, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketItemAdminInline, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )
