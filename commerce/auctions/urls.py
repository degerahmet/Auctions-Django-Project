from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories",views.categories, name="categories"),
    path("wishlist",views.wishlistget, name="wishlistget"),
    path("createlisting",views.createlisting, name="createlisting"),
    path("listings/<int:listing_id>",views.listings, name="listing"),
    path("listings/<int:listing_id>/comment",views.comment,name="comment"),
    path("listings/<int:listing_id>/bid",views.bid,name="bid"),
    path("listings/<int:listing_id>/wishlist",views.wishlist,name="wishlist"),
    path("listings/<int:listing_id>/removewishlist",views.removewishlist,name="removewishlist"),
]
