from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings


def user_logout(request):
    """
    Author: Meet Shah
    source implementing logout: https://www.youtube.com/watch?v=l8f-KFxw-xU source implementing file delete: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
    Diff between os.unlink() and os.remove() => https://stackoverflow.com/questions/42636018/python-difference-between-os-remove-and-os-unlink-and-which-one-to-use
    """
    logout(request)
    return HttpResponseRedirect("/login")


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':

            first_name = request.POST['FirstName']
            last_name = request.POST['LastName']
            email = request.POST['Email']
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            user = request.user
            message = "Your profile has been updated successfully"
            flag = "success"
            company = request.user.groups.values_list('name', flat=True)
            context = {'FirstName': user.first_name, 'LastName': user.last_name, 'UserName': request.user.username,
                       'Group': company[0], 'Email': user.email, 'Message': message, 'Flag': flag}
            return render(request, 'Login/edit_profile.html', context)

        else:
            user = request.user
            company = request.user.groups.values_list('name', flat=True)
            context = {'FirstName': user.first_name, 'LastName': user.last_name, 'UserName': request.user.username,
                       'Group': company[0], 'Email': user.email}
            print(company)
            for k in context:
                print(k, ':', context[k])
            return render(request, 'Login/edit_profile.html', context)
