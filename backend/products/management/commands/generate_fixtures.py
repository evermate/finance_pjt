import os
from django.core.management.base import BaseCommand
import json
from faker import Faker
from random import choice, randint, sample
from django.utils.timezone import now
from accounts.models import User, JoinedProduct
from community.models import Post, Comment
from products.models import Bank, DepositProduct, InterestOption

FIXTURE_DIR = "fixtures"
os.makedirs(FIXTURE_DIR, exist_ok=True)

class Command(BaseCommand):
    help = "Generate fixture data for User, Post, Comment, JoinedProduct, and post_likes"

    def handle(self, *args, **kwargs):
        fake = Faker('ko_KR')

        APP_NAMES = {
            "User": "accounts",
            "JoinedProduct": "accounts",
            "Post": "community",
            "Comment": "community",
            "post_likes": "community",
        }

        banks = list(Bank.objects.all())
        products = list(DepositProduct.objects.all())
        options = list(InterestOption.objects.select_related('product').all())

        if not banks or not products or not options:
            self.stdout.write(self.style.ERROR("❌ Bank, DepositProduct, or InterestOption 테이블이 비어 있음. 먼저 API로 채워야 합니다."))
            return

        users, posts, comments, joined_products, post_likes = [], [], [], [], []

        user_instances = []
        for i in range(1, 50):
            bank = choice(banks)
            u = User.objects.create(
                username=f"user{i}",
                phone_number=fake.phone_number(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
                gender=choice(['M', 'F']),
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

        post_instances = []
        for user in user_instances:
            for _ in range(randint(1, 3)):
                p = Post.objects.create(
                    board_type=choice(['REVIEW', 'NEWS', 'FREE']),
                    author=user,
                    title=fake.sentence(),
                    content=fake.paragraph(),
                    link=fake.url(),
                    rating=randint(1, 5),
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

        for post in post_instances:
            top_comments = []
            for _ in range(randint(1, 4)):
                author = choice(user_instances)
                c = Comment.objects.create(post=post, author=author, content=fake.sentence())
                comments.append({
                    "model": f"{APP_NAMES['Comment']}.comment",
                    "pk": c.id,
                    "fields": {
                        "post": post.id,
                        "author": author.id,
                        "content": c.content,
                        "parent": None,
                        "created_at": c.created_at.strftime('%Y-%m-%dT%H:%M:%S')
                    }
                })
                top_comments.append(c)
            for _ in range(randint(1, 3)):
                if top_comments:
                    parent = choice(top_comments)
                    author = choice(user_instances)
                    c = Comment.objects.create(post=post, author=author, content=fake.sentence(), parent=parent)
                    comments.append({
                        "model": f"{APP_NAMES['Comment']}.comment",
                        "pk": c.id,
                        "fields": {
                            "post": post.id,
                            "author": author.id,
                            "content": c.content,
                            "parent": parent.id,
                            "created_at": c.created_at.strftime('%Y-%m-%dT%H:%M:%S')
                        }
                    })

        for user in user_instances:
            sampled = sample(options, k=randint(1, 4))
            for opt in sampled:
                jp = JoinedProduct.objects.create(user=user, product=opt.product, option=opt)
                joined_products.append({
                    "model": f"{APP_NAMES['JoinedProduct']}.joinedproduct",
                    "pk": jp.id,
                    "fields": {
                        "user": user.id,
                        "product": opt.product.fin_prdt_cd,
                        "option": opt.id,
                        "joined_at": jp.joined_at.strftime('%Y-%m-%dT%H:%M:%S')
                    }
                })

        seen_pairs = set()

        for user in user_instances:
            liked_posts = sample(post_instances, k=min(randint(1, 5), len(post_instances)))
            for post in liked_posts:
                key = (post.id, user.id)
                if key in seen_pairs:
                    continue  # 중복 방지
                seen_pairs.add(key)

                post.likes.add(user)
                post_likes.append({
                    "model": f"{APP_NAMES['post_likes']}.post_likes",
                    "pk": len(post_likes) + 1,  # 명시적 PK 지정
                    "fields": {
                        "post": post.id,
                        "user": user.id
                    }
                })

        with open(os.path.join(FIXTURE_DIR, 'users_fixture.json'), 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        with open(os.path.join(FIXTURE_DIR, 'posts_fixture.json'), 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        with open(os.path.join(FIXTURE_DIR, 'comments_fixture.json'), 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        with open(os.path.join(FIXTURE_DIR, 'joined_products_fixture.json'), 'w', encoding='utf-8') as f:
            json.dump(joined_products, f, ensure_ascii=False, indent=2)
        with open(os.path.join(FIXTURE_DIR, 'post_likes_fixture.json'), 'w', encoding='utf-8') as f:
            json.dump(post_likes, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'✅ 모든 Fixture JSON 파일이 "{FIXTURE_DIR}/" 디렉토리에 저장되었습니다.'))
