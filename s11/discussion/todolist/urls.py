from django.urls import path

from . import views

app_name="todolist"

urlpatterns=[
	path('', views.index, name="index"),

	path('register', views.register, name='register'),
	path('update_user/', views.update_user, name='update_user'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('add_task', views.add_task, name='add_task'),
	path('add_event', views.add_event, name='add_event'),
	path('todoitem/<int:todoitem_id>/', views.todoitem, name='viewtodoitem'),
	path('todoitem/<int:todoitem_id>/edit', views.update_task, name='update_task'),
	path('todoitem/<int:todoitem_id>/delete', views.delete_task, name='delete_task'),
	path('event/<int:event_id>/', views.event, name='viewevent'),
	path('event/<int:event_id>/edit', views.update_event, name='update_event'),
	path('event/<int:event_id>/delete', views.delete_event, name='delete_event'),
	
	# path('change_password', views.change_password, name='change_password'),

]