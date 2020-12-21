from django.db import models
from core import models as core_models
from users import models as user_models

# Create your models here.

class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(user_models.User, blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)
    
    def count_messages(self):
        return self.messages.count()
    count_messages.short_description = "메세지 수"

    def count_participants(self):
        return self.participants.count()
    count_participants.short_description = "참가자 수"

class Message(core_models.TimeStampedModel):
    
    message = models.TextField()
    user = models.ForeignKey(user_models.User, related_name = "messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", related_name = "messages", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} says : {self.message}'