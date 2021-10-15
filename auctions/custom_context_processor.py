from .models import User, Watchlist

def watchlist_renderer(request):
    if request.user.is_anonymous is False:
        user_id = request.user.pk
        user_list = Watchlist.objects.get(user_watchlist=user_id)
        watch_items = user_list.watchlist_items.all()
        return {
            "watchlist_items": watch_items.all()
        }
    else:
        pass
