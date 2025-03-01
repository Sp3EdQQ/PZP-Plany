from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import selenium
from bs4 import BeautifulSoup
import time

# Konfiguracja selenium
options = Options()
options.add_argument("--headless") # Scrapowanie bez otwierania okien
options.add_argument("--log-level=3")  # Minimalne logi
options.add_experimental_option('excludeSwitches', ['enable-logging']) # Opcje logów
driver = webdriver.Chrome(options=options)
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=2#") # Bierzemy drugą kolumne

driver.implicitly_wait(3)

try:
    # Pobierz wydziały
    _wydzialy = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.main_tree.treeview > li"))
    )
    
    wydzialy = _wydzialy[1:-2]  # Pomijamy pierwszy i ostatnie dwa elementy

    for wydzial in wydzialy:
        print(wydzial.text)

        # Wczytanie katedr
        strzalka = wydzial.find_element(By.CSS_SELECTOR, "img[src*='plus1.gif']")
        driver.execute_script("arguments[0].click();", strzalka)
        
        # Pobierz katedry
        katedry = WebDriverWait(wydzial, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.treeview li"))
        )
        
        for katedra in katedry:
            print("\t" + katedra.text)

            # Wczytanie prowadzących
            strzalka = katedra.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", strzalka)
            
            # Pobierz prowadzących
            prowadzacy = WebDriverWait(katedra, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
            
            time.sleep(1)
            for osoba in prowadzacy:
                print("\t\t" + osoba.text)

                try:
                    # Wczytywanie planów prowadzących
                    plan = osoba.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                # Bierzemy pod uwagę dalsze rozwijanie hierarchii (jeśli to możliwe)
                except selenium.common.exceptions.NoSuchElementException:
                    plus = osoba.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
                    driver.execute_script("arguments[0].click();", plus)
                    # Wczytywanie planów prowadzących
                    plan = osoba.find_element(By.CSS_SELECTOR, "ul li a")
                    driver.execute_script("arguments[0].click();", plan)
                    driver.switch_to.window(driver.window_handles[-1])

                try:
                    data_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.data"))
                    )         
                    full_html = data_element.get_attribute("innerHTML")
                    
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
                        print("\t\t\t" + subject)

                except Exception:
                    print("\t\t\tBrak danych")
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()
