
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Insert test data
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        ]
        teams = [
            {"name": "Marvel", "members": ["Iron Man", "Captain America", "Spider-Man"]},
            {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        activities = [
            {"user": "Iron Man", "activity": "Running", "duration": 30},
            {"user": "Batman", "activity": "Cycling", "duration": 45},
        ]
        leaderboard = [
            {"team": "Marvel", "points": 300},
            {"team": "DC", "points": 250},
        ]
        workouts = [
            {"user": "Spider-Man", "workout": "Push-ups", "reps": 50},
            {"user": "Wonder Woman", "workout": "Squats", "reps": 40},
        ]

        for user in users:
            User.objects.create(**user)
        for team in teams:
            Team.objects.create(name=team["name"], members=team["members"])
        for activity in activities:
            Activity.objects.create(**activity)
        for entry in leaderboard:
            Leaderboard.objects.create(**entry)
        for workout in workouts:
            Workout.objects.create(**workout)

        # Create unique index on email using pymongo
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client["octofit_db"]
        db.user.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
