from .models import User, Catagory, Listing, user_watchList, comments


def  my_variable(request):
        current_user = request.user if request.user.is_authenticated else None
        filterlist = user_watchList.objects.filter(ownerWatchList=current_user)
        x = len(filterlist)
        r = 'rrr'
        return {'r':r,'current_user': request.user,'x':x}


def comments(request):
        commentt = comments.objects.all()
        return{'commentt':commentt}