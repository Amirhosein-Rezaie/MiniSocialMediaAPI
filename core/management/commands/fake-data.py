from django.core.management.base import BaseCommand
from faker import Faker
from core import models as CoreModels
from posts import models as PostsModels
from users import models as UsersModels
from random import randint, choice
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from colorama import Fore, Style


def Green_OK():
    print(f"{Fore.GREEN}OK{Style.RESET_ALL}")


faker_fa = Faker('fa_IR')


class Command(BaseCommand):
    print(f"{Fore.CYAN}Inserting fake data ... {Style.RESET_ALL}")

    def handle(self, *args, **options):
        # inserting users
        print("Inserting Users ... ", end='')
        for _ in range(30):
            CoreModels.Users.objects.create(
                first_name=faker_fa.first_name()[:150],
                last_name=faker_fa.last_name()[:150],
                email=faker_fa.email(),
                role=CoreModels.Users.Roles.USER,
                profile=faker_fa.image_url(width=256, height=256),
                status=choice(
                    list(CoreModels.Users.Status)
                ),
                password=make_password(faker_fa.password(special_chars=False)),
                username=faker_fa.user_name()[:150],
                phone=faker_fa.phone_number()[:150],
            )
        # # create test users
        CoreModels.Users.objects.create(
            first_name='user1',
            last_name='user1',
            email=faker_fa.email(),
            role=CoreModels.Users.Roles.USER,
            profile=faker_fa.image_url(width=256, height=256),
            status=CoreModels.Users.Status.ACTIVE,
            password=make_password('1234'),
            username='user1',
            phone=faker_fa.phone_number(),
        )
        CoreModels.Users.objects.create(
            first_name='admin ',
            last_name='admin',
            email=faker_fa.email(),
            role=CoreModels.Users.Roles.ADMIN,
            profile=faker_fa.image_url(width=256, height=256),
            status=CoreModels.Users.Status.ACTIVE,
            password=make_password('admin'),
            username='admin',
            phone=faker_fa.phone_number(),
        )
        user_users_list = list(CoreModels.Users.objects.filter(
            Q(role=CoreModels.Users.Roles.USER)
        ))
        users_count = CoreModels.Users.objects.count()
        Green_OK()

        # inserting texts
        print("Inserting Texts ... ", end='')
        # # Will fill in inserting posts
        Green_OK()

        # inserting videos
        print("Inserting Videos ... ", end='')
        # # Will fill in inserting posts
        Green_OK()

        # inserting Images
        print('Inserting Images ... ', end='')
        # # Will fill in inserting posts
        Green_OK()

        # insertnig posts
        print('Inserting Posts ... ', end='')
        for _ in range(users_count * randint(1, 5)):
            # # inserting image, video and text content and use the in post at the same time
            text = CoreModels.Texts.objects.create(
                text=faker_fa.text(300),
                user=choice(user_users_list),
                status=CoreModels.Texts.Status.IS_USED
            )
            video = CoreModels.Videos.objects.create(
                video=faker_fa.file_path(extension='mp4'),
                user=choice(list(
                    CoreModels.Users.objects.filter(
                        Q(role=CoreModels.Users.Roles.USER)
                    ))),
                caption=faker_fa.text(300) or "",
                status=CoreModels.Texts.Status.IS_USED
            )
            image = CoreModels.Images.objects.create(
                image=faker_fa.image_url(width=1366, height=768),
                user=choice(user_users_list),
                caption=faker_fa.text(300) or "",
                status=CoreModels.Texts.Status.IS_USED
            )
            CoreModels.Posts.objects.create(
                user=choice(user_users_list),
                title=faker_fa.text(20),
                text=text or None,
                video=video or None,
                image=image or None,
            )
        posts_list = list(CoreModels.Posts.objects.all())
        Green_OK()

        # inserting Albums
        print('Inserting Albums ... ', end='')
        for user in user_users_list:
            PostsModels.Albums.objects.create(
                user=user,
                title='Saved Posts',
            )
        Green_OK()

        # inserting SavePosts
        print('Inserting SavePosts ... ', end='')
        for user in user_users_list:
            album = choice(PostsModels.Albums.objects.filter(Q(user=user.pk)))
            PostsModels.SavePosts.objects.create(
                user=user,
                post=choice(posts_list),
                album=album,
            )
        Green_OK()

        # inserting like posts
        print('Inserting LikedPosts ... ', end='')
        for _ in range(users_count):
            PostsModels.LikePost.objects.create(
                user=choice(user_users_list),
                post=choice(posts_list),
            )
        Green_OK()

        # isnerting comments
        print('Inserting Comments ... ', end='')
        for _ in range(users_count):
            PostsModels.Comments.objects.create(
                user=choice(user_users_list),
                post=choice(posts_list),
                comment=faker_fa.text(randint(50, 300)),
            )
        Green_OK()

        # inserting View Posts
        print('Inserting ViewPosts ... ', end='')
        for _ in range(users_count):
            PostsModels.ViewPost.objects.create(
                user=choice(user_users_list),
                post=choice(posts_list),
            )
        Green_OK()

        # inserting Followusers
        print('Inserting Follow ... ', end='')
        for _ in range(users_count * 2):
            flr_user = choice(user_users_list)
            fld_user = choice(
                list(CoreModels.Users.objects.filter(~Q(pk=flr_user.pk)))
            )
            UsersModels.Follow.objects.create(
                follower_user=flr_user,
                followed_user=fld_user,
                status=UsersModels.Follow.Status.FOLLOEWED
            )
        Green_OK()

        print(f'{Fore.CYAN}Completed...! {Style.RESET_ALL}')
