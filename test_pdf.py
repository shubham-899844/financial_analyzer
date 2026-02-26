from tools import read_pdf_raw

content = read_pdf_raw("TSLA-Q2-2025-Update.pdf")

print(content[:1000])