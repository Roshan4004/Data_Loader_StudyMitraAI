import pymupdf
import io

def split_pdf_pages_vertically_reordered_to_bytes(file_obj):
    try:
        file_obj.seek(0)
        doc = pymupdf.open(stream=file_obj.read(), filetype="pdf")
        new_doc = pymupdf.open()

        for page in doc:
            page_height = page.rect.height
            page_width = page.rect.width
            mid_x = page_width / 2

            left_rect = pymupdf.Rect(0, 0, mid_x, page_height)
            right_rect = pymupdf.Rect(mid_x, 0, page_width, page_height)

            left_page = new_doc.new_page(width=mid_x, height=page_height)
            left_page.show_pdf_page(left_page.rect, doc, page.number, clip=left_rect)

            right_page = new_doc.new_page(width=mid_x, height=page_height)
            right_page.show_pdf_page(right_page.rect, doc, page.number, clip=right_rect)

        output_stream = io.BytesIO()
        new_doc.save(output_stream)
        output_stream.seek(0)

        print(f"PDF successfully split and returned as BytesIO stream.")
        return output_stream

    except Exception as e:
        print(f"Error: {e}")
        return None
