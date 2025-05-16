from get_file_folder_id import get_folder_id_from_path
from file_retriever import main_worker, ocr_worker
from creds_manager import loader_func
from unstructured.partition.pdf import partition_pdf
from splitter import split_pdf_pages_vertically_reordered_to_bytes

def main(folder_path,chapter_detection,exact_chapter_cut,book_type="main",book_query="full-book",half_it=False, footer_detection="Compiled by",footer_ocr="Insights"):
    file_folder_id=get_folder_id_from_path(folder_path,book_query)
    pdf_io=loader_func(file_folder_id[1])
    if book_type == "main":
        elements = partition_pdf(file=pdf_io, strategy="auto")
        docs=main_worker(elements,chapter_detection,exact_chapter_cut=exact_chapter_cut,footer_detection=footer_detection)
        print(docs)
    elif book_type=="ocr":
        if half_it:
            pdf_io=split_pdf_pages_vertically_reordered_to_bytes(pdf_io)
        elements = partition_pdf(file=pdf_io, strategy="hi_res")
        docs=ocr_worker(elements,footer=footer_ocr)
    return None

main("IOE/BCT/4/Instrumentation","Microprocessors Chapter",28,book_type="ocr",footer_ocr="Insights on Instrumentation System")