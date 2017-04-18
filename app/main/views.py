from flask import render_template,redirect,url_for,jsonify,abort,flash,request,current_app
from . import main
from flask_sqlalchemy import BaseQuery
from ..models.Post import Post
from ..models.User import User
from ..models.Role import Role
from ..models.Follow import Follow
from ..forms.PostForm import PostForm
from ..forms.EditProfileForm import EditProfileForm
from ..forms.EditProfileAdminForm import EditProfileAdminForm
from .. import db
from .. import qn
from .. import create_app
from ..decorators import admin_required
import uuid;
from flask_login import  current_user,login_required

@main.route("/",methods=["GET","POST"])
def index():
    form=PostForm()
    if form_util(form):
        return redirect(url_for(request.endpoint))  # 跳回首页
    posts=Post.query.order_by(Post.createtime.desc()).limit(20) #首页显示已有博文 按时间排序
    return render_template("index.html",form=form,posts=posts)


#获取七牛凭证
@main.route("/qiniuuptoken",methods=["GET","POST"])
def qiniuuptoken():
    bucket_name="python-nblog"
    key=str(uuid.uuid1())
    token=qn.upload_token(bucket_name,key)
    return  jsonify({
        "uptoken":token,
        "key":key
    })
@main.route("/user/<username>")
def user(username):
    user=User.query.filter_by(username=username).first()
    if(user is None):
        abort(404)
    posts = Post.query.filter_by(author_id=user.id)
    return render_template("user.html",user=user,posts=posts)

@main.route("/edit-profile",methods=["GET","POST"])
@login_required
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname=form.nickname.data
        current_user.birthday = form.birthday.data
        current_user.email = form.email.data
        current_user.headimg = form.headkey.data
        current_user.gender = form.gender.data
        current_user.remark = form.remark.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for("main.user",username=current_user.username))
    form.nickname.data=current_user.nickname
    form.birthday.data=current_user.birthday
    form.remark.data=current_user.remark
    form.email.data=current_user.email
    form.headkey.data=current_user.headimg
    form.gender.data=current_user.gender
    return render_template("edit_profile.html",form=form)

@main.route("/edit-profile/<int:id>",methods=["GET","POST"])
@admin_required
@login_required
def edit_profile_admin(id):
    user=User.query.get_or_404(id);
    form=EditProfileAdminForm(user=user);
    if form.validate_on_submit():
        user.nickname=form.nickname.data
        user.remark=form.remark.data
        user.birthday=form.birthday.data
        user.email=form.email.data
        user.gender=form.gender.data
        user.headimg=form.headkey.data
        user.role=Role.query.get(form.role.data)
        user.username=form.username.data
        db.session.add(user)
        return redirect(url_for("main.user",username=user.username))
    form.nickname.data=user.nickname
    form.remark.data=user.remark
    form.birthday.data=user.birthday
    form.email.data=user.email
    form.gender.data=user.gender
    form.headkey.data=user.headimg
    form.role.data=user.role_id
    form.username.data=user.username
    return render_template("edit_profile.html",form=form,user=user);

@main.route("/follow/<int:userid>",methods=["GET","POST"])
@login_required
def follow(userid):
    user=User.query.get_or_404(userid)
    if(current_user.is_following(user)):
        flash("您不能重复关注用户")
        return redirect(url_for(".user",username=user.username))
    current_user.follow(user)
    flash("您已经成功关注用户 %s" % user.username)
    return redirect(url_for(".user", username=user.username))

@main.route("/unfollow/<int:userid>",methods=["GET","POST"])
@login_required
def unfollow(userid):
    user = User.query.get_or_404(userid)
    if (not current_user.is_following(user)):
        flash("您没有关注此用户")
        return redirect(url_for(".user", username=user.username))
    current_user.unfollow(user)
    flash("您已经成功取关用户 %s" % user.username)
    return redirect(url_for(".user", username=user.username))


@main.route("/<type>/<int:userid>",methods=["GET","POST"])
def follow_list(type,userid):
    user = User.query.get_or_404(userid)
    follows= (user.followers if "follower" ==type else user.followed)
    title=("关注%s用户"%user.nickname ) if "follower" ==type else ("%s关注的用户"%user.nickname)
    return  render_template("follow_list.html",user=user,title=title,follows=follows,type=type)

@main.route("/post",methods=["GET","POST"])
@main.route("/post/<int:page>",methods=["GET","POST"])
def post(page=1):
    form = PostForm()
    if form_util(form):
        return redirect(url_for(request.endpoint))  # 跳回首页
    pagination=Post.query.order_by(Post.createtime.desc()).paginate(
        page,per_page=current_app.config["POSTS_PER_PAGE"],error_out=False
    )
    return render_template("posts.html",posts=pagination.items,form=form,
                           pagination=pagination,endpoint=request.endpoint)

@main.route("/follow_post",methods=["GET","POST"])
@main.route("/follow_post/<int:page>",methods=["GET","POST"])
@login_required
def follow_post(page=1):
    form = PostForm()
    if form_util(form):
        return redirect(url_for(request.endpoint))  # 跳回首页
    print(form.body.data)
    pagination=Post.query.select_from(Follow).filter_by(follower_id=current_user.id)\
    .join(Post,Follow.followed_id == Post.author_id).paginate(
        page,per_page=current_app.config["POSTS_PER_PAGE"],error_out=False
    )
    return render_template("posts.html",posts=pagination.items,form=form,
                           pagination=pagination,endpoint=request.endpoint)

def form_util(form):
    if form.validate_on_submit():
        post = Post(body=form.body.data, author_id=current_user.id)
        db.session.add(post);
        return True
    return False

@main.route("/admin",methods=["GET","POST"])
@admin_required
def for_admin_only():
    return "您好 管理员"