from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import and_



class Clinician:

    def create(self) -> None:
        ...


    def get(
        self,
        database: Session,
        first_name: str,
        last_name: str,
        registration_id:int,
    ):
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Clinician)
                .where(
                    and_(models.Clinician.first_name == first_name,
                         models.Clinician.last_name == last_name,
                         models.Clinician.registration_id == registration_id,
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
        )

clinician = Clinician()
