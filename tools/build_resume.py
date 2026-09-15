"""Compatibility notice for the retired ReportLab resume builder."""

if __name__ == '__main__':
    raise SystemExit(
        'The resume now uses LaTeX to match the supplied template. '
        'Compile assets/resume/shreeyash-wale-resume.tex with pdfLaTeX or Tectonic, '
        'then render and inspect the PDF before updating the public assets. '
        'See README.md. No files were changed.'
    )
