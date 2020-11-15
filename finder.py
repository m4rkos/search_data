from selenium import webdriver
import uuid
import os, sys
import datetime
import time
import sqlite3
import urllib.request

class FinderScript:
    
    def main(self):
        
        type_search = input("What kind of search: \n\nImages: i\nContent: c\n\ntype: ")

        while type_search != 'i' and type_search != 'c':
            type_search = input("\n\nWrong, what kind of search: \n\nImages: i\nContent: c\n\ntype: ")                
            pass

        if(type_search == 'i'):
            self.mainImages()

        elif(type_search == 'c'):
            self.mainContent()
        
    def mainContent(self):

        name = input('\n\nType search: ')
        idf = str(uuid.uuid4())

        if name != None:
            self.sqliteSaveSearch(idf, name)

        name.replace(' ', '+')
        name = name.replace('" "', ', ')
        name = name.replace('"', '')
        name = name.replace('  ', ' ')

        print('\nSearching...\n')

        url = [            
            'https://www.bing.com/search?q=%s&cc=se',
            'https://br.search.yahoo.com/search?p=%s&fr=yfp-search-sb&guccounter=1',           
            'https://www.google.se/search?hl=sv&q=%s&tbas=0&tbs=qdr:y,sbd:1&source=lnt&sa=X"\
            "&ved=0ahUKEwisyI2st9vgAhUuHbkGHSTbAGkQpwUIIw&biw=1920&bih=966',
            'https://duckduckgo.com/?q=%s&t=h_&ia=web'
        ]

        self.engine(url[0], 'b', name, idf)
        self.engine(url[1], 'y', name, idf)
        self.engine(url[2], 'g', name, idf)
        self.engine(url[3], 'd', name, idf)


    def mainImages(self):

        name = input('\n\nType search: ')
        idf = str(uuid.uuid4())

        if name != None:
            self.sqliteSaveSearch(idf, f"{name} - images")

        name.replace(' ', '+')
        name = name.replace('" "', ', ')
        name = name.replace('"', '')
        name = name.replace('  ', ' ')

        print('\nSearching...\n')

        url = [            
            'https://www.bing.com/images/search?q=%s&first=1&scenario=ImageBasicHover',
            'https://duckduckgo.com/?q=%s&t=h_&iar=images&iax=images&ia=images&kp=-2'            
        ]

        # self.downloadImages(url[0], 'b', name, idf)
        self.downloadImages(url[1], 'd', name, idf)
    
    
    def engine(self, url, t, name, idf):
        
        browser_core = webdriver.Firefox(executable_path=r'./geckodriver')
        browser_core.minimize_window()
                
        if t == 'b': 
            t = 'Bing' #browsmainImageser_courl, t, name, idfre.find_element_by_class_name("sb_count").text            
            
        if t == 'y': 
            t = 'Yahoo' #browser_core.find_element_by_css_selector(".compPagination span").text            
            
        if t == 'g': 
            t = 'Google' #browser_core.find_element_by_id("appbar").text            
            
        if t == 'd': 
            t = 'DuckDuckGo'

        link = url % name
        browser_core.get(link)

        print(f'browsing on {t}')

        if name != '' :
            img_name = name.replace('+', '_')
            img_name = img_name.replace(' ', '_')

            path = f'data/{img_name}'            

            if os.path.isdir(path) == False:
                os.mkdir(path)

            browser_core.get_screenshot_as_file(f"{path}/{str(uuid.uuid4())}_{t}.png")
            body = browser_core.find_element_by_tag_name("body").text

            if t == 'Bing':
                res_items = browser_core.find_elements_by_css_selector('#b_results .b_algo')
                for rs in res_items:
                    try:
                        if rs.text != '':
                            #print(rs.text)
                            data = {
                                'id' : idf,
                                'description' : rs.text.replace('"', '').replace("'", ''), 
                                'screen_shot' : rs.screenshot_as_base64, 
                                'folder' : img_name, 
                                'engine' : t
                            }

                            self.sqliteSaveRes(data)
                        pass     

                    finally:
                        pass
                    
                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)


            if t == 'Yahoo':                
                res_items = browser_core.find_elements_by_css_selector('div#web ol.searchCenterMiddle li')
                for rs in res_items:
                    try:
                        if rs.text != '':
                            #print(rs.text)                    
                            data = {
                                'id' : idf,
                                'description' : rs.text.replace('"', '').replace("'", ''), 
                                'screen_shot' : rs.screenshot_as_base64, 
                                'folder' : img_name, 
                                'engine' : t
                            }

                            self.sqliteSaveRes(data)
                        pass

                    finally:
                        pass                    

                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)


            if t == 'Google':
                
                res_items = browser_core.find_elements_by_css_selector('div#res div#search .g')
                for rs in res_items:
                    try:
                        if rs.text != '':
                            #print(rs.text)                    
                            data = {
                                'id' : idf,
                                'description' : rs.text.replace('"', '').replace("'", ''), 
                                'screen_shot' : rs.screenshot_as_base64, 
                                'folder' : img_name, 
                                'engine' : t
                            }

                            self.sqliteSaveRes(data)
                        pass

                    finally:
                        pass                    

                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)


            if t == 'DuckDuckGo':
                
                res_items = browser_core.find_elements_by_css_selector('div.results--main div#links div.result.results_links_deep.highlight_d.result--url-above-snippet div.result__body')
                for rs in res_items:
                    try:
                        if rs.text != '':
                            #print(rs.text)                    
                            data = {
                                'id' : idf,
                                'description' : rs.text.replace('"', '').replace("'", ''), 
                                'screen_shot' : rs.screenshot_as_base64, 
                                'folder' : img_name, 
                                'engine' : t
                            }

                            self.sqliteSaveRes(data)
                        pass

                    finally:
                        pass                    

                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)
                        
            self.save_html(body, path, t)
                        
            #     input('Press ENTER to continue >')            
            browser_core.quit() # -- Close window
            time.sleep(5)


    def downloadImages(self, url, t, name, idf):

        browser_core = webdriver.Firefox(executable_path=r'./geckodriver')
        browser_core.minimize_window()
                
        if t == 'b': 
            t = 'Bing' #browser_core.find_element_by_class_name("sb_count").text            
            
        if t == 'y': 
            t = 'Yahoo' #browser_core.find_element_by_css_selector(".compPagination span").text            
            
        if t == 'g': 
            t = 'Google' #browser_core.find_element_by_id("appbar").text            
            
        if t == 'd': 
            t = 'DuckDuckGo'

        link = url % name
        browser_core.get(link)

        print(f'browsing images on {t}')

        if name != '' :
            img_name = name.replace('+', '_')
            img_name = img_name.replace(' ', '_')

            path = f'data/{img_name}'            

            if os.path.isdir(path) == False:
                os.mkdir(path)

            browser_core.get_screenshot_as_file(f"{path}/{str(uuid.uuid4())}_{t}.png")
            #body = browser_core.find_element_by_tag_name("body").text

            images_path_0 = f"{path}/images"
            if os.path.isdir(images_path_0) == False:
                os.mkdir(images_path_0)
            
            if t == 'Bing':
                res_items = browser_core.find_elements_by_css_selector('div#b_content div#vm_c div.dg_b .dgControl.hover .dgControl_list li a.iusc div.img_cont.hoff img')
                number = 0

                images_path = f"{images_path_0}/{t}"
                if os.path.isdir(images_path) == False:
                    os.mkdir(images_path)

                for rs in res_items:                    
                    try:                 
                        urllib.request.urlretrieve(rs.get_attribute('src'), f"{images_path}/{name}_{number}.jpg")
                        number += 1
                        # print(rs.get_attribute('src'))                           

                    finally:
                        pass
                    
                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)

            # if t == 'DuckDuckGo':
            #     res_items = browser_core.find_elements_by_css_selector('#zci-images .tile-wrap .zci__main.zci__main--tiles.js-tiles.has-nav.tileview__images.has-tiles--grid div.tile.tile--img.has-detail .tile--img__media span.tile--img__media__i img.tile--img__img.js-lazyload')
            #     number = 0

            #     for rs in res_items:
            #         try:
            #             urllib.request.urlretrieve(rs.get_attribute('src'), f"{images_path}/{name}_{number}.jpg")
            #             number += 1
            #             #print(rs.get_attribute('src'))                           

            #         finally:
            #             pass
                    
            #         pass

            #     total = int(len(res_items))
            #     print(f"Results: {total}")

            #     self.sqliteUpdateSaveSearch(idf, total, t)

            # if t == 'DuckDuckGo':
            #     res_items = browser_core.find_elements_by_css_selector('#zci-images .tile-wrap .zci__main.zci__main--tiles.js-tiles.has-nav.tileview__images.has-tiles--grid div.tile.tile--img.has-detail .tile--img__media span.tile--img__media__i img.tile--img__img.js-lazyload')
            #     number = 0

            #     for rs in res_items:
            #         try:
            #             urllib.request.urlretrieve(rs.get_attribute('src'), f"{images_path}/{name}_{number}.jpg")
            #             number += 1
            #             #print(rs.get_attribute('src'))                           

            #         finally:
            #             pass
                    
            #         pass

            #     total = int(len(res_items))
            #     print(f"Results: {total}")

            #     self.sqliteUpdateSaveSearch(idf, total, t)

            if t == 'DuckDuckGo':                
                res_items = browser_core.find_elements_by_css_selector('#zci-images .tile-wrap .zci__main.zci__main--tiles.js-tiles.has-nav.tileview__images.has-tiles--grid div.tile.tile--img.has-detail .tile--img__media span.tile--img__media__i img.tile--img__img.js-lazyload')
                number = 0

                images_path = f"{images_path_0}/{t}"
                if os.path.isdir(images_path) == False:
                    os.mkdir(images_path)

                for rs in res_items:
                    try:
                        urllib.request.urlretrieve(rs.get_attribute('src'), f"{images_path}/{name}_{number}.jpg")
                        number += 1
                        #print(rs.get_attribute('src'))                           

                    finally:
                        pass
                    
                    pass

                total = int(len(res_items))
                print(f"Results: {total}")

                self.sqliteUpdateSaveSearch(idf, total, t)

            browser_core.quit() # -- Close window
            time.sleep(5)


    # --- DB

    def db(self):
        return sqlite3.connect('finder.db')

    @staticmethod
    def save_html(body, path_dir, t):
        timex = datetime.datetime.now()
        tmf = str("tm_" + timex.strftime("%I-%M-%S"))
        path = path_dir + f"/result_time_{tmf}_{t}.html"

        try:
            file = open(path, "ab")
            file.write(bytes(body, encoding='utf-8'))
            file.close()
        except IOError:
            file = open(path, "wb")
            file.write(bytes(body, encoding='utf-8'))
            file.close()
        
        return path

    
    def sqliteUpdateSaveSearch(self, idf, res, tbl):

        conn = self.db()
        c = conn.cursor()
        
        if tbl == 'Bing': tbl = 'count_bing'
        if tbl == 'Google': tbl = 'count_google'
        if tbl == 'Yahoo': tbl = 'count_yahoo'
        if tbl == 'DuckDuckGo': tbl = 'count_duck_duck_go'

        c.execute(f"UPDATE searching_for SET {tbl} = {res} WHERE ID_search = '{idf}' ")
        
        conn.commit()        
        conn.close()


    def sqliteSaveSearch(self, idf, search):

        conn = self.db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS searching_for
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        ID_search TEXT NOT NULL UNIQUE,
                        search VARCHAR(255) NOT NULL,
                        count_bing INTEGER NULL,
                        count_google INTEGER NULL,
                        count_yahoo INTEGER NULL,
                        count_duck_duck_go INTEGER NULL,
                        ct DATETIME DEFAULT CURRENT_TIMESTAMP                        
                    )''')
                
        c.execute(f"INSERT INTO searching_for (ID_search, search) VALUES ('{idf}', '{search}')")
        
        conn.commit()        
        conn.close()

    
    def sqliteSaveRes(self, data):

        conn = self.db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS results_data
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        ID_search TEXT NOT NULL,
                        title VARCHAR(255) NULL,                         
                        description TEXT NULL,
                        url TEXT NULL,
                        screen_shot BLOB,
                        folder NVARCHAR(100),
                        engine NCHAR(55),                        
                        ct DATETIME DEFAULT CURRENT_TIMESTAMP                        
                    )''')
        
        # c.execute(f"INSERT INTO results (ID_search, title, description, url, screen_shot, folder, engine) VALUES ('{data['id']}', '{data['title']}', '{data['description']}', '{data['url']}', '{data['screen_shot']}', '{data['folder']}', '{data['engine']}' )")
        c.execute(f"INSERT INTO results_data (ID_search, description, screen_shot, folder, engine) VALUES ('{data['id']}', '{data['description']}', '{data['screen_shot']}', '{data['folder']}', '{data['engine']}' )")
        
        conn.commit()        
        conn.close()


    
start = FinderScript()
start.main()