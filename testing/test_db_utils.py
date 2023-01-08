from pytest import fixture, mark, param
from sqlalchemy.exc import IntegrityError, PendingRollbackError


from blog.models import Base, Session, SessionType
from blog import db_utils

Base.metadata.drop_all()
Base.metadata.create_all()

@fixture
def session():
    session: SessionType = Session()
    return session


@mark.parametrize('session, username, age, result', [
    param((), 'username 10', 3, 1),
    param((), 'username 11', 3, 2),
    param((), 'username 10', 3, 3)
], indirect=['session'])
def test_create_user(session, username, age, result):
    try:
        user = db_utils.create_user(session, username, age)
        assert user == result
    except IntegrityError:
        session.rollback()
        assert True


@mark.parametrize('session, title_post, user_id, result', [
    param((), 'title 1', 1, 1),
    param((), 'title 2', 2, 2),
    param((), 'title 3', 1, 3),
    param((), 'title 1', 1, 3)
], indirect=['session'])
def test_create_post(session, title_post, user_id, result):
    try:
        post = db_utils.create_post(session, title_post, user_id)
        # assert isinstance(post, int)
        assert post == result
    except IntegrityError:
        session.rollback()
        assert True


@mark.parametrize('session, tag_name, result', [
    param((), 'tag 1', 1),
    param((), 'tag 2', 2),
    param((), 'tag 3', 3),
    param((), 'tag 1', 4),
], indirect=['session'])
def test_create_tag(session, tag_name, result):
    try:
        tag = db_utils.create_tag(session, tag_name)
        assert tag == result
    except IntegrityError:
        session.rollback()
        assert True


@mark.parametrize('session, tag_id, post_id, result', [
    param((), 1, 1, True),
    param((), 1, 2, True),
    param((), 2, 1, True),
    param((), 3, 1, True),
], indirect=['session'])
def test_set_tag_to_post(session, tag_id, post_id, result):
    post_tag = db_utils.set_tag_to_post(session, tag_id, post_id)
    assert post_tag == result


@mark.parametrize('session, user_id, tags, result', [
    param((), 1, ['tag 1', 'tag 2', 'tag 3'], 1),
    param((), 1, ['tag 3'], 1),
    param((), 2, ['tag 3'], 0),
], indirect=['session'])
def test_get_user_posts_by_tags(session, user_id, tags, result):
    r = db_utils.get_user_posts_by_tags(session, user_id, tags)
    assert len(r) == result