from django.db import models

class UserData(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=50)

    
    def __str__(self):
        return self.name

class ChatMessages(models.Model):
    MESSAGE_TYPES = (
        ('sent', 'Sent'),
        ('received', 'Received'),
    )
    user = models.ForeignKey(UserData,on_delete=models.CASCADE,related_name='messages')
    message_type = models.CharField(max_length=100,choices=MESSAGE_TYPES)
    content = models.TextField()
       
    def __str__(self):
        return f"{self.user.name} - {self.message_type} - {self.content[:50]}"

