from django import forms
from django.contrib.auth.models import User
import datetime
from django.forms.extras.widgets import SelectDateWidget
from .models import Users,Ticket,Station,Train,SeatAvailabilty

choice = (
	('M', 'M'),
	('F', 'F'),
	)
coach_choice =(
	('3A', '3A'),
	('2A', '2A'),
	('1A', '1A'),
	('sleeper', 'sleeper'),
	)
class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserRegistrationForm(forms.ModelForm):
	Gender = forms.ChoiceField(choices=choice, required=True)
	#BirthDate = forms.DateField(widget=SelectDateWidget)
	class Meta:
		model = Users
		fields = ['FullName' , 'BirthDate' ]


#searching trains
class search_train(forms.ModelForm):
	date = forms.DateField()
	class Meta:
		model = Train
		fields = [ 'Source' , 'Destination' ]


class book_seat_query(forms.ModelForm):
	date = forms.DateInput()
	src = forms.CharField(error_messages={'required': 'Please enter your source'})
	dest = forms.CharField(error_messages={'required': 'Please enter your destination'})
	coach = forms.ChoiceField(choices =coach_choice, error_messages={'required': 'Please enter your coach'})
	number_of_passengers = forms.IntegerField(min_value=0, error_messages={'required': 'Please enter number of passengers'})
	train_number = forms.IntegerField(error_messages={'required': 'Please enter train number which you want to travel'})
	name = forms.CharField(error_messages={'required': 'Please enter your name'})
	

