# import sys
# import asyncio
# import random
# import threading
# import requests
# import logging
# from concurrent.futures import ThreadPoolExecutor
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
#     QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, QInputDialog
# )
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# from run_getemail import process_urls
# from conf_log import setup_logging
# from driver_setup import setup_driver
# from link_extractor import process_links, validate_links
# from email_sender import send_email
# from email_content import html_content
# from utils import read_email_list
# from email_extractor import extracted_emails
# from PyQt6.QtCore import QThread, pyqtSignal, QObject

# class EmailAutomationApp(QMainWindow):
#     log_signal = pyqtSignal(str)  
#     link_signal = pyqtSignal(str)  # New signal to emit each extracted link
    
#     def __init__(self):
#         super().__init__()
#         self.log_signal.connect(self.update_log_output)  # Connection to log output
#         self.link_signal.connect(self.update_links_output)  # Connection to links output
#         self.setWindowTitle("Email Automation Tool")
#         self.setGeometry(100, 100, 800, 600)

#         # Tab widget
#         self.tabs = QTabWidget()
#         self.setCentralWidget(self.tabs)
        
#         # Create tabs for each functionality
#         self.create_link_extractor_tab()
#         self.create_email_extractor_tab()
#         self.create_email_sender_tab()

#     def update_log_output(self, message):
#         self.log_output.append(message)  # Update log in the main thread

#     def update_links_output(self, link):
#         self.links_result.append(link)  # Append each link to the output

#     def create_link_extractor_tab(self):
#         """Tab for extracting links from search results"""
#         tab = QWidget()
#         layout = QVBoxLayout()
#         layout.setSpacing(2)
#         layout.setContentsMargins(10, 10, 10, 10)

#         # Search input and button
#         self.search_input = QLineEdit()
#         self.search_input.setFixedHeight(40)
#         self.search_input.setPlaceholderText("Enter search query...")
#         layout.addWidget(QLabel("Search Query:"))
#         layout.addWidget(self.search_input)

#         self.extract_links_button = QPushButton("Extract Links")
#         self.extract_links_button.setFixedHeight(40)
#         self.extract_links_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
#         self.extract_links_button.clicked.connect(self.start_link_extraction)
#         layout.addWidget(self.extract_links_button)

#         # Results display
#         self.links_result = QTextEdit()
#         self.links_result.setReadOnly(True)  # Make it read-only
#         layout.addWidget(QLabel("Extracted Links:"))
#         layout.addWidget(self.links_result)

#         # Save links button
#         self.save_links_button = QPushButton("Save Links")
#         self.save_links_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
#         self.save_links_button.clicked.connect(self.save_links_to_file)
#         layout.addWidget(self.save_links_button)

#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Link Extractor")

#     def create_email_extractor_tab(self):
#         """Tab for extracting emails from URLs"""
#         tab = QWidget()
#         layout = QVBoxLayout()
#         layout.setSpacing(2)
#         layout.setContentsMargins(10, 10, 10, 10)

#         self.url_file_input = QLineEdit()
#         self.url_file_input.setFixedHeight(40)  
#         self.url_file_input.setPlaceholderText("Enter filename containing URLs (e.g., urls.txt)")
#         layout.addWidget(QLabel("URL List File:"))
#         layout.addWidget(self.url_file_input)

#         self.extract_emails_button = QPushButton("Extract Emails")
#         self.extract_emails_button.setFixedHeight(40)  
#         self.extract_emails_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
#         self.extract_emails_button.clicked.connect(self.start_email_extraction)
#         layout.addWidget(self.extract_emails_button)

#         # Results display for extracted emails
#         self.emails_result = QTextEdit()
#         self.emails_result.setReadOnly(True)  # Make it read-only
#         layout.addWidget(QLabel("Extracted Emails:"))
#         layout.addWidget(self.emails_result)

#         # Save Email button
#         self.save_email_button = QPushButton("Save Email")
#         self.save_email_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
#         self.save_email_button.clicked.connect(self.save_email_to_file)
#         layout.addWidget(self.save_email_button)
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Email Extractor")

#     def create_email_sender_tab(self):
#         """Tab for sending emails"""
#         tab = QWidget()
#         layout = QVBoxLayout()

#         layout.setSpacing(2)
#         layout.setContentsMargins(10, 10, 10, 10)

#         def add_label_input_pair(label_text, input_field):
#             label = QLabel(label_text)
#             layout.addWidget(label)
#             layout.addWidget(input_field)

#         self.sender_email_input = QLineEdit()
#         self.sender_email_input.setPlaceholderText("Enter your email")
#         self.sender_email_input.setFixedHeight(40)
#         add_label_input_pair("Sender Email:", self.sender_email_input)

#         self.password_input = QLineEdit()
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.password_input.setPlaceholderText("Enter your email password")
#         self.password_input.setFixedHeight(40)
#         add_label_input_pair("Password:", self.password_input)

#         self.email_file_input = QLineEdit()
#         self.email_file_input.setPlaceholderText("Enter path to email list file")
#         self.email_file_input.setFixedHeight(40)
#         add_label_input_pair("Email List File:", self.email_file_input)

#         self.attachment_input = QLineEdit(self)
#         self.attachment_input.setPlaceholderText("Select your CV file...")
#         self.attachment_input.setFixedHeight(40)
#         add_label_input_pair("Attachment:", self.attachment_input)

#         self.attach_file_button = QPushButton("Browse", self)
#         self.attach_file_button.setFixedHeight(40)  
#         self.attach_file_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
#         self.attach_file_button.clicked.connect(self.browse_file)
#         layout.addWidget(self.attach_file_button)

#         self.log_output = QTextEdit()
#         self.log_output.setReadOnly(True)  # Make it read-only
#         layout.addWidget(self.log_output)

#         self.send_emails_button = QPushButton("Send Emails")
#         self.send_emails_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
#         self.send_emails_button.clicked.connect(self.start_email_sending)  
#         layout.addWidget(self.send_emails_button)

#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Email Sender")

#     def start_link_extraction(self):
#         """Start the link extraction process in a separate thread"""
#         search_query = self.search_input.text()
#         if search_query:
#             self.links_result.setPlainText(f"Extracting links for query: {search_query}...")
#             self.extract_links_thread = threading.Thread(target=self.extract_links, args=(search_query,), daemon=True)
#             self.extract_links_thread.start()
#             self.log_signal.emit("Extracting links...")  

#         else:
#             QMessageBox.warning(self, "Input Error", "Please enter a search query.")

#     def extract_links(self, search_query):
#         """Function to extract links based on search query"""
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             loop.run_until_complete(self.extract_links_async(search_query))
#         except Exception as e:
#             logger_info.error(f"Link extraction failed: {e}")
#             self.log_signal.emit(f"Link extraction failed: {e}")
#         finally:
#             loop.close()

#     async def extract_links_async(self, search_query):
#         """Asynchronous link extraction using Selenium"""
#         driver = setup_driver()
#         driver.get("https://www.google.com")

#         try:
#             input_element = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.NAME, "q"))
#             )
#             input_element.send_keys(search_query)
#             input_element.submit()

#             links = set()
#             page_num = 1

#             while True:
#                 print(f"Processing page {page_num}...")
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 await asyncio.sleep(2)

#                 current_links = process_links(driver)
#                 valid_links = await validate_links(current_links)

#                 for link in valid_links:
#                     links.add(link)
#                     self.link_signal.emit(link)  # Emit the signal for each link

#                 await asyncio.sleep(random.uniform(1, 3))

#                 try:
#                     element = WebDriverWait(driver, 20).until(
#                         EC.element_to_be_clickable((By.ID, 'pnnext'))
#                     )
#                     driver.execute_script("arguments[0].scrollIntoView();", element)
#                     element.click()
#                     await asyncio.sleep(random.uniform(1, 3))
#                     page_num += 1

#                 except Exception as e:
#                     print("No more pages to navigate or an error occurred:", e)
#                     break

#             self.links_result.setPlainText("\n".join(links))

#         except Exception as e:
#             logger_info.error(f"An error occurred during link extraction: {str(e)}")
#             QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

#         finally:
#             driver.quit()  # Close the browser after finishing

#     def save_links_to_file(self):
#         """Save extracted links to a file with a custom name"""
#         links = self.links_result.toPlainText()
#         if not links:
#             QMessageBox.warning(self, "No Links", "There are no links to save.")
#             return

#         file_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter the filename to save (e.g., myfile.txt):")
        
#         if ok and file_name:
#             file_name = file_name.strip()  
#             if not file_name.endswith('.txt'):
#                 file_name += '.txt'
#             try:
#                 with open(file_name, "w") as file:
#                     file.write(links)
#                 QMessageBox.information(self, "Success", "Links saved successfully!")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {e}")

#     def start_email_extraction(self):
#         """Start the email extraction process in a separate thread"""
#         filename = self.url_file_input.text()
        
#         if filename:
#             self.thread = QThread()
#             self.thread.started.connect(lambda: self.extract_emails_from_urls(filename)) 
#             self.thread.finished.connect(self.thread.deleteLater)  
#             self.thread.start()
#         else:
#             QMessageBox.warning(self, "Input Error", "Please enter a filename containing URLs.")
 
#     def extract_emails_from_urls(self, filename):
#         """Function to extract emails from the specified URLs file"""
#         global extracted_emails  

#         try:
#             with open(filename, 'r') as file:
#                 urls = list(set(file.read().splitlines()))
#             logger_info.info(f"{len(urls)} unique URLs found.")
            
#             with requests.Session() as session:
#                 url_cache = {}
#                 url_chunks = [urls[i::2] for i in range(2)]
#                 with ThreadPoolExecutor(max_workers=2) as executor:
#                     executor.map(lambda chunk: process_urls(chunk, session, url_cache), url_chunks)

#             # Update the UI with extracted emails
#             self.update_email_results(extracted_emails)  
#             logger_info.info(f"Extracted Emails: {extracted_emails}")

#         except Exception as e:
#             raise BaseException(f"Error is :{e}")

#     def update_email_results(self, emails):
#         """Update the email display area with the extracted emails."""
#         if emails:
#             self.emails_result.setPlainText("\n".join(emails))  
#         else:
#             self.emails_result.setPlainText("No emails found.")  

#     def save_email_to_file(self):
#         """Save extracted emails to a file with a custom name"""
#         emails = self.emails_result.toPlainText()
#         print("Emails to save:", emails)
#         if not emails:
#             QMessageBox.warning(self, "No Emails", "There are no emails to save.")
#             return

#         file_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter the filename to save (e.g., myfile.txt):")
        
#         if ok and file_name:
#             file_name = file_name.strip()
#             if not file_name.endswith('.txt'):
#                 file_name += '.txt'
#             try:
#                 with open(file_name, "w") as file:
#                     file.write(emails)
#                 QMessageBox.information(self, "Success", "Emails saved successfully!")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {e}")

#     def browse_file(self):
#         """Open a file dialog to select a file."""
#         file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
#         if file_name:
#             self.attachment_input.setText(file_name)  

#     def start_email_sending(self):
#         """Start the email sending process in a separate thread"""
#         sender_email = self.sender_email_input.text()
#         password = self.password_input.text()
#         email_file = self.email_file_input.text()
#         attachment_path = self.attachment_input.text()  
#         attachment_path if attachment_path else None
#         if sender_email and password and email_file:
#             attachment_path = attachment_path if attachment_path else None
#             threading.Thread(target=self.send_emails, args=(sender_email, password, email_file, attachment_path), daemon=False).start()
#         else:
#             QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            
#     def send_emails(self, sender_email, password, email_file, attachment_path):
#         self.log_output.append("Starting to send emails...")
#         """Function to send emails to extracted email addresses with attachment"""
#         asyncio.run(self.send_emails_async(sender_email, password, email_file, attachment_path))
        
#     async def send_emails_async(self, sender_email, password, email_file, attachment_path):
#         """Asynchronous email sending with attachment"""
#         try:
#             email_list = await read_email_list(email_file)
#             for receiver_email in email_list:
#                 await self.send_email_with_retry(receiver_email, sender_email, password, attachment_path)
#                 await asyncio.sleep(10)  # Delay of 10 seconds between each email to avoid rate limits
                
#             self.log_signal.emit("Emails sent successfully!")
#             QMessageBox.information(self, "Success", "Emails sent successfully!")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"An error occurred while sending emails: {e}")

#     async def send_email_with_retry(self, receiver_email, sender_email, password, attachment_path=None, retries=3, delay=5):
#         """Send email with retry mechanism"""
#         for attempt in range(retries):
#             try:
#                 await send_email(
#                     receiver_email=receiver_email,
#                     html_content=html_content,
#                     sender_email=sender_email,
#                     password=password,
#                     attachment_path=attachment_path
#                 )
#                 self.log_signal.emit(f"Email sent successfully to {receiver_email}!")  
#                 break  
#             except Exception as e:
#                 self.log_signal.emit(f"Failed to send email to {receiver_email}: {e}")
#                 if attempt < retries - 1:
#                     await asyncio.sleep(delay)  
#                 else:
#                     self.log_signal.emit(f"Giving up on sending email to {receiver_email} after {retries} attempts.")

# if __name__ == "__main__":
#     setup_logging()
#     logger_info = logging.getLogger('info')
#     logger_info.info("This is an info message.")
#     app = QApplication(sys.argv)
#     window = EmailAutomationApp()
#     window.show()
#     sys.exit(app.exec())






import os
import sys
import asyncio
import random
import threading
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, QInputDialog
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from run_getemail import process_urls
from conf_log import setup_logging
from driver_setup import setup_driver
from link_extractor import process_links, validate_links
from email_sender import send_email
from email_content import html_content
from utils import read_email_list
from email_extractor import extracted_emails
from PyQt6.QtCore import QThread, pyqtSignal, QObject


class EmailAutomationApp(QMainWindow):
    log_signal = pyqtSignal(str)
    link_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.log_signal.connect(self.update_log_output)
        self.link_signal.connect(self.update_links_output)
        self.setWindowTitle("Email Automation Tool")
        self.setGeometry(100, 100, 800, 600)

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs for each functionality
        self.create_link_extractor_tab()
        self.create_email_extractor_tab()
        self.create_email_sender_tab()

    def update_log_output(self, message):
        self.log_output.append(message)

    def update_links_output(self, link):
        self.links_result.append(link)

    def create_link_extractor_tab(self):
        """Tab for extracting links from search results"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(10, 10, 10, 10)

        # Search input and button
        self.search_input = QLineEdit()
        self.search_input.setFixedHeight(40)
        self.search_input.setPlaceholderText("Enter search query...")
        layout.addWidget(QLabel("Search Query:"))
        layout.addWidget(self.search_input)

        self.extract_links_button = QPushButton("Extract Links")
        self.extract_links_button.setFixedHeight(40)
        self.extract_links_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
        self.extract_links_button.clicked.connect(self.start_link_extraction)
        layout.addWidget(self.extract_links_button)

        # Results display
        self.links_result = QTextEdit()
        self.links_result.setReadOnly(True)  # Make it read-only
        layout.addWidget(QLabel("Extracted Links:"))
        layout.addWidget(self.links_result)

        # Save links button
        self.save_links_button = QPushButton("Save Links")
        self.save_links_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
        self.save_links_button.clicked.connect(self.save_links_to_file)
        layout.addWidget(self.save_links_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Link Extractor")

    def create_email_extractor_tab(self):
        """Tab for extracting emails from a URL"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(10, 10, 10, 10)

        self.url_input = QLineEdit()
        self.url_input.setFixedHeight(40)
        self.url_input.setPlaceholderText("Enter URL to extract emails from")
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_input)

        self.extract_emails_button = QPushButton("Extract Emails")
        self.extract_emails_button.setFixedHeight(40)
        self.extract_emails_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
        self.extract_emails_button.clicked.connect(self.start_email_extraction)
        layout.addWidget(self.extract_emails_button)

        # Results display for extracted emails
        self.emails_result = QTextEdit()
        self.emails_result.setReadOnly(True)  # Make it read-only
        layout.addWidget(QLabel("Extracted Emails:"))
        layout.addWidget(self.emails_result)

        # Save Email button
        self.save_email_button = QPushButton("Save Email")
        self.save_email_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
        self.save_email_button.clicked.connect(self.save_email_to_file)
        layout.addWidget(self.save_email_button)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Email Extractor")

    def create_email_sender_tab(self):
        """Tab for sending emails"""
        tab = QWidget()
        layout = QVBoxLayout()

        layout.setSpacing(2)
        layout.setContentsMargins(10, 10, 10, 10)

        def add_label_input_pair(label_text, input_field):
            label = QLabel(label_text)
            layout.addWidget(label)
            layout.addWidget(input_field)

        self.sender_email_input = QLineEdit()
        self.sender_email_input.setPlaceholderText("Enter your email")
        self.sender_email_input.setFixedHeight(40)
        add_label_input_pair("Sender Email:", self.sender_email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your email password")
        self.password_input.setFixedHeight(40)
        add_label_input_pair("Password:", self.password_input)

        self.email_file_input = QLineEdit()
        self.email_file_input.setPlaceholderText("Enter path to email list file")
        self.email_file_input.setFixedHeight(40)
        add_label_input_pair("Email List File:", self.email_file_input)

        self.attachment_input = QLineEdit(self)
        self.attachment_input.setPlaceholderText("Select your CV file...")
        self.attachment_input.setFixedHeight(40)
        add_label_input_pair("Attachment:", self.attachment_input)

        self.attach_file_button = QPushButton("Browse", self)
        self.attach_file_button.setFixedHeight(40)
        self.attach_file_button.setStyleSheet("background-color: blue; color: white;margin-bottom:10px")
        self.attach_file_button.clicked.connect(self.browse_file)
        layout.addWidget(self.attach_file_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.log_output)

        self.send_emails_button = QPushButton("Send Emails")
        self.send_emails_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;margin-bottom:10px")
        self.send_emails_button.clicked.connect(self.start_email_sending)
        layout.addWidget(self.send_emails_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Email Sender")

    def start_link_extraction(self):
        """Start the link extraction process in a separate thread"""
        search_query = self.search_input.text()
        if search_query:
            self.links_result.setPlainText(f"Extracting links for query: {search_query}...")
            self.extract_links_thread = threading.Thread(target=self.extract_links, args=(search_query,), daemon=True)
            self.extract_links_thread.start()
            self.log_signal.emit("Extracting links...")

        else:
            QMessageBox.warning(self, "Input Error", "Please enter a search query.")

    def extract_links(self, search_query):
        """Function to extract links based on search query"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.extract_links_async(search_query))
        except Exception as e:
            logger_info.error(f"Link extraction failed: {e}")
            self.log_signal.emit(f"Link extraction failed: {e}")
        finally:
            loop.close()

    async def extract_links_async(self, search_query):
        """Asynchronous link extraction using Selenium"""
        driver = setup_driver()
        driver.get("https://www.google.com")

        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "q"))
            )
            input_element.send_keys(search_query)
            input_element.submit()

            links = set()
            page_num = 1

            while True:
                print(f"Processing page {page_num}...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)

                current_links = process_links(driver)
                valid_links = await validate_links(current_links)

                for link in valid_links:
                    links.add(link)
                    self.link_signal.emit(link)  # Emit the signal for each link

                await asyncio.sleep(random.uniform(1, 3))

                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, 'pnnext'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    element.click()
                    await asyncio.sleep(random.uniform(1, 3))
                    page_num += 1

                except Exception as e:
                    print("No more pages to navigate or an error occurred:", e)
                    break

            self.links_result.setPlainText("\n".join(links))

        except Exception as e:
            logger_info.error(f"An error occurred during link extraction: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        finally:
            driver.quit()

    def save_links_to_file(self):
        """Save extracted links to a file with a custom name"""
        links = self.links_result.toPlainText()
        if not links:
            QMessageBox.warning(self, "No Links", "There are no links to save.")
            return

        file_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter the filename to save (e.g., myfile.txt):")
        
        if ok and file_name:
            file_name = file_name.strip()
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            try:
                with open(file_name, "w") as file:
                    file.write(links)
                QMessageBox.information(self, "Success", "Links saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {e}")

    def start_email_extraction(self):
        """Start the email extraction process in a separate thread"""
        url = self.url_input.text().strip()  # Get the URL input
        if url:
            self.thread = QThread()
            self.thread.started.connect(lambda: self.extract_emails_from_url(url))
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid URL.")

    def extract_emails_from_url(self, url):
        """Function to extract emails from the specified URL"""
        global extracted_emails

        try:
            logger_info.info(f"Extracting emails from URL: {url}")

            # Check if the URL is a Google redirect and get the actual URL
            if 'google.com' in url:
                # Extract the actual URL from the redirect
                actual_url = self.get_actual_url_from_redirect(url)
            else:
                actual_url = url

            logger_info.info(f"Fetching emails from actual URL: {actual_url}")
            
            with requests.Session() as session:
                url_cache = {}
                process_urls([actual_url], session, url_cache)
            # Check for extracted emails
            if extracted_emails:
                logger_info.info(f"Extracted Emails: {extracted_emails}")
                for email in extracted_emails:
                    self.log_signal.emit(f"Extracted Email: {email}")  # Emit signal for each email
                self.update_email_results(extracted_emails)
            else:
                self.log_signal.emit("No emails found in the specified URL.")
                self.update_email_results([])

        except Exception as e:
            logger_info.error(f"Error extracting emails: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error extracting emails: {str(e)}")

    def get_actual_url_from_redirect(self, redirect_url):
        """Extract the actual URL from a Google redirect URL."""
        # Parse the redirect URL
        from urllib.parse import urlparse, parse_qs

        parsed_url = urlparse(redirect_url)
        # Check for the 'url' query parameter
        query_params = parse_qs(parsed_url.query)
        if 'url' in query_params:
            return query_params['url'][0]  # Return the first actual URL

        return redirect_url  # Return the redirect URL itself if no actual URL is found
    def update_email_results(self, emails):
        """Update the email display area with the extracted emails."""
        if emails:
            self.emails_result.setPlainText("\n".join(emails))
        else:
            self.emails_result.setPlainText("No emails found.")

    def save_email_to_file(self):
        """Save extracted emails to a file with a custom name"""
        emails = self.emails_result.toPlainText()
        if not emails:
            QMessageBox.warning(self, "No Emails", "There are no emails to save.")
            return

        file_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter the filename to save (e.g., myfile.txt):")
        
        if ok and file_name:
            file_name = file_name.strip()
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            try:
                with open(file_name, "w") as file:
                    file.write(emails)
                QMessageBox.information(self, "Success", "Emails saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {e}")

    def browse_file(self):
        """Open a file dialog to select a file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_name:
            self.attachment_input.setText(file_name)

    def start_email_sending(self):
        """Start the email sending process in a separate thread"""
        sender_email = self.sender_email_input.text()
        password = self.password_input.text()
        email_file = self.email_file_input.text()
        attachment_path = self.attachment_input.text()
        if sender_email and password and email_file:
            threading.Thread(target=self.send_emails, args=(sender_email, password, email_file, attachment_path), daemon=False).start()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def send_emails(self, sender_email, password, email_file, attachment_path):
        self.log_output.append("Starting to send emails...")
        """Function to send emails to extracted email addresses with attachment"""
        asyncio.run(self.send_emails_async(sender_email, password, email_file, attachment_path))
        
    async def send_emails_async(self, sender_email, password, email_file, attachment_path):
        """Asynchronous email sending with attachment"""
        try:
            email_list = await read_email_list(email_file)
            for receiver_email in email_list:
                await self.send_email_with_retry(receiver_email, sender_email, password, attachment_path)
                await asyncio.sleep(10)  # Delay of 10 seconds between each email to avoid rate limits
                
            self.log_signal.emit("Emails sent successfully!")
            QMessageBox.information(self, "Success", "Emails sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while sending emails: {e}")

    async def send_email_with_retry(self, receiver_email, sender_email, password, attachment_path=None, retries=3, delay=5):
        """Send email with retry mechanism"""
        for attempt in range(retries):
            try:
                await send_email(
                    receiver_email=receiver_email,
                    html_content=html_content,
                    sender_email=sender_email,
                    password=password,
                    attachment_path=attachment_path
                )
                self.log_signal.emit(f"Email sent successfully to {receiver_email}!")
                break
            except Exception as e:
                self.log_signal.emit(f"Failed to send email to {receiver_email}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    self.log_signal.emit(f"Giving up on sending email to {receiver_email} after {retries} attempts.")

if __name__ == "__main__":
    setup_logging()
    logger_info = logging.getLogger('info')
    logger_info.info("This is an info message.")
    app = QApplication(sys.argv)
    window = EmailAutomationApp()
    window.show()
    sys.exit(app.exec())
