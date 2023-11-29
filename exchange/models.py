from django.db import models
from auth_cex.models import User

# Create your models here.

class Exchange(models.Model):
    _id = models.AutoField(primary_key=True)
    senders_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders_id')
    receivers_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers_id')
    amount = models.IntegerField()

    def __str__(self):
        return self.senders_id.name + " to " + self.receivers_id.name + " sended " + str(self.amount) + " INR"
    

class PermissionToSpendViaChild(models.Model):
    _id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_id')
    child_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_id')
    amount = models.IntegerField()

    def __str__(self):
        return self.parent_id.name + " give permission to " + self.child_id.name + " to spend " + str(self.amount) + " INR"
