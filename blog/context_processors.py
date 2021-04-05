from typing import ContextManager
from .models import Category

def common(request):
    """テンプレートに毎回渡すデータ"""
    Context = {
        'category_list':Category.objects.all(),
    }
    return Context
