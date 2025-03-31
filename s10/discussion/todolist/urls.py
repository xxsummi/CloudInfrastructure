from django.urls import path

from . import views

app_name="todolist"

urlpatterns=[
	path('', views.index, name="index"),

	path('register', views.register, name='register'),
	path('change_password', views.change_password, name='change_password'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('add_task', views.add_task, name='add_task'),
	path('update_task', views.update_task, name='update_task'),
	path('todoitem/<int:todoitem_id>/', views.todoitem, name='viewtodoitem'),
	path('todoitem/<int:todoitem_id>/edit', views.update_task, name='update_task'),
	path('todoitem/<int:todoitem_id>/delete', views.delete_task, name='delete_task'),

]