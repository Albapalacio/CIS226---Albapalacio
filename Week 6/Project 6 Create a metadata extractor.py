import os
from PyPDF2 import PdfReader
import zipfile
import xml.dom.minidom

# suspicious keywords (lowercase for easier matching)
SUSPICIOUS_KEYWORDS = ["metasploit", "maldocgen", "exploit", "payload", "malware", "h4ck3r", "secret"]

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MetadataExtractor:
    def extract_metadata(self) -> None:
        pdf_file = os.path.join(__location__, 'Totally_Safe_File.pdf')
        print("\n[+] Scanning file:", pdf_file, "\n")
        pdf_reader = PdfReader(pdf_file)

        metadata = pdf_reader.metadata
        if metadata:
            print("Metadata for PDF file:")
            for key, value in metadata.items():
                value_str = str(value).lower()  # convert to lowercase for matching
                flag = any(susp in value_str for susp in SUSPICIOUS_KEYWORDS)
                
                if flag:
                    print(f"  {key}: {value}  [SUSPICIOUS]")
                else:
                    print(f"  {key}: {value}")
        else:
            print("No metadata found in this PDF.")

        print("\nEncrypted?:", pdf_reader.is_encrypted)

        # Word metadata
        try:
            docx_file = os.path.join(__location__, 'Totally_Safe_File.docx')
            word_document = zipfile.ZipFile(docx_file)
            word_extraction_path = os.path.join(__location__, 'metadata_extraction_sample_word')
            word_document.extractall(word_extraction_path)

            core_xml_path = os.path.join(word_extraction_path, 'docProps/core.xml')
            if os.path.exists(core_xml_path):
                word_xml = xml.dom.minidom.parse(core_xml_path)
                print('\nMetadata for Word file:\n', word_xml.toprettyxml())
            else:
                print("\nNo core.xml metadata found in Word file.")
        except Exception as e:
            print("Error reading Word file:", e)

if __name__ == "__main__":
    extractor = MetadataExtractor()
    extractor.extract_metadata()
