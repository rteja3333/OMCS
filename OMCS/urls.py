from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='show_homepage'),  
    path('home/',views.homepage,name='show_homepage'),  
    path('doctorlogin/',views.doctorlogin,name='doctorlogin'),
    path('patientlogin/',views.patientlogin,name='patientlogin'),
    path('Adminlogin/',views.Adminlogin,name='Adminlogin'),
    # path('approve_doctor/',views.approve_doctor,name='approvedoctor'),
    path('doctorlogout/',views.doctorlogout,name='doctorlogout'),
    path('patientlogout/',views.patientlogout,name='patientlogout'),
    path('Adminlogout/',views.Adminlogout,name='Adminlogout'),

    path('process_doctors/', views.process_doctors, name='process_doctors'),


    path('afterloginpage/',views.afterloginpage,name='show_loginpage'),
    path('get_hospitals_list/',views.get_hospitals_list, name='get_hospitals_list'),
    # path('addnewdoctor/',views.addnewdoctor, name='addnewdoctor'),
    path('addnewdoctor/',views.hospital_list_2, name='addnewdoctor'),
    path('addnewpatient/',views.addnewpatient, name='addnewpatient'),
    path('new/',views.addnewdoctor, name='new'),
    #path('doctor_detail/',views.doctor_detail, name='doctor_detail'),
    path('change_doctor_info/',views.change_doctor_info, name='change_doctor_info'),
    path('afterdoctorlogin/',views.afterdoctorlogin, name='afterdoctorlogin'),
    path('afterpatientlogin/',views.afterpatientlogin,name='afterpatientlogin'),
    path('afterAdminlogin/',views.afterAdminlogin,name='afterAdminlogin'),
    path('change_patient_info/',views.change_patient_info, name='change_patient_info'),
    path('book_appointment/',views.book_appointment, name='book_appointment'),
    path('select_doctor/',views.select_doctor, name='select_doctor'),
    path('show_pending_doctors/',views.show_pending_doctors, name='select_doctor'),
    path('show_doctor_info/',views.show_doctor_info, name='show_doctor_info'),
    path('show_patient_info/',views.show_patient_info, name='show_patient_info'),

    # path('change_doctor_info/',views.change_doctor_info, name='change_doctor_info'),
    # path('get_doctors_list/',views.get_doctors_list, name='get_doctors_list'),
    path('ask_doctor_date_time/',views.ask_doctor_date_time, name='ask_doctor_date_time'),
    path('show_appointments/',views.show_appointments, name='show_appointments'),
    path('my_send_mail/',views.my_send_mail, name='my_send_mail'),
    # path('modify_hospitals/',views.modify_hospitals, name='modify_hospitals'),
    # path('approve_appointment/',views.approve_appointment, name='approve_appointment'),
    # path('new_appointment/',views.new_appointment, name='new_appointment'),
    ####################################
    path('hospital_list/', views.hospital_list, name='hospital_list'),
    path('hospitals/add/', views.hospital_add, name='hospital_add'),
    # path('hospital_edit?id=<int:pk>/', views.hospital_edit, name='hospital_edit'),
    path('hospital_edit/', views.hospital_edit, name='hospital_edit'),
    path('hospital_remove/', views.hospital_remove, name='hospital_remove'),
    # path('hospitals/<int:pk>/remove/', views.hospital_remove, name='hospital_remove'),
    #####################################
]

#########
# <td>
#                         <a href="{% url 'hospital_edit' hospital.pk %}">Edit</a> |
#                         <a href="{% url 'hospital_remove' hospital.pk %}">Remove</a>
#                     </td>