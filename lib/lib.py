import os
import pymupdf


ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
USER_DIR = os.path.join(ROOT_DIR, 'user')
INPUT_DIR = os.path.join(USER_DIR, 'input')
OUTPUT_DIR = os.path.join(USER_DIR, 'output')


def input_path(file_name: str):
    """
    Get a PDF from the input directory.

    Do not include '.pdf' in the file name.
    """
    return os.path.join(INPUT_DIR, f'{file_name}.pdf')


def output_path(file_name: str):
    """
    Get a txt file from the output directory.

    Do not include '.txt' in the file name.
    """
    return os.path.join(OUTPUT_DIR, f'{file_name}.txt')


def open_input_file(file_name: str):
    """
    Open a file from the input directory as a PyMuPDF Document.
    """
    return pymupdf.open(input_path(file_name))


def open_output_file(file_name: str):
    """
    Open a file from the output direcotry as a regular file.
    """
    return open(output_path(file_name), 'w')


def extract_pdf_text(file_name: str):
    """
    Get all text information from an input file.
    """
    document = open_input_file(file_name)
    page_texts = []
    for page in document:
        page_texts.append(page.get_text('words'))
    return page_texts


def extract_pdf_annotations(file_name: str):
    """
    Get all annotation data from an input file.
    """
    document = open_input_file(file_name)
    page_annotations = []
    for page in document:
        annotation_objects = []
        for annotation in page.annots():
            annotation_objects.append({
                'type': annotation.type,
                'rect': annotation.rect,
                'quadpoints': annotation.vertices
            })
        page_annotations.append(annotation_objects)
    return page_annotations


def check_text_bounded(text_edges, quad_edges, margins=(5, 5, 5, 5)):
    """
    Check whether a text rect lies within another rect.

    Edge order: left, top, right, bottom.
    """
    return text_edges[0] > quad_edges[0] - margins[0] and \
        text_edges[1] > quad_edges[1] - margins[1] and \
        text_edges[2] < quad_edges[2] + margins[2] and \
        text_edges[3] < quad_edges[3] + margins[3]


def extract_annotated_text(file_name: str):
    """
    Extract all highlighted text from an input file.
    """
    page_text_datas = extract_pdf_text(file_name)
    page_annotation_datas = extract_pdf_annotations(file_name)
    page_count = len(page_text_datas)

    output_data = []

    # Iterate through pages

    for p in range(page_count):
        text_data = page_text_datas[p]
        annotation_data = page_annotation_datas[p]

        if len(annotation_data) == 0:
            output_data.append([])
            continue

        annotation_data = sorted(annotation_data, key=lambda data: (data['quadpoints'][0][1], data['quadpoints'][0][0]))

        extracted_text = []

        for annotation in annotation_data:
            quad_count = int(len(annotation['quadpoints']) / 4)
            extracted_lines = []

            for quad_points in [annotation['quadpoints'][q * 4:q * 4 + 4] for q in range(quad_count)]:
                quad_edges = [*quad_points[0], *quad_points[3]]
                extracted_words = []

                for text in text_data:
                    text_edges = text[:4]
                    if check_text_bounded(text_edges, quad_edges):
                        extracted_words.append(text[4])

                extracted_lines.append(' '.join(extracted_words))

            extracted_text.append(' '.join(extracted_lines))

        output_data.append(extracted_text)

    return output_data


def write_annotated_text(file_name, output_data):
    """
    Writes extracted annotation text data to the specified output file.
    """
    output_file = open_output_file(file_name)
    output_file.write('\n\n----------\n\n'.join(f'PAGE {p + 1}\n\n{'\n\n'.join(output_data[p])}' for p in range(len(output_data))))
    output_file.close()