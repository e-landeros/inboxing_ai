from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class CampaignBase(BaseModel):
    name: str
    email_subject: str
    email_body: str


class RecipientBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class RecipientCreate(RecipientBase):
    pass


class Recipient(RecipientBase):
    id: int
    campaign_id: int

    class Config:
        orm_mode = True


class CampaignCreate(CampaignBase):
    recipients: List[RecipientCreate]


class Campaign(CampaignBase):
    id: int
    creator_id: int
    recipients: List[Recipient] = []

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    campaigns: List[Campaign] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
