import fitz
import re
import docx
import textract


def parse_pdf_hh_resume(path_to_file: str = 'module_1/data/resume.pdf') -> dict:
    '''
    Функция парсит резюме в формате pdf, извлекая данные о соискателе
    
    Parameters
    ----------
    path_to_file : str
        путь к резюме
    '''
    try:
        pdf_document = fitz.open(path_to_file)
        full_text = ''
        images_list = []
        for page_index in range(pdf_document.page_count):
            page = pdf_document[page_index]
            
            text = page.get_text("text")
            full_text += text
            images = page.get_images(full=True)
            
            for image_index, image in enumerate(images):
                if image_index == 0: continue       ## пропускаем логотип hh
                xref = image[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_path = 'pg{}_resume_image{}.png'.format(page_index+1, image_index)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                    images_list.append(image_path)
    except Exception as e:
        print(f"Ошибка при обработке файла {path_to_file}: {e}")
        return None

    dct_result = data_process(full_text=full_text)
    dct_result['Images'] = images_list

    return dct_result


def parse_docx_hh_resume(path_to_file: str = 'module_1/data/resume.docx') -> dict:
    '''
    Функция парсит текст из файла .docx.

    Parameters
    ----------
    file_path : str
        Путь к файлу .docx.
    '''
    try:
        doc = docx.Document(path_to_file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        full_text = '\n'.join(full_text)
    except Exception as e:
        print(f"Ошибка при обработке файла {path_to_file}: {e}")
        return None
    
    dct_result = data_process(full_text=full_text)    

    return dct_result


def parse_doc_hh_resume(path_to_file: str = 'module_1/data/resume.docx') -> dict:
    try:
        text = textract.process(path_to_file, input_encoding='UTF-8').decode('utf-8')
    except Exception as e:
        print(f"Ошибка при обработке файла {path_to_file}: {e}")
        return None
    
    dct_result = data_process(full_text=text)    

    return dct_result


def data_process(full_text: str) -> dict:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.search(email_pattern, full_text)
    email = email.group(0) if email else None

    city_pattern = r'Проживает: (.+)'
    city = re.search(city_pattern, full_text)
    city = city.group(1) if city else None
    if '\xa0' in city:
        city = city.replace('\xa0', ' ')
    idx_nationality = city.find('Гражданство')
    if idx_nationality != -1:
        city = city[:idx_nationality-1]

    position_pattern = r'Желаемая должность и зарплата[\t\n]{0,3}(.+)\n'
    position = re.search(position_pattern, full_text)
    position = position.group(1) if position else None

    experience_pattern = r'Опыт работы — (.+)'
    experience = re.search(experience_pattern, full_text)
    experience = experience.group(1) if experience else None
    if '\t' in experience:
        experience = experience.replace('\t', '')

    return {'Email': email,
            'City': city,
            'Position': position,
            'Experience': experience}
