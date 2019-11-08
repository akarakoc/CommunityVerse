from django.contrib import admin

# Register your models here.
from community.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts

admin.site.register(Primitives)
admin.site.register(communityUsers)
admin.site.register(Communities)
admin.site.register(Datatypes)
admin.site.register(DatatypeFields)
admin.site.register(Posts)


