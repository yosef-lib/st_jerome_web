import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

old_logo = '''                    {% set cur_lokasi = request.args.get('lokasi', '') %}
                    {% if cur_lokasi == 'IMAVI' %}
                        <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" alt="IMAVI Logo" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" class="w-12 h-12 rounded-full border-2 border-boxdark2 bg-white object-contain">
                    {% elif cur_lokasi == 'STPD' %}
                        <img src="{{ url_for('static', filename='img/logo_stpd.png') }}" alt="STPD Logo" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" class="w-12 h-12 rounded-full border-2 border-boxdark2 bg-white object-contain">
                    {% else %}
                        <img src="{{ url_for('static', filename='img/logo.jpg') }}" alt="Logo" class="w-12 h-12 rounded-full border-2 border-boxdark2 object-cover">
                    {% endif %}'''

new_logo = '''                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" alt="IMAVI Logo" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" class="w-12 h-12 rounded-full border-2 border-boxdark2 bg-white object-contain">'''

code = code.replace(old_logo, new_logo)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(code)
