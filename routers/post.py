from fastapi import FastAPI,Response, status, HTTPException, APIRouter
from fastapi import Body,Depends
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from schema import CreatePost,ResponsePost,UserCreate,UserOut
from models import models
from database.config import engine, get_db
from sqlalchemy.orm import Session
import oauth2

router = APIRouter(
    # bu sayede /posts ile başlayan endpointler oluşturulacak
    # her defasinda tekrar tekrar yazmaya gerek yok. bu islem daha sonra documantation icin de kullanilacak
    prefix="/posts",
    #tags kismini dokumantasyon icin kullanacagiz.
    tags=["Posts"]

)


@router.get("/", response_model=list[ResponsePost])
def get_posts(db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),
                  limit: Optional[int] = None,
                  skip: Optional[int] = None,
                  search: Optional[str] = None,):
    """
    limit is optional parameter. if you don't give limit parameter, it will return all data.
    skip for pagination in frontend
    
    """
    #we remove user relaitionship between post because of tutorial manner
    all_data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        #.filter(models.Post.owner_id == get_current_user.id)\
    return all_data
    # try:
    #     cursor.execute("""SELECT * FROM posts""")
    #     posts = cursor.fetchall()
    #     if posts:
    #         return {"data": posts}
    #     else:
    #         return {"data": None}
    # except Exception as error:
    #     print(error)
    #     return {"data": error}

@router.get("/{post_id}")
def get_post(post_id:int,db: Session = Depends(get_db),get_current_user: models.User = Depends(oauth2.get_current_user)):
    selected_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not selected_post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    # if selected_post.owner_id != get_current_user.id:
    #     raise HTTPException(status_code=403, detail=f"You don't have permission to delete this post")
    return {"data": selected_post}
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    # return {"data": post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_post(new_post: CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    new_post = models.Post(owner_id= get_current_user.id,**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"data": new_post}
    return new_post
    # print("new_post")
    # print(new_post.title)    
    # query = f"""INSERT INTO posts (title, content, published) VALUES
    # ('{new_post.title}', '{new_post.content}', {new_post.published})"""
    
    # cursor.execute(query)
    # conn.commit()

    # # Fetch the inserted post data
    # cursor.execute("SELECT * FROM posts WHERE title = %s", (new_post.title,))
    # post_data = cursor.fetchone()

    # return {"data": post_data}
    # post_dict = new_post.model_dump()
    # post_dict["id"] = len(my_post) + 1
    # my_post.append(post_dict)
    # print(new_post.model_dump())

@router.delete("/{post_id}")
def delete_post(post_id:int,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    selected_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not selected_post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    if selected_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail=f"You don't have permission to delete this post")
    
    db.delete(selected_post)
    db.commit()
    return {"data": f"Post with id {post_id} is deleted."}
    # cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    # # post= cursor.fetchone()
    # # if not post:
    # #     raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    # conn.commit()
    # # print(post)
    # return {"data": "Deleted"}

@router.put("/{post_id}")
def update_post(post_id: int, updated_post: CreatePost,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)    
    post_db = post_query.first()
    if post_db is None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    if post_db.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail=f"You don't have permission to delete this post")

    post_query.update(updated_post.model_dump())
    db.commit()
    return {"data": f"Post with id {updated_post} is updated."}
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
    #                (post.title, post.content, post.published, post_id))
    # # post_data = cursor.fetchone()
    # conn.commit()

    # # Check if the row was updated successfully
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")

    # return {"message": "Post updated successfully"}