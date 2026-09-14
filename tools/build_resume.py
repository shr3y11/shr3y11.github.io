"""Build the public one-page resume from confirmed portfolio information."""
from pathlib import Path
from shutil import copyfile

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output' / 'pdf' / 'shreeyash-wale-resume.pdf'
PUBLIC = ROOT / 'assets' / 'resume'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
PUBLIC.mkdir(parents=True, exist_ok=True)

styles = {
    'name': ParagraphStyle('name', fontName='Times-Bold', fontSize=27, leading=31, alignment=TA_CENTER),
    'contact': ParagraphStyle('contact', fontName='Times-Roman', fontSize=10, leading=14, alignment=TA_CENTER),
    'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=10.5, leading=13.6, spaceAfter=5),
    'entry': ParagraphStyle('entry', fontName='Times-Roman', fontSize=10.6, leading=14, spaceAfter=3),
    'bullet': ParagraphStyle('bullet', fontName='Times-Roman', fontSize=10.5, leading=13.6, leftIndent=11, firstLineIndent=-8, spaceAfter=4),
    'section': ParagraphStyle('section', fontName='Times-Bold', fontSize=12.5, leading=15, spaceBefore=10, spaceAfter=3),
}

def p(text, kind='body'):
    return Paragraph(text, styles[kind])

def section(title):
    return [p(title.upper(), 'section'), HRFlowable(width='100%', thickness=.6, color=colors.black), Spacer(1, 6)]

def bullet(text):
    return p('&#8226; ' + text, 'bullet')

story = [
    p('Shreeyash Wale', 'name'),
    p('<link href="mailto:shrey051106@gmail.com">shrey051106@gmail.com</link> | '
      '<link href="https://www.linkedin.com/in/shreeyashwale/">linkedin.com/in/shreeyashwale</link> | '
      '<link href="https://github.com/shr3y11">github.com/shr3y11</link>', 'contact'),
    p('<link href="https://shr3y11.github.io/">shr3y11.github.io</link> | '
      '<link href="https://orcid.org/0009-0000-3501-5438">ORCID: 0009-0000-3501-5438</link>', 'contact'),
]

story += section('Profile')
story += [p('eJPT-certified security practitioner pursuing opportunities in technical governance, risk and compliance (GRC), cyber risk, and security assurance. Practical project experience in Windows configuration assessment, Python and PowerShell tooling, structured evidence collection, and security reporting. Interested in connecting technical findings with business-risk decisions.')]

story += section('Technical Skills')
story += [
    p('<b>Languages and scripting:</b> Python, PowerShell, SQL'),
    p('<b>Platforms and tools:</b> Windows, Linux, Git, GitHub, SQLite, Tkinter, PyInstaller'),
    p('<b>Security:</b> Penetration-testing fundamentals, host and network assessment, web security fundamentals'),
    p('<b>Assessment and evidence:</b> Configuration checks, structured JSON evidence, assessment scoring, HTML reports'),
]

story += section('Project Experience')
story += [
    p('<b>SecureAudit</b> | Python, PowerShell, SQLite, Tkinter, PyInstaller', 'entry'),
    p('<i>Windows technical configuration assessment tool</i> | <link href="https://github.com/shr3y11/SecureAudit">github.com/shr3y11/SecureAudit</link>', 'entry'),
    bullet('Built a local Windows desktop workflow to select approved controls, run checks, collect structured evidence, and generate standalone HTML assessment reports.'),
    bullet('Implemented five baseline checks covering Windows Firewall, Microsoft Defender, BitLocker, the built-in Guest account, and SMBv1.'),
    bullet('Restricted PowerShell execution to an approved catalog with path validation, timeouts, JSON parsing, and check-ID validation.'),
    bullet('Separated Pass, Fail, and Error outcomes; calculated assessment score and coverage, and stored scan history in SQLite for review.'),
    bullet('Packaged the application with PyInstaller and validated the development build with 89 automated tests. Documented scope as a point-in-time technical assessment.'),
]

story += section('Certifications and Training')
story += [
    p('<b>Junior Penetration Tester (eJPT)</b> - INE Security | May 2026', 'entry'),
    p('Hands-on certification in assessment methodology, host and network auditing, and penetration testing.<br/>Valid through May 2029 | ID: 181937915 | <link href="https://www.credential.net/cb80ab6a-9d09-4139-83dc-7a674bad2b0a">Verify credential</link>'),
    Spacer(1, 3),
    p('<b>Web Fundamentals Learning Path</b> - TryHackMe | August 2025', 'entry'),
    p('Completed 21 hours 20 minutes of coursework. | <link href="https://tryhackme-certificates.s3-eu-west-1.amazonaws.com/THM-AS5R8PKVHB.pdf">Credential: THM-AS5R8PKVHB</link>'),
    Spacer(1, 3),
    p('<b>Pre Security Learning Path</b> - TryHackMe | July 2025', 'entry'),
    p('Completed 7 hours 38 minutes of coursework. | <link href="https://tryhackme-certificates.s3-eu-west-1.amazonaws.com/THM-ZLASOIP0HW.pdf">Credential: THM-ZLASOIP0HW</link>'),
]

story += section('Research Interests')
story += [p('Risk-based control prioritization; relationships between NIST CSF, ISO/IEC 27001, and CIS Controls; cloud governance; enterprise AI risk and third-party cyber risk.')]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=40, leftMargin=40, topMargin=32, bottomMargin=32,
                        title='Shreeyash Wale - Resume', author='Shreeyash Wale')
doc.build(story)
reader = PdfReader(str(OUTPUT))
assert len(reader.pages) == 1, f'Expected one page, got {len(reader.pages)}'
assert 'Shreeyash Wale' in reader.pages[0].extract_text()
copyfile(OUTPUT, PUBLIC / OUTPUT.name)
print(f'Created {OUTPUT} (one page, selectable text)')
