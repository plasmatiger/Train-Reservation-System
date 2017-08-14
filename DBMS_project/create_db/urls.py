from django.conf.urls import url
from . import views

app_name = "create_db"

urlpatterns = [
	url(r'^register/$',views.register,name='register'),
	url(r'^filluserdata/$',views.filluserdata, name='filluserdata'),
	url(r'^logout_user/$', views.logout_user, name='logout_user'),
	url(r'^index/$', views.index, name='index'),
	url(r'^search_trains/$', views.search_train_page, name='search_train_page'),
	url(r'^searching_train/$',views.searching_train, name='searching_train'),
	url(r'^booked_ticket_list/$',views.booked_ticket_list, name="booked_ticket_list"),
]