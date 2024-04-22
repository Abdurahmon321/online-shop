from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # bosh sahifa

    path('', views.index, name="index"),

    # registratsiya yoki chiqish uchun

    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('signin/', views.user_signup, name="sign_in"),

    # elonlar bo'limi uchun'

    path('elonlar/', views.elonlar, name="elonlar"),
    path('add_elon/', views.add_elon, name="add_elon"),
    path("elon_detail/<int:id>/", views.elon_detail, name="elon_detail"),

    # elonlarni o'zgartirish uchun'

    path("update_elon/<int:id>/", views.update_elon, name="update_elon"),
    path("delete_elon/<int:id>/", views.delete_elon, name="delete_elon"),

    # user profileni update va ko'rish uchun'

    path("user_profile/<int:id>/", views.user_profile, name="user_profile"),
    path("edit_user_profile/<int:id>/", views.edit_user_profile, name="edit_user_profile"),

    # commentni update va delete qilish uchun

    path("edit_comment/<int:id>/", views.edit_comment, name="edit_comment"),
    path("delete_comment/<int:id>/", views.delete_comment, name="delete_comment"),

    # messagelar uchun

    path('messages', views.chat_messages, name="messages"),
    path("chat/sender/<int:sender_id>/receiver/<int:receiver_id>/", views.chat_page, name="chat_page"),
    path("send_message/", views.send_message, name="send_message"),

    # like bosih uchun

    path('products/<int:product_id>/like/', views.add_like, name='like_product'),

    # elonlar bo'limaidagi categoriyalar bo'yicha elonlarni chiqarish

    path("mening_elonlarim/", views.meing_elonlarim, name="mening_elonlarim"),
    path("korgan_elonlarim/", views.korgan_elonlarim, name="korgan_elonlarim"),
    path("like_bosgan_elonlarim/", views.like_bosgan_elonlarim, name="like_bosgan_elonlarim"),

    # categoriyala yordamida sralash

    path("filter_by_category/<int:id>", views.filter_by_category, name="filter_by_category"),

    # bosh menyudagi qidiruv bo'limi uchun

    path('qidiruv-url/', views.product_search, name='product_search'),

    # service bo'limi uchun'

    path("services/", views.services, name="services")
]
