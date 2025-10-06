from fastapi import APIRouter, HTTPException, Depends, status, Request
from src.qr import QR
from src.qr_gradient import QR_grad
from src.dao import DatabaseDAO
from src.auth import check_admin_token, check_public_token
from models.pydantic_scheme import User, Users, UserTrans, UserTlg


router = APIRouter()


@router.get("/users", tags=["Users"], response_model=list[Users])
async def get_all_users(token: str = Depends(check_admin_token)):
    users = await DatabaseDAO.get_users()
    return users


@router.get("/user/{telegram_id}", response_model=UserTlg)
async def user_info(telegram_id: int, token: str = Depends(check_admin_token)):
    user = await DatabaseDAO.get_user(telegram_id=telegram_id)
    return user


@router.post("/myuser")
async def tlg(request: Request):
    user_id = int(request.headers.get("user"))
    user = await DatabaseDAO.get_user(telegram_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user = dict(user)
    tr = await DatabaseDAO.get_user_transactions(telegram_id=user_id)
    image = await QR.image_to_base64(f"static/qrs/{user_id}.png")
    user["image"] = image
    user["transactions"] = tr
    return user


@router.post("/pay", tags=["Transactions"])
async def user_transaction(data: UserTrans, token: bool = Depends(check_admin_token)):
    try:
        await DatabaseDAO.transaction(telegram_id=data.telegram_id, sum=data.sum)
        return {"type": "INFO", "msg": f"Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{e}")


@router.post("/add_user", tags=["Users"])
async def add_user(user: User, token: bool = Depends(check_public_token)):
    try:
        await DatabaseDAO.add_user_to_db(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        await QR_grad.create_gradient_qr(
            f"{user.telegram_id}", f"static/qrs/{user.telegram_id}.png"
        )
        return {"type": "info", "msg": f"CREATE {user.telegram_id}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")
