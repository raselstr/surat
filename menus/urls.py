from django.urls import path

from .views import MenuListView, RoleListView, RolePermissionListView, SubMenuListView, UserListView


urlpatterns = [
    path("menu/", MenuListView.as_view(), name="menu_list"),
    path("menu/add/", MenuListView.as_view(), name="menu_add"),
    path("menu/<int:pk>/form/", MenuListView.as_view(), name="menu_update"),
    path("menu/<int:pk>/delete/", MenuListView.as_view(), name="menu_delete"),

    path("sub-menu/", SubMenuListView.as_view(), name="submenu_list"),
    path("sub-menu/add/", SubMenuListView.as_view(), name="submenu_add"),
    path("sub-menu/<int:pk>/form/", SubMenuListView.as_view(), name="submenu_update"),
    path("sub-menu/<int:pk>/delete/", SubMenuListView.as_view(), name="submenu_delete"),

    path("role/", RoleListView.as_view(), name="role_list"),
    path("role/add/", RoleListView.as_view(), name="role_add"),
    path("role/<int:pk>/form/", RoleListView.as_view(), name="role_update"),
    path("role/<int:pk>/delete/", RoleListView.as_view(), name="role_delete"),

    path("user/", UserListView.as_view(), name="user_list"),
    path("user/add/", UserListView.as_view(), name="user_add"),
    path("user/<int:pk>/form/", UserListView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", UserListView.as_view(), name="user_delete"),

    path("hak-akses-menu/", RolePermissionListView.as_view(), name="rolepermission_list"),
    path("hak-akses-menu/add/", RolePermissionListView.as_view(), name="rolepermission_add"),
    path("hak-akses-menu/<int:pk>/form/", RolePermissionListView.as_view(), name="rolepermission_update"),
    path("hak-akses-menu/<int:pk>/delete/", RolePermissionListView.as_view(), name="rolepermission_delete"),
]
