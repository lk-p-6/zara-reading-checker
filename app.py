from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret'

@app.errorhandler(405)
def method_not_allowed(e):
    lang = request.args.get('lang', 'en')
    flash("Method Not Allowed (405). Please select scan type again.")
    return redirect(url_for('index', lang=lang))

@app.errorhandler(500)
def internal_error(e):
    lang = request.args.get('lang', 'en')
    flash("Unexpected Error (500). Please try again or select scan type again.")
    return redirect(url_for('index', lang=lang))

LANGUAGES = {
    'en': {
        'title': "Reading % Calculator (ZARA)",
        'scan_type': "Scan Type:",
        'select': "-- Select --",
        'all': "All Sections Together",
        'each': "Each Section Separately",
        'reading': "Reading (scanned items):",
        'retail': "Retail (expected items):",
        'man': "MAN",
        'woman': "WOMAN",
        'kids': "KIDS",
        'clothing': "Clothing",
        'shoes': "Shoes",
        'perfumes': "Perfumes",
        'calculate': "Calculate",
        'result': "Result:",
        'err_empty': "All fields are required. Please make sure none are left empty.",
        'err_missing': "Missing value for: {field}. Please enter a number.",
        'err_retail': "Retail value is required. Please enter a number.",
        'err_invalid': "Invalid input. Please enter only numeric values."
    },
    'he': {
        'title': "מחשבון אחוז סריקות (ZARA)",
        'scan_type': "סוג סריקה:",
        'select': "-- בחר --",
        'all': "כל המחלקות יחד",
        'each': "כל מחלקה בנפרד",
        'reading': "כמות שנסרקה:",
        'retail': "כמות צפויה:",
        'man': "גברים",
        'woman': "נשים",
        'kids': "ילדים",
        'clothing': "ביגוד",
        'shoes': "נעליים",
        'perfumes': "בשמים",
        'calculate': "חשב",
        'result': "תוצאה:",
        'err_empty': "יש למלא את כל השדות.",
        'err_missing': "חסר ערך עבור: {field}. יש להכניס מספר.",
        'err_retail': "יש להכניס ערך לריטייל.",
        'err_invalid': "קלט לא תקין. נא להזין מספרים בלבד."
    }
}

HTML_TEMPLATE = """
<!doctype html>
<html lang=\"{{ lang }}\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{{ t['title'] }}</title>
  <style>
    body {
      font-family: 'Helvetica Neue', sans-serif;
      padding: 20px;
      background-color: #f8f8f8;
      color: #111;
      margin: 0;
    }
    .navbar {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 15px;
      background-color: transparent;
    }
    .navbar img {
      height: 102px;
      max-width: 100%;
    }
    h1 {
      font-size: 22px;
      font-weight: 500;
      margin-bottom: 20px;
      text-align: left;
    }
    form {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
    input, select, button {
      padding: 12px;
      margin: 10px 0;
      width: 90%;
      max-width: 320px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 16px;
    }
    select {
      background-color: white;
      appearance: none;
      background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 5'%3E%3Cpath fill='%23444' d='M2 0L0 2h4L2 0zM0 3l2 2 2-2H0z'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 10px center;
      background-size: 10px;
    }
    button {
      background-color: #111;
      color: white;
      cursor: pointer;
      border: none;
    }
    button:hover {
      background-color: #333;
    }
    .section {
      margin-bottom: 25px;
      width: 100%;
      max-width: 360px;
    }
    .error {
      color: red;
      list-style: none;
      padding-left: 0;
    }
    @media (max-width: 480px) {
      h1 {
        font-size: 18px;
      }
      .navbar img {
        height: auto;
        max-height: 90px;
      }
    }
  </style>
</head>
<body>
  <div class=\"navbar\">
    <img src=\"{{ url_for('static', filename='zara-logo.png') }}\" alt=\"ZARA Logo\">
  </div>

  <h1>{{ t['title'] }}</h1>
  <form method=\"get\">
    <input type=\"hidden\" name=\"mode\" value=\"{{ mode if mode else '' }}\">
    <label>Language:</label>
    <select name=\"lang\" onchange=\"this.form.submit()\">
      <option value=\"en\" {% if lang == 'en' %}selected{% endif %}>English</option>
      <option value=\"he\" {% if lang == 'he' %}selected{% endif %}>עברית</option>
    </select>
  </form>

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul class='error'>
      {% for message in messages %}
        <li>{{ message }}</li>
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}

  <form method=\"post\" action=\"/calculate?lang={{ lang }}\">
    <div class=\"section\">
      <label>{{ t['scan_type'] }}</label>
      <select name=\"mode\" required onchange=\"this.form.submit()\">
        <option value=\"\">{{ t['select'] }}</option>
        <option value=\"all\" {% if mode == 'all' %}selected{% endif %}>{{ t['all'] }}</option>
        <option value=\"each\" {% if mode == 'each' %}selected{% endif %}>{{ t['each'] }}</option>
      </select>
    </div>

    {% if mode == 'all' %}
    <div class=\"section\">
      <label>{{ t['reading'] }}</label>
      <input type=\"text\" name=\"reading\" required inputmode=\"numeric\">
      <label>{{ t['retail'] }}</label>
      <input type=\"text\" name=\"retail\" required inputmode=\"numeric\">
    </div>
    {% elif mode == 'each' %}
    <div class=\"section\">
      <h3>{{ t['man'] }}</h3>
      <input type=\"text\" name=\"man_clothing\" placeholder=\"{{ t['clothing'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"man_shoes\" placeholder=\"{{ t['shoes'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"man_perfume\" placeholder=\"{{ t['perfumes'] }}\" required inputmode=\"numeric\">
      <h3>{{ t['woman'] }}</h3>
      <input type=\"text\" name=\"woman_clothing\" placeholder=\"{{ t['clothing'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"woman_shoes\" placeholder=\"{{ t['shoes'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"woman_perfume\" placeholder=\"{{ t['perfumes'] }}\" required inputmode=\"numeric\">
      <h3>{{ t['kids'] }}</h3>
      <input type=\"text\" name=\"kids_clothing\" placeholder=\"{{ t['clothing'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"kids_shoes\" placeholder=\"{{ t['shoes'] }}\" required inputmode=\"numeric\">
      <input type=\"text\" name=\"kids_perfume\" placeholder=\"{{ t['perfumes'] }}\" required inputmode=\"numeric\">
      <h3>{{ t['retail'] }}</h3>
      <input type=\"text\" name=\"retail\" required inputmode=\"numeric\">
    </div>
    {% endif %}

    {% if mode %}
    <button type=\"submit\">{{ t['calculate'] }}</button>
    {% endif %}
  </form>

  {% if result %}
    <h2 style=\"text-align:left;\">{{ t['result'] }} {{ result }}</h2>
  {% endif %}
</body>
</html>
"""

import math


def all_section_calc(reading, retail):
    return f"{math.floor((reading/retail)*100)}% ~ ({math.floor((reading/retail) * 10**3) / 10**3})"


def each_section_calc(data, retail):
    man = data['man_clothing'] + data['man_shoes'] + data['man_perfume']
    woman = data['woman_clothing'] + data['woman_shoes'] + data['woman_perfume']
    kids = data['kids_clothing'] + data['kids_shoes'] + data['kids_perfume']
    total_reading = man + woman + kids
    return all_section_calc(total_reading, retail)


@app.route('/', methods=['GET'])
def index():
    lang = request.args.get('lang', 'en')
    mode = request.args.get('mode', '')
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)


@app.route('/calculate', methods=['POST'])
def calculate():
    lang = request.args.get('lang', 'en')
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    mode = request.form.get('mode')
    result = None

    try:
        if mode == 'all':
            reading = request.form.get('reading')
            retail = request.form.get('retail')
            if not reading or not retail:
                flash(t['err_empty'])
                return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)
            reading = int(reading)
            retail = int(retail)
            result = all_section_calc(reading, retail)

        elif mode == 'each':
            fields = [
                'man_clothing', 'man_shoes', 'man_perfume',
                'woman_clothing', 'woman_shoes', 'woman_perfume',
                'kids_clothing', 'kids_shoes', 'kids_perfume'
            ]
            data = {}
            for f in fields:
                val = request.form.get(f)
                if val is None or val == '':
                    field_label = f.replace('_', ' ').title()
                    flash(t['err_missing'].format(field=field_label))
                    return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)
                data[f] = int(val)
            retail = request.form.get('retail')
            if not retail:
                flash(t['err_retail'])
                return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)
            retail = int(retail)
            result = each_section_calc(data, retail)

    except ValueError:
        flash(t['err_invalid'])
        return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)
    except Exception as e:
        flash(f"Unexpected error: {str(e)}")
        return render_template_string(HTML_TEMPLATE, mode=mode, result=None, t=t, lang=lang)

    return render_template_string(HTML_TEMPLATE, mode=mode, result=result, t=t, lang=lang)


if __name__ == '__main__':
    app.run(debug=True)

#fly io 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)