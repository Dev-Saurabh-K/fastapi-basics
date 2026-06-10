from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
def test_api():
    return{
        "message":"ok"
    }

