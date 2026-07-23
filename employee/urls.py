from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_user, name="login"),

    path("employees/", views.employee_list, name="employee_list"),
    path("add/", views.add_employee, name="add_employee"),
    path("employee/<int:id>/", views.employee_details, name="employee_details"),
    path("edit/<int:id>/", views.edit_employee, name="edit_employee"),
    path("delete/<int:id>/", views.delete_employee, name="delete_employee"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_user, name="logout"),
    path(
    "register-face/", views.register_face, name="register_face"),
    path(
    "receive-frame/",
    views.receive_frame,
    name="receive_frame"
),

    path(
    "face-login/",
    views.face_login,
    name="face_login"
),

    path(
    "face-login-api/",
    views.face_login_api,
    name="face_login_api"
),
]