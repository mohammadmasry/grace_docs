from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from .ocr.processor import extract_text_from_pdf
from .utils.fhir_mapper import map_to_fhir
from flask import flash, redirect, url_for

from .models import PreVisitForm  # add this to your imports

import os
from .models import Upload
from . import db
import json

main = Blueprint('main', __name__)


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


from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from .models import PreVisitForm
from . import db



@main.route('/previsit', methods=['GET', 'POST'])
@login_required                # ✅ user must be logged in
def previsit():
    # ─────────────────────────────────────────────
    # Only PATIENTS should reach this page
    # ─────────────────────────────────────────────
    if current_user.role != 'patient':
        flash('Only patients can access this page.', 'danger')
        return redirect(url_for('main.index'))

    # ─────────────────────────────────────────────
    # Handle form submission
    # ─────────────────────────────────────────────
    if request.method == 'POST':
        form = PreVisitForm(
            patient_name       = request.form['patient_name'],
            date_of_birth      = request.form['date_of_birth'],
            address            = request.form['address'],
            phone              = request.form['phone'],
            email              = request.form['email'],
            insurance_provider = request.form['insurance_provider'],
            insurance_number   = request.form['insurance_number'],
            symptoms           = request.form['symptoms'],
            existing_conditions= request.form['existing_conditions'],
            medications        = request.form['medications'],
            allergies          = request.form['allergies'],
            user_id            = current_user.id         # optional link to patient user
        )
        db.session.add(form)
        db.session.commit()
        flash('✅ Form submitted successfully.')
        return redirect(url_for('main.index'))        # stay on form page or redirect elsewhere

    # ─────────────────────────────────────────────
    # GET request → render the blank form
    # ─────────────────────────────────────────────
    return render_template('pre_visit_form.html')

@main.route('/view-previsit')
@login_required
def view_previsit():
    if current_user.role != 'doctor':
        flash('Access denied.')
        return redirect(url_for('main.index'))

    forms = PreVisitForm.query.order_by(PreVisitForm.timestamp.desc()).all()
    return render_template('view_previsit.html', forms=forms)


@main.route('/export-previsit')
@login_required
def export_previsit():
    if current_user.role != 'doctor':
        flash('Only doctors can export submissions.')
        return redirect(url_for('main.index'))

    import csv, io
    from flask import Response

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


@main.route('/previsit/<int:id>')
@login_required
def view_single_previsit(id):
    if current_user.role != 'doctor':
        flash('Only doctors can view detailed submissions.')
        return redirect(url_for('main.index'))

    form = PreVisitForm.query.get_or_404(id)
    return render_template('single_previsit.html', form=form)



@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    print("Current user:", current_user)
    print("Is authenticated:", current_user.is_authenticated)
    text = None
    fhir_data = None
    if request.method == 'POST':
        file = request.files['file']
        lang = request.form.get('lang', 'eng')  # Default to English if not selected

        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        # Pass the language to OCR
        text = extract_text_from_pdf(filepath, lang=lang)
        fhir_data = map_to_fhir(text)
    
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
    return send_file("uploads/fhir_output.json", as_attachment=True)
