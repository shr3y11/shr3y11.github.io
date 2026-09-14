# Shrey — Cybersecurity Portfolio

Source for [shr3y11.github.io](https://shr3y11.github.io), a static portfolio focused on governance, risk, compliance, and practical security engineering.

The site deploys directly through GitHub Pages, with no build step. The résumé overlay lazy-loads a local copy of Mozilla PDF.js (6.3.289, Apache-2.0) when opened. Its license is in `assets/vendor/pdfjs/LICENSE`.

The public résumé is generated from `tools/build_resume.py` using ReportLab and pypdf. Run the builder to update the PDF, then render its first page with Poppler to `assets/resume/shreeyash-wale-resume.png` for the fallback preview. Education, employment history, and career-plan completion dates still need confirmation before adding them to the résumé.
