import os, io, datetime
from creds_manager import get_drive_service
from unstructured.chunking.title import chunk_by_title
from googleapiclient.http import MediaIoBaseDownload
from unstructured.staging.base import elements_from_base64_gzipped_json
from test_cuda import create_embedding

def clean_text(text,watermark):
    text = text.strip()
    if not text or watermark in text:
        return None
    return text

def loader_func(file_id):
    drive_service = get_drive_service()
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

def main_worker(elements, chapter_detection,footer_detection, exact_chapter_cut=0):
    print(exact_chapter_cut)
    docs = []
    all_data={}
    chapter_text = []
    current_chapter_title = None
    output_folder = "test_chunks"
    os.makedirs(output_folder, exist_ok=True)

    def chunk_structured(elems,name,exact_chapter_cut=exact_chapter_cut):
        if not name or not elems:
            return
        chunks = chunk_by_title(elems, multipage_sections=True,max_characters=1000,combine_text_under_n_chars =850)
        # filename = name.replace(":", "").replace("/", "-").strip() + ".txt"
        # filepath = os.path.join(output_folder, filename)
        print(len(chunks))
        all_data[name[exact_chapter_cut:]]=list(chunks)
        # with open(filepath, "w", encoding="utf-8") as f:
        #     for chunk in chunks:
        #         metadata = chunk.metadata.to_dict()
        #         orig_elements = elements_from_base64_gzipped_json(metadata["orig_elements"])
        #         ok=[orig_element.category for orig_element in orig_elements]
        #         f.write(chunk.text + "\n\n" +str(ok)+"---------------------------------------------------------"+"\n\n")
    
    for doc in elements:
        content = doc.text.strip()
        if not content:
            continue
        if chapter_detection in content and content != current_chapter_title:
            print(current_chapter_title)
            chunk_structured(chapter_text,current_chapter_title)
            current_chapter_title = content
            docs.append(current_chapter_title[exact_chapter_cut:])
            chapter_text = []  # Reset chapter buffer
            print(f"\n New chapter: {current_chapter_title}")
        else:
            if doc.category != "Header" and footer_detection not in doc.text :
                chapter_text.append(doc)
    chunk_structured(chapter_text,current_chapter_title)
    
    return [docs,all_data]

def ocr_worker(elements,footer,watermark="CamScanner"):
    filtered_elements = []
    for el in elements:
       if getattr(el, "category", None) != "Image" and watermark not in el.text:
            el.text=el.text.replace(footer,'') .strip()
            el.text=el.text.replace(footer.lower(),'') .strip()
            filtered_elements.append(el)

    chunks = chunk_by_title(filtered_elements, multipage_sections=True,max_characters=1000,combine_text_under_n_chars =850)
    # Save results
    count=0
    with open(os.path.join(os.path.dirname(__file__),'test_chunks/test-ocrrrr.txt'), "w", encoding="utf-8") as f:
        print(datetime.datetime.now())
        for chunk in chunks:
            metadata = chunk.metadata.to_dict()
            print(metadata)
            print(metadata['page_number'])
            create_embedding(chunk.text)
            f.write(chunk.text + "\n\n" +str(metadata['page_number'])+"---------------------------------------------------------"+"\n\n")
            count+=1
            if count == 3:
                print(datetime.datetime.now())
                break
    return None
