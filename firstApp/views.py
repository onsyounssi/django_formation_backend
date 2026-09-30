# from django.http import JsonResponse 
# from django.views.decorators.csrf import csrf_exempt
# from firstApp.models import Student
# import json


# # Create your views here.
# # CRUD 1/ R <==> read ==> rest api ==> GET
# @csrf_exempt
# def get_students(request):
#     if request.method == "GET":
#         students = Student.objects.all() # select * from students
#         # convert to list of dictionnaries (liste)
#         print({"students":students})
#         students_list =[]
#         for student in students:
#             print({"students":student.last_name})
#             students_list.append({
#                 "id": student.id,
#                 "first_name":student.first_name,
#                 "last_name":student.last_name,
#                 "email" : student.email,
#                 "age":student.age,
#                 "is_active" : student.is_active
#             })
#          #return JsonResponse({"students": students},status=200)   
#         return JsonResponse({"students": students_list, "count": len(students_list)},status=200)
#     return JsonResponse({"error":"Methode not allowed"},status=405)

# # @CSRF : base un token fayk pour la communication entre les brawser (postman) et les api django 
# @csrf_exempt

# def get_student(request,student_id):
#     if request.method == "GET":
#         try:
#             student = Student.objects.get(id=student_id) # select * from student where id=student_id
#         except Exception  as e :
#             print({"msg_error": str(e)})
#             return JsonResponse({"error": "student not exist"}, status=404) 
#         #  reformulation les données 
#         student_data={
#             "id": student.id,
#             "first_name": student.first_name,
#             "last_name": student.last_name,
#             "age": student.age,
#             "email": student.email,
#             "is_active": student.is_active
#         }
#         return JsonResponse({"student": student_data},  status=200)
#     return JsonResponse({"error":"Method not allowed"}, status=405)


# # CRUD 2/ c <==> Create ==> rest api ==> POST
# @csrf_exempt
# def create_student(request):
#     # loads les information de creation à travers l'utelisateur sous format json pour en executer fasillement
#     # à la bas return de type byte 
#     if request.method == "POST":
#         print({"request.body":request.body}) # en aff de type binaire 
#         print({type(request.body)})
#         data = json.loads(request.body);
#         print({"data":data}) # aff le meme creation dans le api de create in postman
#         print({"age": data["age"]}) # aff le 
#         print({"email": data["email"]}) #return JsonResponse({"msg":"msg"}, status=200)
        
#         #validate required fields
#         required_fields = ['age','first_name','last_name','email']
#         for field in required_fields:
#             if field not in data:
#                 return JsonResponse({"error": f"Missing field {field}"}, status=400)
        
#         # create student
#         student = Student.objects.create(
#                 first_name=data['first_name'],
#                 last_name=data['last_name'],
#                 email=data['email'],
#                 age=data['age'],
#                 is_active=data.get('is_active',True) 
#             )
#         """ 
#         INSORT INTO student (first_name, last_name, email, age, is_active)
#         VALUES(data["first_name"],data["last_name"],data["email"],data["age"],data["is_active"]);
#         """
        
#         student_data = {
#             "id" : student.id,
#             "first_name" : student.first_name,
#             "last_name" : student.last_name,
#             "email" : student.email,
#             "age" : student.age,
#             "is_active" : student.is_active,
#         }
#         return JsonResponse({"student": student_data}, status=201)
#     return JsonResponse({"error":"Method not allowed"}, status=405)


# # CRUD 3/ U <==> Update ==> rest api ==> PUT  or PATCH 
# # put : en envoiyer tous data <==> en entre tous les donnes et le retour en modifier seule les données necessaire(si en le modifier)
# # patch : en envoyer seullement les cas en modifier 
# # decorateur en : @
# @csrf_exempt
# def update_student(request,pk):
#     if request.method == "PUT":
#             data =json.loads(request.body)
#             try:
#                 student = Student.objects.get(id=pk)
#             except Exception :
#                 return JsonResponse({"error" : "student not exist"}, status=404)
            

#             # update only porovided fields:
#             if 'first_name' in data:
#                 student.first_name = data['first_name']
#             if 'last_name' in data:
#                 student.last_name = data['last_name']
#             if 'email' in data:
#                 student.email = data['email']
#             if 'age' in data:
#                 student.age = data['age']
#             if 'is_active' in data:
#                 student.is_active = data['is_active']
                
#             student.save()  
#             """
#             UPDATE student SET
#             first_name=new_first_name, last_name=new_last_name, email=new_email , age=new_age , is_active=new_is_active 
#             where id=pk
#             """
#             return JsonResponse({"message":"student update successfully"}, status=200)       
    
#     return JsonResponse({"error":"Method not allowed"}, status=405)            
                                                        
# # CRUD 4/ D <==> delete ==> rest api ==> Delete
# @csrf_exempt
# def delete_student(request,sttudent_id):
#     if request.method == "DELETE":
#         try:
#             studente=Student.objects.get(id=sttudent_id)
#         except Exception:
#             return JsonResponse({"message": "student not exist"}, status=404)
        
#         studente.delete()
#         return JsonResponse({"message" :" student delleted successfuly"}, status=200)
#     return JsonResponse({"error":"Method not allowed"},status=405)


from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from firstApp.models import Student
from firstApp.serializers import StudentSerializer
import json 

@csrf_exempt
@require_http_methods(["GET"])
def get_students(request):
    """GET : list all students """
    students =Student.objects.all()
    serializer =StudentSerializer(students, many=True) #  any=true :si que plusieur students
    return JsonResponse({"students": serializer.data, "count": len(serializer.data)}, status=200)

@csrf_exempt
@require_http_methods(["GET"])
def get_student(request, pk):
    """Get: retrieve a student"""
    try:
        student = Student.objects.get(id= pk)
        serializer = StudentSerializer(student)
        return JsonResponse({"student": serializer.data},status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "student not found"},status=404)
    
@csrf_exempt
@require_http_methods(['POST']) # decorateur pour le methode est verifier 
def create_Student(request):
    """POST : create a new student"""
    json_data = json.loads(request.body)
    serializer = StudentSerializer(data=json_data)
    if serializer.is_valid():
        # si student is valide 
        student = serializer.save()
        student_data = StudentSerializer(student).data
        
        return JsonResponse({
            "message": "student created sucessfully",
            "student": student_data
            }, status= 201)
    # le msg d'erreure sur les validateur en verifier dans le fichier serializer
    return JsonResponse({"error": serializer.errors}, status= 400)

@csrf_exempt
@require_http_methods(['PUT','PATCH'])
def update_student(request, student_id):
    """PUT/PATCH : update a student """
    data =json.loads(request.body)
    try:
        student= Student.objects.get(id=student_id)
    except Student.DoesNotExist :
        return JsonResponse({"error": "student not found"}, status=404)
    
    update_serializer = StudentSerializer(student, data=data)
    
    if update_serializer.is_valid():
        students =update_serializer.save()
        student_data =StudentSerializer(students).data
        return JsonResponse({
            "message": "student update successfuly",
            "student": student_data}, 
            status=200)
    return JsonResponse({"error": update_serializer.errors},status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request, sttudent_id):
    """DELETE: deleted a student"""
    try:
        student = Student.objects.get(id=sttudent_id)
        student.delete()
        return JsonResponse({"message": "student deleted successfully"}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error":"student not found"},status=404)