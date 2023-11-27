from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import random
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import CoreSetting
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
#from rest_framework import status
#from .serializers import SDat


def verify_email(request, user, temp_data, service):
    if service == 'registration':
        subject = 'Account Activation'
        content = 'Use this code to verify your email'
    elif service == 'forgot-password':
        subject = 'Password Reset'
        content = 'Use this code to reset your password'
    email_format = "verify-email.html" 
    temp_data = request.session.get('temporary-data')   
    body = get_template(email_format).render({
    	'otp' : temp_data['otp'],
    	'first_name' : user.first_name,
    	'content' : content,
        })
    email = EmailMessage(subject=subject, body=body, from_email=settings.EMAIL_FROM_USER, to=[temp_data['email']])	
    email.content_subtype = 'html'
    email.send()


def support_email(request, user_data):
    subject = 'Customer Query/Support'
    email_format = "support-email.html" 
    body = get_template(email_format).render({
    	'first_last' : user_data['first_last'],
    	'content' : user_data['content'],
    	'email' : user_data['email'],
        })
    email = EmailMessage(subject=subject, body=body, from_email=settings.EMAIL_FROM_USER, to=[settings.EMAIL_FROM_USER])	
    email.content_subtype = 'html'
    email.send()

def home(request):
	social_data = CoreSetting.objects.all()
	social_data = CoreSetting.objects.get(pk=social_data[0].pk)
	return render(request, 'home.html', {"instagram" : social_data.instagram, "facebook" : social_data.facebook, "twitter" : social_data.twitter})

def about(request):
	return render(request, 'about.html')

@login_required
def contact(request):
	if request.method == 'POST':
		first_last =f"{request.user.first_name} {request.user.last_name}"
		email = request.user.email
		content = request.POST.get('content')
		user_data = {'first_last' : first_last, 'email' : email, 'content' : content}
		support_email(request, user_data)
		return render(request, 'contact.html', {'message' : "We've recieved your query, will get back to you shortly"})
	else:
		return render(request, 'contact.html')

def login_user(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(username=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			return render(request, 'login.html', {'message' : 'Wrong Email or Password!'})
	else:
		message = request.session.pop('login-message', '')
		return render(request, 'login.html', {'message' : message})

def register_user(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		email = email.lower()
		password = request.POST.get('password')
		user_check = User.objects.filter(username=email)
		if len(user_check) == 0:
			user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email, email=email, password=make_password(password))
			user.save()
			user.is_active = False
			user.save()
			otp = random.randint(100000,999999)
			data = {'service': 'registration','otp' : otp, 'email' : email}
			request.session['temporary-data'] = data
			verify_email(request, user, request.session['temporary-data'], 'registration')
			return redirect('verify-otp')
		else:
			return render(request, 'register.html' , {'message' : 'Account Already Exists'})
	else:
		return render(request, 'register.html')

def verify_otp(request):
	if request.method == 'POST':
		otp_recieved = request.POST.get('otp')
		temp_data = request.session.get('temporary-data')
		if otp_recieved == str(temp_data['otp']):
			user = User.objects.get(email=temp_data['email'])
			if temp_data['service'] == 'registration':
				user.is_active = True
				user.save()
				request.session['login-message'] = 'Account Verified, Please Login'
				return redirect('login')
			elif temp_data['service'] == 'forgot-password':
				return redirect('reset-password')
		else:
			return render(request, 'verify-otp.html', {'message' : 'Invalid OTP'})

	else:
		return render(request, 'verify-otp.html')


def forgot_password(request):
	if request.method == 'POST':
		email_registered = request.POST.get('email')
		otp = random.randint(100000,999999)
		data = {'service': 'forgot-password','otp' : otp, 'email' : email_registered}
		request.session['temporary-data'] = data
		check_email = User.objects.filter(email=email_registered)
		if len(check_email) == 0:
			return render(request, 'forgot-password.html', {'message': 'Sorry an account with that email does not exist'})
		else:
			user = User.objects.get(email=email_registered)
			verify_email(request, user, request.session['temporary-data'], 'forgot-password')
			return redirect('verify-otp')
	else:
		return render(request, 'forgot-password.html')

def reset_password(request):
	temp_data = request.session.get('temporary-data')
	if request.method == 'POST':
		newpassword = request.POST.get('new-password')
		hashed_password = make_password(newpassword)
		user = User.objects.get(email=temp_data['email'])
		user.password = str(hashed_password)
		user.save()
		request.session['login-message'] = 'Password Reset Successfully'
		return redirect('login')
	else:
		return render(request, 'reset-password.html')

# def play(request):
# 	return render(request, 'play.html')


def post_recent(request, service, data):
	if request.method == 'POST':
		setting = CoreSetting.objects.get(pk=1)
		if service == 'instagram':
			setting.instagram = data
		elif service == 'twitter':
			setting.twitter = data
		elif service == 'facebook':
			setting.facebook = data
		setting.save()











# 		serializer = SDat(data=request.data)
# 		print(serializer, type(serializer))
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 			#facebook
# 			# facebook_st1 = requests.post(f'https://graph.facebook.com/124223670778858/feed')
# 			# facebook_st2 = requests.post(f'https://graph.facebook.com/{facebook_st1[0]["id"]}/attachments')
# 			# facebook_data = facebook_st2['target']['id']
# 			# instagram_st1 = requests.post(f'https://graph.facebook.com/17841432502221522/media')
# 			# instagram_st2 = requests.post(f'https://graph.facebook.com/{instagram_st1[0]["id"]}?fields=permalink')
# 			# instagram_data = instagram_st2['permalink']
# 			# twitter_st1 =

# #{"iwitter" : "Nigga", "instagram" : "niiger", "twitter" : "nigggerrrrr"}