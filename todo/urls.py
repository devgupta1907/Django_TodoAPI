from django.urls import path
from todo import views
from .views import signup, login

urlpatterns = [
    path('signup/', signup, name="sign_up"),
    path('login/', login, name="log_in"),
    path('todos/', views.CreateListTodos.as_view(), name='create_list_todos'),
    path('todos/<int:pk>', views.RetrieveUpdateDestroyTodo.as_view(), name='retrieve_update_destroy_todos')
]