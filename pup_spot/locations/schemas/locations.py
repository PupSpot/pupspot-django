from pydantic import BaseModel, Field, validator
from decimal import Decimal
from typing import Optional

class LocationFormSchema(BaseModel):
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)
    city: Optional[str] = None
    region: Optional[str] = None

    @validator('latitude', 'longitude', pre=True)
    def validate_coordinates(cls, v):
        return Decimal(str(v))

class LocationSchema(LocationFormSchema):
    id: int
    average_crowd_meter: Optional[float] = None
    average_dog_count: Optional[int] = None
    total_likes: int = 0

    class Config:
        from_attributes = True
