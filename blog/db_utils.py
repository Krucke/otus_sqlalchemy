from .models import User, Post, Tag, Post, PostTag, SessionType


def create_user(session: SessionType, username: str, age: int) -> int:
    user = User(username=username, age=age)
    session.add(user)
    session.commit()
    return user.id


def create_post(session: SessionType, title: str, user_id: int) -> int:
    post = Post(title=title, user_id=user_id)
    session.add(post)
    session.commit()
    return post.id


def create_tag(session: SessionType, name: str) -> int:
    tag = Tag(name=name)
    session.add(tag)
    session.commit()
    return tag.id


def set_tag_to_post(session: SessionType, tag_id: int, post_id: int) -> True:
    session.add(PostTag(post_id=post_id, tag_id=tag_id))
    session.commit()
    return True


def get_user_by_id(session: SessionType, user_id: int) -> User:
    user = session.query(User).get(user_id)
    return user


def get_tag_by_tag_name(session: SessionType, tag_name: str) -> Tag or None:
    tag = session.query(Tag).filter(Tag.name==tag_name).one_or_none()
    return tag


def get_post_by_id(session: SessionType, post_id: int) -> Post:
    post = session.query(Post).get(post_id)
    return post


def get_user_posts(session: SessionType, user_id: int):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    return posts


def get_user_posts_ids(session: SessionType, user_id: int) -> list:
    posts = session.query(Post.id).filter(Post.user_id == user_id).all()
    if posts:
        return [x[0] for x in posts]
    return []  


def get_tags_ids_by_tag_names(session: SessionType, tags: list) -> list:
    tags = session.query(Tag.id).filter(Tag.name.in_(tags)).all()
    if tags:
        return [x[0] for x in tags]
    return []


def get_user_posts_by_tags(session: SessionType, user_id: int, tags) -> list:
    tags_id = get_tags_ids_by_tag_names(session, tags)
    posts_id = get_user_posts_ids(session, user_id)
    post_tag = session.query(PostTag.post_id).filter(PostTag.tag_id.in_(tags_id) & PostTag.post_id.in_(posts_id)).all()
    if post_tag:
        return list(set([x[0] for x in post_tag]))
    return []


def init_data(session: SessionType) -> bool:
    for _ in range(1, 4):
        session.add(User(username=f'username {_}', age=_))
        session.add(Post(title=f"title {_}",user_id=_))
        session.add(Tag(name=f'tag {_}'))
    
    session.add(PostTag(post_id=1, tag_id=1))
    session.add(PostTag(post_id=2, tag_id=1))
    session.add(PostTag(post_id=1, tag_id=2))
    session.commit()
    return True


