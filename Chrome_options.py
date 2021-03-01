from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# ChromeOptions allows us use the userdata of chrome
# so that you don't have to sign in manually everytime.

def chrome_webdriver(driver,valid_proxies):
    import os
    import random
    import time
    # El requisito para encontrar el chromedriver puede cambiar o bien puedo copiar el archivo a la carpeta de C:/ primero y luego recien empiezo el programa
    #chromepath = r'C:\chromedriver.exe'
    firefoxpath=r'C:\geckodriver.exe'
    
    #options = webdriver.ChromeOptions()
    options = webdriver.FirefoxOptions()
    user_name = str(os.getenv('username'))
    print(user_name)
    #se agregan las opciones con datos definidos previamente
    #--------------------------------------------------------------------------------------------------------------
    # 1) El argumento más importante. Hace que se puedan usar los datos de usuario de la sesión actual de chrome
    #    - Se permite que los usuarios puedan logearse sin necesidad de saber a priori el nombre de usuario
    #options.add_argument("user-data-dir=C:\\Users\\"+user_name+"\\AppData\\Local\\Google\\Chrome\\User Data 2")
    #--------------------------------------------------------------------------------------------------------------
    #2) Headless
    #3) Block Pop Ups and other stuff
    #4) Iniciar con una extensión específica (VPN)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-binfobars")
    options.add_argument("--mute-audio")

    from pyfiglet import Figlet
    c_text = Figlet(font="slant")
    os.system("cls")
    os.system("mode con: cols=100 lines=50")

    while True :
        break
        #Quitar cuando quiera hacer lo del proxy, dejar en break por ahora
        
        PROXY = valid_proxies[random.randint(1,len(valid_proxies))]
        
        options.add_argument('--proxy-server=%s' % PROXY)
        driver = webdriver.Chrome(executable_path=chromepath, options=options)

        try:
            print(c_text.renderText("Testing : " + PROXY ))
            driver.get("https://www.facebook.com")
            time.sleep(random.randint(10,15))
            print(PROXY)

            try:

                driver.find_element_by_partial_link_text("Aceptar todas")
                print("wena choro")
                time.sleep(random.randint(2,4))
                elem_checker = driver.find_element_by_css_selector("#email")
                print(elem_checker)
                break
            except:

                elem_checker = driver.find_element_by_css_selector("#email")
                print(elem_checker)
                break
    
        except Exception as e:
            if "ERR_TUNNEL_CONNECTION_FAILED" in str(e) :
                print("Proxy : "+ PROXY + " failed!, Next! " + str(e))
            if "PROXY" in str(e) :
                print("Proxy : "+ PROXY + " failed!, Next! " + str(e))
            print("otro error: "+  str(e))
            driver.close()
            pass
    #driver = webdriver.Chrome(executable_path=chromepath, options=options)
    driver = webdriver.Firefox(executable_path=firefoxpath, options=options)
    #webdriver.DesiredCapabilities.CHROME['proxy']={
    #"httpProxy":PROXY,
    #"ftpProxy":PROXY,
    #"sslProxy":PROXY,
    #"proxyType":"MANUAL",
    #}
    return driver

def get_proxy_list(valid_proxies):
    from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
    import requests
    import concurrent.futures
    req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
    proxies_list = req_proxy.get_proxy_list() #this will create proxy list
    proxies = []
    for prox in proxies_list:
        proxies.append(prox.get_address())

    print(proxies)
    
    def extract(proxy):
        try: 
            r = requests.get('https://httpbin.org/ip', proxies={'http':"//" + proxy,'https':"//" +proxy},timeout = 1)
            print(r.json(),'-working')
            valid_proxies.append(proxy)
        except Exception as e:
            pass
        return proxy
    extract("203.115.112.218:3128")
    print("se llego")

    with concurrent.futures.ThreadPoolExecutor() as exector:
        exector.map(extract,proxies)

    return valid_proxies
