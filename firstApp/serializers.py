from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer): # ModelSerializer(middelware entre les models 
    class Meta:
        model = Student
        fields = ["first_name","last_name","email","age","is_active"] 
        
        # en read all les feild 
        #fields = "__all__" # get all fields
        read_anly_fields = ["id"] # variable : read_anly_fields(c'est un attribut)
    
    # les  validateurs en(email) sous forme des fonctions et self : pour accedée les fonstion ou les variable
    def validate_email(self,value): # function : validator_email( c'est un methode) 
        """
        Custom validations for email field. 
        this runs during both create and update operations        
        """
        # check if we're updating an existing instance ==> instance ==  row in table(ligne entre le table)
        if self.instance:
            
            # for update: if email is changed, check if exists for other sttudents
            # <==> en verifié si méme email en create et en verifié email en create d'autre student 
            if self.instance.email != value: # on ligne en check your email not a value  
                if Student.objects.filter(email=value).exists(): # si email est existe (filter ==> get())
                    raise serializers.ValidationError('A student with email already exists.')
        else:
            #for creates: check if email exist for any student 
            if Student.objects.filter(email=value).exists():
                raise serializers.ValidationError('A student with email already exists.')
        
        return value
    
    # validateur en age
    def validate_age(self, value):
        """ 
        Custom validation for age field.
        """
        if value < 1 or value > 120:
            raise serializers.ValidationError('Age must be between 1 and 120')
        
        return value 
    
            
            
    
            
                    
                
        
        