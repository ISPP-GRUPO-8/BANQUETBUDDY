import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLogin():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_login(self):
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(974, 1032)
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    self.driver.find_element(By.ID, "id_username").send_keys("Pablo@gmail.com")
    self.driver.find_element(By.ID, "id_password").send_keys("Pablo")
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.CSS_SELECTOR, ".form-group:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".form-group:nth-child(3)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
  
class TestBooking():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_booking(self):
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(2576, 1416)
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("Pablo@gmail.com")
    self.driver.find_element(By.ID, "id_password").click()
    self.driver.find_element(By.ID, "id_password").send_keys("Pablo")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    self.driver.find_element(By.LINK_TEXT, "Caterings").click()
    self.driver.find_element(By.LINK_TEXT, "View details").click()
    self.driver.find_element(By.LINK_TEXT, "Book").click()
    self.driver.find_element(By.NAME, "event_date").click()
    self.driver.find_element(By.NAME, "event_date").send_keys("2026-01-19")
    self.driver.find_element(By.NAME, "number_guests").click()
    self.driver.find_element(By.NAME, "number_guests").send_keys("100")
    self.driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(1) .btn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
  
