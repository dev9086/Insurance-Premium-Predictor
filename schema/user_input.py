from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities,tier_2_cities


class UserInput(BaseModel):

    age:Annotated[int,Field(...,gt=0,description='age')]
    weight:Annotated[float,Field(...,gt=0,description='weight')]
    height:Annotated[float,Field(...,gt=0,description='height')]
    income_lpa:Annotated[float,Field(...,gt=0,description='salary')]
    smoker:Annotated[bool,Field(...,description='smoker')]
    city:Annotated[str,Field(...,description='')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description='occupation of user ')]


    @field_validator('city')
    @classmethod
    def normalise_city(cls,v:str)-> str:
        v=v.strip().title()
        return v


    @computed_field
    @property
    def bmi(self)-> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self)-> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self)-> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self)-> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
