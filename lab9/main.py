'''Задания 3'''
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from zd1 import User, Post
from zd2 import add_users, add_posts, get_posts_with_users, update_user_email, update_post_content, delete_post, delete_user_and_posts

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/users/")
def get_users_page(request: Request, db: Session = Depends(get_db)):
    '''Показывает всех пользователй'''
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/posts/")
def get_posts_page(request: Request, db: Session = Depends(get_db)):
    '''Показывает все посты'''
    posts = get_posts_with_users(db)
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@app.get("/users/new/")
def create_user_page(request: Request):
    '''Для отображения формы содания пользователя'''
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": None})

@app.post("/users/")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    '''Создание пользователя'''
    add_users(username, email, password, db)
    return {"message": "User created successfully"}

@app.get("/users/edit/{user_id}/")
def edit_user_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    '''Для отображения формы изменения пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post("/users/edit/{user_id}/")
def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    '''Редактирование пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем данные пользователя
    user.username = username
    user.email = email
    user.password = password

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully"}

@app.get("/posts/new/")
def create_post_page(request: Request, db: Session = Depends(get_db)):
    '''Для отображения формы создания поста'''
    users = db.query(User).all()
    return templates.TemplateResponse("edit_post.html", {"request": request, "users": users, "post": None})

@app.post("/posts/new/")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    '''Создание поста'''
    add_posts(title, content, user_id, db)
    return {"message": "Post created successfully"}

@app.get("/posts/edit/{post_id}/")
def edit_post_page(request: Request, post_id: int, db: Session = Depends(get_db)):
    '''Для отображения формы изменения поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    users = db.query(User).all()
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post, "users": users})

@app.post("/posts/edit/{post_id}/")
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    '''Изменение поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = title
    post.content = content
    post.user_id = user_id

    db.commit()
    db.refresh(post)

    return {"message": "Post updated successfully"}

@app.post("/posts/delete/{post_id}/")
def delete_post_by_id(post_id: int, db: Session = Depends(get_db)):
    '''Удаление поста'''
    delete_post(post_id, db)
    return {"message": "Post deleted successfully"}

@app.post("/users/delete/{user_id}/")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    '''Удаление юзера и постов'''
    delete_user_and_posts(user_id, db)
    return {"message": "User and their posts deleted successfully"}
