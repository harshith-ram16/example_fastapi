from .. import models,schemas,oauth2
from fastapi import FastAPI ,status,HTTPException,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),limit : int=10,skip:int=0,search:Optional[str]=""):
   
    #cursor.execute(""" select * from posts """)
    #posts=cursor.fetchall()

   posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user : schemas.UserOut=Depends(oauth2.get_current_user)):

    # cursor.execute(""" insert into posts (title,content,published) values(%s,%s,%s) returning *""",(pay.title,pay.content,pay.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_posts(id : int,db:Session=Depends(get_db)):
    # cursor.execute(""" select * from posts where id=%s """,(str(id),))
    # your_post=cursor.fetchone()

    your_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not your_post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"your post with {id} is not found")
    return your_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db),current_user : int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" delete from posts where id=%s returning *""",(str(id),))
    # deleted_post=cursor.fetchone()

    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} not fount")

    if deleted_post.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not authorized to perform this action")
    
    # conn.commit()

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return

@router.put("/{id}",response_model=schemas.Post)
def update(id: int,updated_post :schemas.PostCreate,db:Session=Depends(get_db),current_user : int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" update posts set title=%s,content=%s,published=%s where id=%s returning *""",(updated_post.title,updated_post.content,updated_post.published,str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()

    post=db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} not fount")

    if post.first().owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not authorized to perform this action")

    post.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    return post.first()