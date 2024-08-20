from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home_page,name='home_page_acesss'),
    path('Create_Acc/',views.Create_Accs,name='Create_Acc_ACCOUNT'),
    path('dashboard',views.welcome_dashboard,name='This page is displayed after login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_data',views.add_data,name='Add Employee Record'),
    path('data_display/',views.data_display,name='Added Data is displayed'),
    path('Employee_Delete',views.Employee_Delete,name='Addes Record is deleted '),
    path('Employee_update',views.Employee_update,name='on this page update data function is performed'),
    path('delete_record/',views.delete_record,name='Table Row Selected Delete'),
    path('update_record',views.update_record,name='selected row updated'),
    path('update_emp',views.update_emp,name='update employee record'),
    path('add_more_files/', views.add_more_files, name='add_more_files'),
    path('del_Prti_fl/', views.del_Prti_fl, name='del_Prti_fl'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)