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

# Konfiguracja selenium
options = Options()
options.add_argument("--headless")  # Scrapowanie bez otwierania okien
options.add_argument("--log-level=3")  # Minimalne logi
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Opcje logów
driver = webdriver.Chrome(options=options)
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=2#")  # Bierzemy drugą kolumnę

# Opóźnienie dla selenium
driver.implicitly_wait(2)

# JSON – struktura do zapisania danych
data = {}

try:
    # Pobierz wydziały
    _faculties = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.main_tree.treeview > li"))
    )
    
    faculties = _faculties[:-2]  # Pomijamy ostatnie elementy
    
    for faculty in faculties:
        faculty_name = faculty.text.strip()
        print("\t", faculty_name)
        data[faculty_name] = {}

        next = faculty.find_element(By.CSS_SELECTOR, "img[src*='plus1.gif']")
        driver.execute_script("arguments[0].click();", next)

        # Pobierz katedry
        departments = WebDriverWait(faculty, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.treeview li"))
        )
        
        time.sleep(1)
        for department in departments:
            department_name = department.text.strip()
            print("\t\t", department_name)
            data[faculty_name][department_name] = {}

            next = department.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", next)
            
            # Pobierz prowadzących
            lecturers = WebDriverWait(department, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
            
            time.sleep(1)
            for person in lecturers:
                person_name = person.text.strip()
                print("\t\t\t", person_name)

                try:
                    plan = person.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                except selenium.common.exceptions.NoSuchElementException:
                    plus = person.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                    driver.execute_script("arguments[0].click();", plus)
                    plan = person.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])

                try:
                    # Pobierz plan prowadzącego (wszystkie divy z klasą "coursediv")
                    course_elements = WebDriverWait(driver, 2).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.coursediv"))
                    )

                    courses_list = []  # lista na kursy dla danego nauczyciela

                    # Iterujemy po wszystkich kursach (każdy kurs to oddzielny div)
                    for course_element in course_elements:
                        full_html = course_element.get_attribute("innerHTML")
                        
                        # Parsowanie HTML-a przy pomocy BeautifulSoup
                        soup = BeautifulSoup(full_html, "html.parser")
                        
                        # Pobierz cały tekst z diva – oddzielony znakami nowej linii
                        raw_text = soup.get_text(separator="\n").strip()
                        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                        
                        # Pierwsza linia zawiera skrót przedmiotu i rodzaj zajęć, np. "So, wyk" lub "Sip, ćw"
                        course_subject = ""
                        course_activity_type = ""
                        if lines:
                            parts = lines[0].split(",")
                            if len(parts) >= 2:
                                course_subject = parts[0].strip()
                                course_activity_type = parts[1].strip()
                            else:
                                course_subject = lines[0].strip()

                        # Pobierz wszystkie znaczniki <a> wewnątrz diva i rozdziel je na linki do grup i do sal
                        all_links = soup.find_all("a")
                        group_links = []
                        room_links = []
                        for a in all_links:
                            href = a.get("href", "")
                            if "type=20" in href:
                                room_links.append(a)
                            elif "type=0" in href or "type=2" in href:
                                group_links.append(a)
                                
                        course_groups = tuple(sorted(a.get_text(strip=True) for a in group_links))
                        course_rooms  = tuple(sorted(a.get_text(strip=True) for a in room_links))
                        
                        # Zbuduj słownik reprezentujący kurs
                        course_data = {
                            "subject": course_subject,
                            "activity_type": course_activity_type,
                            "groups": course_groups,
                            "rooms": course_rooms
                        }
                        
                        # Dodaj kurs do listy, tylko jeśli nie istnieje w tej samej formie
                        if course_data not in courses_list:
                            courses_list.append(course_data)

                    # Wypisz wyniki (lub zapisz do słownika)
                    for course in courses_list:
                        print("\t\t\t\tRodzaj zajęć:", course["activity_type"])
                        print("\t\t\t\tSubject:", course["subject"])
                        print("\t\t\t\tGrupy:", course["groups"])
                        print("\t\t\t\tSale:", course["rooms"])

                    # Zapisz kursy nauczyciela do struktury JSON
                    data[faculty_name][department_name][person_name] = courses_list

                except Exception:
                    driver.close()
                    
                driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()

# Zapis danych do pliku JSON
with open("plan.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
