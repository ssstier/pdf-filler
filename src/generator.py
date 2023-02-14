import pdfrw


#https://github.com/pmaupin/pdfrw/issues/84

def write_fillable_pdf(self, filename, template_path):
        """
        This is a docstring which should describe the function
        :param filename: describe param filename
        :param template_path: describe param template_path
        """
        output_path = self.output_dir + '/' + filename
        template_pdf = pdfrw.PdfReader(template_path)
        template_pdf.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        annotations = template_pdf.pages[0]['/Annots']
        for annotation in annotations:
            if annotation['/Subtype'] == '/Widget':
                if annotation['/T']:
                    key = annotation['/T'][1:-1]
                    if key in self.graphics_dict.keys():
                        annotation.update(pdfrw.PdfDict(
                            V=pdfrw.PdfName('Yes')))
                    if key in self.text_dict.keys():
                        annotation.update(
                            pdfrw.PdfDict(V='{}'.format(self.text_dict[key]))
                        )
        pdfrw.PdfWriter().write(output_path, template_pdf)
        if self.open_after_generation:
            wb.open_new(output_path)
