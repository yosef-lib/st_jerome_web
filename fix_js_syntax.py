import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

bad_js = """                                }
                            } else {
                                await fetch('/api/buku/save_cover', {
                                    method: 'POST', headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                                });
                            }
                        } else {
                            await fetch('/api/buku/save_cover', {
                                method: 'POST', headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                            });
                        }
                            }
                        }
                    } catch(e) {"""

good_js = """                                }
                            } else {
                                await fetch('/api/buku/save_cover', {
                                    method: 'POST', headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                                });
                            }
                        } else {
                            await fetch('/api/buku/save_cover', {
                                method: 'POST', headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                            });
                        }
                    } catch(e) {"""

html = html.replace(bad_js, good_js)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)

print("JS syntax fixed")
