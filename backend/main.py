from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # 0 = INFO, 1 = WARNING, 2 = ERROR, 3 = FATAL (minimalne logi)
driver = webdriver.Chrome()
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=2#") # Zaczynamy od drugiej kolumny

try:
    # Pobierz wydziały
    _wydzialy = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.main_tree.treeview > li"))
    )

    wydzialy = _wydzialy[1:-2]  # Pomijamy pierwszy i ostatnie dwa elementy

    for wydzial in wydzialy:
        print(wydzial.text)

        # Wczytanie katedr
        strzalka = wydzial.find_element(By.CSS_SELECTOR, "img[src*='plus1.gif']")
        driver.execute_script("arguments[0].click();", strzalka)
        
        # Pobierz katedry
        katedry = WebDriverWait(wydzial, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.treeview li"))
        )
        
        for katedra in katedry:
            print("\t" + katedra.text)

            # Wczytanie prowadzących
            strzalka = katedra.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", strzalka)
            
            # Pobierz prowadzących
            prowadzacy = WebDriverWait(katedra, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
            
            for osoba in prowadzacy:
                print("\t\t" + osoba.text)
                
                # Wejdz w plan prowadzącego
                plan = osoba.find_element(By.CSS_SELECTOR, "ul li a")
                driver.execute_script("arguments[0].click();", plan)
                time.sleep(3)
                
                driver.switch_to.window(driver.window_handles[-1])

                try:
                    data_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.data"))
                    )         
                    full_html = data_element.get_attribute("innerHTML")  # Pobranie HTML

                    # Podział tekstu według `<hr>`
                    parts = full_html.split("<hr>")

                    if len(parts) >= 3:
                        extracted_html = parts[1].strip()
                    elif len(parts) >= 2:
                        extracted_html = parts[1].strip()
                    else:
                        extracted_html = full_html.strip()  # Jeśli brak `<hr>`, bierzemy cały tekst

                    # Usunięcie znaczników HTML
                    soup = BeautifulSoup(extracted_html, "html.parser")
                    clean_text = soup.get_text(separator=" ", strip=True)

                    print("\t\t\tDane z planu:", clean_text)

                except Exception as e:
                    print("\t\t\tBłąd podczas pobierania danych:", e)

                # Zamknij nową kartę
                driver.close()

                # Powróć do poprzedniej karty
                driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()
