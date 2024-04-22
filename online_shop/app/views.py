from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .forms import LoginForm, UserSignupForm, ProductForm, CommentForm, UserProfileForm
from .models import Product, Comment, UserProfile, Message, LikedProduct, ViewedProduct
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required


def index(request):
    products = Product.objects.all().order_by('-date_time')
    return render(request, "index.html", {"products": products})


""" User kirishi chiqishi va sing up qilish uchun """


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz saytga muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
            group = Group.objects.get(name='foydalanuvchi')
            user.groups.add(group)
            return redirect('index')
    return render(request, 'login/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return HttpResponse("hato")


def user_signup(request):

    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Siz saytdan muvaffaqiyatli ro'yxatdan o'tdingiz! ")
            return redirect('login')
    else:
        form = UserSignupForm()

    context = {
        'form': form,
        'title': 'Sign up'
    }
    return render(request, 'sign_in/sign_in.html', context)


""" User funksiyalari tugashi """

# ---------------------------------------------------------------

""" Elonlar sahifasi uchun """


@permission_required('app.view_product', login_url='login')
def elonlar(request):
    products = Product.objects.all()
    return render(request, 'elonlar/elonlar.html', {"products": products})


@permission_required('app.add_product', login_url="index")
def add_elon(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            messages.success(request, "Elon qo'shdingiz")
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'elonlar/add_elon.html', {'form': form})


@permission_required('app.view_product', login_url="index")
def elon_detail(request, id):
    if request.user.is_authenticated:
        try:
            viewed_product = ViewedProduct.objects.get(user=request.user, product_id=id)
        except ViewedProduct.DoesNotExist:
            product = Product.objects.get(pk=id)
            ViewedProduct.objects.create(user=request.user, product=product)
            product.views += 1
            product.save()

    product = Product.objects.get(pk=id)
    comments = Comment.objects.filter(product_id=id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
        else:
            form = CommentForm()

        return render(request, 'elonlar/elon_detail.html', {"product": product, "comments": comments, "form": form})
    else:
        return HttpResponse("hato")


@permission_required('app.change_product', login_url="index")
def update_elon(request, id):
    product = Product.objects.get(id=id)
    if request.user.id == product.author.id:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Siz elonni yangiladingiz!")
                return redirect("elon_detail", id=product.id)
        else:
            form = ProductForm(instance=product)

        return render(request, 'elonlar/edit_elon.html', {'form': form})
    else:
        return HttpResponse("Sizda bunday huquq mavjud emas")


@permission_required('app.delete_product', login_url="index")
def delete_elon(request, id):
    product = Product.objects.get(id=id)
    if request.user.id == product.author.id or request.user.is_superuser:
        if request.user == product.author.id:
            if request.method == 'POST':
                product.delete()
                messages.success(request, "siz elonni o'chirdingiz")
                return redirect("elonlar")
            return render(request, 'elonlar/delete_elon.html', {'product': product})
        else:
            return HttpResponse("Siz o'zgartira olmaysiz")
    else:
        return HttpResponse("Sizda ruxsat yo'q")


# -------------------------------------------------------------------

""" comment """


@permission_required("app.change_comment", login_url="index")
def edit_comment(request, id):
    comment = Comment.objects.get(pk=id)
    product = comment.product
    comments = Comment.objects.filter(product_id=product.id)
    if request.user.id == comment.author.id or request.user.is_superuser:
        if request.method == 'POST' and request.user.is_authenticated:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.save()
                messages.success(request, "Siz comentariyani o'zgartirdingiz")
                return redirect('elon_detail', id=product.id)
        else:
            form = CommentForm(instance=comment)

        return render(request, 'comment/edit_comment.html', {'form': form, "product": product, "comments": comments})


@permission_required("app.delete_comment", login_url="index")
def delete_comment(request, id):
    comment = Comment.objects.get(pk=id)
    product = comment.product
    comment.delete()
    messages.success(request, "Siz commentariyani o'chirdingiz")
    return redirect("elon_detail", id=product.id)


# ----------------------------------------------------------------------

"""User profile """


def user_profile(request, id):
    if request.user.is_authenticated:
        products = Product.objects.filter(author_id=id)
        try:
            user = User.objects.get(id=id)
            user_profile = UserProfile.objects.get(user_id=user.id)
            context = {
                "user": user,
                "user_profile": user_profile,
                "title": f"{user.username} profili "
            }
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user)
            context = {
                "user": user,
                "user_profile": user_profile,
                "title": f"{user.username} profili ",
                "products": products,
            }
        return render(request, "user_profile/user_profile.html", context)
    else:
        return redirect("login")


def edit_user_profile(request, id):
    user = UserProfile.objects.get(pk=id)
    if request.user.id == user.id:
        if request.user.id == id:
            if request.method == "POST":
                form = UserProfileForm(request.POST, request.FILES, instance=user)
                form.save()
                messages.success(request, "Siz profilingizni o'zgartirdingiz")
                return redirect("user_profile", id=id)
            else:
                form = UserProfileForm(instance=user)
        return render(request, "user_profile/edit_user_profile.html", {"form": form})
    else:
        return HttpResponse("sizda bunday ruxsat yo'q")


"""Messages"""


def chat_messages(request):
    messages = Message.objects.filter(sender_id=request.user.id).order_by('-timestamp')
    messages2 = Message.objects.filter(receiver=request.user.id).order_by('-timestamp')
    messages = list(chain(messages, messages2))
    return render(request, "messages/messages.html", {"messages": messages})


def chat_page(request, sender_id, receiver_id):
    if request.user.is_authenticated:
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        if sender != receiver:
            messages1 = Message.objects.filter(sender=sender, receiver=receiver)
            messages2 = Message.objects.filter(sender=receiver, receiver=sender)
            messages = list(chain(messages1, messages2))
            context = {
                'sender': sender,
                'receiver': receiver,
                'messages': messages
            }
            return render(request, "chat_page/chat_window.html", context)
        else:
            return HttpResponse("hatolik")
    else:
        return redirect("login")


def send_message(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sender_id = request.POST.get('sender_id')
            receiver_id = request.POST.get('receiver_id')
            message = request.POST.get('message')
            sender = User.objects.get(pk=sender_id)
            receiver = User.objects.get(pk=receiver_id)
            Message.objects.create(sender=sender, receiver=receiver, message=message)
            return redirect("chat_page", sender_id=sender_id, receiver_id=receiver_id)
        return HttpResponse({'status': 'error'})
    else:
        return redirect("login")


def add_like(request, product_id):
    if request.user.is_authenticated:
        try:
            liked_product = LikedProduct.objects.get(user=request.user, product_id=product_id)
        except LikedProduct.DoesNotExist:
            product = Product.objects.get(pk=product_id)
            LikedProduct.objects.create(user=request.user, product=product)
            product.likes += 1
            product.save()
        return redirect("elon_detail", id=product_id)
    else:
        return redirect("login")


"""categoriyalar uchun """


def meing_elonlarim(request):
    if request.user.is_authenticated:
        user = request.user
        products = Product.objects.filter(author_id=user.id)
        return render(request, "elonlar/elonlar.html", {"products": products})
    else:
        return redirect("login")


def korgan_elonlarim(request):
    if request.user.is_authenticated:
        user = request.user
        products = ViewedProduct.objects.filter(user=user)
        return render(request, "elonlar/like_va_view.html", {"products": products})
    else:
        return redirect("login")


def like_bosgan_elonlarim(request):
    if request.user.is_authenticated:
        user = request.user
        products = ViewedProduct.objects.filter(user=user)
        return render(request, "elonlar/like_va_view.html", {"products": products})
    else:
        return redirect("login")


def filter_by_category(request, id):
    products = Product.objects.filter(category_id=id)
    return render(request, "index.html", {"products": products})


""""""


def product_search(request):
    query = request.GET.get('search')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'index.html', {'products': products})


""""""


def services(request):
    return render(request, "services/services.html")
