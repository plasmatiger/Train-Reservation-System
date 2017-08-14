from django.db import models
#from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Permission, User


class Users(models.Model):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
	)

	UserName = models.ForeignKey(User, on_delete=models.CASCADE,default = 1)
	FullName = models.CharField(max_length=50)
	BirthDate = models.DateField()
	Email = models.EmailField()
	Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

	def __str__(self):
		return self.FullName


class Station(models.Model):
	StationCode = models.CharField(max_length=5, unique=True, null = False)
	StationName = models.CharField(max_length=25)
	City = models.CharField(max_length=20)

	def __str__(self):
		return self.StationName

class Train(models.Model):
	Type = models.CharField(max_length=2)
	TrainName = models.CharField(max_length=20)
	TrainNumber = models.IntegerField(unique=True, null = False)
	Source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name = "source")
	Destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name = "destination")
	base_cost = models.PositiveIntegerField()
	
	def __str__(self):
		return self.TrainName


class Ticket(models.Model):
	coach_choice =(
    ('3A', '3A'),
    ('2A', '2A'),
    ('1A', '1A'),
    ('sleeper', 'sleeper'),
    )
	PNR = models.PositiveIntegerField(unique=True, null = False)
	TrainName = models.ForeignKey(Train,on_delete=models.CASCADE)
	From = models.ForeignKey(Station, related_name="fromm")
	to = models.ForeignKey(Station,related_name="to")
	DateofJourney = models.DateField()
	Status = models.CharField(max_length=10)
	Cost = models.PositiveIntegerField()
	No_of_passengers = models.PositiveIntegerField( )
	coach= models.CharField(max_length=10,choices=coach_choice)
	#passangers = models.ArrayField(models.CharField(max_length=20, blank = True), size = 6,)
	pass1 = models.CharField(max_length=20, blank = False)
	
	def __str__(self):
		return self.PNR


class SeatAvailabilty(models.Model):
	TrainNumber = models.ForeignKey(Train, on_delete=models.CASCADE)
	threeA_avail = models.IntegerField()
	threeA_wait = models.IntegerField()
	twoA_avail = models.IntegerField()
	twoA_wait = models.IntegerField()
	oneA_avail = models.IntegerField()
	oneA_wait = models.IntegerField()
	sleeper_avail = models.IntegerField()
	sleeper_wait = models.IntegerField()
	date = models.DateField()


	def dec_threeA_avail(self, number_of_pass):
		self.threeA_avail -= number_of_pass
		self.save()

	def dec_twoA_avail(self, number_of_pass):
		self.threeA_avail -= number_of_pass
		self.save()

	def dec_oneA_avail(self, number_of_pass):
		self.threeA_avail -= number_of_pass
		self.save()

	def dec_sleeper_avail(self, number_of_pass):
		self.threeA_avail -= number_of_pass
		self.save()

	def inc_threeA_wait(self, number_of_pass):
		self.threeA_avail += number_of_pass
		self.save()

	def inc_twoA_wait(self, number_of_pass):
		self.threeA_avail += number_of_pass
		self.save()

	def inc_oneA_wait(self, number_of_pass):
		self.threeA_avail += number_of_pass
		self.save()

	def inc_sleeper_wait(self, number_of_pass):
		self.threeA_avail += number_of_pass
		self.save()



class BookedTicket(models.Model):
 	Username = models.ForeignKey(Users,on_delete=models.CASCADE,default = 1)
 	ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)