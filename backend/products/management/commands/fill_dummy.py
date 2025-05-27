import json
from faker import Faker
from random import choice, randint, sample
from datetime import datetime
from django.utils.timezone import now
from accounts.models import User, JoinedProduct
from community.models import Post, Comment
from products.models import Bank, DepositProduct, InterestOption

fake = Faker('ko_KR')

# 모델별 앱 이름 정의
APP_NAMES = {
    "User": "accounts",
    "JoinedProduct": "accounts",
    "Post": "community",
    "Comment": "community",
    "post_likes": "community",
}

# 실제 Bank, Product, InterestOption 로드
banks = list(Bank.objects.all())
products = list(DepositProduct.objects.all())
options = list(InterestOption.objects.select_related('product').all())

# 사용자 생성
users = []
user_instances = []
for i in range(1, 21):
    bank = choice(banks)
    u = User.objects.create(
        username=f"user{i}",
        phone_number=fake.phone_number(),
        birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
        gender=choice(['M', 'F', 'O']),
        main_bank=bank,
        monthly_income_range=choice(['200만원 미만', '200~300만원', '300~400만원', '400만원 이상']),
    )
    users.append({
        "model": f"{APP_NAMES['User']}.user",
        "pk": u.id,
        "fields": {
            "username": u.username,
            "phone_number": u.phone_number,
            "birth_date": u.birth_date.strftime('%Y-%m-%d'),
            "gender": u.gender,
            "main_bank": u.main_bank.fin_co_no,
            "monthly_income_range": u.monthly_income_range,
            "profile_image": ""
        }
    })
    user_instances.append(u)

# 게시글 생성
posts = []
post_instances = []
for user in user_instances:
    for _ in range(randint(1, 3)):
        p = Post.objects.create(
            board_type=choice(['REVIEW', 'NEWS', 'FREE']),
            author=user,
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=5),
            link=fake.url(),
            rating=randint(1, 5),
            created_at=fake.date_time_between(start_date='-1y', end_date='now'),
            views=randint(0, 500)
        )
        posts.append({
            "model": f"{APP_NAMES['Post']}.post",
            "pk": p.id,
            "fields": {
                "board_type": p.board_type,
                "author": p.author.id,
                "title": p.title,
                "content": p.content,
                "link": p.link,
                "rating": p.rating,
                "created_at": p.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
                "views": p.views
            }
        })
        post_instances.append(p)

# 댓글 생성
comments = []
for post in post_instances:
    top_comments = []
    for _ in range(randint(1, 3)):
        c = Comment.objects.create(
            post=post,
            author=choice(user_instances),
            content=fake.sentence(),
            parent_id=None,
            created_at=now()
        )
        comments.append({
            "model": f"{APP_NAMES['Comment']}.comment",
            "pk": c.id,
            "fields": {
                "post": c.post.id,
                "author": c.author.id,
                "content": c.content,
                "parent": None,
                "created_at": c.created_at.strftime('%Y-%m-%dT%H:%M:%S')
            }
        })
        top_comments.append(c)
    for _ in range(randint(0, 2)):
        if top_comments:
            parent = choice(top_comments)
            c = Comment.objects.create(
                post=post,
                author=choice(user_instances),
                content=fake.sentence(),
                parent=parent,
                created_at=now()
            )
            comments.append({
                "model": f"{APP_NAMES['Comment']}.comment",
                "pk": c.id,
                "fields": {
                    "post": c.post.id,
                    "author": c.author.id,
                    "content": c.content,
                    "parent": parent.id,
                    "created_at": c.created_at.strftime('%Y-%m-%dT%H:%M:%S')
                }
            })

# 가입상품 생성
joined_products = []
jp_id = 1
for user in user_instances:
    sampled_options = sample(options, k=randint(1, 4))
    for opt in sampled_options:
        jp = JoinedProduct.objects.create(
            user=user,
            product=opt.product,
            option=opt,
            joined_at=now()
        )
        joined_products.append({
            "model": f"{APP_NAMES['JoinedProduct']}.joinedproduct",
            "pk": jp.id,
            "fields": {
                "user": jp.user.id,
                "product": jp.product.fin_prdt_cd,
                "option": jp.option.id,
                "joined_at": jp.joined_at.strftime('%Y-%m-%dT%H:%M:%S')
            }
        })

# 좋아요 생성
post_likes = []
for user in user_instances:
    liked = sample(post_instances, k=randint(1, 5))
    for post in liked:
        post.likes.add(user)
        post_likes.append({
            "model": f"{APP_NAMES['post_likes']}.post_likes",
            "pk": None,
            "fields": {
                "post": post.id,
                "user": user.id
            }
        })

# JSON 파일 저장
with open('/mnt/data/users_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=2)

with open('/mnt/data/posts_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

with open('/mnt/data/comments_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(comments, f, ensure_ascii=False, indent=2)

with open('/mnt/data/joined_products_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(joined_products, f, ensure_ascii=False, indent=2)

with open('/mnt/data/post_likes_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(post_likes, f, ensure_ascii=False, indent=2)

"/mnt/data/ 경로에 모든 fixture 파일이 저장되었습니다."
