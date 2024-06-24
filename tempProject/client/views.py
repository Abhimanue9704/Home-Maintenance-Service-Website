from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from .models import ServiceProvider,Client,fileUpload,Section,serviceList,NewUser,customerList,booked
import uuid
import pip._vendor.requests
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_protect
from .models import Section
import base64
from django.http import HttpResponse


def user_services(request):
    return render(request,'general\services.html')

def panVerify(panNo):
    if(panNo[3] in 'CF'):
        return 1
    else:
        return 0
        
def home(request):
    return render(request, 'general\home.html')

def waitVerification(request):
    return render(request,'general/verifyUser.html')

def user_signup(request):
    return render(request, 'general\signup.html')

def client_signUpPage(request):
    return render(request,'general\signupClient.html')

def serviceProvider_signUp(request):
    return render(request,'general\signupUser.html')
    
def user_signupUser(request):#customer
    print("hellooww", request)
    if request.method == 'POST':
        userID=str(uuid.uuid4())
        print(userID)
        user_email = request.POST.get('user_email')
        username = request.POST.get('username')
        user_pswd = request.POST.get('user_pass')
        user_phNo=request.POST.get('user_phNo')
        user_adr=request.POST.get('user_adr')
        print(username,user_email,user_pswd)
        userType="User"
        if not username.strip():
            messages.error(request, 'Something is wrong.')
            return render(request, 'general\signupUser.html')
        user_obj = Client.objects.create(username=username,email=user_email,password=user_pswd,phoneNo=user_phNo,address=user_adr,userType=userType)
        user_obj.set_password(user_pswd)
        user_obj.save()
        user_auth = authenticate(username=username, password=user_pswd)
        ##
        if user_auth:
            print("Hi 1")
            login(request, user_auth)
            request.session.save()
            return redirect('services')
        print("Hi 2")
        return render(request, 'general\signupUser.html')

def user_signupClient(request):#Service provider
    print("hellooww", request)
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        username = request.POST.get('username')
        user_pswd = request.POST.get('user_pass')
        user_cmpName=request.POST.get('user_cmpName')
        user_ownName=request.POST.get('user_ownName')
        user_offAdr=request.POST.get('user_offAdr')
        user_phNo=request.POST.get('user_phNo')
        user_gst=request.POST.get('user_gst')
        userType="Service Provider"
        userPan=request.POST.get('user_pan')
        pan_date=request.POST.get('pan_date')
        full_name = request.POST.get('pan_name')
        print(username,user_email,user_pswd)
        
        if not username.strip():
            messages.error(request, 'Something is wrong.')
            return render(request, 'general\signupClient.html')

        # Encode full name to base64
        encoded_full_name = base64.b64encode(full_name.encode()).decode()

        
        pan_data = {
        "panNumber": userPan,
        "fullName": encoded_full_name,
        "dob": pan_date,
        "mobNo": user_phNo,
        "areaCd": "91",
        "serviceName": "verifyYourPanService",
        "formName": "FO-009-VYPAN"
        }

        # Convert PAN details to JSON format
        payload = json.dumps(pan_data)

        # Request headers
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en-GB;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sn": "verifyYourPanService"
        }
        # "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Microsoft Edge\";v=\"99\", \"Mozilla Firefox\";v=\"99\"",
        # include this to allow multiple websites
        # Request URL
        url = "https://eportal.incometax.gov.in/iec/guestservicesapi/saveEntity/"

        # Send POST request
        response = pip._vendor.requests.post(url, data=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the response data here
            response_data = response.json()
            print(response_data)
            if(len(response_data['messages'])>0):
                print("\nError\n")
            else:
                reqId=response_data['reqId']
                content={
                    'panNo':userPan,'mobile':user_phNo,'pan_date':pan_date,'panName':encoded_full_name,'ID':reqId,'username':username,'email':user_email,'password':user_pswd,'company_name':user_cmpName,'office_address':user_offAdr,'owner_name':user_ownName,'gstNo':user_gst,'type':userType
                }
                return render(request, 'general/otp.html',content)
            # Do something with the response data
            print("Request sent successfully")
        else:
            # Handle errors
            print("Error: Request failed")
    return render(request, 'general\signupClient.html')
        
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        panNo = request.POST.get('panNo')
        mobile = request.POST.get('mobile')
        panName = request.POST.get('panName') 
        panDate = request.POST.get('pan_date')
        reqId=request.POST.get('reqId')
        username=request.POST.get('username')
        email=request.POST.get('user_email')
        password=request.POST.get('user_pswd')
        company_name=request.POST.get('compName')
        office_address=request.POST.get('officeAddr')
        owner_name=request.POST.get('owner_name')
        gst=request.POST.get('gstNo')
        user_type=request.POST.get('type')
        request_body = {
            "panNumber": panNo,
            "fullName": panName,
            "dob": panDate,
            "mobNo": mobile,
            "areaCd": "91",
            "otp": otp,  # Include OTP here
            "serviceName": "verifyYourPanService",
            "formName": "FO-009-VYPAN",
            "reqId": reqId
        }
        print(otp)
        # Convert request body to JSON format
        payload = json.dumps(request_body)

        # Request headers
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en-GB;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sn": "verifyYourPanService"
        }

        # Request URL
        url = "https://eportal.incometax.gov.in/iec/guestservicesapi/validateOTP/"

        try:
            # Send POST request
            response = pip._vendor.requests.post(url, data=payload, headers=headers)
            response_data = response.json()
            # Do something with the response data
            print("hello",response_data)
            # Check if the request was successful
            if response.status_code == 200:
                # Process the response data here
                if(response_data['messages'][1]['desc']=='PAN is Active and details are as per PAN.'):
                    if(panVerify(panNo)==1):
                        panName = base64.b64decode(request.POST.get('panName')).decode() 
                        user_obj = ServiceProvider.objects.create(username=username,email=email,password=password,companyName=company_name,officeAddress=office_address,ownerName=owner_name,gstNo=gst,phoneNo=mobile,userType=user_type,pan=panNo,panName=panName)
                        user_obj.set_password(password)
                        user_obj.save()     
                        user_auth = authenticate(username=username, password=password)
                ##
                        if user_auth:
                            login(request, user_auth)    
                            request.session.save()
                            return redirect('register')  
                    else:
                        error_message = 'Invalid Pancard.'
                        messages.error(request, error_message)
                        return redirect('otp')  
                else:
                    error_message = 'Invalid Pancard.'
                    messages.error(request, error_message)
                    return redirect('otp')
            else:
                # Handle errors
                print("Wrong response.")
        except Exception as e:
            # Handle exceptions
            print(f"Error: {str(e)}")
    else:
        return render(request, 'general\otp.html')  
        

def user_login(request):
    if request.user.is_authenticated:
        if(request.user.userType=="User"):
            return render(request, 'general\services.html')
        else:
            return render(request, 'general\customerRequest.html')    
    return render(request, 'general\login.html')


def user_logout(request):
    try:
        logout(request)
    except:
        messages.error(request, 'Something is wrong.')
    return redirect('login')


def user_authenticate(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        user_pswd = request.POST.get('user_password')
        
        print("username :",user_email,"pass:",user_pswd)
        
        try:
            type_obj=NewUser.objects.get(username=user_email)
            print(type_obj.userType)
            if(type_obj.userType=="Service Provider"):
                user_auth = authenticate(username=user_email, password=user_pswd)
                login(request, user_auth)
                current_user=request.user
                service_obj=ServiceProvider.objects.get(email=current_user.email)
                request_obj=customerList.objects.filter(ID=service_obj.clientID)
                return render(request,'general\customerRequest.html',{'requests':request_obj})
            elif(type_obj.userType=="User"):
                user_auth = authenticate(username=user_email, password=user_pswd)
                login(request, user_auth)
                request.session.save()
                return redirect('services')
        except:
            messages.error(request, 'Something is wrong.')
            return render(request, 'general\login.html')
    else:
        return render(request, 'general\login.html')




@csrf_protect
def add_section(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Retrieve form data
            title = request.POST.get('title')
            rate = request.POST.get('rate')
            employeeCount = request.POST.get('employeeCount')
            description = request.POST.get('description')
            images = request.FILES.getlist('images', None) if 'images' in request.FILES else None#file
            employeePerArea = request.POST.get('employeePerArea')
            timeToComplete = request.POST.get('timeToComplete')
            type=request.POST.get('type')

            current_user=request.user
            print(current_user)
            service_provider = ServiceProvider.objects.get(email=current_user.email)
            # Create a new Section instance
            new_section = Section.objects.create(
                sectionID=service_provider,
                title=title,
                rate=rate,
                employeeCount=employeeCount,
                description=description,
                employeePerArea=employeePerArea,
                timeToComplete=timeToComplete,
                sectionType=type
            )
            new_section.save()

            print(images)
            
            for uploaded_file in images:#file
                    file_obj= fileUpload.objects.create(field_name=uploaded_file,ID=service_provider)
                    file_obj.save()
            # Redirect to a new page or the same page
            serviceListFn(title,rate,service_provider,type)
            request_obj=customerList.objects.filter(ID=service_provider.clientID)
            print(request_obj)
            return render(request,'general\customerRequest.html',{'requests':request_obj})
        else:
            # User is anonymous, handle appropriately (redirect to login page, show error message, etc.)
            return redirect('register')
    else:
        # Render the form page if it's not a POST request
        return render(request, 'individualService.html')

def serviceListFn(title,rate,id,type):
      service_obj=serviceList.objects.create(title=title,rate=rate,type=type,ID=id)
      service_obj.save()
    

def service_list(request):
    if 'service' in request.GET:
        service_type = request.GET['service']
        service_objects = serviceList.objects.filter(type=service_type)
        image_objs=fileUpload.objects.all()
        print(service_objects)
        return render(request, 'general\serviceList.html', {'sections': service_objects,'image_objs': image_objs})
    else:
        current_user=request.user
        currentClient = Client.objects.get(email=current_user.email)
        book_obj=booked.objects.filter(ID=currentClient)
        return render(request,'general\\booked.html', {'tracks':book_obj})
    
def service_details(request,section_id):
    section_obj = get_object_or_404(Section, sectionID__clientID=section_id)
    image_objs = fileUpload.objects.all()
    return render(request, 'general\serviceDetails.html', {'details': section_obj, 'image_objs': image_objs})

def book_now(request,section_id):
    print("hellooo",section_id)
    pay_obj=get_object_or_404(Section, sectionID__clientID=section_id)
    return render(request,'general\payment.html',{'pay':pay_obj})
            
def track(request,section_id):
    if request.method == 'POST':
        price=request.POST.get('price')
        currentDate=request.POST.get('currentDate')
        endDate=request.POST.get('endDate')
        print(currentDate)
        print(price)
        
        current_user=request.user
        service_obj=ServiceProvider.objects.get(clientID=section_id)
        currentClient = Client.objects.get(email=current_user.email)
        username=currentClient.username
        email=currentClient.email
        phone=currentClient.phoneNo
        address=currentClient.address
        bookedCustomer=customerList.objects.create(customerID=uuid.uuid4(),ID=service_obj,username=username,email=email,phoneNo=phone,address=address,price=price,startDate=currentDate)
        bookedCustomer.save()
        
        companyName=service_obj.companyName
        serviceMail=service_obj.email
        servicePhone=service_obj.phoneNo
        serviceAddr=service_obj.officeAddress
        
        track_obj=get_object_or_404(Section, sectionID__clientID=section_id)
        serviceType=track_obj.sectionType
        trackProvider=booked.objects.create(bookedID=uuid.uuid4(),ID=currentClient,companyName=companyName,email=serviceMail,phoneNo=servicePhone,officeAddress=serviceAddr,type=serviceType,startDate=currentDate,endDate=endDate,status='Pending')
        trackProvider.save()
        
        book_obj=booked.objects.filter(ID=currentClient)
        
        print(track_obj.timeToComplete)
        return render(request,'general\\booked.html', {'tracks':book_obj})            

def register(request):
    return render(request,'general\individualService.html')

def customer_request(request):
    current_user=request.user
    service_obj=ServiceProvider.objects.get(email=current_user.email)
    request_obj=customerList.objects.filter(ID=service_obj.clientID)
    return render(request,'general\customerRequest.html',{'requests':request_obj})

def status_change(request):
    if request.method =='POST':
        providerID=request.POST.get('providerID')
        username=request.POST.get('username')
        startDate=request.POST.get('currentDate')
        print("fwjfwewejf",startDate)
        user_obj=Client.objects.get(username=username)
        provider_obj=ServiceProvider.objects.get(clientID=providerID)
        customer_obj=booked.objects.get(ID__userID=user_obj.userID,email=provider_obj.email,startDate=startDate)
        customer_obj.status = 'completed'
        customer_obj.save()
        customerList.objects.filter(ID__clientID=providerID).delete()
        current_user=request.user
        service_obj=ServiceProvider.objects.get(email=current_user.email)
        request_obj=customerList.objects.filter(ID=service_obj.clientID)
        return render(request,'general\customerRequest.html',{'requests':request_obj})