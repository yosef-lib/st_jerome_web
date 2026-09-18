import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

# Remove the outer <tbody> and </tbody> that surrounds the <template>
code = code.replace('<tbody>\n                <template x-for="b in bibliografi" :key="b.id">', '<template x-for="b in bibliografi" :key="b.id">')
code = code.replace('</template>\n                <tr x-show="bibliografi.length === 0 && !isLoading">', '</template>\n            <tbody>\n                <tr x-show="bibliografi.length === 0 && !isLoading">')

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed tbody nesting")
