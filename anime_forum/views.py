from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import RegisterForm, AddAnimeForm, CommentForm, PostForm
from .models import AddAnime, Comment, Post, Profile


# Create your views here.
def home(request):
    # Pegar todos os objetos do model AddAnime na DB(Nome,Image,Descricao)
    anime = AddAnime.objects.all()
    post = Post.objects.all()

    return render(request, "home.html", {"anime": anime, "post": post})


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
        form_post = PostForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid() and form_post.is_valid():
                form.save()
                form_post.save(commit=False)
                form_post.instance.user = request.user
                form_post.save()
                messages.success(request, "Anime Adicionado Com Sucesso")
                return redirect("home")
        return render(request, "add_anime.html", {"form": form, "form_post": form_post})
    else:
        return render(request, "add_anime.html", {"form": form, "form_post": form_post})


def show_anime(request, pk):
    anime = get_object_or_404(AddAnime, id=pk)
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            form.save(commit=False)
            form.instance.post = Post.objects.get(pk=post.id)
            form.instance.user = request.user
            form.save()
        return redirect(request.META.get("HTTP_REFERER"))

    return render(
        request,
        "show_anime.html",
        {
            "post": post,
            "anime": anime,
            "form": form,
        },
    )


def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)

    return render(request, "add_comment.html", {"form": form, "post": post})


def post_likes(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Comment, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))


# path("comment/<int:post_id>/", CommentCreateView, name="comment-create")
# <a class="btn btn-primary" href="{% url 'comment-create' userpost.id %}" role="button">Leave a Comment</a>
# class CommentCreateView(CreateView):
#     model = Comment
#     fields = ['content'] # remove field post here

#     def form_valid(self, form):
#        form.instance.post_id = self.kwargs.get("post_id")
#        return super().form_valid(form)
