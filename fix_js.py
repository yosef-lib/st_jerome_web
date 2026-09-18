import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

# Remove DOMContentLoaded wrapper
old_start = '''<script>
document.addEventListener("DOMContentLoaded", function() {
    const ddcData = ['''

new_start = '''<script>
(function() {
    const ddcData = ['''

old_end = '''    }
});
</script>'''

new_end = '''    }
})();
</script>'''

html = html.replace(old_start, new_start)
html = html.replace(old_end, new_end)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)
print("Removed DOMContentLoaded wrapper.")
