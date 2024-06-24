from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.home, name='home'),
	path('waitVerification',views.waitVerification,name="waitVerification"),
	path('signupUser', views.user_signupUser, name='signupUser'),
	path('signupClient', views.user_signupClient, name='signupClient'),
	path('serviceProvider_signUp',views.serviceProvider_signUp,name='serviceProvider_signUp'),
	path('client_signUpPage',views.client_signUpPage,name='client_signUpPage'),
  	path('signup', views.user_signup, name='signup'),
	path('login', views.user_login, name='login'),
    path('services1', views.user_authenticate, name='authenticate'),
	path('logout', views.user_logout, name='logout'),
	path('services',views.user_services,name="services"),
	path('section',views.add_section,name='add_section'),
	path('serviceList',views.service_list,name="serviceList"),
	path('service-details/<uuid:section_id>/', views.service_details, name='service_details'),
	path('book/<uuid:section_id>/',views.book_now,name="book"),
	path('track/<uuid:section_id>/',views.track,name="track"),
	path('register',views.register,name="register"),
	path('customerRequest',views.customer_request,name="customerRequest"),
	path('status',views.status_change,name='status'),
	path('otp',views.verify_otp,name='otp'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)