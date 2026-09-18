import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

old_biblio_err = '''            } catch (e) {
                  console.error(e); alert("Error");
              }
          },
          async deleteEksemplar'''

new_biblio_err = '''            } else {
                  const txt = await res.text();
                  alert("Gagal hapus buku. Server: " + res.status + " - " + txt.substring(0, 200));
              }
          } catch (e) {
              console.error(e); alert("Error hapus buku: " + e.message);
          }
        },
          async deleteEksemplar'''

code = code.replace(old_biblio_err, new_biblio_err)

old_eks_err = '''            } catch (e) {
                  console.error(e); alert("API Error: " + (e.message || e));
              }
          },
  
          async loadData'''

new_eks_err = '''            } else {
                  const txt = await res.text();
                  alert("Gagal hapus barcode. Server: " + res.status + " - " + txt.substring(0, 200));
              }
          } catch (e) {
              console.error(e); alert("Error hapus barcode: " + e.message);
          }
        },
  
          async loadData'''

code = code.replace(old_eks_err, new_eks_err)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Better error reporting added")
