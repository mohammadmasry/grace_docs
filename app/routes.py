import os
import json
import csv
import io
from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for, Response
from flask_login import login_required, current_user

from .ocr.processor import extract_text_from_pdf, extract_text_from_image
from .utils.fhir_mapper import map_to_fhir
from .models import PreVisitForm, Upload
from . import db

main = Blueprint('main', __name__)

# ─────────────────────────────────────────────
# Allowed file extensions
# ─────────────────────────────────────────────
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
@login_required
def upload_file():
    text = None
    fhir_data = None
    file = request.files.get('file')
    lang = request.form.get('lang', 'eng')

    if not file or not allowed_file(file.filename):
        flash("❌ Invalid file type. Only PDF and image files are allowed.", "danger")
        return redirect(url_for('main.index'))

    # Save file
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    # OCR
    if file.filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(filepath, lang=lang)
    else:
        text = extract_text_from_image(filepath, lang=lang)

    fhir_data = map_to_fhir(text)

    # Save to DB
    upload = Upload(
        filename=file.filename,
        raw_text=text,
        fhir_json=json.dumps(fhir_data),
        user_id=current_user.id
    )
    db.session.add(upload)
    db.session.commit()

    # Save structured JSON temporarily
    with open("uploads/fhir_output.json", "w") as f:
        json.dump(fhir_data, f, indent=2)

    return render_template('index.html', text=text, fhir_data=fhir_data)


@main.route('/download-json')
@login_required
def download_json():
    json_path = os.path.join('uploads', 'fhir_output.json')
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=True)
    else:
        flash("❌ No JSON file found.", "danger")
        return redirect(url_for('main.index'))


@main.route('/history')
@login_required
def history():
    if current_user.role != 'doctor':
        flash("Access denied: Doctors only.", "danger")
        return redirect(url_for('main.index'))

    uploads = Upload.query.order_by(Upload.timestamp.desc()).all()
    for u in uploads:
        u.fhir_data = json.loads(u.fhir_json)
    return render_template('history.html', uploads=uploads)


@main.route('/previsit', methods=['GET', 'POST'])
@login_required
def previsit():
    if current_user.role != 'patient':
        flash('Only patients can access this page.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        form = PreVisitForm(
            patient_name=request.form['patient_name'],
            date_of_birth=request.form['date_of_birth'],
            address=request.form['address'],
            phone=request.form['phone'],
            email=request.form['email'],
            insurance_provider=request.form['insurance_provider'],
            insurance_number=request.form['insurance_number'],
            symptoms=request.form['symptoms'],
            existing_conditions=request.form['existing_conditions'],
            medications=request.form['medications'],
            allergies=request.form['allergies'],
            user_id=current_user.id
        )
        db.session.add(form)
        db.session.commit()
        flash('✅ Form submitted successfully.')
        return redirect(url_for('main.index'))

    return render_template('pre_visit_form.html')


@main.route('/view-previsit')
@login_required
def view_previsit():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))

    forms = PreVisitForm.query.order_by(PreVisitForm.timestamp.desc()).all()
    return render_template('view_previsit.html', forms=forms)


@main.route('/previsit/<int:id>')
@login_required
def view_single_previsit(id):
    if current_user.role != 'doctor':
        flash('Only doctors can view detailed submissions.', 'danger')
        return redirect(url_for('main.index'))

    form = PreVisitForm.query.get_or_404(id)
    return render_template('single_previsit.html', form=form)


@main.route('/export-previsit')
@login_required
def export_previsit():
    if current_user.role != 'doctor':
        flash('Only doctors can export submissions.', 'danger')
        return redirect(url_for('main.index'))

    forms = PreVisitForm.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Patient Name', 'DOB', 'Email', 'Phone', 'Symptoms', 'Conditions', 'Medications', 'Allergies'])

    for f in forms:
        cw.writerow([
            f.patient_name,
            f.date_of_birth,
            f.email,
            f.phone,
            f.symptoms,
            f.existing_conditions,
            f.medications,
            f.allergies
        ])

    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=previsit_forms.csv"
    return output
