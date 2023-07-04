
from django.shortcuts import render,redirect,get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from datetime import date,timedelta
from django.core.mail import send_mail
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from corsheaders.decorators import cors_allow_all_origin
from django.contrib.auth.hashers import make_password, check_password
# from .serializers import doctorserializer,hospitalserializer,patientserializer
from .models import hospital,doctor,patient,appointments,bookedappointments,Admin,pending_doctors
from .forms import DoctorForm , PatientForm ,HospitalForm
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.conf import settings 


def hospital_list(request):
    hospitals = hospital.objects.all()
    return render(request, 'hospital_list.html', {'hospitals': hospitals})

def hospital_add(request):
    if request.method == "POST":
        form = HospitalForm(request.POST)
        if form.is_valid():
            my_hospital = form.save(commit=False)
            my_hospital.save()
            messages.success(request,'Successfully added hospital')
            return redirect('hospital_list')
    else:
        form = HospitalForm()
    return render(request, 'hospital_add.html', {'form': form})

def hospital_edit(request):#, pk):
    # my_hospital = hospital.objects.filter(id=request.GET.get('id')) 
    my_hospital = hospital.objects.get(id=request.GET.get('id'))
    # my_hospital = get_object_or_404(hospital, pk=pk)
    if request.method == "POST":
        form = HospitalForm(request.POST, instance=my_hospital) #########
        if form.is_valid():
            my_hospital = form.save(commit=False)
            my_hospital.save()
            messages.success(request,'Successfully edited hospital details')
            return redirect('hospital_list')
    else:
        # form = HospitalForm(instance=hospital)
        form = HospitalForm(instance=my_hospital)
    return render(request, 'hospital_edit.html', {'form': form})

def hospital_remove(request):#, pk):
    my_hospital = hospital.objects.filter(id=request.GET.get('id'))
    # my_hospital = get_object_or_404(hospital, pk=pk)
    my_hospital.delete()
    messages.success(request,'Successfully deleted hospital')
    return redirect('hospital_list')

@csrf_exempt

def homepage(request):
    alert=True
    return render(request,'homePage.html',{'alert':alert}) 

def get_hospitals_list(request):
    queryset = hospital.objects.all()
    hospitals_list = [{'id': obj.id,'name':obj.name,'email':obj.email,'address':obj.address,'phone_number':obj.phone_number,'description':obj.description,'pincode':obj.pincode} for obj in queryset]
    return render(request,'get_hospitals_list.html',{'hospitals_list':hospitals_list})

def addnewdoctor(request):
    # if request.method == 'POST':
    #     name=request.POST.get('name')
    #     gender=request.POST.get('gender')
    #     email=request.POST.get('email')
    #     # password=request.POST.get('password')
    #     hashed_password = make_password(request.POST.get('password'))
    #     phone=request.POST.get('phone')
    #     address=request.POST.get('address')
    #    # pincode=request.POST.get('pincode')
    #     age=request.POST.get('age')
    #     specialization=request.POST.get('specialization')
    #     experience=request.POST.get('experience')
    #     #pincode=request.POST.get('pincode')
    #     hospital_id = request.POST.get('hospital')
    #     my_hospital = hospital.objects.get(pk=hospital_id)
    #     context = {'my_hospital': my_hospital}
    #     # hospitalid=request.POST.get('hospitalid')
    #     #slotlist=request.POST.get('slotlist') 
    #     #certificate=request.POST.get('certificate')
    #     newdoctor=pending_doctors(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,specialization=specialization,experience=experience,age=age,hospitalid=my_hospital.id,pincode=my_hospital.pincode)
    #     newdoctor.save()
    #     # response_data = {'success': 'Data was successfully saved.'}
    #     # # Return the response as a JSON-encoded string
    #     # return JsonResponse(response_data)
    #     # return render(request,'')
    #     # result = { 'name' : name , 'email' : email }
    #     # print(name + " " + newdoctor('id'))
    #     # my_dict = {'name': name, 'id': newdoctor.id }
    #     # request.session['my_dict'] = my_dict 
    #     request.session['my_dict.name'] = newdoctor.name
    #     request.session['my_dict.id'] = newdoctor.id 

    #     request.session['my_dict.specialization'] = newdoctor.specialization
    #     request.session['my_dict.hospitalid'] = newdoctor.hospitalid 

    #     # return render(request, 'add_doctor.html', {'result': result})
    #     messages.success(request, 'Your account has been created successfully!,wait for admin approval')
    #     return redirect('/afterloginpage/') 
    #     # return render(request,'add_doctor.html')

    # else:
    #     # If an error occurs, return an error response
    #     # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
    #     # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
    #     # return redirect('/')
    #     return render(request,'add_doctor.html') 
    if request.method == 'POST':
        x = 0 
        if request.POST.get('password') == request.POST.get('p2') :
            x = 1 
        hashed_password = make_password(request.POST.get('password'))
        hashed_p2 = make_password(request.POST.get('p2'))
        if hashed_password == hashed_p2 : 
            x = 1
        if x == 0 :
            messages.error(request, 'Passwords didnot match ') 
            return redirect('/addnewdoctor/') 
        name=request.POST.get('name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        # password=request.POST.get('password') 
        phone=request.POST.get('phone')
        address=request.POST.get('address')
       # pincode=request.POST.get('pincode')
        age=request.POST.get('age')
        specialization=request.POST.get('specialization')
        experience=request.POST.get('experience')
        # pdf_file = request.POST.get('pdf_file') 
        # pdf_file = request.FILES['pdf_file'].read()
        #pincode=request.POST.get('pincode')
        hospital_id = request.POST.get('hospital')
        my_hospital = hospital.objects.get(pk=hospital_id)
        context = {'my_hospital': my_hospital}

        if pending_doctors.objects.filter(email=email).exists():
            messages.error(request, 'This email already exists.')
            return redirect('/addnewdoctor/') 

        # if form.is_valid():
        #     print("Form is valid ") 
        # else : 
        #     messages.error(request, 'This username already exists.')
        #     return redirect('/addnewdoctor/') 
        
        newdoctor=pending_doctors(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,specialization=specialization,experience=experience,age=age,hospitalid=my_hospital.id,pincode=my_hospital.pincode)#,pdf_file=pdf_file)
        newdoctor.save()
        # response_data = {'success': 'Data was successfully saved.'}
        # # Return the response as a JSON-encoded string
        # return JsonResponse(response_data)
        # return render(request,'')
        # result = { 'name' : name , 'email' : email }
        # print(name + " " + newdoctor('id'))
        # my_dict = {'name': name, 'id': newdoctor.id }
        # request.session['my_dict'] = my_dict 
        request.session['my_dict.name'] = newdoctor.name
        request.session['my_dict.id'] = newdoctor.id 

        request.session['my_dict.specialization'] = newdoctor.specialization
        request.session['my_dict.hospitalid'] = newdoctor.hospitalid 

        # return render(request, 'add_doctor.html', {'result': result})
        messages.success(request, 'Your account has been created successfully!')
        messages.success(request, 'Wait for admin approval') 
        return redirect('/doctorlogin/') 
         # return render(request,'add_doctor.html')

    else:
        # If an error occurs, return an error response
        # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
        # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
        # return redirect('/')
        return render(request,'add_doctor.html') 



# def afterloginpage(request):
#     # print(request.name+""+request.email) 
#     info = request.session.get('my_dict.name' , 'my_dict.id') 
#     return render(request,'afterloginpage.html',{"info":info})   

def afterloginpage(request):
    name = request.session.get('my_dict.name', 'default_name')
    id = request.session.get('my_dict.id', 'default_id')
    specialization = request.session.get('my_dict.specialization', 'default_specialization')
    hospitalid = request.session.get('my_dict.hospitalid', 'default_hospitalid')
    info = {'name': name, 'id': id, 'specialization':specialization, 'hospitalid':hospitalid} 
    return render(request, 'afterloginpage.html', {"info": info})

def addnewpatient(request):
    # if request.method == 'POST':
    #     name=request.POST.get('name')
    #     gender=request.POST.get('gender')
    #     email=request.POST.get('email')
    #     # password=request.POST.get('password')
    #     hashed_password = make_password(request.POST.get('password'))
    #     phone=request.POST.get('phone')
    #     address=request.POST.get('address')
    #     pincode=request.POST.get('pincode')
    #     age=request.POST.get('age')
    #     # pincode=request.POST.get('pincode')
    #     description=request.POST.get('description') 
    #     newpatient=patient(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,age=age,description=description)
    #     newpatient.save()
    #     # response_data = {'success': 'Data was successfully saved.'}
    #     # # Return the response as a JSON-encoded string
    #     # return JsonResponse(response_data)
    #     # return render(request,'')
    #     # result = { 'name' : name , 'email' : email }
    #     # print(name + " " + newdoctor('id'))
    #     # my_dict = {'name': name, 'id': newdoctor.id }
    #     # request.session['my_dict'] = my_dict 
    #     request.session['my_dict.name'] = newpatient.name
    #     request.session['my_dict.id'] = newpatient.id
    #     # return render(request, 'add_docto
    #   
    if request.method == 'POST':
        x = 0 
        if request.POST.get('password') == request.POST.get('p2') :
            x = 1 
        hashed_password = make_password(request.POST.get('password'))
        hashed_p2 = make_password(request.POST.get('p2'))
        if hashed_password == hashed_p2 : 
            x = 1
        if x == 0 :
            messages.error(request, 'Passwords didnot match ') 
            return redirect('/addnewpatient/')  
        name=request.POST.get('name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        # password=request.POST.get('password')
        # hashed_password = make_password(request.POST.get('password'))
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        age=request.POST.get('age')
        # pincode=request.POST.get('pincode')
        description=request.POST.get('description') 
        # pdf_file = request.POST.get('pdf_file')
        # pdf_file = request.FILES['pdf_file'].read()

        if patient.objects.filter(email=email).exists():
            messages.error(request, 'This email already exists.')
            return redirect('/addnewpatient/') 
        # if form.is_valid():
        #     print("Form is valid ") 
        # else : 
        #     messages.error(request, 'This username already exists.')
        #     return redirect('/addnewdoctor/') 
        newpatient=patient(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,age=age,description=description)#,pdf_file=pdf_file)
        newpatient.save() 
        request.session['my_dict.name'] = newpatient.name
        request.session['my_dict.id'] = newpatient.id
        # return render(request, 'add_doctor.html', {'result': result})
        messages.success(request, 'Your account has been created successfully!')
        return redirect('/patientlogin/') 
        # return render(request,'add_doctor.html')

    else:
        # If an error occurs, return an error response
        # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
        # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
        # return redirect('/')
        return render(request,'add_patient.html')   




def doctorlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_doctor = doctor.objects.get(email=email) 
            if check_password(password, my_doctor.password):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['doctor_name'] = my_doctor.name
                request.session['doctor_id'] = my_doctor.id 
                messages.success(request, "Login successful" )
                return redirect('/afterdoctorlogin')
             
            else:
                # Password is incorrect, show an error message
                # ...
                print(" Incorrect Password") 
                # return redirect('/afterdoctorlogin')
                messages.error(request, "Incorrect password" ) 
                return render(request,'doctor_login.html') 
        except doctor.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            print(" Doctor with given email does not exist") 
            messages.error(request, "No account exist with given email" ) 
            return render(request,'doctor_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'doctor_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctorlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')
    return redirect('doctorlogin')

def patientlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_patient = patient.objects.get(email=email) 
            if check_password(password,my_patient.password):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['patient_id'] = my_patient.id 
                messages.success(request, "Login successful" )
                return redirect('/afterpatientlogin') 
            else:
                # Password is incorrect, show an error message
                # ...
                print(" Incorrect Password  1111") 
                messages.error(request, "Incorrect password" ) 
                               # return redirect('/afterpatientlogin') 

                return render(request,'patient_login.html') 
        except patient.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            print(" Patient with given email does not exist") 
            messages.error(request, "No account exist with given email" ) 
            return render(request,'patient_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'patient_login.html')  

def Adminlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')
    return redirect('Adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def patientlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')

    return redirect('patientlogin')

def afterpatientlogin(request):
    my_id = request.session.get('patient_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/patientlogin')
    request.session['patient_id'] = request.session.get('patient_id', 'default_id')

    my_patient = patient.objects.get(id=my_id) 
    info = {'name': my_patient.name, 'id': my_patient.id} 
    return render(request, 'after_patient_login.html', {"info": info})

def hospital_list_2(request):
    hospitals = hospital.objects.all()
    context = {'hospitals': hospitals}
    return render(request, 'add_doctor.html', context)

def afterdoctorlogin(request): 
    my_id = request.session.get('doctor_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/doctorlogin')
    d = doctor.objects.get(id=my_id)
    my_doctor = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    request.session['doctor_id'] = request.session.get('doctor_id', 'default_id')
    return render(request,'after_doctor_login.html',{'my_doctor':my_doctor})

def change_doctor_info(request):
    my_id = request.session.get('doctor_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/doctorlogin')
    d = doctor.objects.get(id=my_id)
    my_doctor = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            # doctor_id = form.cleaned_data['my_id']
            doctor_id = request.session.get('doctor_id', 'default_id')
            my_doctor = get_object_or_404(doctor, pk=doctor_id)
            form = DoctorForm(request.POST, instance=my_doctor)
            form.save()
            messages.success(request,'Successfully changed your info')
            return redirect("/afterdoctorlogin") #('/doctor_detail/')
    else:
        my_id = request.session.get('doctor_id', 'default_id') 
        d = doctor.objects.get(id=my_id)
        # my_doctor = doctor.objects.first() # Get the first doctor instance as an example
        form = DoctorForm(instance=d)
    # return render(request, 'doctor_detail.html', {'my_doctor':my_doctor,'form': form})
    return render(request, 'change_doctor_info.html', {'my_doctor': d, 'form': form})

def change_patient_info(request):
    my_id = request.session.get('patient_id', 'default_id') 
    if type(my_id)==str:
        return redirect('/patientlogin')
    p = patient.objects.get(id=my_id)
    my_patient = {'name':  p.name , 'id':p.id, 'age': p.age , 'phone_number': p.phone_number ,'email': p.email ,'address':p.address ,'description':p.description }
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # doctor_id = form.cleaned_data['my_id']
            patient_id = request.session.get('patient_id', 'default_id')
            my_patient = get_object_or_404(patient, pk=patient_id)
            form = PatientForm(request.POST, instance=my_patient)
            form.save()
            messages.success(request,'Successfully changed your info')
            return redirect("/afterpatientlogin") #('/patient_detail/')
    else:
        my_id = request.session.get('patient_id', 'default_id') 
        p = patient.objects.get(id=my_id)
        # my_doctor = doctor.objects.first() # Get the first doctor instance as an example
        form = PatientForm(instance=p)
    # return render(request, 'doctor_detail.html', {'my_doctor':my_doctor,'form': form})
    return render(request, 'change_patient_info.html', {'my_patient': p, 'form': form})

def book_appointment(request):
    # if request.method == 'POST':
    id=request.session.get('patient_id','default-value')
    if type(id)==str:
        return redirect('/patientlogin')
    print("entered with")
    print(type(id))
    # return render(request,'book_appointment.html')
    if request.method == 'POST':
        
        pincode = request.POST.get('pincode', None)
        specialization = request.POST.get('specialization', None)
    # pincode=123456
    # specialization="a"

    # ... add more fields as needed
    # hospital_ = hospital.objects.get(id=obj.hospitalid)


    # Building the queryset based on the conditions provided in the request
        queryset = doctor.objects.all()
        if pincode:
            queryset = queryset.filter(pincode=pincode)
            if not queryset:       
                messages.warning(request, f"No doctors found for pincode '{pincode}'. Please try a different pincode.")
                return redirect('/afterpatientlogin/')
        if specialization:
            queryset = queryset.filter(specialization=specialization)
            queryset1 = queryset.filter(specialization=specialization)

            if not queryset1:       
                messages.warning(request, f"No doctors found for specialization '{specialization}'. Please try a different specialization.")
                return redirect('/afterpatientlogin/')

        # Converting the queryset to a list of dicts and returning as JSON response
        doctors_list = []
        for obj in queryset:
            hospital_ = hospital.objects.get(id=obj.hospitalid)
            doctors_list.append({
                'id': obj.id,
                'name': obj.name,
            # 'email': obj.email,
                'gender': obj.gender,
            # 'phone_number': obj.phone_number,
            # 'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
            # 'age': obj.age,
                'hospital_id':obj.hospitalid,
                'hospital_name': hospital_.name,
                'hospital_address': hospital_.address
            })
        # context={'doctors_list':doctors_list}
        request.session['doctors_list'] = doctors_list
        return redirect('/select_doctor') 
    else:
        return render(request,'book_appointment.html') #,context)

def select_doctor(request):
    print("select doctor")
    if request.method == 'POST':
        print("entered if select")
        date= request.POST.get('date', '') # get the date from the query parameters
        slot= request.POST.get('slot', '') # get the id from the query parameters
        description=request.POST.get('description', '')
        appointment_preference=request.POST.get('appointment_preference', '')
        doctor_id=request.POST.get('selected_doctor_id', '')
        patient_id=request.session.get('patient_id')
        new_booking=bookedappointments(date=date,slot=slot,doctorid=doctor_id,patientid=patient_id,description=description,appointment_preference=appointment_preference,time='00:00')
        new_booking.save()
        if appointments.objects.filter(doctorid=doctor_id,date=date):
            doctor_appointments=appointments.objects.get(doctorid=doctor_id,date=date)
            if slot=="morning":
                doctor_appointments.morning.append(new_booking.bookingid)
            elif slot=="afternoon":
                doctor_appointments.afternoon.append(new_booking.bookingid)
            else :
                doctor_appointments.evening.append(new_booking.bookingid)
        else:
            doctor_appointments=appointments(doctorid=doctor_id,date=date)
            if slot=="morning":
                doctor_appointments.morning.append(new_booking.bookingid)
            elif slot=="afternoon":
                doctor_appointments.afternoon.append(new_booking.bookingid)
            else :
                doctor_appointments.evening.append(new_booking.bookingid)
        doctor_appointments.save()
        messages.success(request, f"appointment booked on '{date}' for the slot {slot}. Please wait for doctor's response mail.")
        print("beforeafter pat login")
        return redirect('/afterpatientlogin/')
    else:
        doctors_list = request.session.get('doctors_list')
        context={'doctors_list':doctors_list}
        print("else in select doctor")
        return render(request,'select_doctor.html',context)

##########################################################
def ask_doctor_date_time(request):
    if request.method == 'POST':
        my_date = request.POST.get('date','')
        slot = request.POST.get('slot','') 
        request.session['date'] = my_date
        request.session['slot'] = slot

        request.session['doctor_id'] = request.session.get('doctor_id')
        print("Exiting ask doctor function")
        return redirect('/show_appointments') 
    else:
        today = date.today().strftime("%Y-%m-%d")
        seven_days_from_now = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        selected_date = request.POST.get('date')
        context = {
            'today': today,
            'seven_days_from_now': seven_days_from_now
        }
        return render(request,'ask_doctor_date_time.html',context) 

def show_appointments(request):
    if request.method == 'POST':
        # selected_options = request.POST.getlist('option')
        # for option in selected_options:
        #     print(option) 
        doctor_id = request.session.get('doctor_id') 
        if type(doctor_id)==str:
            return redirect('/patientlogin')
        my_date = request.session.get('date') 
        slot = request.session.get('slot')
        if bookedappointments.objects.filter(doctorid=doctor_id,date=my_date,slot=slot,status='no action taken'):
            for b in bookedappointments.objects.filter(doctorid=doctor_id,date=my_date,slot=slot,status='no action taken'):
                option = request.POST.get('option_' + str(b.bookingid)) 
                time = request.POST.get('time_' + str(b.bookingid))
                msg = request.POST.get('msg_'+str(b.bookingid)) 
                  # print('Booking ID:', b.bookingid, 'Selected option:', option)
                b.status = option 
                b.time=time
                b.save()
                patientid = b.patientid 
                pat = patient.objects.get(id=patientid) 
                email = pat.email
                # print("***show appointments ****") 
                # print(time,email) 
                # print("***show appointments ****")
                # val = {
                #     'patientid' : patientid ,
                #     'email' : pat.email ,
                #     'time' : time ,
                # } 
                # print(b.status) 
                if option == 'offline':
                    # print("Entered option = offline")
                    # offline = request.session.get('offline', [])  
                    # offline.append( (time,email) ) 
                    # request.session['offline'] = offline 
                    # request.session['offline'] =request.session.get('offline',[]).append((time,email)) 
                    request.session.setdefault('offline', []).append((time,email,msg))
                elif option == 'online':
                    request.session.setdefault('online', []).append((time,email,msg))
                elif option == 'decline':
                    request.session.setdefault('decline', []).append((time,email,msg))

            request.session['my_date'] = my_date 
            request.session['slot'] = slot 
            request.session['doctor_id'] = doctor_id 
            # print("going to redirect ") 
            return redirect('/my_send_mail')  

        else:
            print("No Pending Appointments :(  :(") 
            return redirect('/afterdoctorlogin') 
    else:
        doctor_id = request.session.get('doctor_id') 
        my_date = request.session.get('date') 
        slot = request.session.get('slot') 
        inf = {
            'd' : my_date,
            's' : slot,
        }
        

        print(doctor_id , my_date , slot) 
        completed_appointments = bookedappointments.objects.filter(doctorid=doctor_id,date=my_date,slot=slot).exclude(status='no action taken')

        if bookedappointments.objects.filter(doctorid=doctor_id,date=my_date,slot=slot):
            b = bookedappointments.objects.filter(doctorid=doctor_id,date=my_date,slot=slot,status='no action taken')
            return render(request,'show_appointments.html',{'b':b, 'completed_appointments':completed_appointments , 'inf':inf})
        else:
            print("No appointments :( ") 
            return redirect('/afterdoctorlogin') 

def my_send_mail(request):
    offline_patients = request.session.get('offline') 
    online_patients = request.session.get('online') 
    decline_patients = request.session.get('decline') 

    # print("Entered my_send_mail : ") 

    if offline_patients:
        # print("Entered if: ")
        for time,email,msg in request.session.get('offline') :
            # print("OFFLINE SENDING")
            # time = p['time']  # access the 'time' attribute of the dictionary
            # email = p['email']
            # time = p[0]
            # email = p[1] 
            subject = 'OMCS Confirmation'
            message = 'Your offline appointment is confirmed at ' + time + ('. Doctor message : ' + msg if msg != '' else '' )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email] 
            # print("******")
            # # print(p) 
            # print(settings.DEFAULT_FROM_EMAIL)
            # print(recipient_list) 
            # print(time) 
            # print("******")
        
            send_mail(subject, message, from_email, recipient_list)
    
    if online_patients:
        for time,email,msg in request.session.get('online') :
            subject = 'OMCS Confirmation'
            message = 'Your online appointment is confirmed at ' + time + ('. Doctor message : ' + msg if msg != '' else '')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]      
            send_mail(subject, message, from_email, recipient_list)

    if decline_patients:
        for time,email,msg in request.session.get('decline') :
            subject = 'OMCS Declination' 
            message = 'Sorry! Your appointment is declined'+ ('. Doctor message : ' + msg if msg != '' else '')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email] 
            send_mail(subject, message, from_email, recipient_list)

    request.session.pop('offline', None)
    request.session.pop('online', None)
    request.session.pop('decline', None) 
    return redirect('/afterdoctorlogin') 



# def change_doctor_info(request):
#     return render(request,'doctor_detail.html',{'my_doctor':my_doctor})

# def doctor_detail(request):
#     if request.method == 'POST':
#         form = DoctorForm(request.POST)
#         if form.is_valid():
#             doctor_id = form.cleaned_data['doctor_id']
#             my_doctor = get_object_or_404(doctor, pk=doctor_id)
#             form = DoctorForm(request.POST, instance=my_doctor)
#             form.save()
#             return HttpResponseRedirect('/doctor_detail/')
#     else:
#         my_doctor = doctor.objects.first() # Get the first doctor instance as an example
#         form = DoctorForm(instance=my_doctor)
#     return render(request, 'doctor_detail.html', {'form': form})

def show_doctor_info(request):
    my_id = request.session.get('doctor_id', 'default_id')
    if type(my_id)==str:
       return redirect('/doctorlogin') 
    d = doctor.objects.get(id=my_id)
    my_doctor = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    form = DoctorForm(instance=d)
    return render(request, 'show_doctor_info.html', {'my_doctor': d, 'form': form})

def show_patient_info(request):
    my_id = request.session.get('patient_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/patientlogin')
    d = patient.objects.get(id=my_id)
    my_patient = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'description':d.description }
    form = PatientForm(instance=d)
    return render(request, 'show_patient_info.html', {'my_patient': d, 'form': form})

# @csrf_exempt
# @cors_allow_all_origin
# def change_doctor_info(request):
#     id = request.POST.get('id', '') # get the id from the query parameters
#     doctor=get_object_or_404(doctor,id=id)
#     if not doctor:
#         return JsonResponse({'error': f"No doctor found with id '{id}'."})
#     for key in request.POST:
#         if key != 'id':
#             setattr(doctor, key, request.POST.get(key))
#     doctor.save()
#     return JsonResponse({'success': f"doctor with ID '{id}' updated successfully."})

# @csrf_exempt
# @cors_allow_all_origin

# def get_doctors_list(request):
#     # # Retrieve the query parameters from the request
#     # pincode = request.POST.get('pincode', None)
#     # specialization = request.POST.get('specialization', None)
#     # ... add more fields as needed


#     # Building the queryset based on the conditions provided in the request
#     queryset = doctor.objects.all()
#     # if pincode:
#     #     queryset = queryset.filter(pincode=pincode)
#     #     if not queryset:       
#     #         return JsonResponse({'message': 'No doctors found based on your location '})

#     # if specialization:
#     #     queryset = queryset.filter(specialization=specialization)
#     #     queryset1 = queryset.filter(specialization=specialization)

#     #     if not queryset1:       
#     #         return JsonResponse({'message': 'No doctors found with given specialization in your location.'})

#     #     # Converting the queryset to a list of dicts and returning as JSON response

#     objects_list = [{'id': obj.id,'name':obj.name,'email':obj.email,'gender':obj.gender,'phone_number':obj.phone_number,'address':obj.address,'specialization':obj.specialization,'experience':obj.experience,'age':obj.age,'hospitalid':obj.hospitalid} for obj in queryset]
#     return JsonResponse({'objects': objects_list})

# @csrf_exempt
# @cors_allow_all_origin
# def show_appointments(request):
#     # id = request.POST.get('id', None)
#     # date = request.POST.get('date', None)   
#     # appointmentslist=appointments.objects.get(id=id,date=date)

#     # morningappointments=appointmentslist.morning
#     # afternoonappointments=appointmentslist.afternoon
#     # eveningappointments=appointmentslist.evening
#     # data={
#     #     'morningappointments':morningappointments,
#     #     'afternoonappointments':afternoonappointments,
#     #     'eveningappointments':eveningappointments
#     # }
#     queryset = appointments.objects.all()
#     obj_list=[{'morningappointments': obj.morningtoken ,'afternoonappointments': obj.afternoontoken,'eveningappointments': obj.eveninggtoken}for obj in queryset]
#     return JsonResponse(obj_list)


# @csrf_exempt
# @cors_allow_all_origin
# def approve_appointment(request):
#     # Retrieve the query parameters from the request
#     bookingid = request.POST.get('bookingid', None)
#     date = request.POST.get('date', None)
#     patientid=request.POST.get('patientid',None)
#     doctorid=request.POST.get('doctorid',None)
#     description=request.POST.get('description',None)
#     status=request.POST.get('status',None)
#     patient=patient.objects.get(id=patientid)
#     if status=='confirm' :
#         subject = 'Your Subject Here'
#         message = f'Hello {patient.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about appointment confirmation
#         from_email = 'your-email@example.com'
#         recipient_list = [patient.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     elif status=='decline':
#         subject = 'Your Subject Here'
#         message = f'Hello {patient.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about declination
#         from_email = 'your-email@example.com'
#         recipient_list = [patient.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     elif status=='online consultation':
#         subject = 'Your Subject Here'
#         message = f'Hello {patient.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about online consultation
#         from_email = 'your-email@example.com'
#         recipient_list = [patient.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     # morning_no_of_appointments=request.POST.get('morning', None)
#     # afternoon_no_of_appointments=request.POST.get('afternoon', None)
#     # evening_no_of_appointments=request.POST.get('evening', None)
#     # if date< date.today():
#     #     error_message = {'error': 'you cannot approve an appointment on past dates.'}
#     #     return JsonResponse(error_message, status=400)
#     # elif appointments.objects.filter(id=id,date=date).exists():
#     #     appointmentslist=appointments.objects.get(id=id,date=date)
#     #     i=0
#     #     while i<=morning_no_of_appointments and i<=len(appointmentslist.morning):
#     #         id=appointmentslist.morning[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about appointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.morning):
#     #         id=appointmentslist.morning[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     i=0
#     #     while i<=afternoon_no_of_appointments and i<=len(appointmentslist.afternoon):
#     #         id=appointmentslist.afternoon[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about apointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.afternoon):
#     #         id=appointmentslist.afternoon[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     i=0
#     #     while i<=evening_no_of_appointments and i<=len(appointmentslist.evening):
#     #         id=appointmentslist.evening[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about apointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.evening):
#     #         id=appointmentslist.evening[i]
#     #         patient_=patient.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {patient_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [patient_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     return JsonResponse({'message': 'mails sent for confirmation and declination for 3 slots respectively'})

#     # else:
#     #     return JsonResponse({'message': 'No appointments for you on the given date'})


# # @csrf_exempt
# # @cors_allow_all_origin

# # def addnewpatient(request):
# #     try:
# #         name=request.POST.get('name')
# #         gender=request.POST.get('gender')
# #         email=request.POST.get('email')
# #         phone=request.POST.get('phone')
# #         address=request.POST.get('address')
# #         pincode=request.POST.get('pincode')
# #         age=request.POST.get('age')
# #         description=request.POST.get('description')
# #         newpatient=patient(name=name,email=email,gender=gender,phone_number=phone,address=address,description=description,pincode=pincode,age=age)
# #         newpatient.save()
# #         # response_data = {'success': 'Data was successfully saved.'}
# #         # Return the response as a JSON-encoded string
# #         # return JsonResponse(response_data)
# #         return redirect('/')

# #     except Exception as e:
# #         # If an error occurs, return an error response
# #         response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
# #         return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')

# # @csrf_exempt
# # @cors_allow_all_origin


# # @csrf_exempt
# # @cors_allow_all_origin

# # def change_patient_info(request):
# #     id = request.POST.get('id', '') # get the id from the query parameters
# #     patient=get_object_or_404(patient,id=id)
# #     if not patient:
# #         return JsonResponse({'error': f"No patient found with id '{id}'."})
# #     for key in request.POST:
# #         if key != 'id':
# #             setattr(patient, key, request.POST.get(key))
# #     patient.save()
# #     return JsonResponse({'success': f"patient with ID '{id}' updated successfully."})

# #################################check below class

# # @csrf_exempt
# @cors_allow_all_origin
# def new_appointment(request):
#     id = request.POST.get('id', '') # get the id from the query parameters
#     date= request.POST.get('date', '') # get the date from the query parameters
#     slot= request.POST.get('slot', '') # get the id from the query parameters
#     description=request.POST.get('description', '')
#     if date< date.today():
#             error_message = {'error': 'you cannot book an appointment on past dates.'}
#             return JsonResponse(error_message, status=400)

#     elif appointments.objects.filter(id=id,date=date).exists():
#         appointmentslist=appointments.objects.get(id=id,date=date)
#         if (slot=='morning'):
#             appointmentslist.morning.append(id)
#             return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
        
#         elif slot=='afternoon':
#             if len(appointmentslist.afternoon)<10:
#                 appointmentslist.afternoon.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='evening'):
#             if len(appointmentslist.evening)<10:
#                 appointmentslist.evening.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#     else:
#         appointmentslist=appointments(id=id,date=date)
#         if (slot=='morning'):
#             if len(appointmentslist.morning)<10:
#                 appointmentslist.morning.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='afternoon'):
#             if len(appointmentslist.afternoon)<10:
#                 appointmentslist.afternoon.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='evening'):
#             if len(appointmentslist.evening)<10:
#                 appointmentslist.evening.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from doctor'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})


def Adminlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_Admin = Admin.objects.get(email=email) 
            if check_password(password, make_password(my_Admin.password)):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['my_id'] = my_Admin.id
                # context={'doctors_list':doctors_list}
                messages.success(request,'Succesfully logged in!') 
                return redirect('/afterAdminlogin')
             
            else:
                # Password is incorrect, show an error message
                # ...
                messages.error(request,'Incorrect password!')
                print(" Incorrect Password") 
                # return redirect('/afterdoctorlogin')

                return render(request,'Admin_login.html') 
        except Admin.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            messages.error(request,'No account exists with given email!')
            print(" Admin with given email does not exist") 
            return render(request,'Admin_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'Admin_login.html')

def afterAdminlogin(request):

    my_id = request.session.get('my_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Adminlogin')
    print("Entered after admin login")
    if request.method=='POST':
        print("Entered if")
        return redirect('Adminlogin')
    else:
        print("Entered else")
        my_id = request.session.get('my_id', 'default_id') 
        request.session['my_id'] = my_id

        pending_doctors_=pending_doctors.objects.all()
        pending_doctors_list = []
        for obj in pending_doctors_:
            # pending_doctor = pending_doctors.objects.get(id=obj.id)
            pending_doctors_list.append({
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'gender': obj.gender,
                'password': obj.password,
                'phone_number': obj.phone_number,
                'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
                'age': obj.age,
                'pincode': obj.pincode,
                'hospital_id':obj.hospitalid,
                'isdelete':obj.isdelete
                ########################certificate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            })
        my_Admin = Admin.objects.get(id=my_id) 
        info = {'name': my_Admin.name, 'id': my_Admin.id, 'pending_doctors_list': pending_doctors_list} 
        return render(request, 'after_Admin_login.html', {"info": info})
    # else:


def show_pending_doctors(request):
    my_id = request.session.get('my_id', 'default_id') 
    if type(my_id)==str:
        return redirect('/Adminlogin')
    print("Entered after admin login")
    if request.method=='POST':
        print("Entered if")
        return redirect('Adminlogin')
    else:
        print("Entered else")
        my_id = request.session.get('my_id', 'default_id') 
        request.session['my_id'] = my_id

        pending_doctors_=pending_doctors.objects.all()
        pending_doctors_list = []
        for obj in pending_doctors_:
            # pending_doctor = pending_doctors.objects.get(id=obj.id)
            pending_doctors_list.append({
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'gender': obj.gender,
                'password': obj.password,
                'phone_number': obj.phone_number,
                'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
                'age': obj.age,
                'pincode': obj.pincode,
                'hospital_id':obj.hospitalid,
                'isdelete':obj.isdelete
                ########################certificate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            })
        my_Admin = Admin.objects.get(id=my_id) 
        info = {'name': my_Admin.name, 'id': my_Admin.id, 'pending_doctors_list': pending_doctors_list} 
        return render(request, 'show_pending_doctors.html', {"info": info})
# def approve_doctor(request,doctor_id):
#     doctor = get_object_or_404(pending_doctors, id=doctor_id)
#     newdoctor=doctor(name=doctor.name,email=doctor.email,password=doctor.password,gender=doctor.gender,phone_number=doctor.phone_number,address=doctor.address,specialization=doctor.specialization,experience=doctor.experience,age=doctor.age,hospitalid=doctor.hospitalid,pincode=doctor.pincode)
#     newdoctor.save()
#     doctor.delete()
#     return redirect('/afterAdminlogin')


# def process_doctors(request):
#     my_id = request.session.get('my_id', 'default_id') 
#     if type(my_id)==str:
#        return redirect('/Adminlogin')
#     request.session['my_id'] = my_id
    
#     if request.method == 'POST':
#         selected_options = request.POST.dict()
#         for doctor_id, action in selected_options.items():
#             if action == 'approve':
#                 id=doctor_id[7]
#                 print("doctor id:")
#                 print(id)
#                 pending_doctor = get_object_or_404(pending_doctors, id=id)
#                 newdoctor = doctor(name=pending_doctor.name, email=pending_doctor.email, password=pending_doctor.password, gender=pending_doctor.gender, phone_number=pending_doctor.phone_number, address=pending_doctor.address, specialization=pending_doctor.specialization, experience=pending_doctor.experience, age=pending_doctor.age, hospitalid=pending_doctor.hospitalid, pincode=pending_doctor.pincode)
#                 newdoctor.save()
#                 pending_doctor.delete()

#                 print("approve_doctor in views")
#             elif action == 'decline':
#                 id=doctor_id[7]
#                 print("doctor id:")
#                 print(id)
#                 pending_doctor=pending_doctors(id=id)
#                 pending_doctor.delete()
#                 print("decline_doctor in views")
                
#                 # Perform the action for the doctor with the given ID
#                 # e.g. decline_doctor(doctor_id)
#             else:
#                 # Perform the action for the doctor with the given ID
#                 # e.g. do_nothing_with_doctor(doctor_id)
#                 print("nothing selected")
#         return redirect('/afterAdminlogin')

def process_doctors(request):
    my_id = request.session.get('my_id', 'default_id') 
    request.session['my_id'] = my_id

    if request.method == 'POST':
        selected_options = request.POST.dict()
        # d = pending_doctor.objects.all() 
        for doctor_id, action in selected_options.items():
            if action == 'approve':
                id=int(doctor_id[7:])
                # id = request.POST.get('action_' + str(doctor_id)) 
                # time = request.POST.get('time_' + str(b.bookingid))

                print("doctor id:")
                print(id)
                pending_doctor = get_object_or_404(pending_doctors, id=id)
                newdoctor = doctor(name=pending_doctor.name, email=pending_doctor.email, password=pending_doctor.password, gender=pending_doctor.gender, phone_number=pending_doctor.phone_number, address=pending_doctor.address, specialization=pending_doctor.specialization, experience=pending_doctor.experience, age=pending_doctor.age, hospitalid=pending_doctor.hospitalid, pincode=pending_doctor.pincode)
                newdoctor.save()

                subject = 'OMCS Confirmation'
                message = 'Congrats!! Your (doctor)request is approved ' 
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [pending_doctor.email]      
                # if pending_doctor:
                send_mail(subject, message, from_email, recipient_list)
                # else:
                    # print("***************") 
                print("approve_doctor in views")

                pending_doctor.delete()

            elif action == 'decline':
                id=int(doctor_id[7:])
                # id = request.POST.get('action_' + str(doctor_id)) 
                # status = request.POST.get('action_' + str(doctor_id)) 
                print("doctor id:")
                print(id) 
                # pending_doctor=pending_doctors(id=id)
                pending_doctor = get_object_or_404(pending_doctors, id=id) 
                
                print("decline_doctor in views")
                
                subject = 'OMCS Declination'
                message = 'Sorry!! Your (doctor)request is rejected ' 
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [pending_doctor.email] 
                print(recipient_list) 
                # if pending_doctor:
                send_mail(subject, message, from_email, recipient_list)
                # else:
                    # print("***************")      
                # send_mail(subject, message, from_email, recipient_list)
                print("Mail sent in decline_doctor in views")

                pending_doctor.delete() 
                # Perform the action for the doctor with the given ID
                # e.g. decline_doctor(doctor_id)
            else:
                # Perform the action for the doctor with the given ID
                # e.g. do_nothing_with_doctor(doctor_id)
                print("nothing selected")
        return redirect('/afterAdminlogin')
# def modify_hospitals(request):
#     if request.method == 'POST':
#         print("**")
#     else:
#         return render(request,'hospital_list.html')        