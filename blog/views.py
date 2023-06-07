from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import BlogPostForm,CommentForm,AdminCommentForm
from .models import BlogPost, Comment,SubBlogPost,AdminComment
from django.urls import reverse
from django.core.files.base import ContentFile
# Create your views here.
def blogPostPage(request):
    if request.method == 'POST':
        #form = BlogPostForm(request.POST, request.FILES)
            title = request.POST.get('title')
            location = request.POST.get('location')
            content = request.POST.get('content')
            thumbnail =request.FILES.get('thumbnail')
        # Access the subform data
            arrSH,arrSL,arrSI,arrST=[],[],[],[]
            for i in range(10):
                subheading = request.POST.get(f'subheading{i+1}')
                subloc = request.POST.get(f'subloc{i+1}')
                subimage =request.FILES.get(f'subimage{i+1}')
                subtext = request.POST.get(f'subtext{i+1}')
                if subheading or subloc or subimage or subtext:
                    arrSH.append(subheading) 
                    arrSL.append(subloc) 
                    arrSI.append(subimage) 
                    arrST.append(subtext)
            user = request.user
            b1 = BlogPost(user=user,thumbnail=thumbnail,location=location,title=title,content=content)
            b1.save()
            for i in range(len(arrSH)):
                sb=SubBlogPost(subheading=arrSH[i],location=arrSL[i],image=arrSI[i],text=arrST[i])
                sb.save()
                b1.sub_posts.add(sb)
            url = reverse('blog_preview', kwargs={'blog_id': b1.id})
            return redirect(url)
    else:
        return render(request,'blog/blogPost.html',{'form':BlogPostForm})

def preview_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    sub_posts = blog.sub_posts.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        content = request.POST.get('content')
        thumbnail = request.FILES.get('thumbnail')

        blog.title = title
        blog.location = location
        blog.content = content

        if thumbnail:
            # Handle thumbnail file upload
            blog.thumbnail.save(thumbnail.name, thumbnail)

        blog.save()

        for sub_post in sub_posts:
            subheading = request.POST.get(f'subheading{sub_post.id}')
            subloc = request.POST.get(f'location{sub_post.id}')
            image = request.FILES.get(f'image{sub_post.id}')
            text = request.POST.get(f'text{sub_post.id}')

            sub_post.subheading = subheading
            sub_post.location = subloc

            if image:
                # Handle subpost image file upload
                sub_post.image.save(image.name, image)

            sub_post.text = text
            sub_post.save()

        return redirect('home')

    return render(request, 'blog/blogPreview.html', {'blog': blog, 'sub_posts': sub_posts})

def blog_details(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    
    if request.method == 'POST':
        form1 = AdminCommentForm(request.POST)
        form2 = CommentForm(request.POST)

        if form1.is_valid():
            status = form1.cleaned_data['status']
            content = form1.cleaned_data['content']

            if status == 'Approve':
                blog.status = 1
                blog.save()
                return redirect('home')
            else:
                ac = AdminComment(comment=content, blog=blog)
                ac.save()
                return redirect('home')
        elif form2.is_valid():
            comment_id = request.POST.get('comment_id')
            reply_to = Comment.objects.get(id=comment_id) if comment_id else None

            new_comment = Comment(user=request.user, text=form2.cleaned_data['content'])
            new_comment.save()

            if reply_to:
                reply_to.replies.add(new_comment)
                reply_to.save()

            else:
                blog.comments.add(new_comment)
                blog.save()

            url = reverse('blog_details', kwargs={'blog_id': blog_id})
            return redirect(url)    
    else:
            form = AdminCommentForm() if blog.status == 0 else CommentForm()

    comments = blog.comments.all()
    return render(request, 'blog/blogDetail.html', {'blog': blog, 'form': form, 'comments': comments, 'ac': AdminComment.objects.filter(blog=blog)})

def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'blog/confirmDelete.html', {'blog': blog})

def delete_comment(request, blog_id, comment_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('blog_details', blog_id=blog_id)
    return render(request, 'blog/confirmDelete.html', {'blog': blog, 'comment': comment})
    
def search(request):
    query = request.GET.get('search')
    if query:
        blogs = BlogPost.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        blogs = []
    return render(request, 'blog/search.html', {'blogs': blogs, 'query': query})