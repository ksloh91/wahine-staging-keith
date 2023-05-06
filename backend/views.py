from django.shortcuts import render,redirect
from backend.forms import *
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm #add this
from django.views.generic.edit import UpdateView
from django.db.models import Avg, Count, Min, Sum
import datetime
from django.apps import apps
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies
"""End V2 """

def logout_view(request):
    logout(request)
    return redirect('index')

def terms_of_service(request):
    return render(request,'backend/terms-of-service.html')

def return_refund_policy(request):
    return render(request,'backend/return-refund-policy.html')

def privacy_policy(request):
    return render(request,'backend/privacy-policy.html')

def contactus(request):
    return render(request,'backend/contact-us.html')

def index(request):
    ## Source of data (Database)
    items = Item.objects.filter(item_type="Notifier List") ## Get all notifier list from database
    for item in items: ## Loop
        print(item.data['notifier_event'])   ## Display item type

    return render(request,'backend/index.html')

def whoweare(request):
    return render(request,'backend/who-we-are.html')

def faq(request):
    return render(request,'backend/faq.html')

def joinnow(request):
    return render(request,'backend/joinnow.html')

def signup(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('assets-bank-createform')
            messages.info(request, f"You can login now.")
            return redirect('login')
        else:
            print(form.errors)
            print(form.cleaned_data)
            return render(request,'backend/signup.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/signup.html', {'form': form})

def login_view(request):
    if request.POST:
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard-new")
            return redirect('dashboard-new')
        else:
            return render(request,'backend/login.html', {'form': form})
    form = AuthenticationForm()
    print(form)
    return render(request,'backend/login.html', {'form': form})

def selectplan(request):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan']
            item = Subscription.objects.create(
                user=request.user,
                plan = plan)
            redirect('profile')
        else:
            return render(request,'backend/select-a-plan.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/select-a-plan.html', {'form': form})

def profile(request):
    return render(request,'backend/profile.html')

@login_required
def load_residential_type(request):
    property_type = request.GET.get('property_type')
    residential_types = ResidentialType.objects.filter(property_type__name=property_type).order_by('name')
    return render(request, 'backend/residential-type-dropdown-list.html', {'residential_types': residential_types})

@login_required
def assets_bank_modelform(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        print(post_data)
        formset = BankModelFormset(post_data)
        context = {'formset':formset}
        print(formset.errors)
        print(formset)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-epf-createform')


        messages.error(request, "Please correct the errors in the form and try again.")
        print(formset.errors)
        return render(request,"backend/assets-bank-create.html",context)

    # we don't want to display the already saved model instances
    formset = BankModelFormset(queryset=Bank.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-bank-create.html",context)

@login_required
def assets_epf_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='EPF',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-socso-createform')
        post_data = request.POST.copy()
        post_data['user'] = request.user
        form = EpfForm(post_data)
        context = {'form':form}

        if form.is_valid():
            form.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-socso-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        print(form.errors)
        return render(request,"backend/assets-epf-create.html",context)

    # we don't want to display the already saved model instances
    form = EpfForm()
    context = {'form':form}
    return render(request,"backend/assets-epf-create.html",context)

@login_required
def assets_socso_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Socso',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-insurance-createform')
        post_data = request.POST.copy()
        post_data['user'] = request.user
        form = SocsoForm(post_data)
        context = {'form':form}

        if form.is_valid():
            form.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-insurance-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-socso-create.html",context)

    # we don't want to display the already saved model instances
    form = SocsoForm()
    context = {'form':form}
    return render(request,"backend/assets-socso-create.html",context)

@login_required
def assets_insurance_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Insurance',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-securities-investment-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = InsuranceModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-securities-investment-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-insurance-create.html",context)

    # we don't want to display the already saved model instances
    formset = InsuranceModelFormset(queryset=Insurance.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-insurance-create.html",context)

@login_required
def assets_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = InvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = InvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-investment-create.html",context)

@login_required
def assets_securities_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-unittrust-investment-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = SecuritiesInvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-unittrust-investment-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-securities-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = SecuritiesInvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-securities-investment-create.html",context)

@login_required
def assets_unittrust_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = UnitTrustInvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-unittrust-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = UnitTrustInvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-unittrust-investment-create.html",context)

@login_required
def assets_property_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Property',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-vehicle-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PropertyModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-vehicle-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        print(formset.errors)
        return render(request,"backend/assets-property-create.html",context)

    # we don't want to display the already saved model instances
    formset = PropertyModelFormset(queryset=Property.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-property-create.html",context)

@login_required
def assets_vehicle_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Vehicle',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = VehicleModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-vehicle-create.html",context)

    # we don't want to display the already saved model instances
    formset = VehicleModelFormset(queryset=Vehicle.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-vehicle-create.html",context)

@login_required
def assets_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Other Assets',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-crypto-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherAssetModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-crypto-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherAssetModelFormset(queryset=OtherAsset.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-other-create.html",context)

@login_required
def assets_crypto_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Crypto Assets',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets_overview')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = CryptoModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets_overview')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-crypto-create.html",context)

    # we don't want to display the already saved model instances
    formset = CryptoModelFormset(queryset=Crypto.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-crypto-create.html",context)

@login_required
def liabilities_creditcard_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-personalloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = CreditCardModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-personalloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-creditcard-create.html",context)

    # we don't want to display the already saved model instances
    formset = CreditCardModelFormset(queryset=CreditCard.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-creditcard-create.html",context)

@login_required
def liabilities_personalloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-vehicleloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PersonalLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-vehicleloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-vehicleloan-create.html",context)

    # we don't want to display the already saved model instances
    formset = PersonalLoanModelFormset(queryset=PersonalLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-personalloan-create.html",context)

@login_required
def liabilities_vehicleloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-propertyloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = VehicleLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-propertyloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-propertyloan-create.html",context)

    # we don't want to display the already saved model instances
    formset = VehicleLoanModelFormset(queryset=VehicleLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-vehicleloan-create.html",context)

@login_required
def liabilities_propertyloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PropertyLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = PropertyLoanModelFormset(queryset=PropertyLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-propertyloan-create.html",context)

@login_required
def liabilities_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities_overview')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherLiabilityModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities_overview')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherLiabilityModelFormset(queryset=OtherLiability.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-other-create.html",context)
    
@login_required
def liabilities_overview(request):
    user = request.user
    items = Item.objects.filter(user=user)
    creditcard = CreditCard.objects.filter(user=user).last()
    personalloan = PersonalLoan.objects.filter(user=user).last()
    vehicleloan = VehicleLoan.objects.filter(user=user).last()
    propertyloan = PropertyLoan.objects.filter(user=user).last()
    others_liabilities = OtherLiability.objects.filter(user=user).last()
    context = {'items':items,'creditcard':creditcard,'personalloan':personalloan,'vehicleloan':vehicleloan,'propertyloan':propertyloan,'others_liabilities':others_liabilities}
    return render(request,'backend/liabilities-overview.html',context)

## Editing Assets ##
def assets_bank_editform(request,uuid):
    instance = Bank.objects.get(uuid=uuid)
    form = BankForm(request.POST or None,instance=instance)
    print(instance.account_type)
    account_type = instance.account_type
    bank_name = instance.bank_name
    account_no = instance.account_no
    account_value = instance.account_value
    item_type = 'Bank Account'
    if request.POST and form.is_valid():
        form.account_no = account_no
        form.account_value = account_value
        form.account_type = account_type
        form.bank_name = bank_name
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Bank data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'account_value':account_value,'account_no':account_no,'bank_name':bank_name,'account_type':account_type}
    return render(request,'backend/edit-assets-1-bank.html',context)

def assets_epf_editform(request,uuid):
    instance = Epf.objects.get(uuid=uuid)
    form = EpfForm(request.POST or None,instance=instance)
    account_no = instance.account_no
    account_value = instance.account_value
    nominee_name = instance.nominee_name
    form.user = request.user
    item_type = 'EPF'
    print(form.is_valid())
    print(form.errors)

    if request.POST and form.is_valid():
        form.account_no = account_no
        form.account_value = account_value
        form.nominee_name = nominee_name
        form.item_type = "EPF"

        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'EPF data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'account_value':account_value,'account_no':account_no,'nominee_name':nominee_name}
    return render(request,'backend/edit-assets-2-epf.html',context)

def assets_socso_editform(request,uuid):
    instance = Socso.objects.get(uuid=uuid)
    account_no = instance.account_no
    nominee_name = instance.nominee_name
    account_value = instance.account_value
    form = SocsoForm(request.POST or None,instance=instance)
    item_type = 'Socso'

    if request.POST and form.is_valid():
        form.account_no = account_no
        form.account_value = account_value
        form.nominee_name = nominee_name
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Socso data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'account_value':account_value,'account_no':account_no,'nominee_name':nominee_name}
    return render(request,'backend/edit-assets-2-socso.html',context)

def assets_insurance_editform(request,uuid):
    instance = Insurance.objects.get(uuid=uuid)
    form = InsuranceForm(request.POST or None,instance=instance)    
    insurance_type = instance.insurance_type
    provider = instance.provider
    policy_no = instance.policy_no
    nominee_name = instance.nominee_name
    sum_insured = instance.sum_insured

    item_type = 'Insurance'

    print(form.errors)
    if request.POST and form.is_valid():
        form.insurance_type = insurance_type
        form.policy_no = policy_no
        form.provider = provider
        form.nominee_name = nominee_name
        form.sum_insured = sum_insured
        form.item_type = "Insurance"
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Insurance data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'insurance_type':insurance_type,'provider':provider,'policy_no':policy_no,'nominee_name':nominee_name,'sum_insured':sum_insured}
    return render(request,'backend/edit-assets-3-insurance.html',context)

def assets_securityinvestment_editform(request,uuid):
    instance = SecuritiesInvestment.objects.get(uuid=uuid)
    form = SecuritiesInvestmentForm(request.POST or None, instance=instance)
    account_type = instance.account_type
    broker_name = instance.broker_name
    account_no = instance.account_no
    account_value = instance.account_value
    item_type = 'Investment'
    print(form.errors)

    if request.POST and form.is_valid():
        form.account_type = account_type
        form.broker_name = broker_name
        form.account_no = account_no
        form.account_value = account_value
        form.updated_at = datetime.datetime.now()
        instance.save()
        messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
        return redirect('dashboard-new')
    context = {'form':form,'account_type':account_type,'broker_name':broker_name,'account_no':account_no,'account_value':account_value}
    return render(request,'backend/edit-assets-4-securityinvestment.html',context)

def assets_unittrustinvestment_editform(request,uuid):
    instance = UnitTrustInvestment.objects.get(uuid=uuid)
    form = UnitTrustInvestmentForm(request.POST or None, instance=instance)
    unittrust_name = instance.unittrust_name
    account_no = instance.account_no
    agent_name  = instance.agent_name
    agent_contact_no = instance.agent_contact_no
    account_value = instance.account_value
    item_type = 'Investment'

    if request.POST and form.is_valid():
        form.unittrust_name = unittrust_name
        form.account_no = account_no
        form.account_value = account_value
        form.agent_name = agent_name
        form.agent_contact_no = agent_contact_no
        form.updated_at = datetime.datetime.now()
        instance.save()
        messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
        return redirect('dashboard-new')
    context = {'form':form,'unittrust_name':unittrust_name,'agent_name':agent_name,'agent_contact_no':agent_contact_no,'account_no':account_no,'account_value':account_value}
    return render(request,'backend/edit-assets-4-unittrustinvestment.html',context)

def assets_property_editform(request,uuid):
    instance = Property.objects.get(uuid=uuid)
    form = PropertyForm(request.POST or None, instance=instance)
    property_type = instance.property_type
    residential_type = instance.residential_type
    address = instance.address
    state = instance.state
    postcode = instance.postcode
    titleno = instance.titleno
    item_type = 'Property'
    print(form.errors)
    if request.POST and form.is_valid():
        form.property_type = property_type
        form.residential_type = residential_type
        form.address = address
        form.state = state
        form.postcode = postcode
        form.titleno = titleno
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Property data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'property_type':property_type,'residential_type':residential_type,'address':address,'state':state,'postcode':postcode,'titleno':titleno}
    return render(request,'backend/edit-assets-5-property.html',context)

def assets_vehicle_editform(request,uuid):
    instance = Vehicle.objects.get(uuid=uuid)
    form = VehicleForm(request.POST or None, instance=instance)
    vehicle_type = instance.vehicle_type
    make_model = instance.make_model
    registration_no = instance.registration_no
    item_type = 'Vehicle'
    print(form.errors)
    if request.POST and form.is_valid():
        form.vehicle_type = vehicle_type
        form.make_model = make_model
        form.registration_no = registration_no
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'vehicle_type':vehicle_type,'make_model':make_model,'registration_no':registration_no}
    return render(request,'backend/edit-assets-6-vehicle.html',context)

def assets_other_editform(request,uuid):
    instance = OtherAsset.objects.get(uuid=uuid)
    form = OtherAssetForm(request.POST or None, instance=instance)
    name = instance.name
    value = instance.value
    item_type = 'Other Assets'
    print(form.errors)
    if request.POST and form.is_valid():
        form.name = name
        form.value = value
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Other assets data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'name':name,'value':value}
    return render(request,'backend/edit-assets-7-others.html',context)

def assets_crypto_editform(request,uuid):
    instance = Crypto.objects.get(uuid=uuid)
    form = CryptoForm(request.POST or None, instance=instance)
    crypto_type = instance.crypto_type
    wallet_name = instance.wallet_name
    value = instance.value
    item_type = 'Other Assets'
    print(form.errors)
    if request.POST and form.is_valid():
        form.crypto_type = crypto_type
        form.wallet_name = wallet_name
        form.value = value
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Other assets data successfully updated.')
        return redirect('dashboard-new')

    context = {'form':form,'crypto_type':crypto_type,'wallet_name':wallet_name,'value':value}
    return render(request,'backend/edit-assets-8-crypto.html',context)

## Editing Assets End ##
def liability_credit_card_form(request):
    form = CreditCardForm()
    if request.POST:
        form = CreditCardForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Credit Card Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
            return redirect('personal_loan_form')
        if form.is_valid():
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            amount_outstanding_2 = form.cleaned_data['amount_outstanding_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding},item_type='Credit Card',created_by=request.user)
            if account_no_2 and bank_name_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'amount_outstanding':amount_outstanding_2},item_type='Credit Card',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Credit Card Info Added.')
            messages.add_message(request, messages.INFO, 'Credit Card Info Added.')
            return redirect('personal_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-1-credit-card.html',context)


def edit_liability_credit_card_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    if instance.data['amount_outstanding']:
        amount_outstanding = instance.data['amount_outstanding']
    else:
        amount_outstanding = ''
    account_no = instance.data['account_no']
    bank_name = instance.data['bank_name']
    item_type = 'Credit Card'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'amount_outstanding':amount_outstanding,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['amount_outstanding'] = form.data['amount_outstanding']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Credit Card"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Credit card data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-1-credit-card.html',context)

def personal_loan_form(request):
    form = PersonalLoanForm()
    if request.POST:
        form = PersonalLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Personal Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
            return redirect('vehicles_loan_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            amount_outstanding_2 = form.cleaned_data['amount_outstanding_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding,'loan_tenure':loan_tenure},item_type='Personal Loan',created_by=request.user)
            if bank_name_2 and account_no_2 and amount_outstanding_2 and loan_tenure_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'amount_outstanding':amount_outstanding_2,'loan_tenure':loan_tenure_2},item_type='Personal Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Added Personal Loan.')
            messages.add_message(request, messages.INFO, 'Added Personal Loan.')
            return redirect('vehicles_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-2-personal-loan.html',context)

def edit_personal_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    amount_outstanding = instance.data['amount_outstanding']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Personal Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'amount_outstanding':amount_outstanding,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['amount_outstanding'] = form.data['amount_outstanding']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Personal Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Personal loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-2-personal-loan.html',context)

def vehicles_loan_form(request):
    form = VehicleLoanForm()
    if request.POST:
        form = VehicleLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Vehicle Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
            return redirect('property_loan_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            amount_outstanding_2 = form.cleaned_data['amount_outstanding_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding,'loan_tenure':loan_tenure},item_type='Vehicle Loan',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Vehicle Loan Added.')
            if bank_name_2 and account_no_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'amount_outstanding':amount_outstanding_2,'loan_tenure':loan_tenure_2},item_type='Vehicle Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Vehicle Loan Added.')
            return redirect('property_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-3-vehicle-loan.html',context)

def edit_vehicle_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    amount_outstanding = instance.data['amount_outstanding']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Vehicle Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'amount_outstanding':amount_outstanding,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['amount_outstanding'] = form.data['amount_outstanding']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Vehicle Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Vehicle loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-3-vehicle-loan.html',context)


def property_loan_form(request):
    form = PropertyLoanForm()
    if request.POST:
        form = PropertyLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Property Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
            return redirect('liabilities_others_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            amount_outstanding_2 = form.cleaned_data['amount_outstanding_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding,'loan_tenure':loan_tenure},item_type='Property Loan',created_by=request.user)
            if bank_name_2 and account_no_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'amount_outstanding':amount_outstanding_2,'loan_tenure':loan_tenure_2},item_type='Property Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Property Loan Added.')
            messages.add_message(request, messages.INFO, 'Property Loan Added.')
            return redirect('liabilities_others_form')
    context = {'form':form}
    return render(request,'backend/liabilities-4-property.html',context)

def edit_property_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    amount_outstanding = instance.data['amount_outstanding']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Property Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'amount_outstanding':amount_outstanding,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['amount_outstanding'] = form.data['amount_outstanding']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Vehicle Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Property loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-4-property-loan.html',context)

def liabilities_others_form(request):
    form = LiabilitiesOthersForm()
    if request.POST:
        form = LiabilitiesOthersForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'No Liabilities Added.')
                item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
                return redirect('notifier_list_form')
            liability_name = form.cleaned_data['liability_name']
            liability_value = form.cleaned_data['liability_value']
            item = Item.objects.create(user=request.user,data={'liability_value':liability_value,'liability_name':liability_name},item_type='Other Liabilities',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Added Other Liabilities.')
            return redirect('notifier_list_form')
    context = {'form':form}
    return render(request,'backend/liabilities-5-others.html',context)

def edit_liabilities_others_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    liability_name = instance.data['liability_name']
    liability_value = instance.data['liability_value']
    item_type = 'Other Liabilities'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'liability_name':liability_name,
        'liability_value':liability_value,
        }
        )
    if request.POST:
        instance.data['liability_name'] = form.data['liability_name']
        instance.data['liability_value'] = form.data['liability_value']
        instance.data['item_type'] = 'Other Liabilities'
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Other liabilities data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'liability_name':liability_name,'liability_value':liability_value}
    return render(request,'backend/edit-liabilities-5-others.html',context)

def notifier_list_form(request):
    form = NotifierForm()
    if request.POST:
        form = NotifierForm(request.POST)
        if form.is_valid():
            notifier_name = form.cleaned_data['notifier_name']
            notifier_email = form.cleaned_data['notifier_email']
            notifier_ic = form.cleaned_data['notifier_ic']
            notifier_contactno = form.cleaned_data['notifier_contactno']
            notifier_relationship = form.cleaned_data['notifier_relationship']
            notifier_event = form.cleaned_data['notifier_event']
            notifier_name_2 = form.cleaned_data['notifier_name_2']
            notifier_email_2 = form.cleaned_data['notifier_email_2']
            notifier_ic_2 = form.cleaned_data['notifier_ic_2']
            notifier_contactno_2 = form.cleaned_data['notifier_contactno_2']
            notifier_relationship_2 = form.cleaned_data['notifier_relationship_2']
            notifier_event_2 = form.cleaned_data['notifier_event_2']
            item = Item.objects.create(user=request.user,data={'notifier_name':notifier_name,'notifier_email':notifier_email,'notifier_relationship':notifier_relationship,'notifier_event':notifier_event,'notifier_contactno':notifier_contactno,'notifier_ic':notifier_ic},item_type='Notifier List',created_by=request.user)
            if notifier_name_2 and notifier_contactno_2 and notifier_ic_2:
                item = Item.objects.create(user=request.user,data={'notifier_name':notifier_name_2,'notifier_email':notifier_email_2,'notifier_relationship':notifier_relationship_2,'notifier_event':notifier_event_2,'notifier_contactno':notifier_contactno_2,'notifier_ic':notifier_ic_2},item_type='Notifier List',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Added notifier.')
            messages.add_message(request, messages.INFO, 'Added notifier.')
            return redirect('access_list_form')
        else:
            messages.add_message(request, messages.INFO, 'Please add a valid notifier with name and email.')
            return redirect('notifier_list_form')
    context = {'form':form}
    return render(request,'backend/notifier-list-form.html',context)

def access_list_form(request):
    form = AccessListForm()
    if request.POST:
        form = AccessListForm(request.POST)
        if form.is_valid():
            accesslist_name = form.cleaned_data['accesslist_name']
            accesslist_email = form.cleaned_data['accesslist_email']
            accesslist_ic = form.cleaned_data['accesslist_ic']
            accesslist_contactno = form.cleaned_data['accesslist_contactno']
            accesslist_relationship = form.cleaned_data['accesslist_relationship']

            item = Item.objects.create(user=request.user,data={'accesslist_name':accesslist_name,'accesslist_email':accesslist_email,'accesslist_relationship':accesslist_relationship,'accesslist_contactno':accesslist_contactno,'accesslist_ic':accesslist_ic},item_type='Access List',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Added Access List.')
            return redirect('dashboard-new')
        else:
            messages.add_message(request, messages.INFO, 'Please make sure to key in Name and Email.')
    context = {'form':form}
    return render(request,'backend/access-list-form.html',context)

def assets_overview(request):
    user = request.user
    banks = Bank.objects.filter(user=user).last()
    epf = Epf.objects.filter(user=user).last()
    socso = Socso.objects.filter(user=user).last()
    insurances = Insurance.objects.filter(user=user).last()
    
    investments = SecuritiesInvestment.objects.filter(user=user).last()
    investments = UnitTrustInvestment.objects.filter(user=user).last()
    properties = Property.objects.filter(user=user).last()
    vehicles = Vehicle.objects.filter(user=user).last()
    others = OtherAsset.objects.filter(user=user).last()
    cryptos = Crypto.objects.filter(user=user).last()
    context = {'banks':banks,'epf':epf,'socso':socso,'investments':investments,'insurances':insurances,'vehicles':vehicles,'properties':properties,'others':others,'cryptos':cryptos}
    return render(request,'backend/assets-overview.html',context)

def dashboard_new(request):
    user = request.user
    items = Item.objects.filter(user=user)
    banks = Bank.objects.filter(user=user)
    if banks.count() == 0:
        return redirect('assets-bank-createform')
    bank_total = 0
    bank_values = banks.values('account_value')
    for x in bank_values:
        if x['account_value'] == "" or x['account_value'] is None:
            bank_total = bank_total
        else:
            bank_total += float(x['account_value'])

    insurances = Insurance.objects.filter(user=user)
    insurance_total = 0
    insurance_values = insurances.values('sum_insured')
    for x in insurance_values:
        if x['sum_insured'] == "" or x['sum_insured'] is None:
            insurance_total = insurance_total
        else:
            insurance_total += float(x['sum_insured'])

    security_investments = SecuritiesInvestment.objects.filter(user=user)
    unittrust_investments = UnitTrustInvestment.objects.filter(user=user)
    investment_total = 0
    security_investment_values = security_investments.values('account_value')
    unittrust_investment_values = unittrust_investments.values('account_value')
    for x in security_investment_values:
        if x['account_value'] == "" or x['account_value'] is None:
            investment_total = investment_total
        else:
            investment_total += float(x['account_value'])
    for x in unittrust_investment_values:
        if x['account_value'] == "" or x['account_value'] is None:
            investment_total = investment_total
        else:
            investment_total += float(x['account_value'])

    epf = Epf.objects.filter(user=user)
    socso = Socso.objects.filter(user=user)
    properties = Property.objects.filter(user=user)
    vehicles = Vehicle.objects.filter(user=user)

    cryptos = Crypto.objects.filter(user=user)
    crypto_total = 0
    crypto_values = cryptos.values('value')
    for x in crypto_values:
        if x['value'] == "" or x['value'] is None:
            crypto_total = crypto_total
        else:
            crypto_total += float(x['value'])

    other_assets = OtherAsset.objects.filter(user=user)
    other_asset_total = 0
    asset_values = other_assets.values('value')
    for x in asset_values:
        if x['value'] == "" or x['value'] is None:
            other_asset_total = other_asset_total
        else:
            other_asset_total += float(x['value'])

    creditcard = CreditCard.objects.filter(user=user)
    creditcard_total = 0
    creditcard_values = creditcard.values('amount_outstanding')
    for x in creditcard_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            creditcard_total = creditcard_total
        else:
            creditcard_total += float(x['amount_outstanding'])

    personalloan = PersonalLoan.objects.filter(user=user)
    personalloan_total = 0
    personalloan_values = personalloan.values('amount_outstanding')
    for x in personalloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            personalloan_total = personalloan_total
        else:
            personalloan_total += float(x['amount_outstanding'])

    vehicleloan = VehicleLoan.objects.filter(user=user)
    vehicleloan_total = 0
    vehicleloan_values = vehicleloan.values('amount_outstanding')
    for x in vehicleloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            vehicleloan_total = vehicleloan_total
        else:
            vehicleloan_total += float(x['amount_outstanding'])

    propertyloan = PropertyLoan.objects.filter(user=user)
    propertyloan_total = 0
    propertyloan_values = propertyloan.values('amount_outstanding')
    for x in propertyloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            propertyloan_total = propertyloan_total
        else:
            propertyloan_total += float(x['amount_outstanding'])

    other_liabilities = OtherLiability.objects.filter(user=user)
    other_liabilities_total = 0
    liabilities_values = other_liabilities.values('value')
    for x in liabilities_values:
        if x['value'] == "" or x['value'] is None:
            other_liabilities_total = other_liabilities_total
        other_liabilities_total += float(x['value'])

    context = {'bank_total':bank_total,
                'banks':banks,
                'epf':epf,
                'socso':socso,
                'insurance_total':insurance_total,
                'insurances':insurances,
                'security_investments':security_investments,
                'unittrust_investments':unittrust_investments,
                'investment_total':investment_total,
                'properties':properties,
                'vehicles':vehicles,
                'cryptos':cryptos,
                'crypto_total':crypto_total,
                'other_assets':other_assets,
                'other_asset_total':other_asset_total,
                'creditcard':creditcard,
                'creditcard_total':creditcard_total,
                'personalloan':personalloan,
                'personalloan_total':personalloan_total,
                'vehicleloan':vehicleloan,
                'vehicleloan_total':vehicleloan_total,
                'propertyloan':propertyloan,
                'propertyloan_total':propertyloan_total,
                'other_liabilities':other_liabilities,
                'other_liabilities_total':other_liabilities_total
                }
    return render(request,'backend/dashboard-new.html',context)

class assets_bank_deleteform(DeleteView):
    model = Bank
    context_object_name = 'bank'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Bank.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_bank_deleteform,self).form_valid(form)