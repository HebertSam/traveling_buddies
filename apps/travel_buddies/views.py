from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Trips
import bcrypt

# Create your views here.
def main(request):
    if 'user_id' not in request.session:
        return render(request, 'travel_buddies/index.html')
    else:
        return redirect('/travels')

def dashboard(request):
    user = Users.objects.get(id=request.session['user_id'])
    user_trips = Trips.objects.filter(user__id=request.session['user_id'])
    other_trips = Trips.objects.all().exclude(user=user)
    print other_trips

    data = {
        'user': user,
        'userTrips': user_trips,
        'otherTrips': other_trips,
    }
    return render(request, 'travel_buddies/dashboard.html', data)

def destination(request, trip_id):
    user = Users.objects.get(id=request.session['user_id'])
    trip = Trips.objects.get(id=trip_id)
    trip_users = trip.user.all()

    data = {
        'trip': trip,
        'trip_users': trip_users,
        'currentuser': user,
    }
    return render(request, 'travel_buddies/destination.html', data)

def add_trip(request):
    return render(request, 'travel_buddies/add_trip.html')

def registraton(request):
    errors = Users.objects.basic_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')

    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(name=request.POST['name'], userName=request.POST['userName'], password=password)
        user.save()
        request.session['user_id'] = user.id
        return redirect('/travels')

def login(request):
    errors = Users.objects.login(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        user = Users.objects.filter(userName=request.POST['username'])
        request.session['user_id'] = user[0].id
        return redirect('/travels')

def create_trip(request):
    errors = Trips.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travels/add')
    else:
        user = Users.objects.get(id=request.session['user_id'])
        trip = Trips.objects.create(destination=request.POST['destination'], description=request.POST['description'], date_from=request.POST['date_from'], date_to=request.POST['date_to'], primaryuser=user)
        trip.user.add(user)
        trip.save()
        return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/main')

def join(request, trip_id):
    trip = Trips.objects.get(id=trip_id)
    user = Users.objects.get(id=request.session['user_id'])
    trip.user.add(user)
    trip.save()
    return redirect('/main')