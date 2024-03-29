from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.createListeing, name="create"),
    path('selectedCategory', views.displayCategory, name='displayCategory'),
    path('creatCategory',views.creatCategory, name='creatCategory'),
    #path('listing/<int:id>', views.listing, name='listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('addWathcList/<int:pk>', views.addWathcList, name='addWathcList'),
    path('removewatchList/<int:pk>', views.removewatchList, name='removewatchList'),
    path('Listingself/<int:pk>', views.Listingself, name='Listingself'),
    path('commentsAL/<int:pk>', views.commentsa, name='commentsa'),
    path('bid/<int:pk>', views.bid, name='bid'),
]