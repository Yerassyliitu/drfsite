from django.contrib import admin
from .models import User, Tag, Restaurant, Status, RestaurantImage, SumOfCredit, PeriodOfCredit


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Restaurant)
admin.site.register(Status)
admin.site.register(RestaurantImage)
admin.site.register(SumOfCredit)
admin.site.register(PeriodOfCredit)