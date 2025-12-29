import os
from flask import Flask, redirect, url_for, render_template, request, send_file
from grad_cam import apply_grad_cam, model, class_names  
from knee_check import check_for_knee
import smtplib
from fpdf import FPDF
from email.message import EmailMessage
import precautions

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    knee_check_result = check_for_knee(file_path)
    if "Please upload only knee images" in knee_check_result:
        return knee_check_result

    result_path, predicted_label = apply_grad_cam(file_path, model, class_names)

    return render_template("result.html", original_image=file_path, grad_cam_image=result_path, prediction=predicted_label)

@app.route('/generate', methods=['POST'])
def rep_gen():
    name = request.form['name']
    age = request.form['age']
    sex = request.form['sex']
    mobile = request.form['mobile']
    email = request.form['email']
    address = request.form['address']

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    knee_check_result = check_for_knee(file_path)
    if "Please upload only knee images" in knee_check_result:
        return knee_check_result


    result_path, predicted_label = apply_grad_cam(file_path, model, class_names)
    precaution_text = precautions.precautions.get(predicted_label, "No precautions available.")

    pdf_path = generate_pdf(name, age, sex, mobile, email, address, file_path, result_path, predicted_label, precaution_text)

    return render_template("preview.html", pdf_path=pdf_path, email=email)

@app.route('/send_email', methods=['POST'])
def send_email_route():
    receiver_email = request.form['email']
    pdf_path = request.form['pdf_path']

    send_email(receiver_email, pdf_path)

    return "Email sent successfully!"


def generate_pdf(name, age, sex, mobile, email, address, xray_path, grad_cam_path, severity, precautions_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", style='B', size=16)
    
    pdf.cell(200, 10, "Knee Osteoarthritis Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Times", size=12)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Sex: {sex}", ln=True)
    pdf.cell(200, 10, f"Mobile: {mobile}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Address: {address}", ln=True)
    pdf.ln(10)

    
    pdf.set_font("Times", style='B', size=14)
    pdf.cell(200, 10, "Prediction Result:", ln=True)
    pdf.set_font("Times", size=12)
    pdf.cell(200, 10, f"Predicted Severity: {severity}", ln=True)
    pdf.ln(10)

    
    x_offset = 25  
    y_offset = pdf.get_y()  
    img_width = 80  
    img_height = 80  

    pdf.image(xray_path, x=x_offset, y=y_offset, w=img_width, h=img_height)
    pdf.image(grad_cam_path, x=x_offset + img_width + 10, y=y_offset, w=img_width, h=img_height)  

    
    pdf.ln(img_height + 10)

    
    pdf.set_font("Times", style='B', size=14)
    pdf.cell(200, 10, "Precautions:", ln=True)
    pdf.set_font("Times", size=12)
    pdf.multi_cell(0, 10, precautions_text)

    
    pdf_path = f"static/results/{name}_report.pdf"
    pdf.output(pdf_path)
    
    return pdf_path


def send_email(receiver_email, pdf_path):
    sender_email = "your_mail@gmail.com"
    sender_password = "your_password"  

    msg = EmailMessage()
    msg["Subject"] = "Knee Osteoarthritis Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find your Knee OA report attached.")

    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)  
        smtp.send_message(msg)


@app.route('/handle_button', methods=['POST'])
def handle_button():
    button_name = request.form.get('button')
    if button_name == 'home':
        return redirect(url_for('home_page'))
    elif button_name == 'about':
        return redirect(url_for('about'))
    elif button_name == 'prediction':
        return redirect(url_for('prediction'))
    elif button_name == 'report':
        return redirect(url_for('report'))
    else:
        return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run(debug=True)
