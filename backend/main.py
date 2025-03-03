from selenium import webdriver
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import selenium
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm

# Konfiguracja selenium
options = Options()
options.add_argument("--headless")  # Scrapowanie bez otwierania okien
options.add_argument("--log-level=3")  # Minimalne logi
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Opcje logów
driver = webdriver.Chrome(options=options)
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=2#")  # Bierzemy drugą kolumnę

# Opóźnienie dla selenium
driver.implicitly_wait(2)

# JSON
data = {}

# Formatowanie nazwy przedmiotu
def normalize_subject(subject):
    base = subject.split(",")[0].strip()
    words = base.split()
    if words and words[0].lower() == "zarządzania":
        words[0] = "Zarządzanie"
    return " ".join(words)

try:
    # Pobierz wydziały
    _faculties = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.main_tree.treeview > li"))
    )
    
    faculties = _faculties[1:-2]  # Pomijamy pierwszy i ostatnie dwa elementy

    # Nawigacja po hierarchii
    for faculty in tqdm(faculties, desc="Wydziały"):
        faculty_name = faculty.text.strip()
        data[faculty_name] = {}

        next = faculty.find_element(By.CSS_SELECTOR, "img[src*='plus1.gif']")
        driver.execute_script("arguments[0].click();", next)

        # Pobierz katedry
        departments = WebDriverWait(faculty, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.treeview li"))
        )
        
        for department in tqdm(departments, desc="Katedry", leave=False):
            department_name = department.text.strip()
            data[faculty_name][department_name] = {}

            next = department.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", next)
            
            # Pobierz prowadzących
            lecturers = WebDriverWait(department, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
            
            time.sleep(1)
            for person in tqdm(lecturers, desc="Prowadzący", leave=False):
                person_name = person.text.strip()

                try:
                    plan = person.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                # Można zmienić na ogólny Exception (idk)
                except selenium.common.exceptions.NoSuchElementException:
                    plus = person.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                    driver.execute_script("arguments[0].click();", plus)
                    plan = person.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])

                try:
                    # Pobierz plan prowadzącego
                    data_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.data"))
                    )         
                    full_html = data_element.get_attribute("innerHTML")
                    
                    # Formatowanie planu
                    parts = full_html.split("<hr>")
                    extracted_html = parts[1].strip() if len(parts) >= 2 else full_html.strip()

                    soup = BeautifulSoup(extracted_html, "html.parser")
                    subject_lines = []
                    
                    for strong_tag in soup.find_all("strong"):
                        text = strong_tag.get_text(strip=True)
                        if strong_tag.next_sibling:
                            description = strong_tag.next_sibling.strip()
                            subject_lines.append(f"{text} {description}")
                        else:
                            subject_lines.append(text)

                    for subject in subject_lines:
                        subject_name = subject.split(" - ")[1].strip()
                        subject_name = subject_name.split(",")[0].strip() 

                        if subject_name not in data[faculty_name][department_name]:
                            data[faculty_name][department_name][subject_name] = []
                        
                        if person_name not in data[faculty_name][department_name][subject_name]:
                            data[faculty_name][department_name][subject_name].append(person_name)

                except Exception:
                    driver.close()
                    
                driver.switch_to.window(driver.window_handles[0])
                

finally:
    driver.quit()

# Zapis danych do pliku JSON
with open("frontend/public/plan.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
