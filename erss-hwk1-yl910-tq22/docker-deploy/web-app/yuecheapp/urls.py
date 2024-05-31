from django.urls import path

from . import accountviews
from . import funcviews

app_name = "yuecheapp"
urlpatterns = [
    path("", accountviews.root, name = "root"),
    path("login/", accountviews.login, name = "login"),
    path("user-register/", accountviews.user_register, name = "user_register"),
    path("main/", funcviews.main, name = "main"),
    path("logout/", accountviews.logout, name = "logout"),
    path("driver-register/", accountviews.driver_register, name = "driver_register"),
    path("profile/", accountviews.profile, name = "profile"),
    path("profile/modify/", accountviews.profile_modify, name = "profile_modify"),
    path("ride-launch/", funcviews.ride_launch, name = "ride_launch"),
    path("ride-search/sharer/", funcviews.ride_search_sharer, name = "ride_search_sharer"),
    path("ride-search/driver/", funcviews.ride_search_driver, name = "ride_search_driver"),
    path("ride-list/user/", funcviews.ride_list_user, name = "ride_list_user"),
    path("ride-list/driver/", funcviews.ride_list_driver, name = "ride_list_driver"),
    path("ride/<int:ride_id>/", funcviews.ride_detail, name = "ride_detail"),
    path("ride/<int:ride_id>/quit/", funcviews.ride_quit, name = "ride_quit"),
    path("ride/<int:ride_id>/modify/", funcviews.ride_modify, name = "ride_modify"),
    path("ride/<int:ride_id>/join/", funcviews.ride_join, name = "ride_join"),
    path("ride/<int:ride_id>/confirm/", funcviews.ride_confirm, name = "ride_confirm"),
    path("ride/<int:ride_id>/complete/", funcviews.ride_complete, name = "ride_complete"),
]