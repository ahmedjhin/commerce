from .models import User, Catagory, Listing, user_watchList


def  my_variable(request):
        current_user = request.user if request.user.is_authenticated else None
        filterlist = user_watchList.objects.filter(ownerWatchList=current_user)
        x = len(filterlist)
        r = 'rrr'
        return {'my_variable':'rr','current_user': request.user,'x':x}