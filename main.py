from blog.models import *
from blog import db_utils


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()
    session: SessionType = Session()
    db_utils.init_data(session)

    new_user = db_utils.create_user(session, 'username 1', 3)
    new_post = db_utils.create_post(session, 'new post title 1', new_user)
    new_tag = db_utils.create_tag(session, 'new tag name 1')
    db_utils.set_tag_to_post(session=session, tag_id=new_tag, post_id=new_post)

    user = db_utils.get_user_by_id(session, 1)
    user_posts = db_utils.get_user_posts(session, user.id)
    print(f'Для пользователя {user.username} найдены следующие посты:')
    for post in user_posts:
        print(f'ID -> {post.id} Заголовок -> {post.title}')

if __name__ == "__main__":
    main()
