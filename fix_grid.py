import codecs

with codecs.open('templates/analisis_lanjutan.html', 'r', 'utf-8') as f:
    content = f.read()

# Add a closing div before C. ANALISIS PERPUTARAN
content = content.replace(
    '<!-- C. ANALISIS PERPUTARAN & DORMAN (Legacy) -->',
    '    </div>\n\n    <!-- C. ANALISIS PERPUTARAN & DORMAN (Legacy) -->'
)

# And remove one closing div from the end to balance it out
content = content.replace(
    '    </div>\n</div>\n{% endblock %}',
    '</div>\n{% endblock %}'
)

with codecs.open('templates/analisis_lanjutan.html', 'w', 'utf-8') as f:
    f.write(content)

print("Grid fixed")
