from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path

from createfiles.createfiles import write_toc


@dataclass
class SopWriter:
    filepath: Path
    controls: dict
    title: str

    def create_file(self):
        try:
            self.output_file = StringIO()
            self.__write_header()
            self.__write_introduction()
            self.__write_controls()
            self.__write_file()
        finally:
            self.output_file.close()

    def __write_file(self):
        print(f"Writing file to {self.filepath}")
        with open(self.filepath, "w+") as md:
            print(self.output_file.getvalue(), file=md)
        write_toc(self.filepath)

    def __write_header(self):
        self.output_file.write(f"# {self.title}\n\n")
        self.output_file.write(f"*Reviewed and updated {date.today()}*\n\n")
        self.output_file.write("----\n")
        self.output_file.write("**Table of Contents**")
        self.output_file.write("\n<!--TOC-->\n---\n\n")

    def __write_introduction(self):
        self.output_file.write("# Introduction\n\n")
        self.output_file.write("## Purpose\n\n")
        self.output_file.write("## Scope\n\n")
        self.output_file.write("## Standards\n\n")

    def __write_controls(self):
        for control_id, control in self.controls.items():
            self.output_file.write(f"### {control_id}\n\n")
            self.__write_text(control)
            self.__write_parts(control)

    def __write_text(self, control: dict):
        text = control.get("text", None)
        if text:
            prose = "\n\n".join(text)
            self.output_file.write(f"{prose}\n\n")

    def __write_parts(self, control: dict):
        for part, text in control.items():
            if part != "text":
                prose = "\n\n".join(text)
                self.output_file.write(f"{part}.\t{prose}\n")
