from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import RegisterForm, AddAnimeForm, CommentForm
from .models import AddAnime, Comment


# Create your views here.
def home(request):
    # Pegar todos os objetos do model AddAnime na DB(Nome,Image,Descricao)
    anime = AddAnime.objects.all()

    return render(request, "home.html", {"anime": anime})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Autenticar usuario e senha de quem esta tentando fazer login
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Loga o usuario se username e password estiverem corretos
            login(request, user)
            messages.success(request, "Logado Sucesso")
            return redirect("home")
        else:
            # Se usuario e password estiverem errados, volta para pagina de login
            messages.success(
                request, "Houve um Erro Na Hora do Login, Tente Novamente!"
            )
            return redirect("login")

    else:
        return render(request, "login.html", {})


def logout_user(request):
    # Deslogar usuario que fez requisicao
    logout(request)
    messages.success(request, "Deslogado Com Sucesso")
    return redirect("home")


def register_user(request):
    # Formulario do registro que esta no forms.py
    form = RegisterForm()

    if request.method == "POST":
        # Se requicisao for um POST e todas as informacoes estiverem de acordo com o formulario, registra o novo usuario
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # Caso o registro tenha sido feito, efetua o login o usuario e redirecionar para home
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registro Concluido Com Sucesso")

            return redirect("home")
        else:
            # Caso alguma informacao nao estiver de acordo com o formulario de registro, printa uma messagem e redirecionar para pagina de registro novamente
            messages(request, "Algo Deu Errado")
            return redirect("register_user")
    return render(request, "register.html", {"form": form})


def add_anime(request):
    # Verifica se o quem fez a requisicao esta logado
    if request.user.is_authenticated:
        # Se requisicao for um POST, Usa o formuladio de AddAnimeForm do forms.py
        form = AddAnimeForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Anime Adicionado Com Sucesso")
                return redirect("home")
        return render(request, "add_anime.html", {"form": form})
    else:
        return render(request, "add_anime.html", {"form": form})


def show_anime(request, pk):
    anime = get_object_or_404(AddAnime, id=pk)
    form = CommentForm(request.POST or None)
    comment = Comment.objects.all()

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("show_anime")

    if anime:
        return render(
            request,
            "show_anime.html",
            {"anime": anime, "form": form, "comment": comment},
        )
    else:
        return redirect("home")
