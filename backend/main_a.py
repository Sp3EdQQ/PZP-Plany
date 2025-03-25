from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import selenium.common
import json
import time

# Konfiguracja Selenium
options = Options()
options.add_argument("--headless")  # Scrapowanie bez otwierania okien
options.add_argument("--log-level=3")  # Minimalne logi
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=1")

# Opóźnienie implicite
driver.implicitly_wait(0.5)

# Struktura danych JSON
data = {}

# Opóźnienia
for_delay = 0.3
driver_delay = 0.3

try:
    # Pobierz wydziały
    faculties = WebDriverWait(driver, driver_delay).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.main_tree.treeview > li"))
    )
    
    time.sleep(for_delay)
    for faculty_index, faculty in enumerate(faculties):
        # Pobierz nazwę wydziału
        faculty_name = faculty.text.strip()
        print(f"\t{faculty_name}")
        data[faculty_name] = {}

        # Rozwiń wydział
        next_img = faculty.find_element(By.CSS_SELECTOR, "img[src*='plus1.gif']")
        driver.execute_script("arguments[0].click();", next_img)
        WebDriverWait(driver, driver_delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.treeview li"))
        )

        # Pobierz tryby studiów (np. Niestacjonarne Zaoczne)
        studies = faculty.find_elements(By.CSS_SELECTOR, "ul.treeview > li")

        # Pommiń wieczorowe
        if faculty_index == 0:
            studies = studies[1:]
        
        time.sleep(for_delay)
        for study in studies:
            # Pobierz nazwę trybu (Stacjonarne/Zaoczne)
            study_name = study.text.strip()
            print(f"\t\t{study_name}")
            data[faculty_name][study_name] = {}

            # Rozwiń tryb
            next_img = study.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", next_img)
            WebDriverWait(driver, driver_delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
            )

            # Pobierz kierunki studiów
            programs = study.find_elements(By.CSS_SELECTOR, "ul > li")
            
            time.sleep(for_delay)
            for program in programs:
                # Pobierz nazwę kierunku
                program_name = program.text.strip()
                print(f"\t\t\t{program_name}")
                data[faculty_name][study_name][program_name] = {}

                # Rozwiń kierunek
                next_img = program.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                driver.execute_script("arguments[0].click();", next_img)
                WebDriverWait(driver, driver_delay).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
                )

                # Pobierz stopnie
                degrees = program.find_elements(By.CSS_SELECTOR, "ul > li")
                
                time.sleep(for_delay)
                for degree in degrees:
                    # Pobierz nazwę stopnia
                    degree_name = degree.text.strip()
                    print(f"\t\t\t\t{degree_name}")
                    data[faculty_name][study_name][program_name][degree_name] = {}

                    # Rozwiń stopień
                    next_img = degree.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                    driver.execute_script("arguments[0].click();", next_img)
                    WebDriverWait(driver, driver_delay).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
                    )

                    # Pobierz semestry
                    semesters = degree.find_elements(By.CSS_SELECTOR, "ul > li")
                    
                    time.sleep(for_delay)
                    for semester in semesters:
                        # Pobierz nazwę semestru
                        try: 
                            semester_name = semester.find_element(By.CSS_SELECTOR, "a").text.strip()
                            print(f"\t\t\t\t\t{semester_name}")
                            data[faculty_name][study_name][program_name][degree_name][semester_name] = {}
                        
                        except Exception:
                            pass

                        # Rozwiń semestr (jeśli istnieje plus)
                        try:
                            next_img = semester.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                            driver.execute_script("arguments[0].click();", next_img)
                            WebDriverWait(driver, driver_delay).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
                            )

                            # Pobierz grupy
                            groups = semester.find_elements(By.CSS_SELECTOR, "ul > li")
                            
                            time.sleep(for_delay)
                            for group in groups:
                                # Pobierz nazwę grupy
                                group_name = group.find_element(By.CSS_SELECTOR, "a").text.strip()
                                print(f"\t\t\t\t\t\t{group_name}")
                                data[faculty_name][study_name][program_name][degree_name][semester_name][group_name] = {}
                                
                                try:
                                    next_img = group.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                                    driver.execute_script("arguments[0].click();", next_img)
                                    WebDriverWait(driver, driver_delay).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
                                    )

                                    # Pobierz podgrupy
                                    subgroups = group.find_elements(By.CSS_SELECTOR, "ul > li")
                                    
                                    time.sleep(for_delay)
                                    for subgroup in subgroups:
                                        # Pobierz nazwę podgrupy
                                        subgroup_name = subgroup.find_element(By.CSS_SELECTOR, "a").text.strip()
                                        print(f"\t\t\t\t\t\t\t{subgroup_name}")
                                        data[faculty_name][study_name][program_name][degree_name][semester_name][group_name][subgroup_name] = {}

                                        plan = subgroup.find_element(By.CSS_SELECTOR, "ul li a")
                                        driver.execute_script("arguments[0].click();", plan)
                                        driver.switch_to.window(driver.window_handles[-1])
                                        
                                        try:
                                            # Pobierz wszystkie divy z kursami
                                            course_elements = WebDriverWait(driver, driver_delay).until(
                                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.coursediv"))
                                            )
                                            
                                            printed = set()  # zbiór, w którym przechowujemy (subject, activity_type)
                                            
                                            # Iteruj po wszystkich znalezionych kursach
                                            for course_element in course_elements:
                                                course_html = course_element.get_attribute("innerHTML")
                                                soup = BeautifulSoup(course_html, "html.parser")
                                                
                                                # Pobierz cały tekst z diva, oddzielony znakami nowej linii
                                                raw_text = soup.get_text(separator="\n").strip()
                                                lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                                                
                                                # Pierwsza linia powinna zawierać dane np. "TwI, wyk"
                                                if lines:
                                                    first_line = lines[0]
                                                    parts = first_line.split(",")
                                                    subject = parts[0].strip() if len(parts) >= 1 else ""
                                                    activity_type = parts[1].strip() if len(parts) >= 2 else ""
                                                    
                                                    # Sprawdzamy, czy ta kombinacja już wystąpiła
                                                    if (subject, activity_type) not in printed:
                                                        print("Subject:", subject)
                                                        print("Activity Type:", activity_type)
                                                        printed.add((subject, activity_type))
                                                        
                                        except Exception:
                                            driver.close()

                                        driver.switch_to.window(driver.window_handles[0])

                                except selenium.common.exceptions.NoSuchElementException:
                                    plan = group.find_element(By.CSS_SELECTOR, "ul li a")
                                    driver.execute_script("arguments[0].click();", plan)
                                    driver.switch_to.window(driver.window_handles[-1])

                                    try:
                                        # Pobierz wszystkie divy z kursami
                                        course_elements = WebDriverWait(driver, driver_delay).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.coursediv"))
                                        )
                                        
                                        printed = set()  # zbiór, w którym przechowujemy (subject, activity_type)
                                        
                                        # Iteruj po wszystkich znalezionych kursach
                                        for course_element in course_elements:
                                            course_html = course_element.get_attribute("innerHTML")
                                            soup = BeautifulSoup(course_html, "html.parser")
                                            
                                            # Pobierz cały tekst z diva, oddzielony znakami nowej linii
                                            raw_text = soup.get_text(separator="\n").strip()
                                            lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                                            
                                            # Pierwsza linia powinna zawierać dane np. "TwI, wyk"
                                            if lines:
                                                first_line = lines[0]
                                                parts = first_line.split(",")
                                                subject = parts[0].strip() if len(parts) >= 1 else ""
                                                activity_type = parts[1].strip() if len(parts) >= 2 else ""
                                                
                                                # Sprawdzamy, czy ta kombinacja już wystąpiła
                                                if (subject, activity_type) not in printed:
                                                    print("Subject:", subject)
                                                    print("Activity Type:", activity_type)
                                                    printed.add((subject, activity_type))
                                                    
                                    except Exception:
                                        driver.close()

                                    driver.switch_to.window(driver.window_handles[0])

                                except selenium.common.exceptions.NoSuchElementException:
                                    continue
                        except selenium.common.exceptions.NoSuchElementException:
                            continue

finally:
    driver.quit()

# Zapis danych do pliku JSON
with open("plan_a.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)