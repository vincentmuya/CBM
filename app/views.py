from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Computer, CompCategory
from django.http import JsonResponse, HttpResponseRedirect
from .forms import NewUserForm, QuoteForm, FeedbackInquiryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from cart.forms import CartAddProductForm
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import requests
import random
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
# Create your views here.


def getAccessToken(request):
    consumer_key = 'GjPRRmzBn870YZw2bqylAIlfAQE5aXa2'
    consumer_secret = 'yEb03uvft3dCrF7T'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254710902541,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254710902541,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Vincent",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


def index(request):
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, "index.html", {'random_items': random_items, 'random_items2': random_items2,
                                          'random_items3': random_items3, 'feedback_form': feedback_form})


def on_sale(request):
    computers = Computer.objects.all()
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, "on_sale.html", {'computers': computers, 'random_items': random_items,
                                            'random_items2': random_items2, 'random_items3': random_items3,
                                            'feedback_form': feedback_form})


def search_results(request):
    categories = CompCategory.objects.all()
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    if 'name' in request. GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Computer.search_by_title(search_term)
        message = f"{search_term}"
        return render(request, "search.html", {"message": message, "name": searched_ref, "categories": categories,
                                               'random_items': random_items, 'random_items2': random_items2,
                                               'random_items3': random_items3, 'feedback_form': feedback_form})
    else:
        message = "No match for search"

        return render(request, 'search.html', {'random_items': random_items})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "registration/register.html", {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                     "email": user.email,
                     'domain': '127.0.0.1:8000',
                     'site_name': 'Website',
                     "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                     "user": user,
                     'token': default_token_generator.make_token(user),
                     'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("registration/password_reset_done.html")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form": password_reset_form})


def digital_press(request):
    comp = Computer.objects.filter(compcategory__parent_id=26)
    category = CompCategory.objects.filter(parent_id__id=26)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'digital_press.html', {"comp": comp, "category": category, 'random_items': random_items,
                                                  'random_items2': random_items2, 'random_items3': random_items3,
                                                  'feedback_form': feedback_form})


def lenovo(request):
    comp = Computer.objects.filter(compcategory__parent_id=17)
    category = CompCategory.objects.filter(parent_id__id=17)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'lenovo.html', {"comp": comp, "category": category, 'random_items': random_items,
                                           'random_items2': random_items2, 'random_items3': random_items3,
                                           'feedback_form': feedback_form})


def dell(request):
    comp = Computer.objects.filter(compcategory__parent_id=22)
    category = CompCategory.objects.filter(parent_id__id=22)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'dell.html', {"comp": comp, "category": category, 'random_items': random_items,
                                         'random_items2': random_items2, 'random_items3': random_items3, 'feedback_form':feedback_form})


def hp(request):
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'hp.html', {'random_items': random_items, 'random_items2': random_items2,
                                       'random_items3': random_items3, 'feedback_form': feedback_form})


def security_surveillance(request):
    comp = Computer.objects.filter(compcategory__parent_id=29)
    category = CompCategory.objects.filter(parent_id__id=29)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'security_surveillance.html', {"comp": comp, "category": category,
                                                          'random_items': random_items, 'random_items2': random_items2,
                                                          'random_items3': random_items3, 'feedback_form': feedback_form})


def software(request):
    comp = Computer.objects.filter(compcategory__parent_id=33)
    category = CompCategory.objects.filter(parent_id__id=33)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'software.html', {"comp": comp, "category": category, 'random_items': random_items,
                                             'random_items2': random_items2, 'random_items3': random_items3,
                                             'feedback_form': feedback_form})


def apc(request):
    comp = Computer.objects.filter(compcategory__parent_id=36)
    category = CompCategory.objects.filter(parent_id__id=36)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'apc.html', {"comp": comp, "category": category, 'random_items': random_items,
                                        'random_items2': random_items2, 'random_items3': random_items3, 'feedback_form': feedback_form})


def comp_detail(request, id, slug, compcategory_slug=None):
    comp = get_object_or_404(Computer, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    category = CompCategory.objects.all()
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    if compcategory_slug:
        compcategory = get_object_or_404(CompCategory, slug=compcategory_slug)
        comp = comp.filter(compcategory=compcategory)
    return render(request, 'comp_detail.html', {'comp': comp, "category": category, 'random_items': random_items,
                                                'random_items2': random_items2, 'random_items3': random_items3,
                                                'cart_product_form': cart_product_form, 'feedback_form': feedback_form})


def category(request, compcategory_slug=None):
    comp = Computer.objects.all()
    category = CompCategory.objects.all()
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    category_by_product = CompCategory.objects.filter(parent_id__id=None)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    if compcategory_slug:
        compcategory = get_object_or_404(CompCategory, slug=compcategory_slug)
        comp = comp.filter(compcategory=compcategory)
    return render(request, 'category.html', {"comp": comp, "category": category, "compcategory": compcategory,
                                             "category_by_product":category_by_product, 'random_items': random_items,
                                             'random_items2': random_items2, 'random_items3': random_items3, 'feedback_form': feedback_form})


def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            phone_number = "Phone Number: {}".format(form.cleaned_data['phone_number'])
            subject = "You have a new Quote from {}:{}:{}".format(name, sender, phone_number)
            application = "\n Application: {}".format(form.cleaned_data['application'])
            product = "\n Product: {}".format(form.cleaned_data['product'])
            message = "The quote request is for: {}{}".format(product, application)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('received.html')
    else:
        form = QuoteForm()
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'quote.html', {'form': form, 'feedback_form': feedback_form})


def received(request):
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'received.html', {'random_items': random_items, 'random_items2': random_items2,
                                             'random_items3': random_items3, 'feedback_form': feedback_form})


def feedback_inquiry(request):
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('footer.html')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'footer.html', {'feedback_form': feedback_form})