Here you go, Moe — the complete and polished **`README.md`** file ready for you to copy-paste directly into your project folder:

---

````markdown
# 🏥 GraceDocs - Intelligent Discharge Document Scanner

GraceDocs is a web application built to help healthcare professionals digitize and process discharge documents. It uses OCR to extract text from uploaded PDFs and maps them to a structured format (FHIR-like JSON), streamlining documentation and patient intake workflows.

---

## 🚀 Features

- ✅ Upload and scan discharge PDFs using Tesseract OCR
- 🌐 OCR in **English** 🇬🇧 and **German** 🇩🇪
- 🧬 Maps text to **FHIR-style JSON** for interoperability
- 👥 Login system with roles: **doctor** and **patient**
- 📝 Patients fill out pre-visit forms digitally
- 📂 Doctors view and export submissions
- 🔐 Secure authentication using Flask-Login
- 📜 Upload history with timestamp and JSON download
- 📦 Ready for Docker deployment (coming soon)

---

## 🧠 Use Case

- 👨‍⚕️ **Doctors** get structured patient data before appointments
- 🏥 **Clinics** digitize patient intake forms and discharge summaries
- 💻 **Students & Developers** learn health informatics tools
- 🧾 Cuts down paperwork, saves time, and prevents data loss

---

## 🛠 Tech Stack

- **Backend:** Python + Flask
- **Frontend:** HTML, Bootstrap 5
- **OCR:** Tesseract + pytesseract
- **Database:** SQLite + SQLAlchemy
- **Authentication:** Flask-Login
- **Language Support:** English 🇬🇧, German 🇩🇪
- **FHIR Mapping:** Basic simulated mapping

---

## 🖥️ Getting Started (Run Locally)

### 1. Clone the Repo

```bash
git clone ("https://github.com/mohammadmasry/grace_docs")
cd grace_docs
````

### 2. Set Up Virtual Environment (Python 3.11 Required)

```bash
python3.11 -m venv venv311
source venv311/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python run.py
```

Now open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser 🎉

---


## 🧪 Test Files

Use these sample files from `/uploads/` to test OCR:

* `sample_discharge_summary.pdf`
* `sample_discharge_sarah_thompson.pdf`
* `german_discharge_summary.pdf`

These generate FHIR-style structured output upon scanning.

---

## 🗂 Upload History

The "View Upload History" page allows doctors to:

* 🕓 See uploaded files by date/time
* 📋 View the extracted OCR text
* 🧬 View mapped FHIR output
* ⬇️ Download structured data in JSON format

This saves time by organizing scanned records and making them exportable or integrable into other health systems.

---

## 📢 Flash Messages / Alerts

* Green = Success
* Yellow = Warnings
* Red = Access Denied or Errors

All role-based access is handled cleanly. For example:

* Doctors can’t fill forms → get a red alert.
* Patients can’t view submissions → blocked and redirected.

---

## ⚙️ Notes

* You MUST use `python3.11` to avoid compatibility issues (not 3.13+).
* The correct venv is `venv311`, delete the older `venv/` if not used.
* Make sure Tesseract is installed on your system and accessible via PATH.

---

## 🧠 Future Improvements (Ideas)

* Add Docker support for 1-line deployment
* REST API version for hospital system integration
* AI-based intelligent summary and anomaly detection
* Multilingual UI support

---

## 👨‍💻 Authors

- **Mohammad El Masri**  (Backend Dev)
  Student of Health Informatics  
  Origin: Lebanon 🇱🇧  
  Email: mohammad.el-masri@stud.th-deg.de

- **Kenga Olti**  (Product Manager)
  Origin: Albania 🇦🇱  
  Email: olti.kenga@stud.th-deg.de

- **Kashfia Anika**  (Business Lead)
  Origin: Bangladesh 🇧🇩  
  Email: anika.kashfia@stud.th-deg.de

- **Leen Ali**  (Frontend and text)
  Origin: Egypt 🇪🇬  
  Email: leen.ali@stud.th-deg.de

## ❤️ Built with Purpose

This project is a real-world response to messy, outdated hospital discharge systems. With OCR + FHIR + structured uploads, **GraceDocs** brings simplicity and structure to health data.

> *“Digitizing healthcare, one discharge at a time.”*

