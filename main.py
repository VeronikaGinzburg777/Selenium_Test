from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def format_paragraph(text, line_length = 50):
    lines = [text[i:i + line_length] for i in range(0, len(text), line_length)]
    return "\n".join(lines)

def get_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for i, paragraph in enumerate(paragraphs):
        preview_text = paragraph.text[:100]  # Take the first 100 characters for preview
        print(f"{i + 1}. {format_paragraph(preview_text)}...")
    return paragraphs

def get_hatnotes(browser):
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, "div"):
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable":
            hatnotes.append(element)
    return hatnotes

def navigate_to_link(browser, link):
    browser.get(link)
    time.sleep(2)  # Wait for the page to load

def main():
    browser = webdriver.Chrome()
    base_url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D0%B5%D1%87%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0"

    try:
        browser.get(f"{base_url}")
        time.sleep(2)  # Wait for the page to load

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            choice = input("Ваш выбор (1, 2, 3): \n")

            if choice == '1':
                paragraphs = get_paragraphs(browser)
                para_choice = int(input("\nВведите номер параграфа для просмотра полностью:\n "))
                full_text = paragraphs[para_choice - 1].text
                print(format_paragraph(full_text))

            elif choice == '2':
                hatnotes = get_hatnotes(browser)
                for i, hatnote in enumerate(hatnotes):
                    link = hatnote.find_element(By.TAG_NAME, "a")
                    print(f"{i + 1}. {link.text} - {link.get_attribute('href')}")

                if hatnotes:
                    hatnote_choice = int(input("\nВведите номер ссылки для перехода:\n"))
                    link = hatnotes[hatnote_choice - 1].find_element(By.TAG_NAME, "a").get_attribute("href")
                    navigate_to_link(browser, link)
                else:
                    print("Нет связанных страниц.")

            elif choice == '3':
                print("Пока!")
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите снова.")

    finally:
        browser.quit()

main()

