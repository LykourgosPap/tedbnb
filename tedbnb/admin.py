from django.contrib import admin

# Register your models here.
from tedbnb.models import tedbnbuser,tedbnbhouses,tedbnbrent

admin.site.register(tedbnbuser)
admin.site.register(tedbnbhouses)
admin.site.register(tedbnbrent)

