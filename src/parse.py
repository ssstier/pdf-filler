import pdfrw
from pdfrw.objects.pdfstring import PdfString
import os
import generator


class Parser:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def parser(self, prefix, delimiters=None):
        if delimiters is None:
            try:
                return self.raw_data.split(prefix)[1].split()[0]
            except (IndexError, ValueError):
                return ""
        for delimiter in delimiters:
            try:
                x = self.raw_data.split(prefix)[1].split()[0:10]
                y = " ".join(x[0:x.index(delimiter)])
            except IndexError:
                continue
            except ValueError:
                return ""
            if y:
                return y
            return ""

    def build_data(self):
        text_dict = {"Name": self.parser("name?", ["Where"]),
                     "Address": self.parser("live?", ["What"]),
                     "City": self.parser("What city is this?", ["What"]),
                     "State": self.parser("What state is this?"),
                     "License Checkbox": None, "Gender List box": None,
                     "Radiobox": self.parser("employment status?"),
                     "Language Listbox": None}

        gender = self.parser("What is your gender?").lower()
        if gender == "male":
            text_dict["Gender List Box"] = "Male"
        elif gender == "female":
            text_dict["Gender List Box"] = "Female"

        drivers_license = self.parser("license (y/n)?").lower()
        if drivers_license[0] == 'y':
            text_dict["License Checkbox"] = True

        choices = {"English", "Spanish", "French", "Russian"}
        response = set(self.parser("What languages do you speak?",
                                   ["EOF"]).title().split())

        print(list(choices & response))
        text_dict["Language Listbox"] = list(choices & response)

        return text_dict
