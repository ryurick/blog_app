from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .forms import CommentCreateForm
from .models import Post,Category, Comment



class IndexView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        #並び替え(昇順は"-created_at")
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get("keyword")
        """
        検索フォームに入力があった場合、入力内容と同じ記事タイトルを返す(__icontainsでkeywordを含むかどうか)
        "Q"を使用することによって、タイトルor本文にkeywordが含まれてるかどうかのor検索ができる　
        """
        if keyword:
            queryset = queryset.filter(
            Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset
            

class CategoryView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        #クリックされたカテゴリー(pk番目)をcategoryにセットし、そのカテゴリーの記事をquerysetにセットする
        """
        category = get_object_or_404(Category,pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(category=category)
        """
        category_pk = self.kwargs['pk']
        queryset = Post.objects.order_by('-created_at').filter(category__pk=category_pk)
        return queryset

class DetailView(generic.DetailView):
    model = Post

class CommentView(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    # formのチェックに合格したら呼び出される(CreateView,UpdateViewで呼び出されるメソッド)
    def form_valid(self,form):
        # urlに含まれているpkを取得
        post_pk = self.kwargs['post_pk']
        # データを保存する一歩手前のモデルインスタンスを返す(DBには保存されていないため自由に編集できる)
        comment = form.save(commit=False)
        # modelsのpost属性を指定
        comment.post = get_object_or_404(Post,pk=post_pk)
        comment.save()
        return redirect('blog:detail',pk=post_pk)