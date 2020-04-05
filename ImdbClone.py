import requests
import re
import os
import turtle
from pathlib import Path
from bs4 import BeautifulSoup
global way_array
def data_installer():
    # To download data from the imdb webpage,  for loop is used
    # The numbers in the range means that which pages we download
    # There are 16 pages
    for i in range(1, 3):
        #The link of the film page
        link = "https://www.imdb.com/list/ls005750764/?page="
        #Url is created with the page number which is assign by range function
        link = link + str(i)
        url = link
        response = requests.get(url)
        #Some of characters are not shown so data are encoding
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        html_icerigi = response.content
        soup = BeautifulSoup(html_icerigi,"html.parser", from_encoding=encoding)
        array_transfer = []
        #In the page, film stars are taken here
        #but with their name, film votes, cost,lenght are coming
        for i in soup.find_all("p", {"class": "text-muted text-small"}):
            array_transfer.append(str(i.text.strip(" ")))
        stars = []
        #At this progress, the informations except stars' name are deleted and assign in the array
        for i in array_transfer:
            if ("$" not in i):
                if "Votes:" not in i:
                    if "| Gross:" not in i:
                        if "min" not in i:
                            i = i.replace("|", "")
                            i = i.replace("\n", "")
                            i=i.strip(" ")
                            i=i.lower()
                            stars.append(str(i))
        array_transfer_2 = []
        #At this progress, title of the films(names)are taken and assign in the array
        for i in soup.find_all("h3", {"class": "lister-item-header"}):
            i=str(i.text.strip(" "))
            i=i.lower()
            array_transfer_2.append(i)
        data_array = []
        #Spaces and next line character(\n) are deleted
        for i in array_transfer_2:
            array_transfer_1 = []
            i = i.replace("\n", "")
            indexer = i.index(".")
            i = i[indexer + 1:len(i)]
            index_start = i.index("(")
            index_finish = i.index(")")
            i = i[:index_start] + i[index_finish + 1:len(i)]
            i = i.strip()
            array_transfer_1.append(i)
            data_array.append(array_transfer_1)
        counter = 0
        data_array_2 = []
        #Stars and Director title come with the actor name so they are deleted here and the last array which is include only names of acterres
        for i in stars:
            start_index = stars[counter].rindex(":")
            stars[counter].replace("Stars:", "")
            stars[counter].replace(" ", "")
            stars[counter].replace("Director:", "")
            temp_string = stars[counter]
            temp_string = temp_string[start_index + 1:len(stars[counter])]
            temp_string_array=[]
            for i in range(0,3):
                index=temp_string.index(',')
                temp_string_transporter=temp_string[:index]
                temp_string_array.append(temp_string_transporter)
                temp_string=temp_string[index+1:len(temp_string)]
            temp_string_array.append(temp_string)
            counter = counter + 1
            data_array_2.append(temp_string_array)
        #Titles and stars name are combined here
        last_array=zip(data_array,data_array_2)
    return last_array
def writter(array_writter,which_menu):
    #array_writter is the array which result of the selected menu section is saved on it
    #which_menu is the shown that which menu option is selected
    my_file = Path("result.txt")
    #If file is not exist, given information is written
    if my_file.is_file():
        file_for_write=open("result.txt","a",encoding="utf-8")
        file_for_write.write(which_menu+'\n')
        for file_writter in array_writter:
            if(file_writter!=''):
                file_for_write.write(file_writter+'\n')
    #If the file is exist, given information is written
    else:
        file_for_write = open("result.txt", "w",encoding="utf-8")
        file_for_write.write(which_menu+'\n')
        for file_writter in array_writter:
            if(file_writter!=''):
                file_for_write.write(file_writter+'\n')
def menu_creater():
    print("                                     _________ ")
    print("                                    |         |")
    print("                                    |   MENU  |")
    print("+-----------------------------------|         |----------------------------------------+")
    print("| 1.All movies of actor or actress.                                                    |")
    print("| 2.List Actor with Whom Acted                                                         |")
    print("| 3.List all actors and actresses in a movie.                                          |")
    print("| 4.List all actors and actresses in two movies.                                       |")
    print("| 5.List all actors and actresses in either of the movies but not both.                |")
    print("| 6.List Actors in Either of The Movies                                                |")
    print("| 7.Save The Result                                                                    |")
    print("| 0.Exit                                                                               |")
    print("+--------------------------------------------------------------------------------------+")
    print('\n')
def menu_type_1(data_array,file_array):
    actors = input("Please enter actor name")
    actors = actors.lower()
    actors=actors.strip(" ")
    list_of_actors = actors.split(",")
    for index in list_of_actors:
        set_menu_1 = set()
        if (index != ''):
            for index_2 in file_array:
                if index in index_2:
                    for index_3 in index_2:
                        if index_3 != index:
                            set_menu_1.add(index_3)
            for index_2 in data_array:
                for index_3 in index_2[1]:
                    if index == index_3:
                        element = str(index_2[0][0])
                        set_menu_1.add(element)
                        break
            print("***-----------------***")
            print(index)
            for printer in set_menu_1:
                print(printer)
            writter(set_menu_1, "Menu Option 1"+'\n'+actors)
            print("***-----------------***")
def menu_type_2(data_array,file_array):
    actors = input("Please enter the actor name")
    actors = actors.lower()
    actors=actors.strip(" ")
    actors_array = list()
    actors = actors.replace(".","")
    actors_array=re.split(',', actors)
    for actors_array_index in actors_array:
        actor_helper = set()
        actors_film = set()
        for film_finder in file_array:
            counter=0
            if actors_array_index in film_finder:
                for indexer in film_finder:
                    counter = counter + 1
                    if (counter > 1 and indexer!=actors_array_index):
                        actors_film.add(indexer)
        for film_selector in actors_film:
            for indexer_2 in file_array:
                if (indexer_2 in file_array):
                    actor_helper.add(indexer_2[0])
        for index in data_array:
            for index_2 in index[1]:
                actors_array_index = str(actors_array_index)
                actors_array_index = actors_array_index.replace("[", "")
                actors_array_index = actors_array_index.replace("'", "")
                actors_array_index = actors_array_index.replace("]", "")
                if actors_array_index == index_2:
                    for index_2 in index[1]:
                        if actors_array_index != index_2:
                            actor_helper.add(str(index_2))
        print(actors_array_index, " Helpers")
        print("***--------------------***")
        for printer_for_menu_2 in actor_helper:
            print(printer_for_menu_2)
        print("***--------------------***")
        writter(actor_helper, "Menu Section 2" + '\n' + actors_array_index)
def menu_type_3_and_4(data_array,file_array,type_of_input):
    film_one = input("Please enter the film name")
    film_one = film_one.lower()
    film_one = film_one.strip(" ")
    film_one = film_one.replace('\n', ' ')
    array_menu_4 = list()
    printer = set()
    searcher = film_one
    for film_finder in file_array:
        for index in film_finder:
            index=index.lstrip(" ")
            if(index==film_one):
                actor_in_the_film = film_finder[0]
                printer.add(actor_in_the_film)
    for film_finder in data_array:
        if searcher in str(film_finder[0]):
            for index_2 in film_finder[1]:
                printer.add(index_2)
    if (type_of_input == 4):
        film_two = input("Please enter the film name")
        film_two = film_two.lower()
        film_two = film_two.strip(" ")
        film_two = film_two.replace('\n', ' ')
        searcher = film_two
        for film_finder in file_array:
            for index in film_finder:
                index=index.lstrip(" ")
                if (film_two==index):
                    actor_in_the_film = film_finder[0]
                    printer.add(actor_in_the_film)
        for film_finder in data_array:
            if searcher in str(film_finder[0]):
                for index_2 in film_finder[1]:
                    printer.add(index_2)
        print("***-----------------***")
        for index in printer:
            array_menu_4.append(index)
            print(index)
        print("***-----------------***")
        writter(array_menu_4, "Menu Option 4" + '\n' + film_one + " & " + film_two)
    else:
        print("***-----------------***")
        for index in printer:
            array_menu_4.append(index)
            print(index)
        print("***-----------------***")
        writter(array_menu_4, "Menu Option 3" + '\n' + film_one)
def menu_type_5_and_6(data_array,file_array,type_of_input):
    film_one = input("Please enter the actor name")
    film_one = film_one.lower()
    film_one = film_one.strip(" ")
    film_one = film_one.replace('\n', ' ')
    array_menu_5 = list()
    printer = set()
    searcher = film_one
    for film_finder in file_array:
        for index in film_finder:
            index = index.lstrip(" ")
            if (film_one == index):
                actor_in_the_film = film_finder[0]
                printer.add(actor_in_the_film)
    for film_finder in data_array:
        if searcher in str(film_finder[0]):
            for index_2 in film_finder[1]:
                printer.add(index_2)
    film_two = input("Please enter the actor name")
    film_two = film_two.lower()
    film_two = film_two.strip(" ")
    film_two = film_two.replace('\n', ' ')
    array_menu_5.append(" and " + film_two)
    printer_2 = set()
    searcher = film_two
    for film_finder in file_array:
        for index in film_finder:
            index = index.lstrip(" ")
            if (film_two == index):
                actor_in_the_film = film_finder[0]
                printer_2.add(actor_in_the_film)
    for film_finder in data_array:
        if searcher in str(film_finder[0]):
            for index_2 in film_finder[1]:
                printer_2.add(index_2)
    if (type_of_input == 5):
        printer = printer.intersection(printer_2)
        print("***-----------------***")
        for index in printer:
            print(index)
            array_menu_5.append(index)
        print("***-----------------***")
        writter(array_menu_5,
                "Menu Option 5" + '\n' + "COMMON ACTOR OR ACTRESSES IN " + film_one.upper() + " & " + film_two.upper())
    else:
        printer = printer ^ printer_2
        print("***-----------------***")
        for index in printer:
            print(index)
            array_menu_5.append(index)
        print("***-----------------***")
        writter(array_menu_5, "Menu Option 6")
def graph_creator(way_array):
    #The page which the graph of the user searchs is drawn
    t = turtle.Turtle()
    t.hideturtle()
    #Vertices of the graph are drawn
    t.dot(14, "BLACK")
    t.forward(80)
    t.dot(14, "BLACK")
    is_drawn_1="false"
    is_drawn_2="false"
    is_drawn_3="false"
    is_drawn_4="false"
    is_drawn_5="false"
    is_drawn_6="false"
    graph_check=set()
    #Graph is drawn here
    #graph_check is created because if all possible vertices is drawn, the loop will end
    for i in way_array:
        t.hideturtle()
        if i == 1 and is_drawn_1=="false":
            t.right(150)
            t.forward(80)
            t.dot(14, "BLACK")
            t.left(180)
            t.forward(80)
            is_drawn_1="true"
        elif i == 2 and is_drawn_2=="false":
            t.right(150)
            t.forward(80)
            if is_drawn_1=="true":
                t.right(100)
                t.forward(40)
                t.left(180)
                t.forward(40)
                t.right(80)
            t.dot(14, "BLACK")
            t.left(180)
            t.forward(80)
            is_drawn_2="true"
        elif i == 3 and is_drawn_3=="false":
            t.right(150)
            t.forward(130)
            t.dot(14, "BLACK")
            t.left(180)
            t.forward(130)
            is_drawn_3="true"
        elif i == 4 and is_drawn_4=="false":
            t.right(150)
            t.forward(145)
            if is_drawn_3=="true":
                t.right(116.32)
                t.forward(80)
                t.left(180)
                t.forward(80)
                t.left(-63.68)
            t.dot(14, "BLACK")
            t.left(180)
            t.forward(145)
            is_drawn_4="true"
        elif i == 5 and is_drawn_5=="false":
            t.right(170)
            t.forward(190)
            if is_drawn_4=="true":
                t.right(152.32)
                t.forward(60)
                t.left(180)
                t.forward(60)
            t.dot(14, "BLACK")
            t.goto(80, 0)
            is_drawn_5="true"
        elif i == 6 and is_drawn_6=="false":
            t.right(20)
            t.forward(120)
            t.dot(14, "BLACK")
            if is_drawn_5=="true":
                t.right(70)
                t.forward(54)
                t.left(-63.68)
            is_drawn_6="true"
        graph_check.add(i)
        if len(graph_check)==7:
            break
    if len(graph_check)!=0:
        t.hideturtle()
        t.penup()
        if is_drawn_1=="true":
            t.goto(-75.50,-57)
            t.write("MENU OPTION 1")
        if is_drawn_2 == "true":
            t.goto(-70.50,-86.28)
            t.write("MENU OPTION 2")
        if is_drawn_3 == "true":
            t.goto(81,-148)
            t.write("MENU OPTION 3")
        if is_drawn_4 == "true":
            t.goto(170,-133.57)
            t.write("MENU OPTION 4")
        if is_drawn_5 == "true":
            t.goto(213.63,-163.55)
            t.write("MENU OPTION 5")
        if is_drawn_6 == "true":
            t.goto(170.23,-98.79)
            t.write("MENU OPTION 6")
        t.goto(0,10)
        t.write("FILMS")
        t.goto(86,10)
        t.write("ACTRESS")
        turtle.done()
def menu_decision(type_of_input,data_array):
    file_array = list()
    path_of_the_data="movies.csv"
    path_of_the_data_save="movies.csv"
    #File is opened here to read
    my_file = Path(path_of_the_data)
    # If file is not exist, given information is written
    wrong_data="false"
    if my_file.is_file():
        wrong_data="false"
    else:
        wrong_data="true"
    while wrong_data=="true":
        print("Program doesn't work.Do you want to enter a new path?(Y(yes) or N(no))"+'\n'+"If you enter the N program will be closed or you can use default path(Press q)")
        entry_of_path = "nothing"
        try:
            entry_of_path = str(input())
            entry_of_path = entry_of_path.lower()
        except:
            entry_of_path = "nothing"
        while entry_of_path != "y" and entry_of_path != "n" and entry_of_path != "q" :
            print("PLEASE PRESS ONLY Y OR N")
            entry_of_path = str(input())
            entry_of_path = entry_of_path.lower()
        if(entry_of_path=="n"):
            exit()
        elif(entry_of_path=="q"):
            path_of_the_data=path_of_the_data_save
            wrong_data = "false"
        else:
            path_of_the_data=str(input("Please enter the path"))
            my_file = Path(path_of_the_data)
            if my_file.is_file():
                wrong_data = "false"
            else:
                wrong_data = "true"
    file = open(path_of_the_data, "r",encoding="utf-8")
    line = file.readline()
    #Line which was read,is edited here
    line=line.lower()
    line=line.rstrip(" ")
    line=line.lstrip(" ")
    #While loop check the file if it is empty
    while line != '':
        line = line.replace(";", ",")
        line=line.rstrip('\n')
        file_array.append(re.split(',', line))
        line = file.readline()
        line=line.lower()
        line=line.rstrip(" ")
        line=line.lstrip(" ")
    if(type_of_input==1):
        menu_type_1(data_array,file_array)
    elif(type_of_input==2):
        menu_type_2(data_array, file_array)
    elif(type_of_input == 3 or type_of_input == 4):
        menu_type_3_and_4(data_array, file_array, type_of_input)
    else:
        menu_type_5_and_6(data_array,file_array,type_of_input)
def main():
    way_array=list()
    #Menu is written here
    menu_creater()
    print("PLEASE WAIT... FILM DATAS IS DOWNLOAD...( in less than 1 minute)")
    #List of the film is download here and assing here
    list_of_imdb=list(data_installer())
    program_finish="false"
    save_the_file="false"
    entry = -1
    while program_finish=="false":
        # Input of the menu option is taken here
        check="false"
        try:
            entry = int(input("Please enter a number in table" + "\t"))
        except:
            print("Please enter a number")
            check="true"
        if(entry>8 or entry<0):
            check="true"
        # Input is checked here. If input is zero or seven while loop will be ended
        while check=="true":
            no_error="true"
            try:
                entry = int(input("Please enter a number in table correct"))
            except:
                print("Please enter a number")
                no_error="false"
            if entry>8 or entry<0:
                no_error="false"
            if no_error=="true":
                check="false"
        if(entry!=0 and entry!=7):
            menu_decision(entry,list_of_imdb)
            menu_creater()
            way_array.append(entry)
        elif(entry==7 or entry==0):
            program_finish="true"
            if(entry==7):
                save_the_file="true"
    #At the all option, results is written so if the user enter zero, text document will be deleted
    if(entry==0):
        if save_the_file=="false":
            my_file = Path("result.txt")
            if my_file.is_file():
                os.remove("result.txt")
    if(entry==0 or entry==7):
        print("Do you want to see the graph of your search ?(Press only Y(yes) or N(no)")
        entry_of_graph="nothing"
        try:
            entry_of_graph=str(input())
            entry_of_graph=entry_of_graph.lower()
        except:
            entry_of_graph = "nothing"
        while entry_of_graph!="y" and entry_of_graph!="n":
            print("PLEASE PRESS ONLY Y OR N")
            entry_of_graph = str(input())
            entry_of_graph = entry_of_graph.lower()
        if entry_of_graph=="y":
            print("NOW YOU WILL SEE A NEW APPLICATION ON THE COMPUTER WHICH WAS ALREAD OPENED ON THE BELOW ")
            graph_creator(way_array)
            decision=input("PRESS ANY BUTTONTO EXIT...")
main()
