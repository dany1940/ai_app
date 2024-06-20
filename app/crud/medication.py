from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import or_



class Medication:

    def create(self) -> None:
        ...


    def get(
        self,
        database: Session,
        code: str,
        code_name: str,
    ):
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Medication)
                .where(
                    or_(models.Medication.medication_reference == code,
                         models.Medication.code_name == code_name,
             )
            )
            )
            .unique()
            .scalar_one_or_none()
        )



medication = Medication()
