from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class PatientCaseDB(Base):
    __tablename__ = "patient_cases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    primary_site = Column(String)
    clinical_history = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    reports = relationship("TumorBoardReportDB", back_populates="patient_case")

class TumorBoardReportDB(Base):
    __tablename__ = "tumor_board_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("patient_cases.case_id"))
    pathology_data = Column(JSON)
    imaging_data = Column(JSON)
    guideline_data = Column(JSON)
    synthesis_data = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    patient_case = relationship("PatientCaseDB", back_populates="reports")
