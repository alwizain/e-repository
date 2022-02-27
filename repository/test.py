from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        driver = webdriver.Firefox()
        

        #Opening the link we want to test
        driver.get('https://localhost:8000/registration')
        #find the form element
        first_name = driver.find_element_by_id('id_name')
        last_name = driver.find_element_by_id('id_last_name')
        email = driver.find_element_by_id('id_email')
        username = driver.find_element_by_id('id_username')
        password1 = driver.find_element_by_id('id_password1')
        password2 = driver.find_element_by_id('id_password2')

        submit = driver.find_element_by_name('registrasi')

        #Fill the form with data
        first_name.send_keys('Repository')
        last_name.send_keys('Poltekpos')
        email.send_keys('repository@poltekpos.ac.id')
        username.send_keys('repository')
        password1.send_keys('inipassword123')
        password2.send_keys('inipassword123')

        #submitting the form
        submit.send_keys(Keys.RETURN)

        #check the returned result
        assert 'Check your email' in driver.page_source