from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import and_



class Patient:

    def create(self) -> None:
        ...


    def get(
        self,
        database: Session,
        first_name: str,
        last_name,
        date_of_birth,
    ):
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Patient)
                .where(
                    and_(models.Patient.first_name == first_name,
                         models.Patient.last_name == last_name,
                         models.Patient.date_of_birth == date_of_birth
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
        )



patient = Patient()
