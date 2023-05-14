from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from ..mailer import send_campaign_emails

router = APIRouter()

@router.post("/campaigns/", response_model=schemas.Campaign)
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    # Check if campaign name is already in use
    db_campaign = db.query(models.Campaign).filter(models.Campaign.name == campaign.name).first()
    if db_campaign:
        raise HTTPException(status_code=400, detail="Campaign name already in use")

    # Create new campaign
    new_campaign = models.Campaign(
        name=campaign.name,
        email_subject=campaign.email_subject,
        email_body=campaign.email_body,
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return new_campaign

@router.post("/campaigns/{campaign_id}/send")
def send_campaign(campaign_id: int, db: Session = Depends(get_db)):
    # Get campaign from database
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Send campaign emails
    send_campaign_emails(db_campaign)

    return {"message": "Campaign emails sent successfully"}
