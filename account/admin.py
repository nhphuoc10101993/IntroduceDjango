from django.contrib import admin
from account.models import UserProfile,Document,Publisher,Author,Book,FileStorage
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(FileStorage)