from fastapi import APIRouter, HTTPException, Depends, status
from src.qr import QR
from src.dao import DatabaseDAO
from src.auth import check_admin_token, check_public_token
from models.pydantic_scheme import User, Users, UserTrans, UserInfo
from fastapi.responses import HTMLResponse


from fastapi.templating import Jinja2Templates
from fastapi import Request


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/users", tags=["Users"], response_model=list[Users])
async def get_all_users(token:str = Depends(check_admin_token)):
    users = await DatabaseDAO.get_users()
    return users


@router.get("/users/{telegram_id}", tags=["Users", "Transactions"], response_model=UserInfo)
async def get_user_info(telegram_id: int):
    user  = await DatabaseDAO.get_user(telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = dict(user)
    tr = await DatabaseDAO.get_user_transactions(telegram_id=telegram_id)
    image = await QR.image_to_base64(f"static/qrs/{telegram_id}.png")
    user["image"] = image
    user["transactions"] = tr
    return user


@router.get("/front_users/{telegram_id}", tags=["Users", "Transactions"], response_class=HTMLResponse)
async def get_user_info_front(telegram_id: int, request: Request):
    user  = await DatabaseDAO.get_user(telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = dict(user)
    tr = await DatabaseDAO.get_user_transactions(telegram_id=telegram_id)
    image = await QR.image_to_base64(f"static/qrs/{telegram_id}.png")
    user["image"] = image
    user["transactions"] = tr
    user.update({"request": request})
    print(user)
    return templates.TemplateResponse("index1.html", user)

@router.post("/pay", tags=["Transactions"])
async def user_transaction(data: UserTrans, token:bool=Depends(check_admin_token)):
    try:
        await DatabaseDAO.transaction(telegram_id=data.telegram_id, sum=data.sum)
        return {"type": "INFO", "msg": f"Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{e}")


@router.post("/add_user", tags=["Users"])
async def add_user(user: User, token:bool = Depends(check_public_token)):
    try:
        await DatabaseDAO.add_user_to_db(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        await QR.make_qr("user.telegram_id", f"static/qrs/{user.telegram_id}.png")
        return {"type": "info", "msg": f"CREATE {user.telegram_id}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")


@router.get('/test')
async def test(token:bool=Depends(check_admin_token)):
    if token:
        return {"msg": "Success"}
    raise HTTPException(status_code=401, detail="Wrong token")

# @router.get("/", response_class=HTMLResponse)
# async def main_page(request: Request, telegram_id: str=None):
#    exists = os.path.exists(f'static/qrs/{telegram_id}.png')
#    if not exists:
#        await make_qr(telegram_id, f'static/qrs/{telegram_id}.png')
#    user = await get_user(telegram_id=int(telegram_id))
#    user['transactions'] = await get_user_transactions(telegram_id=int(telegram_id))
#    user['request'] = request
#    return templates.TemplateResponse("index.html", user)