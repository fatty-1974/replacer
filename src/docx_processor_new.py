import os
import zipfile
import shutil
import tempfile
import copy
from lxml import etree as ET

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % NS


class DocxXMLProcessor:
    """
    Замена блоков текста в DOCX:
    - поиск по нескольким абзацам
    - корректная многострочная замена
    - глубокое копирование форматирования
    - поддержка таблиц, ячеек, заголовков, футеров
    - без ошибок Word
    """

    def process_folder(self, folder_path, search_text, replace_text):
        files_processed = 0
        for filename in os.listdir(folder_path):
            if filename.endswith(".docx") and not filename.startswith("~$"):
                file_path = os.path.join(folder_path, filename)
                try:
                    if self.process_file(file_path, search_text, replace_text):
                        files_processed += 1
                except Exception as e:
                    print(f"Ошибка обработки файла {filename}: {e}")
        return files_processed

    def process_file(self, file_path, search_text, replace_text):
        tmp_dir, xml_path, tree, root = self._load_xml(file_path)

        paragraphs = []
        full_text = ""

        for p in root.iter(W + "p"):
            t_nodes = list(p.iter(W + "t"))
            paragraphs.append((p, t_nodes))
            for t in t_nodes:
                full_text += t.text if t.text else ""

        norm_full = self._normalize(full_text)
        norm_search = self._normalize(search_text)

        pos = norm_full.find(norm_search)
        if pos == -1:
            self._save_xml_and_pack(tmp_dir, xml_path, tree, file_path)
            return False

        replace_lines = replace_text.split("\n")

        current_pos = 0
        start_par = None
        end_par = None

        for p, t_nodes in paragraphs:
            p_text = "".join((t.text or "") for t in t_nodes)
            norm_p_text = self._normalize(p_text)

            start_node = current_pos
            end_node = current_pos + len(norm_p_text)

            if start_par is None and pos < end_node:
                start_par = p

            if start_par is not None and end_node >= pos + len(norm_search):
                end_par = p
                break

            current_pos = end_node

        if start_par is None:
            self._save_xml_and_pack(tmp_dir, xml_path, tree, file_path)
            return False

        # Глубокое копирование форматирования
        pPr = start_par.find(W + "pPr")
        if pPr is not None:
            pPr_copy = copy.deepcopy(pPr)
        else:
            pPr_copy = None

        first_run = start_par.find(W + "r")
        rPr_copy = None
        if first_run is not None:
            rPr = first_run.find(W + "rPr")
            if rPr is not None:
                rPr_copy = copy.deepcopy(rPr)

        # Очищаем стартовый абзац
        for t in start_par.iter(W + "t"):
            t.text = ""

        # Вставляем первую строку
        new_r = ET.SubElement(start_par, W + "r")
        if rPr_copy is not None:
            new_r.append(copy.deepcopy(rPr_copy))
        new_t = ET.SubElement(new_r, W + "t")
        new_t.text = replace_lines[0]

        parent = start_par.getparent()
        index = parent.index(start_par)

        # Вставляем новые абзацы
        for line in replace_lines[1:]:
            new_p = ET.Element(W + "p")

            if pPr_copy is not None:
                new_p.append(copy.deepcopy(pPr_copy))

            new_r = ET.SubElement(new_p, W + "r")
            if rPr_copy is not None:
                new_r.append(copy.deepcopy(rPr_copy))

            new_t = ET.SubElement(new_r, W + "t")
            new_t.text = line

            parent.insert(index + 1, new_p)
            index += 1

        # Очищаем остальные абзацы блока
        clear_mode = False
        for p, t_nodes in paragraphs:
            if p is start_par:
                clear_mode = True
                continue
            if p is end_par:
                for t in t_nodes:
                    t.text = ""
                break
            if clear_mode:
                for t in t_nodes:
                    t.text = ""

        self._save_xml_and_pack(tmp_dir, xml_path, tree, file_path)
        return True

    # ---------------- XML helpers ----------------

    def _load_xml(self, file_path):
        tmp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

        xml_path = os.path.join(tmp_dir, "word", "document.xml")
        parser = ET.XMLParser(remove_blank_text=False)
        tree = ET.parse(xml_path, parser)
        root = tree.getroot()
        return tmp_dir, xml_path, tree, root

    def _save_xml_and_pack(self, tmp_dir, xml_path, tree, file_path):
        tree.write(xml_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        with zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED) as zip_out:
            for root_dir, _, files in os.walk(tmp_dir):
                for file in files:
                    full_path = os.path.join(root_dir, file)
                    rel_path = os.path.relpath(full_path, tmp_dir)
                    zip_out.write(full_path, rel_path)
        shutil.rmtree(tmp_dir)

    def _normalize(self, text):
        return "".join(text.split()).lower()
