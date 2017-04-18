from flask import current_app,jsonify,request
from ..models.Post import Post
from ..api_1_0 import api
@api.route("/posts",methods=["GET","POST"])
def posts():
    page=int( request.args.get("page"))

    pagination = Post.query.order_by(Post.createtime.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    print(request.endpoint)
    return jsonify(
        {
            "has_next":1 if  pagination.has_next else 0,
            "page":pagination.page,
            "posts":[post.to_json() for post in pagination.items]
        });
