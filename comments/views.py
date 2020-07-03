from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from products.models import ProductDb
from .forms import CommentsForm, DivErrorList


def post_comment(request, product_id):
    template_name = 'product.html'
    product = get_object_or_404(ProductDb, id=product_id)
    comments = product.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentsForm(request.POST, error_class=DivErrorList)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()

    else:
        comment_form = CommentsForm()

    return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
