import codecs

with codecs.open('templates/sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

# Update the catch block in fetchMember
old_catch1 = '''} catch (err) {
                this.showAlert('error', 'Error Jaringan', 'Gagal terhubung ke server.');
            }'''
new_catch1 = '''} catch (err) {
                this.showAlert('error', 'Error Sistem', 'Error: ' + err.message + ' (Pastikan Anda sudah restart server PM2)');
            }'''
html = html.replace(old_catch1, new_catch1)

with codecs.open('templates/sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
