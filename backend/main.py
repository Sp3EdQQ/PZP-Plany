from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # 0 = INFO, 1 = WARNING, 2 = ERROR, 3 = FATAL (minimalne logi)
driver = webdriver.Chrome()
driver.get("https://plany.ubb.edu.pl/left_menu.php?type=2#")

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

            # Wczytanie prowadzacych
            strzalka = katedra.find_element(By.CSS_SELECTOR, "img[src*='plus.gif']")
            driver.execute_script("arguments[0].click();", strzalka)
            
            # Pobierz prowadzacych
            prowadzacy = WebDriverWait(katedra, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
            
            for osoba in prowadzacy:
                print("\t\t" + osoba.text)

finally:
    driver.quit()
