import codecs

with codecs.open('handover_st_jerome.md', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace("- [ ] Phase 3: Kataloging Pintar (AI Metadata Assistant)", "- [x] Phase 3: Kataloging Pintar (AI Metadata Assistant)")

with codecs.open('handover_st_jerome.md', 'w', 'utf-8') as f:
    f.write(text)
