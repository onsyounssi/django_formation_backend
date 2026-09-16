from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100) # ==> VARCHAR(100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # @ include in email  (la validateur de @ en email)
    age = models.PositiveIntegerField() # age always > 0 # ==> int #(age un entier et  valeur positif) 
    is_active = models.BooleanField(default=True) # bool obligatoire default
    created_at= models.DateTimeField(auto_now_add=True) # par default creaction un student en date et le time
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    