from fastapi import APIRouter, HTTPException, status
import app.schemas
from app import models
from app.dependencies import Database, Patient, Institution, Clinician, Apointment, ClinicalTrial
from datetime import datetime
from datetime import timezone





router = APIRouter(
    prefix="/clinical_trials", tags=["clinical_trials"], responses={404: {"description": "Not Found"}}
)

@router.post("/{clinical_trial_code}", status_code=status.HTTP_201_CREATED, response_model=None)
def post_clinical_trials(
    fields: app.schemas.ClinicalTrialCreate,
    clinical_trial_code: str,
    existing_clinical_trial: ClinicalTrial,
    clinician_code: Clinician,
    patient_code: Patient,
    institution_name: Institution,
    apointment: Apointment,
    database: Database,
):
    """
    Create a new clinical trial in DB
    """

    if existing_clinical_trial:
        raise HTTPException(
            409, detail="There is already a clinical trial with this credentials"
        )
    if not apointment:
        raise HTTPException(
            409, detail="There is no apointment with this credentials"
        )


    new_clinical_trial = models.ClinicalTrials(
        clinical_trial_code=clinical_trial_code,
        clinician_refrence=clinician_code.registration_id,
        patient_refrence=patient_code.registration_id,
        institution_refrence=institution_name.id,
        updated_on=datetime.now(timezone.utc),
        created_on=datetime.now(timezone.utc),
        **fields.model_dump(),

    )

    database.add(new_clinical_trial)
    database.commit()
