import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Add cover_status parameter to api_koleksi_list
old_api = """    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = 20"""

new_api = """    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        cover_status = request.args.get('cover_status', 'all')
        per_page = 20"""
app_code = app_code.replace(old_api, new_api)

# Update query construction
old_query = """        query = \"\"\"
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT ? OFFSET ?
        \"\"\"
        cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))
        results = [dict(row) for row in cursor.fetchall()]
        
        total_query = \"\"\"
            SELECT COUNT(DISTINCT b.id)
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?
        \"\"\"
        total = conn.execute(total_query, (f'%{search}%', f'%{search}%', f'%{search}%')).fetchone()[0]"""

new_query = """        where_clause = "(b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?)"
        params = [f'%{search}%', f'%{search}%', f'%{search}%']
        
        if cover_status == 'has_cover':
            where_clause += " AND ((b.image IS NOT NULL AND b.image != '' AND b.image != 'NOT_FOUND') OR (b.isbn IS NOT NULL AND b.isbn != ''))"
        elif cover_status == 'no_cover':
            where_clause += " AND (b.isbn IS NULL OR b.isbn = '') AND (b.image IS NULL OR b.image = '' OR b.image = 'NOT_FOUND')"
            
        query = f\"\"\"
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE {where_clause}
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT ? OFFSET ?
        \"\"\"
        cursor = conn.execute(query, tuple(params + [per_page, offset]))
        results = [dict(row) for row in cursor.fetchall()]
        
        total_query = f\"\"\"
            SELECT COUNT(DISTINCT b.id)
            FROM bibliografi b
            WHERE {where_clause}
        \"\"\"
        total = conn.execute(total_query, tuple(params)).fetchone()[0]"""
app_code = app_code.replace(old_query, new_query)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)


# Update frontend
with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

# Add coverStatus to JS state
old_state = """        searchQuery: '',
        bibliografi: [],"""
new_state = """        searchQuery: '',
        coverStatus: 'all',
        bibliografi: [],"""
html = html.replace(old_state, new_state)

# Add coverStatus to fetch URL
old_fetch = """const res = await fetch('/api/koleksi/list?search=' + encodeURIComponent(this.searchQuery) + '&page=' + page);"""
new_fetch = """const res = await fetch('/api/koleksi/list?search=' + encodeURIComponent(this.searchQuery) + '&cover_status=' + this.coverStatus + '&page=' + page);"""
html = html.replace(old_fetch, new_fetch)

# Add Dropdown to UI
old_search_ui = """            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                <i class="fa-solid fa-magnifying-glass"></i>
            </span>
            <input type="text" x-model="searchQuery" @input.debounce.500ms="loadData(1)" class="w-full border border-stroke rounded pl-10 pr-3 py-2 outline-none focus:border-primary text-black" placeholder="Cari Judul, Pengarang, atau DDC...">
        </div>
    </div>"""
new_search_ui = """            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                <i class="fa-solid fa-magnifying-glass"></i>
            </span>
            <input type="text" x-model="searchQuery" @input.debounce.500ms="loadData(1)" class="w-full border border-stroke rounded pl-10 pr-3 py-2 outline-none focus:border-primary text-black" placeholder="Cari Judul, Pengarang, atau DDC...">
        </div>
        <div>
            <select x-model="coverStatus" @change="loadData(1)" class="border border-stroke rounded px-3 py-2 outline-none focus:border-primary bg-white text-slate-700 font-medium">
                <option value="all">Semua Buku</option>
                <option value="has_cover">? Sudah Bersampul</option>
                <option value="no_cover">? Belum Bersampul</option>
            </select>
        </div>
    </div>"""
html = html.replace(old_search_ui, new_search_ui)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Filter patched")
