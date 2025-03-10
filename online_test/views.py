from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from online_test.models import *
import google.generativeai as ai
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import Profile
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt #include this 
import random
def welcome(request):
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)

def signup(request):
    template=loader.get_template("signup.html")
    res=template.render()
    return HttpResponse(res)

@csrf_exempt
def store_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {'msg': 'Username already taken. Try another.'})

        User.objects.create(username=username, password=password, name=name)
        return render(request, "login.html")

    return render(request, "signup.html", {'msg': 'Invalid request. First, signup.'})

    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['username'] = username
            user_data = User.objects.filter(username=username)
            profile_data = Profile.objects.filter(username=username)

            return render(request, "homepage.html", {'user_data': user_data, 'profile_data': profile_data})

        return render(request, "login.html", {'msg': 'Invalid credentials. Try again.'})

    return render(request, "login.html")


def homepage(request):
    if 'username' not in request.session:
        return render(request, "welcome.html")

    username = request.session.get('username')
    user_data = User.objects.filter(username=username)
    profile_data = Profile.objects.filter(username__username=username).first()


    return render(request, "homepage.html", {'user_data': user_data, 'profile_data': profile_data})


def profile(request):
    return render(request, 'profile.html')  # Ensure 'profile.html' exists in templates

def profile_view(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse("Unauthorized", status=401)

    user = User.objects.get(username=username)
    profile, created = Profile.objects.get_or_create(username=user)

    return render(request, 'profile.html', {'profile': profile})



@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Fetch user profile (adjust this according to your database structure)
        username = request.session.get('username')
        if not username:
            return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)

        user = User.objects.get(username=username)
        user_profile, created = Profile.objects.get_or_create(username=user)

        for field, value in data.items():
            setattr(user_profile, field, value)

        user_profile.save()

        return JsonResponse({"success": True, "updated_data": data})
  

        # Update the fields dynamically
        for field, value in data.items():
            setattr(user_profile, field, value)

        user_profile.save()  # Save changes

        return JsonResponse({"success": True, "updated_data": data})
    
    return JsonResponse({"success": False, "error": "Invalid request"})

def subject1(request):
    ques=Test_paper_subject1.objects.all()
    quse_list=list(ques)
    random.shuffle(quse_list)
    quse_list=quse_list[:4:1] ###### total questions can be customized
    context={
        'quse_list':quse_list
    }
    template=loader.get_template("subject1.html")
    res=template.render(context,request)
    return HttpResponse(res)

@csrf_exempt # include  this
def result1(request):
    if request.method=='POST':
        subject='DBMS'
        correct=0
        total=4
        for i in range(1,7,1): # traverse total number of questions
            if ('id'+str(i)) in request.POST.keys():  
                q_id=request.POST['id'+str(i)]
                ans=request.POST['option'+str(i)]
                ques=Test_paper_subject1.objects.filter(q_id=q_id)
                if(len(ques.filter(ans=ans))):
                    correct=correct+1
        wrong=total-correct
        percentage=(correct/total)*100
        username=request.session.get('username')
        history=Test_history()
        history.subject=subject
        history.username=User.objects.get(username=username)
        history.total=total
        history.correct=correct
        history.wrong=wrong
        history.percentage=percentage
        history.save()
        context={
            'total':total,
            'correct':correct,
            'wrong':wrong,
            'percentage':percentage
        }
        template=loader.get_template("result1.html")
        res=template.render(context,request)
        return HttpResponse(res)
    else:
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    
def subject2(request):
    ques=Test_paper_subject2.objects.all()
    quse_list=list(ques)
    random.shuffle(quse_list)
    quse_list=quse_list[:4:1] ###### total questions can be customized
    context={
        'quse_list':quse_list
    }
    template=loader.get_template("subject2.html")
    res=template.render(context,request)
    return HttpResponse(res)

@csrf_exempt # include  this
def result2(request):
    if request.method=='POST':
        subject='OS'
        correct=0
        total=4
        for i in range(1,7,1): # traverse total number of questions
            if ('id'+str(i)) in request.POST.keys():  
                q_id=request.POST['id'+str(i)]
                ans=request.POST['option'+str(i)]
                ques=Test_paper_subject2.objects.filter(q_id=q_id)
                if(len(ques.filter(ans=ans))):
                    correct=correct+1
        wrong=total-correct
        percentage=(correct/total)*100
        username=request.session.get('username')
        history=Test_history()
        history.username=User.objects.get(username=username)
        history.subject=subject
        history.total=total
        history.correct=correct
        history.wrong=wrong
        history.percentage=percentage
        history.save()
        context={
            'total':total,
            'correct':correct,
            'wrong':wrong,
            'percentage':percentage
        }
        template=loader.get_template("result2.html")
        res=template.render(context,request)
        return HttpResponse(res)
    else:
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    
def subject3(request):
    ques=Test_paper_subject3.objects.all()
    quse_list=list(ques)
    random.shuffle(quse_list)
    quse_list=quse_list[:4:1] ###### total questions can be customized
    context={
        'quse_list':quse_list
    }
    template=loader.get_template("subject3.html")
    res=template.render(context,request)
    return HttpResponse(res)

@csrf_exempt # include  this
def result3(request):
    if request.method=='POST':
        subject='CN'
        correct=0
        total=4 #total number of questions displayed on subject3.html
        for i in range(1,7,1): # traverse total number of questions
            if ('id'+str(i)) in request.POST.keys():  
                q_id=request.POST['id'+str(i)]
                ans=request.POST['option'+str(i)]
                ques=Test_paper_subject3.objects.filter(q_id=q_id)
                if(len(ques.filter(ans=ans))):
                    correct=correct+1
        wrong=total-correct
        percentage=(correct/total)*100
        username=request.session.get('username')
        history=Test_history()
        history.username=User.objects.get(username=username)
        history.subject=subject
        history.total=total
        history.correct=correct
        history.wrong=wrong
        history.percentage=percentage
        history.save()
        context={
            'total':total,
            'correct':correct,
            'wrong':wrong,
            'percentage':percentage
        }
        template=loader.get_template("result3.html")
        res=template.render(context,request)
        return HttpResponse(res)
    else:
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)

def test_history(request):
    username=request.session.get('username')
    history=Test_history.objects.filter(username=username)
    context={
        'history':history
    }
    template=loader.get_template("test_history.html")
    res=template.render(context,request)
    return HttpResponse(res)

def logout(request):
    del request.session['username'] #must destroy session keys
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)

def aboutUs(request):
    template=loader.get_template("about.html")
    res=template.render()
    return HttpResponse(res)


# API Key
API_KEY = 'Your API Key'

# Configure the Gemini API
ai.configure(api_key=API_KEY)

# Create a new model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# View to handle the chatbot interface
@csrf_exempt
def ChatBot(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')

        try:
            gemini_response = chat.send_message(user_input)
            response = gemini_response.text  # Get dynamic response from Gemini API
        except Exception as e:
            print(f"Gemini API error: {e}")
            response = "Sorry, I encountered an error. Please try again later."

        return JsonResponse({'response': response})

    else:
        # Render the home.html page containing the chatbot UI if it's a GET request
        return render(request, 'home.html')
