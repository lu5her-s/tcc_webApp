from docx import Document
import subprocess


class DocxFiller:
    def __init__(self, template_path: str, output_path: str, data: dict):
        self.template_path = template_path
        self.output_path = output_path
        self.data = data

    def fill_document(self):
        """
        fill the word document with the data
        """
        document = Document(self.template_path)

        paragraphs_to_delete = []
        for paragraph in document.paragraphs:
            for key, value in self.data.items():
                if key in paragraph.text:
                    if value is not None and value != "":
                        for run in paragraph.runs:
                            run.text = run.text.replace("{" + key + "}", value)
                    else:
                        paragraphs_to_delete.append(paragraph)

        # Delete marked paragraphs in reverse order to avoid index shifting
        for paragraph in reversed(paragraphs_to_delete):
            paragraph._element.getparent().remove(paragraph._element)

        document.save(self.output_path)

    def convert_to_pdf(self):
        """Converts a file to PDF using LibreOffice.

        This function uses the `libreoffice` command-line tool to convert a file to PDF.
        The file can be any type that LibreOffice can open, such as DOCX, XLSX, or PPTX.

        Args:
          file_path: The path to the file to convert.

        Raises:
          subprocess.CalledProcessError: If the `libreoffice` command fails.
        """

        try:
            subprocess.run(
                ["libreoffice", "--headless", "--convert-to", "pdf", self.output_path]
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert file: {e}")


if __name__ == "__main__":
    data = {
        "urgency": "ด่วนที่สุด",
        "sector": "ฝสส.มทบ.๒๙",
        "telephone": "ทบ. ๒๑๑๔๖",
        "doc_no": "๐๔๘๒.๗๗/๑๒๓",
        "date": "๑ ต.ค. ๖๗",
        "title": "ขอทดสอบระบบสร้างเอกสาร",
        "open_doc": "ผบ.มทบ.๒๙",
        "topic_1": "ฝสส.มทบ.๒๙ ขอทดสอบระบบการสร้างเอกสารจากการใช้แบบฟอร์มสำเร็จรูป กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก",
        "topic_2": "เพื่อใช้สำหรับระบบสารบรรณอิเล็กทรอนิกส์ ฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟฟ",
        # "topic_2": "",
        "topic_3": "เพื่อขออนุมัติการใช้งาน ฟฟฟฟฟฟฟฟฟฟฟฟฟ.-",
        "choice_1": "1. aaaaaaaaaaaaaaaaaaa",
        "choice_2": "2. bbbbbbbbbbbbbbbbbbb",
        # "choice_3": "3. ccccccccccccccccc",
        "choice_3": "",
        "close_doc": "จึงเรียนมาเพื่อกรุณาพิจารณา",
        "name": "กฤษดา",
        "last_name": "สุวรรณเทน",
        "position": "ผช.ฝสส.มทบ.๒๙ ทกท.ฯ",
    }
    if data["urgency"] == "ด่วนที่สุด":
        template_path = "tpl_urgency.docx"
    else:
        template_path = "tpl.docx"
    output_path = f"{data['title']}.docx"
    docx_filler = DocxFiller(template_path, output_path, data)
    docx_filler.fill_document()
    docx_filler.convert_to_pdf()
