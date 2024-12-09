'''Задание 2'''
from sqlalchemy.orm import Session
from zd1 import User, Post

def add_users(username, email, password, db: Session):
    '''Добавление пользователя'''
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()

def add_posts(title, content, user_id, db: Session):
    '''Добавление поста'''
    new_post = Post(title=title, content=content, user_id=user_id)
    db.add(new_post)
    db.commit()

def get_posts_with_users(db: Session):
    '''Получение поста с именем пользователя'''
    return db.query(Post).join(Post.owner).all()

def update_user_email(user_id, new_email, db: Session):
    '''Обновление почты пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()

def update_post_content(post_id, new_content, db: Session):
    '''Обновление содержания поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()

def delete_post(post_id, db: Session):
    '''Удаление поста по id'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()

def delete_user_and_posts(user_id, db: Session):
    '''Удаление пользователя по id'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.query(Post).filter(Post.user_id == user.id).delete()
        db.delete(user)
        db.commit()
