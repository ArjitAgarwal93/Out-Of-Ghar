from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,related_name='comments')
    id = models.AutoField(primary_key=True,auto_created=True,verbose_name='ID',serialize=False)
    text = models.TextField(max_length=255)
    replies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='replied_to')
    created_at = models.DateTimeField(auto_now_add=True)


class SubBlogPost(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,verbose_name='ID',serialize=False)
    subheading = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=50,blank=True, null=True)
    image = models.ImageField(upload_to='subBlogImages/',blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subheading
    
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,related_name='blog_posts')
    id = models.AutoField(primary_key=True,auto_created=True,verbose_name='ID',serialize=False)
    thumbnail = models.ImageField(upload_to='thumbnailImages/')#,default='download.jpg')
    location = models.CharField(max_length=50,blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sub_posts = models.ManyToManyField('SubBlogPost', related_name='blog_posts')
    comments = models.ManyToManyField('Comment',related_name='comment',blank=True)
    status = models.SmallIntegerField(default=0)
    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,blank=True,null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"Like by {self.user.username} at {self.liked_at}"
    

class AdminComment(models.Model):
    comment = models.TextField(max_length=400)
    blog = models.ForeignKey(BlogPost,on_delete=models.CASCADE)

class Report(models.Model):
    REPORT_CHOICES = (
        ('harassment', 'Harassment'),
        ('bullying', 'Bullying'),
        ('harmful', 'Harmful Content'),
        ('sexual', 'Sexual Content'),
        ('child_abuse', 'Child Abuse'),
        ('spam', 'Spam'),
    )

    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Reported by {self.reporter.username} at {self.blog} for {self.report_type}"
