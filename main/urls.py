from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name="index"),


    path("yenikino/", views.yenikino, name="yenikino"),
    path('details/<int:id>',views.details,name='details'),
    path('category/<int:id>',views.category,name='category'),
    path("addkino/",views.addkino, name="addkino"),
    path("delete1/",views.delete1, name="delete1"),
    path("about/",views.about, name="about"),
    path("contacts/",views.contacts, name="contacts"),
    path('axtar/',views.axtar,name='axtar'),
    path('videocdn/',views.videocdn,name='videocdn'),


]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)



