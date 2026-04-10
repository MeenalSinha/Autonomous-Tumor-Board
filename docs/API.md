# API Documentation: Autonomous Tumor Board

The ATB Backend is powered by **FastAPI** and provides RESTful endpoints for case management and report generation.

## Base URL
Default: `http://localhost:8000`

## 1. Case Management

### Submit a Case
`POST /api/cases/submit`

Submits a new patient case for processing through the AI orchestration pipeline.

**Request Body:**
```json
{
  "age": 65,
  "gender": "Male",
  "primary_site": "Lung",
  "clinical_history": "65M with chronic cough and smoking history."
}
```

**Response:**
```json
{
  "success": true,
  "case_id": "TB-20260410-880D67",
  "report": { ... }
}
```

## 2. File Uploads

### Upload Pathology Slide
`POST /api/upload/pathology`

Uploads an image for CV analysis.

**Multipart Form-Data:**
- `file`: (Image/JPG/PNG)

### Upload Imaging Scan
`POST /api/upload/imaging`

Uploads a scan for DICOM processing.

**Multipart Form-Data:**
- `file`: (DICOM/.dcm)

## 3. Reports

### Retrieve JSON Report
`GET /api/reports/{case_id}`

### Download PDF Report
`GET /api/reports/{case_id}/pdf`

Returns professional PDF generated via ReportLab.

## 4. System Health & Stats

### Health Check
`GET /health`

### System Statistics
`GET /api/stats`

Returns metrics on processed cases and agent execution speeds.

## Data Models
Data validation is handled via Pydantic. See `models/case_models.py` for full schema definitions.
