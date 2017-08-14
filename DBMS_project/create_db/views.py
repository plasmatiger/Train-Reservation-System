from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .models import Users,Ticket,Station,Train,SeatAvailabilty,BookedTicket
from .forms import UserForm,UserRegistrationForm,search_train
import random
# Create your views here.
coach_choice =(
    ('3A', '3A'),
    ('2A', '2A'),
    ('1A', '1A'),
    ('sleeper', 'sleeper')
    )

def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        retypepassword = form.cleaned_data['retype_password']
        if len(password) < 8:
            context = {
                "form" : form,
                "error_message" : "Password length should be grater than or equal to 8",
            }
            return render(request, 'register.html' , context)
        if password != retypepassword:
            context = {
                "form" : form,
                "error_message" : "Password and retype password are not equal",
            }
            return render(request, 'register.html' , context)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                regform = UserRegistrationForm()
                context = {
                	"form" : regform,
                	"username" : username,
                	"email" : email
                }
                return render(request, 'fillUserData.html', context)
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)


def register_form(request):
    form = UserForm()
    return render(request, 'register.html', {"form" : form})


def filluserdata(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                
                Username = request.user.username
                FullName = form.cleaned_data['FullName']
                BirthDate = form.cleaned_data['BirthDate']
                Gender = form.cleaned_data['Gender']
                Email = request.user.email
                newUser = Users(UserName = User.objects.get(username=Username), FullName = FullName, BirthDate = BirthDate, Email = Email, Gender = Gender)
                newUser.save()
                #print("something")
                return render(request, 'index.html', { "username" : Username})
            else:
                regform = UserRegistrationForm()	
                context = {
                    "form" : regform,
                    "username" : request.user.username,
                    "email" : request.user.email,
                    "error_message" : "Form is invalid"
                }
                return render(request, 'fillUserData.html', context)
        return render(request, 'index.html')
    else:
        return redirect('create_db:register')


def logout_user(request):
    logout(request)
    return redirect('create_db:register')

def index(request):
    if request.user.is_authenticated():
    	#print("something")
        return render(request, 'index.html')
    else:
        return redirect('create_db:login_user')



def searching_train(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form = search_train(request.POST)
			if form.is_valid():
				source = form.cleaned_data['Source']
				destination = form.cleaned_data['Destination']
				list_of_trains = Train.objects.filter(Source = source , Destination = destination)
				return render(request, 'show_train_list.html', { "train_list" : list_of_trains })
			else:
				return redirect('create_db:search_train')
		else:
			return redirect('create_db:index')
	else:
		return redirect('create_db:index')


def booked_ticket_list(request):
	if request.user.is_authenticated():
		user = request.user.username
		booked_ticket_list_obj = BookedTicket.objects.filter(Username=user)
		return render(request, 'booked_ticket_history.html', { "ticketlist" : booked_ticket_list_obj })
	else:
		return redirect('create_db:index')


def search_train_page(request):
	form = search_train()
	return render(request, 'search_train_page.html' , { "form" : form })


def book_ticket(request):
    if request.method == 'POST':
        form = book_ticket_query(request.POST)
        if form.is_valid():
            date_of_journey = form.cleaned_data['date']
            src = form.cleaned_data['src']
            dest = form.cleaned_data['dest']
            coach = form.cleaned_data['coach']
            tot_passengers = form.cleaned_data['number_of_passengers']
            train_number = form.cleaned_data['train_number']
            name = form.cleaned_data['name']
            pnr = Ticket.objects.count()+1

            if coach == '3A':
                avail = SeatAvailabilty.objects.value_list('threeA_avail', flat=True).filter(date = date, TrainNumber = train_number)
                wait = SeatAvailabilty.objects.value_list('threeA_wait', flat=True).filter(date = date, TrainNumber = train_number)
                cost = Train.objects.value_list('base_cost', flat=True).filter(TrainNumber = train_number)
                train_name = Train.objects.value_list('TrainName', flat=True).filter(TrainNumber = train_number)
                ticket_context={
                        "train_num" :train_number,
                        "train_name" : train_name,
                        "doj" : date_of_journey,
                        "from" : src,
                        "to" : dest,
                        "coach" : coach,
                        "passenger" : name,
                        "num_of_copass" : tot_passengers,
                        "cost" : 1.5*cost
                }
                if avail > 0:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "CNF", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.dec_threeA_avail(tot_passengers)
                    return render(request, 'confirm_ticket.html', train_context)
                else:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "WL", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.inc_threeA_wait(tot_passengers)
                    return render(request, 'wait_ticket.html', train_context)


            elif coach == '2A':
                avail = SeatAvailabilty.objects.value_list('twoA_avail', flat=True).filter(date = date, TrainNumber = train_number)
                wait = SeatAvailabilty.objects.value_list('twoA_wait', flat=True).filter(date = date, TrainNumber = train_number)
                cost = Train.objects.value_list('base_cost', flat=True).filter(TrainNumber = train_number)
                train_name = Train.objects.value_list('TrainName', flat=True).filter(TrainNumber = train_number)
                ticket_context={
                        "train_num" :train_number,
                        "train_name" : train_name,
                        "doj" : date_of_journey,
                        "from" : src,
                        "to" : dest,
                        "coach" : coach,
                        "passenger" : name,
                        "num_of_copass" : tot_passengers,
                        "cost" : 2.5*cost
                }
                if avail > 0:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "CNF", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.dec_twoA_avail(tot_passengers)
                    return render(request, 'confirm_ticket.html', train_context)
                else:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "WL", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.inc_twoA_wait(tot_passengers)
                    return render(request, 'waiting_ticket.html', train_context)

            elif coach == '1A':
                avail = SeatAvailabilty.objects.value_list('oneA_avail', flat=True).filter(date = date, TrainNumber = train_number)
                wait = SeatAvailabilty.objects.value_list('oneA_wait', flat=True).filter(date = date, TrainNumber = train_number)
                cost = Train.objects.value_list('base_cost', flat=True).filter(TrainNumber = train_number)
                train_name = Train.objects.value_list('TrainName', flat=True).filter(TrainNumber = train_number)
                ticket_context={
                        "train_num" :train_number,
                        "train_name" : train_name,
                        "doj" : date_of_journey,
                        "from" : src,
                        "to" : dest,
                        "coach" : coach,
                        "passenger" : name,
                        "num_of_copass" : tot_passengers,
                        "cost" : 4*cost
                }
                if avail > 0:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "CNF", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.dec_oneA_avail(tot_passengers)
                    return render(request, 'confirm_ticket.html', train_context)
                else:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "WL", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.inc_oneA_wait(tot_passengers)
                    return render(request, 'waiting_ticket.html', train_context)

            else:
                avail = SeatAvailabilty.objects.value_list('sleeper_avail', flat=True).filter(date = date, TrainNumber = train_number)
                wait = SeatAvailabilty.objects.value_list('sleeper_wait', flat=True).filter(date = date, TrainNumber = train_number)
                cost = Train.objects.value_list('base_cost', flat=True).filter(TrainNumber = train_number)
                train_name = Train.objects.value_list('TrainName', flat=True).filter(TrainNumber = train_number)
                ticket_context={
                        "train_num" :train_number,
                        "train_name" : train_name,
                        "doj" : date_of_journey,
                        "from" : src,
                        "to" : dest,
                        "coach" : coach,
                        "passenger" : name,
                        "num_of_copass" : tot_passengers,
                        "cost" : 1.5*cost
                }
                if avail > 0:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "CNF", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.dec_sleeper_avail(tot_passengers)
                    return render(request, 'confirm_ticket.html', train_context)
                else:
                    ticket_obj = Ticket(PNR =pnr, TrainName=train_name, From=src, to=dest, DateofJourney=date_of_journey, Status= "WL", Cost= cost, No_of_passengers=tot_passengers , coach= coach,pass1 = name)
                    ticket_obj.save()
                    train_seat = SeatAvailabilty.objects.filter(date = date, TrainNumber = train_number)
                    train_seat.inc_sleeper_wait(tot_passengers)
                    return render(request, 'waiting_ticket.html', train_context)
