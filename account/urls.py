from django.conf.urls import include,url
from django.contrib.auth import logout
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import login,logout
from django.conf.urls.static import static
from IntroduceDjango import settings
from django.contrib.auth.views import password_change
urlpatterns=[
    url(r'^login/$',login,{'template_name':'login.html'}),
    url(r'^logout/$',logout,{'template_name':'logout.html'}),
    url(r'^home/$',views.home,name='home'),
    url(r'^about/$',views.about,name='about'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^createuser/$',views.createUser,name='createuser'),
    url(r'^changepass/$',views.changePass,name='changepass'),
    url(r'^upload_image/$',views.upload_document,name='upload_image'),
    url(r'^list_image/$',views.list_file_after_uploaded,name='list_image'),
    url(r'^list_book/$',views.loadBook,name='list_book'),
    url(r'^validate_login/$',views.validateUserLogin,name='validate_login'),
    url(r'^permission/$',views.viewPermission,name='permission'),
    url(r'^add_perm/$',views.add_perms,name='add_perm'),
    url(r'^delete_perm/$',views.delete_perms,name='delete_perm'),
    url(r'^search_user/$',views.search_user,name='search_user'),
    url(r'^delete_object_selected/$',views.deleteObjectSelected,name='delete_object_selected'),
    url(r'^remove_all_permission/$',views.removeAllPermission,name='remove_all_permission'),
    url(r'^delete_document/$',views.delete_document,name='delete_document'),
    url(r'^upload_document/$',views.upload_file,name='upload_document'),
    url(r'^view_list_files/$',views.view_list_files,name='view_list_files'),
    url(r'^download_file/$',views.download_file,name='download_file'),
    url(r'^view_file_content/$',views.view_file_content,name='view_file_content'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
