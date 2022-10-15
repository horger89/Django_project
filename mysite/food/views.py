from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import item, Comment
from django.template import loader
from food.forms import ItemForm, CommentForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from food.owner import OwnerDeleteView, OwnerUpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
# Create your views here.


def index(request):
    Item_list = item.objects.all()
    
    context = {
        'item_list' : Item_list,

    }
    return render(request,'food/index.html',context)


class index_class_view(ListView):
    model = item
    template_name = 'food/index.html'
    context_object_name = 'item_list'



def detail(request,item_id):
    Item = item.objects.get(pk=item_id)
    context = {
        'item':Item,
    }
    return render(request,'food/detail.html',context)

class FoodDetail(DetailView):
    model = item
    template_name = 'food/detail.html'

    def get_context_data(self,*args,**kwargs):
        food_menu = item.objects.all()
        context = super(FoodDetail, self).get_context_data()
        stuff = get_object_or_404(item, id= self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id = self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


def create_item(request):
    Form = ItemForm(request.POST or None)

    if Form.is_valid():
        Form.save()
        return redirect('food:index')

    return render(request,'food/item-form.html',{'form':Form})

class CreateItem(CreateView):
    model = item
    fields = ['item_name','item_disc','item_price','item_image']
    template_name = 'food/item-form.html'

    def form_valid(self,form):
        # find logged in user
        form.instance.user_name = self.request.user

        return super().form_valid(form)


def update_item(request,item_id):
    Item_update = item.objects.get(pk=item_id)
    Form_update = ItemForm(request.POST or None, instance = Item_update)

    if Form_update.is_valid():
        Form_update.save()
        return redirect('food:index')

    return  render(request,'food/item-form.html',{'form':Form_update, 'item':Item_update})

class UpdateItem(OwnerUpdateView):
    model = item
    fields = ['item_name','item_disc','item_price','item_image']
    template_name = 'food/update.html'

    def form_valid(self,form):
        # find logged in user
        form.instance.user_name = self.request.user

        return super().form_valid(form)


def delete_item(request,item_id):
    Item_delete = item.objects.get(pk=item_id)
    
    if request.method == 'POST':
        Item_delete.delete()
        return redirect('food:index')

    return render(request, 'food/item-delete.html',{'item':Item_delete})


class ItemDeleteView(OwnerDeleteView):
    model = item
    template_name = 'food/item-delete.html'
    success_url = reverse_lazy('food:index')
    


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'food/add_comment.html'
    fields = ['text']
    
    def post(self, request, pk) :
        
        f = get_object_or_404(item, id=pk)
        comment = Comment(text=request.POST['text'], user_name=request.user, Item=f)
        comment.save()
        return redirect(reverse('food:detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "food/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        Item = self.object.Item
        return reverse('food:detail', args=[Item.id])



def post_detail(request, slug):
    template_name = 'detail.html'
    Item = get_object_or_404(item, slug=slug)
    comments = Item.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'Item': Item,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



def LikeView(request,pk):
    f = get_object_or_404(item, id=pk)
    liked = False
    if f.likes.filter(id = request.user.id).exists():
        f.likes.remove(request.user)
        liked = False
    else:
        f.likes.add(request.user)
        liked = True
    return redirect(reverse('food:detail', args=[pk]))



def SearchView(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        searched_items = item.objects.filter(item_name__contains=searched)
        return render(request,'food/searched_item_list.html',{'searched':searched, 'searched_items':searched_items})
    else:
        return render(request,'food/searched_item_list.html',{})




