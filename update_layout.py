with open('templates/layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''                    <div>
                        <h3 class="mb-4 ml-4 text-sm font-semibold text-bodydark2 uppercase tracking-wider">Ekspor Data</h3>
                        <ul class="mb-6 flex flex-col gap-1.5">
                            <li>
                                <a href="/export_biblio" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-bodydark duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                    <i class="fa-solid fa-file-export w-5 text-center"></i> Ekspor Bibliografi
                                </a>
                            </li>
                            <li>
                                <a href="/export_item" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-bodydark duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                    <i class="fa-solid fa-file-csv w-5 text-center"></i> Ekspor Item
                                </a>
                            </li>
                        </ul>
                    </div>'''

new_block = '''                    <div>
                        <h3 class="mb-4 ml-4 text-sm font-semibold text-bodydark2 uppercase tracking-wider">Ekspor & Impor Data</h3>
                        <ul class="mb-6 flex flex-col gap-1.5">
                            <li>
                                <a href="/import_slims" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/import_slims' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-cloud-arrow-up w-5 text-center"></i> Sinkronisasi SLiMS
                                </a>
                            </li>
                            <li>
                                <a href="/export_biblio" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-bodydark duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                    <i class="fa-solid fa-file-export w-5 text-center"></i> Ekspor Bibliografi
                                </a>
                            </li>
                            <li>
                                <a href="/export_item" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-bodydark duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                    <i class="fa-solid fa-file-csv w-5 text-center"></i> Ekspor Item
                                </a>
                            </li>
                        </ul>
                    </div>'''

content = content.replace(old_block, new_block)

with open('templates/layout.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done layout")
