from django.core.management.base import BaseCommand

class Command:
    help = "this command tells me she loves me"
    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many times do you wnat me to tell you that I love you?",)
    
    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            print("i love you")