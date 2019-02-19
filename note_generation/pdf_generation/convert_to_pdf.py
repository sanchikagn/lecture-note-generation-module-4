import pdfkit
import webbrowser


def converting_pdf(lesson):
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'footer-right': '[page] of [topage]',
    }
    print('Creating PDF File')
    pdfkit.from_file('/home/kasumi/PycharmProjects/LecNote/lecture.html',
                     lesson + '.pdf', options=options)


def open_note(path):
    webbrowser.open_new(path)
