# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.


from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path

from createfiles.createfiles import write_toc


@dataclass
class SopWriter:
    filepath: Path
    family: str
    controls: dict
    config: dict
    title: str

    def create_file(self):
        """
        Create a file stream to be used to be written to the markdown files.
        """
        try:
            self.output_file = StringIO()
            self.__write_header()
            self.__write_purpose()
            self.__write_scope()
            self.__write_controls()
            self.__write_file()
        finally:
            self.output_file.close()

    def __write_file(self):
        """
        Write the file with the table of contents to the filesystem.
        """
        print(f"Writing file to {self.filepath}")
        with open(self.filepath, "w+") as md:
            print(self.output_file.getvalue(), file=md)
        write_toc(self.filepath)

    def __write_header(self):
        """
        Add the page header with generation date and TOC placeholder.
        """
        self.output_file.write(f"# {self.title}\n\n")
        self.output_file.write(f"*Reviewed and updated {date.today()}*\n\n")
        self.output_file.write("----\n")
        self.output_file.write("**Table of Contents**")
        self.output_file.write("\n<!--TOC-->\n---\n\n")
        self.output_file.write("## Introduction\n\n")

    def __write_purpose(self):
        self.output_file.write("### Purpose\n\n")
        self.output_file.write(self.config.get("sop").get(self.family).get("purpose"))
        self.output_file.write("\n\n")

    def __write_scope(self):
        self.output_file.write("### Scope\n\n")
        self.output_file.write(self.config.get("sop").get(self.family).get("scope"))
        self.output_file.write("\n\n")

    def __write_controls(self):
        """
        Write the controls to the file stream.
        """
        self.output_file.write("## Standards\n\n")
        for control_id, control in self.controls.items():
            self.output_file.write(f"### {control_id}\n\n")
            self.__write_text(control)
            self.__write_parts(control)

    def __write_text(self, control: dict):
        """
        Write the non-parts control narrative text.

        :param control: a dictionary of control narratives.
        """
        text = control.get("text", None)
        if text:
            prose = "\n\n".join(text)
            self.output_file.write(f"{prose}\n\n")

    def __write_parts(self, control: dict):
        """
        Write the control parts narrative text.

        :param control: a dictionary of control narratives.
        """
        for part, text in control.items():
            if part != "text":
                prose = "\n\n".join(text)
                self.output_file.write(f"**{part}.**\t{prose}\n")
