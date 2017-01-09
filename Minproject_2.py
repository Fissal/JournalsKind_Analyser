__author__ = 'fissalalsharef'



from BeautifulSoup import *
from urllib2 import *
from Tkinter import *
from urlparse import urljoin
import clusters
from clusters import *
from nltk.corpus import stopwords
import nltk

re_title = re.compile("^(<.*>)(.*)(<.*>)$",re.VERBOSE)
forbided_words = ['and','or','of','a','an','on','in','the','to','for','about','articles','columns','Articles','COLUMNS','which,that',
                  'who','were','was','whom','when','where','there','nbsp','this']
data_dict1 = {}

class DailySabahanalyser():

    def __init__(self):
        self.sharedwords = dict()
        self.allwords = dict()
        self.list =[]
        self.list1=[]

        self.Interface()

    def opening_url_and_making_soup(self,url):
            request = Request(url)
            response = urlopen(request)
            html_version = response.read()
            soup = BeautifulSoup(html_version)
            return soup


    def Make_Matrix(self):
        dic = self.fetcher_only_Journalists_and_words()
        dic1 = self.fetcher_All_Words()
        count1 = 0
        file2 = open('Matrix','w')
        file2.write('Journalist name' + '\t')
        for i in dic1:
            file2.write(i + '\t')
        for name in dic:
            file2.write('\n' + name + '\t')
            count1 += 1
            for w in dic1:
                if w not in dic[name]:
                    file2.write('0\t')
                else:
                    file2.write(str(dic[name][w]) + '\t')


    def fetcher_only_Journalists_and_words(self):
        dic = self.fetcher_Journalist_with_Titles()
        da_dict = {}
        for key_1 in dic:
            da_dict.setdefault(key_1,{})
            for Titles in dic[key_1]:
                for word in dic[key_1][Titles]:
                    if word in da_dict[key_1]:
                        da_dict[key_1][word] += 1
                    else:
                        da_dict[key_1].setdefault(word,1)
        return da_dict


    def fetcher_All_Words(self):
        dic = self.fetcher_Journalist_with_Titles()
        da_dict = {}
        for key_1 in dic:
            for Titles in dic[key_1]:
                for word in dic[key_1][Titles]:
                    if word in da_dict:
                        da_dict[word] += dic[key_1][Titles][word]
                    else:
                        da_dict[word] = dic[key_1][Titles][word]

        return da_dict

    def Reverse_Fetcher_Dictionary(self):
        dic = self.fetcher_Journalist_with_Titles()
        da_dict = {}
        for key_1 in dic:
            for Titles in dic[key_1]:
                for word in dic[key_1][Titles]:
                    if word not in da_dict:
                        da_dict.setdefault(word,[])
                        da_dict[word].append((dic[key_1][Titles][word],Titles))
                    else:
                        da_dict[word].append((dic[key_1][Titles][word],Titles))

        return da_dict

    def Downloading_Urls(self):

        links = []
        if len(self.Entryofurls.get(1.0,END)) <= 15:
            self.Error_Message()

        self.Listofdownloading_Journlasits.delete(0,END)
        input_for_urls = self.Entryofurls.get(0.0,'end-1c')
        for i in input_for_urls.split('\n'):
            if len(self.Entryofurls.get(1.0,END)) >= 15:
                self.Listofdownloading_Journlasits.insert(END,"Downloaded")
            links.append(i)

        return links


    def fetcher_Journalist_with_Titles(self):
        list_of_journalists_names = []
        self.list2 = []
        links = self.Downloading_Urls()
        # links = ['http://www.dailysabah.com/columns/yahya_bostan/archive', 'http://www.dailysabah.com/columns/cetin-kaya-koc/archive', 'http://www.dailysabah.com/columns/hatem-ete/archive','http://www.dailysabah.com/columns/halit-yerebakan/archive']
        count1 = 0

        for link in links:
            name = link.split("/")
            list_of_journalists_names.append(name[4])
            soup = self.opening_url_and_making_soup(link)

            count = 0
            for i in soup.fetch('a'):
                if ('target' in dict(i.attrs)) and (i['target'] == "_blank"):
                    new_url  = urljoin(link,i['href'])
                    new_soup = self.opening_url_and_making_soup(new_url)

                    for i in new_soup.fetch('h1'):
                        if ('id' in dict(i.attrs)) and (i['id'] == "newsTitle"):
                            so = BeautifulSoup(str(i))
                            title = re_title.match(str(so)).group(2)
                            self.list2.append(title)

                    for ii in new_soup.fetch('div'):
                        if ('class' in dict(ii.attrs))and (ii['class'] == "txtIn"):
                            data_dict1.setdefault(list_of_journalists_names[count1],{})
                            data_dict1[list_of_journalists_names[count1]].setdefault(self.list2[count],{})
                            # print data_dict1
                            so1 = BeautifulSoup(str(ii))
                            all_text = ''.join(so1.findAll(text=True))
                            tokens = nltk.word_tokenize(all_text)
                            stopset = set(stopwords.words('english'))
                            cleanup = []
                            for token in tokens:
                                if token not in stopset and len(token)>3:
                                    cleanup.append(token.lower())
                            Converting_the_list = ' '.join(cleanup)
                            splitter = re.compile('\\W*')
                            words = [s.lower() for s in splitter.split(Converting_the_list) if len(s)>1 and len(s)<10 and s not in forbided_words]
                            for w in words:
                                if w in data_dict1[list_of_journalists_names[count1]][self.list2[count]]:
                                    data_dict1[list_of_journalists_names[count1]][str(self.list2[count])][w] += 1
                                else:
                                    data_dict1[list_of_journalists_names[count1]][str(self.list2[count])].setdefault(w,1)

                            count += 1
            count1 += 1

        return data_dict1

    def Error_Message(self):
        error_Window = Toplevel()
        error_Massage = Label(error_Window,text = """Please Insert the URLs\nand Download them""",font="Times 40 bold",fg = "red", bg = "black")
        error_Massage.pack()


    def view_Top_n_words(self):
        try:
            dic = self.fetcher_All_Words()

            if len(data_dict1) == 0:
                self.Error_Message()

            Top_n_Words = []
            input = self.words.get()
            convert_to_tuple = [(v, k) for k, v in dic.items()]
            sort_The_tuble = sorted(convert_to_tuple,reverse=True)

            for i in range(input):
                Top_n_Words.append(sort_The_tuble[i])

            self.All_Results.delete(0,END)
            for i in Top_n_Words:
                output = "%s              %d" %(i[1], i[0])
                self.All_Results.insert(END, output)

            return Top_n_Words

        except:
            pass


    def view_Top_n_Articles(self):

        try:
            dic = self.Reverse_Fetcher_Dictionary()
            dic1 = self.view_Top_n_words()
            list_of_top_n_words = []
            list_of_top_titles = []

            if len(data_dict1) == 0:
                    self.Error_Message()

            for i in dic1:
                list_of_top_n_words.append(i[1])

            self.All_Results.delete(0,END)
            input = self.Articles.get()
            for word in dic:
                if word in list_of_top_n_words:
                    v = sorted(dic[word],reverse=True)
                    for i in range(input):
                        try:
                            output = "%s             %d               %s" %(word,v[i][0],v[i][1])
                            self.All_Results.insert(END,output)
                        except:
                            pass

        #     return list_of_top_titles
        except:
            pass


    def Clustering(self):
        try:
            dic = self.fetcher_Journalist_with_Titles()

            if len(data_dict1) == 0:
                self.Error_Message()
                return

            Matrix = self.Make_Matrix()
            Journlist,word,freq = clusters.readfile('Matrix')
            if self.Radio_Values3.get() == 0:
                H_clustering = hcluster(freq)
                self.All_Results.delete(0,END)
                for i in range(len(clust2str(H_clustering,labels = Journlist).split('\n'))):
                    self.All_Results.insert(END, clust2str(H_clustering,labels = Journlist).split('\n')[i])
            elif self.Radio_Values3.get() == 1:
                K_Vlaue = self.Valueof_k.get()
                Cluster_Value = kcluster(freq,k = int(K_Vlaue))
                Journalists = dic.keys()
                list = [(len(i),i) for i in Cluster_Value]
                list.sort(reverse=True)
                counter = 0
                self.All_Results.delete(0,END)
                for i,j in list:
                    list1 = [Journalists[k] for k in range(len(j))]
                    new_str = ""
                    for i in list1:
                        new_str += str(i)+"  "
                    self.All_Results.insert(END,"Cluster %d:{"%(counter+1)+new_str+"}"+"\n")
                    counter += 1

        except:
            pass



    def Interface(self):

        # Main window part
        self.root = Tk()
        self.root.geometry("1000x1000+100+-22")
        self.root.resizable(width=False,height=False)
        self.cluster = IntVar()
        self.words = IntVar()
        self.Articles = IntVar()

        #Background part
        self.Background = Label(self.root,bg="black")
        self.Background.place(relx = 0.0,rely = 0.0,width = 1000,height = 1000)

        #Title of project part
        self.Title = Label(self.root,text = 'Journalism Puplication Analyzer v1.0',font = "Times 30 bold")
        self.Title.place(relx = 0.2,rely = 0.0)

        #Quit Button
        self.QuitButton = Button(self.root,text = "Quit",bg = "Red", command=self.root.quit)
        self.QuitButton.place(relx = 0.97,rely = 0.0)

        #Left part of project
        self.Titleofurls = Label(self.root,text = 'Please enter Daily Sabah profile URLs(one URL per line:)',font= "Times 16")
        self.Titleofurls.place(relx = 0.05 ,rely = 0.08)
        self.Entryofurls = Text(self.root,font = ("Times 7",10))
        self.Entryofurls.place(relx = 0.05 ,rely =0.13,height = 150,width=500)

        #Right part of project
        self.Buttonof_profiles = Button(self.root,text = 'Download Publication Profiles',font = "Times 15", command=self.Downloading_Urls)
        self.Buttonof_profiles.place(relx = 0.65,rely = 0.08)
        self.Listofdownloading_Journlasits = Listbox(self.root,font = "Times 12")
        self.Listofdownloading_Journlasits.place(relx = 0.65,rely=0.13,height = 150,width = 250)


        self.Title_of_listing_Words = Label(self.root,text='View Words',font ="Times 15")
        self.Title_of_listing_Words.place(relx = 0.05,rely =0.29)
        self.Background_of_WordsList_part = Label(self.root,bg = "Light Blue")
        self.Background_of_WordsList_part.place(relx =0.05 ,rely = 0.318,width = 220,height=200)
        self.Background_of_WordsList_part = Label(self.root,bg = "Light Blue")
        self.Background_of_WordsList_part.place(relx =0.35 ,rely = 0.318,width = 220,height=200)
        self.Combobox = Label(self.root,text = """Choose the\n   number of\n words:""",bg = "Light Blue",font = "Times 10 bold")
        self.Combobox.place(relx = 0.05,rely=0.33,width=75,height = 50)
        self.Nameof_Words = Label(self.root,text = "Price:",font = "Times 10 bold",fg='white',bg='black')
        self.Nameof_Words.place(relx = 0.13,rely= 0.34)
        self.Valueof_Words = Entry(self.root,textvariable = self.words)
        self.Valueof_Words.place(relx = 0.16,rely = 0.34,width = 50)

        self.ButtonofListing_Words = Button(self.root,text = 'View Words',font = "Times 13",command=self.view_Top_n_words)
        self.ButtonofListing_Words.place(relx = 0.16 ,rely = 0.47)
        self.Title_of_listing_Articles = Label(self.root,text='View Articles',font ="Times 15")
        self.Title_of_listing_Articles.place(relx = 0.35,rely =0.290)
        self.Combobox = Label(self.root,text = """Choose the\n   number of\n Articles:""",bg = "Light Blue",font = "Times 10 bold")
        self.Combobox.place(relx = 0.35,rely=0.324,width=75,height = 50)
        self.Nameof_Articles = Label(self.root,text = "No:",font = "Times 10 bold",fg='white',bg='black')
        self.Nameof_Articles.place(relx = 0.43,rely= 0.334)
        self.Valueof_No_of_Articles = Entry(self.root,textvariable = self.Articles)
        self.Valueof_No_of_Articles.place(relx = 0.46,rely = 0.334,width = 50)

        self.ButtonofListing_Articles = Button(self.root,text = 'View Articles',font = "Times 13", command= self.view_Top_n_Articles)
        self.ButtonofListing_Articles.place(relx = 0.45 ,rely = 0.467)


        self.Titleofviewing_clusterings = Label(self.root,text='Cluster Journalists',font ="Times 15")
        self.Titleofviewing_clusterings.place(relx = 0.65,rely =0.29)
        self.Backgroundofvievingclustrings = Label(self.root,bg = "Light Blue")
        self.Backgroundofvievingclustrings.place(relx =0.65 ,rely = 0.318,width = 250,height=200)

        self.Name_of_Radio_Button3 = Label(self.root,text = "Clustering Method:",bg = "Light Blue",font = "Times 10 bold")
        self.Name_of_Radio_Button3.place(relx = 0.65,rely=0.32,width=125,height = 50)
        self.Radio_Values3 = IntVar()
        self.Types_of_Clustring1 = Radiobutton(self.root,text = "Hiearacial",variable = self.Radio_Values3,bg = "Light Blue",value = 0)
        self.Types_of_Clustring1.place(relx = 0.68 ,rely = 0.36)
        self.Types_of_Clustring2 = Radiobutton(self.root,text = "K-Means",variable = self.Radio_Values3,bg = "Light Blue",value = 1)
        self.Types_of_Clustring2.place(relx = 0.68 ,rely = 0.385)
        self.Radio_Values3.set(0)

        self.Nameof_k = Label(self.root,text = "k:",font = "Times 10 bold",bg = "Light Blue")
        self.Nameof_k.place(relx = 0.8,rely= 0.385)
        self.Valueof_k = Entry(self.root,textvariable = self.cluster)
        self.Valueof_k.place(relx = 0.82,rely = 0.385,width = 50)


        self.Button = Button(self.root,text = 'View Clusters',font = "Times 13",command= self.Clustering)
        self.Button.place(relx = 0.77 ,rely = 0.47)


        self.All_Results = Listbox(self.root,font = "Bold 12")
        self.All_Results.place(relx = 0.05,rely = 0.530,width = 850,height = 200)
        self.scroll = Scrollbar(self.All_Results)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command = self.All_Results.yview)


        mainloop()



Application = DailySabahanalyser()







