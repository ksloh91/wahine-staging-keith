from django.urls import path, include

from django.contrib import admin
from backend.views import *
from backend.admin import *
# admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.activation.views import RegistrationView
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	## Creating Assets
	path("v2/assets/bank",assets_bank_modelform,name="assets-bank-createform"),
	path("v2/assets/epf",assets_epf_modelform,name="assets-epf-createform"),
	path("v2/assets/socso",assets_socso_modelform,name="assets-socso-createform"),
	path("v2/assets/insurance",assets_insurance_modelform,name="assets-insurance-createform"),
	path("v2/assets/securities-investment",assets_securities_investment_modelform,name="assets-securities-investment-createform"),
	path("v2/assets/unittrust-investment",assets_unittrust_investment_modelform,name="assets-unittrust-investment-createform"),
	path("v2/assets/property",assets_property_modelform,name="assets-property-createform"),
	path("v2/assets/vehicle",assets_vehicle_modelform,name="assets-vehicle-createform"),
	path("v2/assets/others",assets_other_modelform,name="assets-other-createform"),
	path("v2/assets/crypto",assets_crypto_modelform,name="assets-crypto-createform"),

	## Editing Assets
	path("v2/assets/bank/delete/<uuid>",assets_bank_deleteform.as_view(),name="assets-bank-deleteform"),
	path("v2/assets/bank/edit/<uuid>",assets_bank_editform,name="assets-bank-editform"),
	path("v2/assets/epf/edit/<uuid>",assets_epf_editform,name="assets-epf-editform"),
	path("v2/assets/socso/edit/<uuid>",assets_socso_editform,name="assets-socso-editform"),
	path("v2/assets/insurance/edit/<uuid>",assets_insurance_editform,name="assets-insurance-editform"),
	path("v2/assets/securityinvestment/edit/<uuid>",assets_securityinvestment_editform,name="assets-securityinvestment-editform"),
	path("v2/assets/unittrustinvestment/edit/<uuid>",assets_unittrustinvestment_editform,name="assets-unittrustinvestment-editform"),
	path("v2/assets/property/edit/<uuid>",assets_property_editform,name="assets-property-editform"),
	path("v2/assets/vehicles/edit/<uuid>",assets_vehicle_editform,name="assets-vehicle-editform"),
	path("v2/assets/others/edit/<uuid>",assets_other_editform,name="assets-other-editform"),
	path("v2/assets/crypto/edit/<uuid>",assets_crypto_editform,name="assets-crypto-editform"),

	path("v2/liabilities/creditcard",liabilities_creditcard_modelform,name="liabilities-creditcard-createform"),
	path("v2/liabilities/personalloan",liabilities_personalloan_modelform,name="liabilities-personalloan-createform"),
	path("v2/liabilities/vehicle",liabilities_vehicleloan_modelform,name="liabilities-vehicleloan-createform"),
	path("v2/liabilities/property",liabilities_propertyloan_modelform,name="liabilities-propertyloan-createform"),
	path("v2/liabilities/others",liabilities_other_modelform,name="liabilities-other-createform"),

	path("v2/assets/overview",assets_overview,name="assets-overview"),
	path("v2/liabilities/overview",liabilities_overview,name="liabilities-overview"),

    path('ajax/load-residential-type/', load_residential_type, name='data-residential-type-url'),
	path("",index,name="index"),
	path("joinnow",joinnow,name="joinnow"),
	path("whoweare/",whoweare,name="whoweare"),
	path("contact/",contactus,name="contactus"),
	path("terms-of-service/",terms_of_service,name="terms-of-service"),
	path("privacy-policy/",privacy_policy,name="privacy-policy"),
	path("return-refund-policy/",return_refund_policy,name="return-refund-policy"),
	path("profile/",profile,name="profile"),
	path("plan/",selectplan,name="plan"),
	path("faq/",faq,name="faq"),
	# path("dashboard/",dashboard,name="dashboard"),
	path("dashboard-new/",dashboard_new,name="dashboard-new"),
	path("logout/",logout_view,name="logout"),

	## Editing Liabilities
	path("liabilities/card/edit/<uuid>",edit_liability_credit_card_form,name="edit_credit_card_form"),
	path("liabilities/personal/edit/<uuid>",edit_personal_loan_form,name="edit_personal_loan_form"),
	path("liabilities/vehicles/edit/<uuid>",edit_vehicle_loan_form,name="edit_vehicles_loan_form"),
	path("liabilities/property/edit/<uuid>",edit_property_loan_form,name="edit_property_loan_form"),
	path("liabilities/others/edit/<uuid>",edit_liabilities_others_form,name="edit_liabilities_others_form"),

	## Onboarding Trigger Events
	path("triggers/notifier/",notifier_list_form,name="notifier_list_form"),
	path("triggers/accesslist/",access_list_form,name="access_list_form"),
 	path("admin/", admin.site.urls),

 	
 	## Django Registration Urls
    path('accounts/register/',
        RegistrationView.as_view(
            form_class=MyCustomUserForm
        ),
        name='django_registration_register',
    ),
    path('accounts/',
        include('django_registration.backends.activation.urls')
    ),
    path('accounts/', include('django.contrib.auth.urls')),
	# path("login/",login_view,name="login"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
