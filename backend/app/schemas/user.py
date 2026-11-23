from  pydantic import BaseModel,EmailStr,ConfigDict

class UserCreate(BaseModel):
    clerk_user_id:str
    email:EmailStr
    full_name:str|None = None


class UserResponse(BaseModel):
    id:int
    clerk_user_id:str
    email:EmailStr
    full_name:str|None = None

    model_config = ConfigDict(from_attributes=True)