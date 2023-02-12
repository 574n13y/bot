from weasyprint import HTML
HTML('http://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf')
