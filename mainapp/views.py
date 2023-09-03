# ***************** Django Libraries *****************
from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, ListView, View
from rest_framework import mixins, permissions, viewsets
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import requests


# ***************** Models *****************
from mainapp.models import *

# Create your views here.

class redirectPageView(TemplateView):
    template_name = 'landingpage.html'

    def get_context_data(self, status, **kwargs):
        context = super().get_context_data(**kwargs)
        if status == 'Complete':
            context['redirectpageheading'] = 'COMPLETE'
            context['redirectpagemessage'] = 'We really appreciate you stepping in to share your opinion. Your expertise was vital for this project. '
        elif status == 'Quotafull':
            context['redirectpageheading'] = 'QUOTAFULL'
            context['redirectpagemessage'] = 'This survey is quotafull. Will update you as soon as we have further information.'
        else:
            context['redirectpageheading'] = 'TERMINATE'
            context['redirectpagemessage'] = 'Pardon ! This Survey is terminated because the respondent filled wrong data.'
        
        return context

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, status, *args, **kwargs):
        # status = request.GET.get('status','Terminate')
        project_id = request.GET.get('PID', None)
        unique_id = request.GET.get('UID', None)
        ip_address = self.get_client_ip(request)
        # ip_address = '157.32.88.190'
        context = self.get_context_data(status, **kwargs)

        if project_id != None and unique_id != None:
            # if URLDetail.objects.filter(project_id=project_id, unique_id=unique_id).exists():
            if URLDetail.objects.filter(project_id=project_id, unique_id=unique_id, ip_address = ip_address).exists():
                context['reentry'] = 'YES'
                context['redirectpageheading'] = 'YOU HAVE ALREADY ATTEMPTED THIS SURVEY!'
            else:
                # url = "https://iprisk1.p.rapidapi.com/getipinfo/json/157.32.88.190/96d2bec0111ae7fd557083b6e5f7be27"

                # headers = {
                #     'x-rapidapi-key': "f9796bc092msh08147dd8ea3c235p150a82jsna4601e956526",
                #     'x-rapidapi-host': "iprisk1.p.rapidapi.com"
                #     }

                # api_response = requests.request("GET", url, headers=headers)

                # print(api_response.text)
                                
                
                # try:
                #     if location_Api_response.status == 'success':
                #         country = location_Api_response.country
                #         regionName = location_Api_response.regionName
                #         city = location_Api_response.city
                # except:
                if True:
                    country = "N/A"
                    regionName = "N/A"
                    city = "N/A"
                
                urldetail_obj = URLDetail.objects.create(
                    status=status,
                    project_id=project_id,
                    unique_id=unique_id,
                    ip_address=ip_address,
                    country=country,
                    regionName=regionName,
                    city=city
                    )
                context['UID'] = unique_id
                context['PID'] = project_id
                context['status'] = status
                context['ip_address']= ip_address
                context['country']= country
        return self.render_to_response(context)

class projectlistView(LoginRequiredMixin,TemplateView):
    login_url = '/login'
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        # print(self.request.user.id)
        login_user = userType.objects.get(user = self.request.user)
        return {'user_dep':login_user.userdepartment, 'dashboard':' active'}

def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('mainapp:projectlist')
        else:
            template_name = 'signin.html'
            return render(request,template_name)

    if request.method == 'POST':
        template_name = 'signin.html'
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password):
            return render(request,template_name, {'error': 'Invalid email or password...!'})
            
        else:
            user = authenticate(username = email, password = password)
            if user is not None and user.is_active:
                login(request, user)
                if request.POST.get("next", None):
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return redirect("mainapp:projectlist")
            else:
                return render(request,template_name,{'error': 'Invalid email or password...!'})

@login_required(login_url='signout')
def signout(request):
    logout(request)
    return redirect("mainapp:signin")

class LeadershipAccessMixIn(PermissionRequiredMixin):

    def has_permission(self):
        if self.request.user.usertype.userdepartment == '1':
            return True
        else:
            return False
        
    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('mainapp:projectlist')

class deleteEntry(LoginRequiredMixin, LeadershipAccessMixIn, DeleteView):
    model = URLDetail
    login_url = '/login'
    template_name = 'confirm_delete.html'
    success_url ="/dashboard"

    # def get_context_data(self, **kwargs):
    #     login_user = userType.objects.get(user = self.request.user)
    #     return {'user_dep':login_user.userdepartment, 'object':self.get_object()}
    # @login_required(login_url='mainapp:signin')
    # def delete(self, request, *args, **kwargs):
    #     print("=============================Inside Delete==================")
    #     print("================", request.user)
    #     if self.request.user.usertype.userdepartment == '1':
    #         instance = self.get_object()
    #         instance.delete()
    #     return redirect("mainapp:projectlist")
    
    # # def post(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)


class allUserList(LoginRequiredMixin, ListView):
    # queryset = User.objects.all()
    template_name = 'allusers.html'
    def get_context_data(self):
        login_user = userType.objects.get(user = self.request.user)
        return {'userlist':' active', 'allusers':self.get_queryset(),'user_dep':login_user.userdepartment}
    
    def get_queryset(self):
        return User.objects.filter(is_superuser = False)

class changePassword(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        userid = request.POST.get('users', None)
        userpassword = request.POST.get('floatingPassword', None)

        if userid and userpassword:
            get_user = User.objects.get(id = userid)
            get_user.password = make_password(userpassword)
            get_user.save()

            if get_user.id == request.user.id:
                return redirect('mainapp:signin')
        return redirect("mainapp:userlist")
