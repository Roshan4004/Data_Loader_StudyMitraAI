from get_file_folder_id import get_folder_id_from_path
from file_retriever import main_worker, ocr_worker
from creds_manager import loader_func
from unstructured.partition.pdf import partition_pdf
from splitter import split_pdf_pages_vertically_reordered_to_bytes
import os

def main(folder_path,chapter_detection,exact_chapter_cut,book_type="main",book_query="main",half_it=False, footer_detection="Compiled by",footer_ocr="Insights"):
    file_folder_id=get_folder_id_from_path(folder_path,book_query)
    pdf_io=loader_func(file_folder_id[1])
    if book_type == "main":
        elements = partition_pdf(file=pdf_io, strategy="hi_res")
        docs=main_worker(elements,chapter_detection,exact_chapter_cut=exact_chapter_cut,footer_detection=footer_detection)
        print(docs)
        with open(os.path.join(os.path.dirname(__file__),'test_chunks/test-mainn.txt'), "w", encoding="utf-8") as f:
            for ok in docs[1]["Introduction"]:
                print(ok.text+"\n\n")
                print("Page Number:"+str(ok.metadata.page_number)+"\n\n")
                f.write(f'{str(ok.text)}--------------{ok.metadata.page_number}--\n\n')
    elif book_type=="ocr":
        print("HII")
        if half_it:
            pdf_io=split_pdf_pages_vertically_reordered_to_bytes(pdf_io)
        elements = partition_pdf(file=pdf_io, strategy="hi_res")
        print(len(elements))
        docs=ocr_worker(elements,footer=footer_ocr)
        print(docs)
        with open(os.path.join(os.path.dirname(__file__),'test_chunks/test-ocr.txt'), "w", encoding="utf-8") as f:
            f.write(str(docs))
    return None

main("IOE/BCT/4/Microprocessor","Microprocessors Chapter",exact_chapter_cut=28,book_type="main",footer_ocr="Insights on Instrumentation System")