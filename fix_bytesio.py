import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

app_code = app_code.replace("output = BytesIO()\\n    with pd.ExcelWriter", "from io import BytesIO\\n    output = BytesIO()\\n    with pd.ExcelWriter")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
