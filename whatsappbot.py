# Import as bibliotecas
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time 
import pyodbc
import pyautogui

# configuração da conexão do sql server 
server = 'servidor'
database = 'banco'
username = 'usario '
password = 'senha'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cmd = cnxn.cursor()


# Nevegar até o whatsapp web 
options = webdriver.ChromeOptions()
options.add_argument('lang=pt-br')
options.add_argument('--start-maximized')
options.add_argument('--user-data-dir=C:\\Users\\GABRIEL\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.get('https://web.whatsapp.com/')
time.sleep(10)

# Definir contratos e grupos e mensagem a ser enviada
cmd.execute("select id from whatsapp_bot.dbo.content where item_sent = 0")
id_list = cmd.fetchall()



for query in id_list:
  id = query[0]
  
  cmd.execute("SELECT mensagem FROM whatsapp_bot.dbo.content WHERE id=?", id)
  content = cmd.fetchall()
  mensagem = content[0][0]

  cmd.execute("SELECT group_whatsapp FROM whatsapp_bot.dbo.content WHERE id=?", id)
  content = cmd.fetchall()
  contato = content[0][0]

  cmd.execute("SELECT src FROM whatsapp_bot.dbo.images a inner join whatsapp_bot.dbo.content b on a.id_content = b.id WHERE  a.id_content = ? and	   b.attached_image = 1", [id])
  src_img = cmd.fetchall() 

  cmd.execute("SELECT src FROM whatsapp_bot.dbo.document a inner join whatsapp_bot.dbo.content b on a.id_content = b.id WHERE  a.id_content = ? and	   b.attached_docum = 1", [id])
  src_doc = cmd.fetchall()

  cmd.execute("SELECT src FROM whatsapp_bot.dbo.video a inner join whatsapp_bot.dbo.content b on a.id_content = b.id WHERE  a.id_content = ? and	   b.attached_video = 1", [id])
  src_vid = cmd.fetchall()  


  cmd.execute("UPDATE  whatsapp_bot.dbo.content SET item_sent = 1,send_date = GETDATE() WHERE id = ?", [id])
  cmd.commit()
  
  # Buscar contatos/grupos
  def buscar_contato(contato):
    campo_pesquisa = driver.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')

    time.sleep(3)

    campo_pesquisa.click()
    campo_pesquisa.send_keys(contato)
    campo_pesquisa.send_keys(Keys.ENTER)

  def anexar_imagem(src_img):
    src = str(src_img[0])
    campo_anexar = driver.find_element_by_xpath("//span[@data-icon='clip']")
    campo_anexar.click()

    time.sleep(3)

    button_img = driver.find_element_by_xpath("//span[@data-icon='attach-image']")
    button_img.click()

    time.sleep(3)

    pyautogui.typewrite(src)
    pyautogui.press('enter')
    time.sleep(3)

    button_env = driver.find_element_by_xpath("//span[@data-icon='send']")
    button_env.click()

  def anexar_documento(src_doc):
    campo_anexar = driver.find_element_by_xpath("//span[@data-icon='clip']")
    campo_anexar.click()

    time.sleep(3)

    button_img = driver.find_element_by_xpath("//span[@data-icon='attach-document']")
    button_img.click()

    time.sleep(3)

    pyautogui.typewrite(src_doc[0][0])
    pyautogui.press('enter')
    time.sleep(3)

    button_env = driver.find_element_by_xpath("//span[@data-icon='send']")
    button_env.click()

  def anexar_video(src_vid):
    campo_anexar = driver.find_element_by_xpath("//span[@data-icon='clip']")
    campo_anexar.click()

    time.sleep(3)

    button_img = driver.find_element_by_xpath("//span[@data-icon='attach-image']")
    button_img.click()

    time.sleep(3)

    pyautogui.typewrite(src_vid[0][0])
    pyautogui.press('enter')
    time.sleep(3)

    button_env = driver.find_element_by_xpath("//span[@data-icon='send']")
    button_env.click()
    
  def enviar_mensagem(mensagem):
    campo_mensagem = driver.find_elements_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    campo_mensagem[1].click()
    
    time.sleep(3)
    
    campo_mensagem[1].send_keys(mensagem)
    campo_mensagem[1].send_keys(Keys.ENTER)
    
  # chamando as funçoes
  buscar_contato(contato)
  enviar_mensagem(mensagem)

  if len(src_img) != 0:
    for src in src_img:
      anexar_imagem(src)
      time.sleep(5)

  if len(src_doc) != 0:
    anexar_documento(src_doc)
    time.sleep(5)

  if len(src_vid) != 0:
    anexar_video(src_vid)
    time.sleep(20)
  
  

#fechar navegador 
time.sleep(3)
driver.quit();
