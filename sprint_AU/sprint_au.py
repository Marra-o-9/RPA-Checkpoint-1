import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys  
import time
import pandas as pd

def obter_dados_usuario():
    ROOT = tk.Tk()
    ROOT.withdraw()  

    vaga = simpledialog.askstring(title="Busca de Vagas", prompt="Qual vaga você deseja procurar?")
    localizacao = simpledialog.askstring(title="Busca de Vagas", prompt="Qual a localização desejada?")

    return vaga, localizacao

geckodriver_path = "drivers\geckodriver.exe"

service = Service(geckodriver_path)

driver = webdriver.Firefox(service=service)

dados_vagas = []

try:
    vaga_desejada, localizacao_desejada = obter_dados_usuario()

    driver.get("https://www.infojobs.com.br/")
    
    wait = WebDriverWait(driver, 10)
    accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="didomi-notice-agree-button"]')))
    accept_cookies_button.click()

    busca_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="keywordsCombo"]')))
    
    busca_input.send_keys(vaga_desejada)
    time.sleep(1)
    busca_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)

    localizacao_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="city"]')))
    localizacao_input.send_keys(localizacao_desejada)
    time.sleep(1)
    localizacao_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)

    localizacao_input.send_keys(Keys.ENTER)

    time.sleep(5) 


    numero_vagas = 20 


    for i in range(1, numero_vagas + 1):
        try:
            
            xpath_vaga = f'/html/body/main/div[2]/form/div/div[1]/div[2]/div[1]/div[{i}]'
            

            vaga_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_vaga)))
            vaga_element.click()
            time.sleep(5) 

            titulo = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[1]/div[1]/div[1]/h2'))).text
            nome_empresa = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[1]').text
            descricao = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/p[1]').text
            
            try:
                avaliacao = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[1]/a').text
            except:
                avaliacao = "Não informado"

            try:
                num_vagas = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/p[2]').text
            except:
                num_vagas = "Não informado"

            try:
                tipo_contrato_jornada = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/p[3]').text
            except:
                tipo_contrato_jornada = "Não informado"
                
            try:
                area_profissional = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/p[4]').text
            except:
                area_profissional = "Não informado"
            
            try:
                exigencias = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/div[2]').text
            except:
                exigencias = "Não informado"
            
            try:
                valorizado = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[2]/div[4]/ul').text
            except:
                valorizado = "Não informado"

            try:
                presencial_homeoffice = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/div[3]').text
            except:
                presencial_homeoffice = "Não informado"

            dados_vagas.append({
                'Título': titulo,
                'Nome da Empresa': nome_empresa,
                'Avaliação': avaliacao,
                'Descrição': descricao,
                'Número de Vagas': num_vagas,
                'Tipo de Contrato e Jornada': tipo_contrato_jornada,
                'Área Profissional': area_profissional,
                'Exigências': exigencias,
                'Valorizado': valorizado,
                'Presencial/Home Office': presencial_homeoffice
            })

        except Exception as e:
            print(f'Erro ao coletar dados da vaga {i}: {e}')

    # Criar um DataFrame a partir dos dados coletados
    df = pd.DataFrame(dados_vagas)
    
    print(df)

    # Salvar o DataFrame em um arquivo Excel
    df.to_excel('vagas_infojobs.xlsx', index=False)

    print("Dados das vagas salvos em 'vagas_infojobs.xlsx'.")

finally:
    # Fechar o driver
    driver.quit()
