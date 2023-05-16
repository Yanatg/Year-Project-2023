from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from facade import CountryFacade
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from PIL import Image
import webbrowser
import socket
import os
from threading import Thread


class CountryManage(ctk.CTk):
    """ Main class of the app. The class manages the main window and the pages.
        Also contains the facade. """

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Countries of the World")
        self.geometry(f"1080x720+{int(self.winfo_screenwidth() / 2 - 540)}+" +
                      f"{int(self.winfo_screenheight() / 2 - 400)}")
        self.resizable(False, False)
        # set the frame of the app
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        # create the facade instance
        self.facade = CountryFacade()

    def raise_page(self, page):
        """ Raise a page of the app. """

        # self.frame refers to the frame of the main window of the app.
        page_to_show = page(self, self.frame)
        page_to_show.grid(row=0, column=0, sticky="nsew")
        page_to_show.lift()

    def run_app(self):
        """ Run the app. and raise the homepage first."""
        
        self.raise_page(Home)
        self.mainloop()


class FramePage(ctk.CTkFrame):
    """ Base class of all the pages in the app. """

    def __init__(self, root, main_frame):
        super().__init__(main_frame)
        # the root is the main window of the app
        self.root = root
        self.facade = root.facade
        self.set_bg()

    def set_bg(self, pic="pics/homepage_bg.png"):
        """ Set the background of the page. """

        pic_path = os.path.join(os.getcwd(), pic)
        bg_pic = Image.open(pic_path)
        bg = ctk.CTkImage(light_image=bg_pic, dark_image=bg_pic, size=(1080, 720))
        bg_label = ctk.CTkLabel(self, text='', image=bg)
        bg_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_button(self):
        """ Set the menu buttons of the page. """

        button_style = {"font": ("PK Maehongson", 17), "fg_color": "#071638", "text_color": "white",
                        "hover_color": "#7ea5e8", "corner_radius": 0}
        general_btn = ctk.CTkButton(self, text="GENERAL DATAS",
                                    command=lambda: self.root.raise_page(GeneralPage),
                                    **button_style)
        general_btn.place(relx=0.75, rely=0.05, anchor="center")

        statistic_btn = ctk.CTkButton(self, text="STATISTIC DATAS",
                                      command=lambda: self.root.raise_page(DefaultGraphPage),
                                      **button_style)
        statistic_btn.place(relx=0.875, rely=0.05, anchor="center")

        home_btn = ctk.CTkButton(self, text="HOME",
                                 command=lambda: self.root.raise_page(Home),
                                 **button_style)
        home_btn.configure(fg_color="#071c44")
        home_btn.place(relx=0.125, rely=0.05, anchor="center")


class Home(FramePage):
    """ The home page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/home_bg.png")
        self.set_button()
        self.set_label()

    def set_label(self):
        """ Set the title of the app. """

        info_button = ctk.CTkButton(self, text=" MORE  INFO", font=("PK Maehongson", 17),
                                    text_color="white", fg_color="#0b265c",
                                    hover_color="#7ea5e8", corner_radius=0,
                                    command=lambda: self.root.raise_page(InfoPage))
        info_button.place(relx=0.5, rely=0.9, anchor="center")


class GeneralPage(FramePage):
    """ The general data menu page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/general_bg.png")
        self.set_button()

    def set_button(self):
        """ Set the buttons of the page. """

        super(GeneralPage, self).set_button()
        button_style = {"font": ("PK Maehongson", 17), "text_color": "white",
                        "hover_color": "#7ea5e8", "corner_radius": 0,
                        "border_color": "#84c2fd", "border_width": 2}
        search_name_btn = ctk.CTkButton(self, text="search by name", **button_style,
                                        fg_color="#0b255a",
                                        command=lambda: self.root.raise_page(SearchByNamePage))
        search_name_btn.place(relx=0.275, rely=0.75, anchor="center")

        search_region_btn = ctk.CTkButton(self, text="search by region", **button_style,
                                          fg_color="#0b255a",
                                          command=lambda: self.root.raise_page(SearchByRegionPage))
        search_region_btn.place(relx=0.725, rely=0.75, anchor="center")


class SearchByNamePage(FramePage):
    """ The search by name page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/search_name_bg.png")
        self.data_label_list = []
        self.name_label = None
        self.set_button()
        self.set_search_bar()
        self.set_label()
        self.data_label = None
        # data of the country
        self.name = None
        self.region = None
        self.population = None
        self.area = None
        self.pop_den = None
        self.net_migration = None
        self.infant_mortal = None
        self.gdp = None

    def set_label(self):
        """ Set the labels of the page. """

        search_label = ctk.CTkLabel(self, text="Search the country's name",
                                    font=("PK Maehongson", 35, "bold"),
                                    text_color="white", fg_color="#092150")
        search_label.place(relx=0.225, rely=0.2, anchor="center")

        y = 0.33
        for key, value in self.facade.search_by_name("Afghanistan").items():
            subject_label = ctk.CTkLabel(self, text=f"{key}", font=("PK Maehongson", 20),
                                         text_color="white", fg_color="#2f3e6d")
            subject_label.place(relx=0.5, rely=y, anchor="nw")

            self.data_label = ctk.CTkLabel(self, text=f"{value}", font=("PK Maehongson", 20),
                                           text_color="white", fg_color="#2b3355")
            self.data_label.place(relx=0.9, rely=y, anchor="ne")
            self.data_label_list.append(self.data_label)

            y += 0.06

        self.name_label = ctk.CTkLabel(self, text="Afghanistan",
                                       font=("PK Maehongson", 40, "bold"),
                                       text_color="white", fg_color="#0a2354")
        self.name_label.place(relx=0.48, rely=0.15, anchor="nw")

    def set_search_bar(self):
        """ Set the search bar of the page. """

        search_bar_style = {"font": ("PK Maehongson", 17), "width": 350, "border_width": 0,
                            "corner_radius": 0,
                            "button_color": "#ffc661", "dropdown_fg_color": "#5ad2ae",
                            "text_color": "black", "fg_color": "#4baf91", "bg_color": "#4baf91"}

        combobox_var = ctk.StringVar(value="Afghanistan")  # set initial value
        country_name = self.facade.get_all_countries()

        combobox = ctk.CTkComboBox(self,
                                   values=country_name,
                                   variable=combobox_var,
                                   **search_bar_style,
                                   command=lambda x: self.show_data(combobox_var.get()))
        combobox.place(relx=0.225, rely=0.3, anchor="center")

    def show_data(self, name):
        """ Show the data of the country. """

        country_data_dict = self.facade.search_by_name(name)

        for label in self.data_label_list:
            label.destroy()

        self.name_label.configure(text=country_data_dict["Name"])
        self.name_label.place(relx=0.48, rely=0.15, anchor="nw")

        data_list = [self.name, self.region, self.population, self.area, self.pop_den,
                     self.net_migration, self.infant_mortal, self.gdp]
        index = 0
        y = 0.33
        for key, value in country_data_dict.items():
            data_list[index] = ctk.CTkLabel(self, text=f"{value}", font=("PK Maehongson", 20),
                                            text_color="white", fg_color="#2b3355")
            data = data_list[index]
            data.place(relx=0.9, rely=y, anchor="ne")
            self.data_label_list.append(data)
            y += 0.06
            index += 1


class SearchByRegionPage(FramePage):
    """ The search by region page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/search_region.png")
        self.set_button()
        self.set_label()
        self.search_label = None

    def set_label(self):
        """ Set the labels of the page. """

        self.search_label = ctk.CTkLabel(self, text="Select the region to see the countries",
                                         font=("PK Maehongson", 35, "bold"),
                                         text_color="white", fg_color="#09204e")
        self.search_label.place(relx=0.5, rely=0.16, anchor="center")

        btn_style = {"font": ("PK Maehongson", 17), "text_color": "#05102a",
                     "corner_radius": 0, "border_width": 0, "hover": False}
        europe_btn = ctk.CTkButton(self, text="Europe", **btn_style,
                                   command=lambda: self.show_region("EUROPE"))
        europe_btn.configure(bg_color='#e9e283', fg_color='#e9e283', width=15, height=0.5,
                             font=("PK Maehongson", 10, "bold"))

        asia_btn = ctk.CTkButton(self, text="Asia", **btn_style,
                                 command=lambda: self.show_region("ASIA"))
        asia_btn.configure(bg_color='#9e8efd', fg_color='#9e8efd', width=10, height=1)

        africa_btn = ctk.CTkButton(self, text="Africa", **btn_style,
                                   command=lambda: self.show_region("AFRICA"))
        africa_btn.configure(bg_color='#3fe0fa', fg_color='#3fe0fa', width=13, height=2,
                             font=("PK Maehongson", 14, "bold"))

        north_america_btn = ctk.CTkButton(self, text="North America", **btn_style,
                                          command=lambda: self.show_region("NORTH AMERICA"))
        north_america_btn.configure(bg_color='#40f281', fg_color='#40f281', width=15, height=2,
                                    font=("PK Maehongson", 12, "bold"))

        south_america_btn = ctk.CTkButton(self, text="South America", **btn_style,
                                          command=lambda: self.show_region("SOUTH AMERICA"))
        south_america_btn.configure(bg_color='#6daaff', fg_color='#6daaff', width=15, height=2,
                                    font=("PK Maehongson", 12, "bold"))

        oceania_btn = ctk.CTkButton(self, text="Oceania", **btn_style,
                                    command=lambda: self.show_region("OCEANIA"))
        oceania_btn.configure(bg_color='#e8ab6e', fg_color='#e8ab6e', width=15, height=2,
                              font=("PK Maehongson", 10, "bold"))

        europe_btn.place(relx=0.5, rely=0.35, anchor="center")
        asia_btn.place(relx=0.65, rely=0.35, anchor="center")
        africa_btn.place(relx=0.5, rely=0.475, anchor="center")
        north_america_btn.place(relx=0.275, rely=0.35, anchor="center")
        south_america_btn.place(relx=0.34, rely=0.57, anchor="center")
        oceania_btn.place(relx=0.75, rely=0.62, anchor="center")

    def show_region(self, region):
        """ Show the countries in the selected region. """

        top_level = ctk.CTkToplevel(self, width=400, height=700, fg_color="#0e2e6c")
        top_level.title("Countries")
        top_level.geometry("400x700")

        list_label = ctk.CTkLabel(top_level, text=f"{region} Countries",
                                  font=("PK Maehongson", 20), text_color="white",
                                  fg_color="#0e2e6c")
        list_label.pack(pady=5)

        frame = ctk.CTkScrollableFrame(top_level, width=400, height=700,
                                       bg_color="#0e2e6c", fg_color="#0e2e6c")
        frame.pack(fill="both", expand=True)

        country_by_region = self.facade.region_list()[region]
        for country in country_by_region:
            ctk.CTkLabel(frame, text=country, font=("PK Maehongson", 20),
                         text_color="white", fg_color="#0e2e6c").pack(pady=5)


class StatisticPage(FramePage):
    """ The statistic page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/static_bg.png")
        self.set_button()
        self.set_label()

    def set_label(self):
        """ Set the labels of the page. """

        button_style = {"font": ("PK Maehongson", 17), "text_color": "white",
                        "hover_color": "#7ea5e8", "corner_radius": 0,
                        "border_color": "#84c2fd", "border_width": 2}

        distribute_btn = ctk.CTkButton(self, text="Distribution",
                                       **button_style,
                                       command=lambda: self.root.raise_page(DistributeGraphPage))
        distribute_btn.place(relx=0.165, rely=0.45, anchor="nw")

        everyday_graph = ctk.CTkButton(self, text="Part-to-whole",
                                       **button_style,
                                       command=lambda: self.root.raise_page(EverydayGraphPage))
        everyday_graph.place(relx=0.435, rely=0.45, anchor="nw")

        correlation_btn = ctk.CTkButton(self, text="Correlation",
                                        **button_style,
                                        command=lambda: self.root.raise_page(CorrelationGraphPage))
        correlation_btn.place(relx=0.72, rely=0.45, anchor="nw")

        descriptive_btn = ctk.CTkButton(self, text="Descriptive statistics",
                                        **button_style,
                                        command=lambda: self.root.raise_page(DescriptivePage))
        descriptive_btn.place(relx=0.31, rely=0.825, anchor="nw")

        network_btn = ctk.CTkButton(self, text="Network graph",
                                    **button_style,
                                    command=lambda: self.root.raise_page(NetworkPage))
        network_btn.place(relx=0.61, rely=0.825, anchor="nw")


class DistributeGraphPage(FramePage):
    """ The distribution graph page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/default_bg.png")
        self.attribute_label = None
        self.set_button()
        self.set_label()
        self.plot_graph('Population')

    def set_label(self):
        """ Set the labels of the page. """

        select_label = ctk.CTkLabel(self, text="Select the attribute to see the histogram",
                                    font=("PK Maehongson", 23, "bold"), text_color="white",
                                    fg_color="#071a3f")
        select_label.place(relx=0.915, rely=0.13, anchor="ne")

        search_bar_style = {"font": ("PK Maehongson", 17), "width": 350, "border_width": 0,
                            "corner_radius": 0,
                            "button_color": "#ffc661", "dropdown_fg_color": "#5ad2ae",
                            "text_color": "black", "fg_color": "#4baf91", "bg_color": "#4baf91"}
        combobox_var = ctk.StringVar(value="Population")  # set initial value

        attributes = self.facade.get_all_attributes()

        combobox = ctk.CTkComboBox(self,
                                   values=attributes,
                                   variable=combobox_var,
                                   **search_bar_style,
                                   command=lambda x: self.plot_graph(combobox_var.get()))
        combobox.place(relx=0.915, rely=0.2, anchor="ne")

        self.attribute_label = ctk.CTkLabel(self, text="The distribution of Population",
                                            font=("PK Maehongson", 35, "bold"),
                                            text_color="white", fg_color="#0a2151")
        self.attribute_label.place(relx=0.085, rely=0.14, anchor="nw")

        description = ctk.CTkLabel(self,
                                   text="The graph shows the distribution of the selected attribute",
                                   font=("PK Maehongson", 20), text_color="#3fe0fa",
                                   fg_color="#0a2252")
        description.place(relx=0.085, rely=0.22, anchor="nw")

    def plot_graph(self, attribute):
        """ Plot the graph of the selected attribute. """

        ax = self.facade.distribution_graph(attribute)
        fig = ax.figure
        frame = ctk.CTkFrame(self, width=500, height=400)

        # show graph on the page
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        canvas.draw()
        frame.place(relx=0.5, rely=0.6, anchor="center")

        # change the label
        att_dict = self.facade.att_dict()
        att_to_change = att_dict[attribute]
        self.attribute_label.configure(text=f"The distribution of {att_to_change}")

        plt.close(fig)


class EverydayGraphPage(FramePage):
    """ The everyday graph page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/default_bg.png")
        self.attribute_label = None
        self.set_button()
        self.set_label()
        self.plot_graph('Population')

    def set_label(self):
        """ Set the labels of the page. """

        select_label = ctk.CTkLabel(self, text="Select the attribute to see the pie chart",
                                    font=("PK Maehongson", 23, "bold"), text_color="white",
                                    fg_color="#071a3f")
        select_label.place(relx=0.915, rely=0.13, anchor="ne")

        search_bar_style = {"font": ("PK Maehongson", 17), "width": 350, "border_width": 0,
                            "corner_radius": 0,
                            "button_color": "#ffc661", "dropdown_fg_color": "#5ad2ae",
                            "text_color": "black", "fg_color": "#4baf91", "bg_color": "#4baf91"}
        combobox_var = ctk.StringVar(value='Population')  # set initial value

        attributes = self.facade.get_everyday_attributes()
        combobox = ctk.CTkComboBox(self,
                                   values=attributes,
                                   variable=combobox_var,
                                   **search_bar_style,
                                   command=lambda x: self.plot_graph(combobox_var.get()))
        combobox.place(relx=0.915, rely=0.2, anchor="ne")

        self.attribute_label = ctk.CTkLabel(self, text="World region's population",
                                            font=("PK Maehongson", 35, "bold"),
                                            text_color="white", fg_color="#0a2151")
        self.attribute_label.place(relx=0.085, rely=0.12, anchor="nw")

        description_label = ctk.CTkLabel(self,
                                         text="The pie chart shows the proportion of the summation",
                                         font=("PK Maehongson", 20, "bold"), text_color="#3fe0fa",
                                         fg_color="#0a2252")
        description_label.place(relx=0.085, rely=0.2, anchor="nw")
        description_label2 = ctk.CTkLabel(self,
                                          text="of each attribute for each region",
                                          font=("PK Maehongson", 20, "bold"), text_color="#3fe0fa",
                                          fg_color="#0a2252")
        description_label2.place(relx=0.085, rely=0.24, anchor="nw")

    def plot_graph(self, attribute):
        """ Plot the graph of the selected attribute. """

        ax = self.facade.everyday_graph(attribute)
        fig = ax.get_figure()
        frame = ctk.CTkFrame(self, width=500, height=400)

        # show graph on the page
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        canvas.draw()
        frame.place(relx=0.5, rely=0.6, anchor="center")

        att_dict = self.facade.att_dict()
        att_to_change = att_dict[attribute]
        self.attribute_label.configure(text=f"World region's {att_to_change}")

        plt.close(fig)


class CorrelationGraphPage(FramePage):
    """ The correlation graph page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/default_bg.png")
        self.set_button()
        self.set_label()
        self.plot_graph('Population', 'Area(sq. km.)')

    def set_label(self):
        """ Set the labels of the page. """

        select_label = ctk.CTkLabel(self, text="Select the attribute to see the correlation graph",
                                    font=("PK Maehongson", 19, "bold"), text_color="white",
                                    fg_color="#071a3f")
        select_label.place(relx=0.915, rely=0.13, anchor="ne")

        and_label = ctk.CTkLabel(self, text="&", font=("PK Maehongson", 23, "bold"),
                                 text_color="white", fg_color="#071a3f")
        and_label.place(relx=0.765, rely=0.19, anchor="ne")

        combobox_style = {"font": ("PK Maehongson", 17), "width": 150, "border_width": 0,
                          "corner_radius": 0,
                          "button_color": "#ffc661", "dropdown_fg_color": "#5ad2ae",
                          "text_color": "black", "fg_color": "#4baf91", "bg_color": "#4baf91"}

        values_att1 = ['Population', 'Pop. Density (per sq. km.)', 'Deathrate', 'Birthrate']
        values_att2 = ['Area(sq. km.)', 'GDP ($ per capital)', 'Net migration',
                       'Infant mortality (per 1000 births)']

        combobox_var1 = ctk.StringVar(value='Population')
        combobox_var2 = ctk.StringVar(value='Area(sq. km.)')

        combobox1 = ctk.CTkComboBox(self,
                                    values=values_att1,
                                    variable=combobox_var1,
                                    **combobox_style,
                                    command=lambda x: self.plot_graph(combobox_var1.get(),
                                                                      combobox_var2.get()))
        combobox1.place(relx=0.74, rely=0.2, anchor="ne")

        combobox2 = ctk.CTkComboBox(self,
                                    values=values_att2,
                                    variable=combobox_var2,
                                    **combobox_style,
                                    command=lambda x: self.plot_graph(combobox_var1.get(),
                                                                      combobox_var2.get()))
        combobox2.place(relx=0.915, rely=0.2, anchor="ne")

        title_label = ctk.CTkLabel(self, text="The correlation graph between two attributes",
                                   font=("PK Maehongson", 30, "bold"),
                                   text_color="white", fg_color="#0a2151")
        title_label.place(relx=0.085, rely=0.11, anchor="nw")

        description_label = ctk.CTkLabel(self,
                                         text="The graph shows the correlation between two attributes",
                                         font=("PK Maehongson", 20, "bold"), text_color="#3fe0fa",
                                         fg_color="#0a2252")
        description_label.place(relx=0.085, rely=0.18, anchor="nw")
        description_label2 = ctk.CTkLabel(self, text="The color of the point represents the region",
                                          font=("PK Maehongson", 20, "bold"), text_color="#3fe0fa",
                                          fg_color="#0a2252")
        description_label2.place(relx=0.085, rely=0.22, anchor="nw")

    def plot_graph(self, att1, att2):
        """ Plot the graph of the selected attributes. """

        ax = self.facade.correlation_graph(att1, att2)
        frame = ctk.CTkFrame(self, width=500, height=400)

        # show graph on the page
        canvas = FigureCanvasTkAgg(ax.fig, master=frame)
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        canvas.draw()
        frame.place(relx=0.5, rely=0.6, anchor="center")

        plt.close(ax.fig)


class DefaultGraphPage(FramePage):
    """ The default graph page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/default_bg.png")
        self.set_button()
        self.set_label()
        self.plot_graph()

    def set_label(self):
        """ Set the labels of the page. """

        title_label = ctk.CTkLabel(self, text="World's region population",
                                   font=("PK Maehongson", 30, "bold"),
                                   text_color="white", fg_color="#0a2151")
        title_label.place(relx=0.085, rely=0.11, anchor="nw")

        select_more_button = ctk.CTkButton(self, text="See more statistics",
                                           font=("PK Maehongson", 17), text_color="white",
                                           hover_color="#7ea5e8", corner_radius=0,
                                           border_color="#84c2fd", border_width=2,
                                           command=lambda: self.root.raise_page(StatisticPage))
        select_more_button.place(relx=0.85, rely=0.2, anchor="center")

        description_label = ctk.CTkLabel(self, text="The graph shows the population of each region",
                                         font=("PK Maehongson", 20, "bold"), text_color="#3fe0fa",
                                         fg_color="#0a2252")
        description_label.place(relx=0.085, rely=0.2, anchor="nw")

    def plot_graph(self):
        """ Plot the default graph. """

        ax = self.facade.default_graph()
        fig = ax.get_figure()
        frame = ctk.CTkFrame(self, width=500, height=400)

        # show graph on the page
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        canvas.draw()
        frame.place(relx=0.5, rely=0.6, anchor="center")

        plt.close(fig)


class DescriptivePage(FramePage):
    """ The descriptive page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/descript_bg.png")
        self.set_button()
        self.set_label()

    def set_label(self):
        """ Set the labels of the page. """
        attribute_label = ctk.CTkLabel(self, text="Attribute",
                                       font=("PK Maehongson", 30, "bold"),
                                       text_color="white", fg_color="#2d375f")
        attribute_label.place(relx=0.08, rely=0.4, anchor="nw")

        data_list, att_list, data_col = self.facade.descriptive_stat()

        y = 0.5
        for att in att_list:
            att_label = ctk.CTkLabel(self, text=att, font=("PK Maehongson", 20, "bold"),
                                     text_color="white", fg_color="#2d375e")
            att_label.place(relx=0.08, rely=y, anchor="nw")
            y += 0.05

        x = 0.37
        for col in data_list:
            y = 0.5
            for data in col:
                data_label = ctk.CTkLabel(self, text=data, font=("PK Maehongson", 20, "bold"),
                                          text_color="white", fg_color="#2e3d6c")
                data_label.place(relx=x, rely=y, anchor="nw")
                y += 0.05
            x += 0.15

        colors = ['#303f6f', '#405084', '#404e7f', '#2c3458']

        x = 0.37
        for index, col in enumerate(data_col):
            col_label = ctk.CTkLabel(self, text=col, font=("PK Maehongson", 30, "bold"),
                                     text_color="white", fg_color="#2e3d6c")
            col_label.configure(fg_color=colors[index])
            col_label.place(relx=x, rely=0.4, anchor="nw")
            x += 0.15


class InfoPage(FramePage):
    """ The info page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/info_bg.png")
        self.set_button()
        self.set_label()

    def set_label(self):
        """ Set the label of the page. """

        button_style = {"font": ("PK Maehongson", 17), "fg_color": "#2a406d", "text_color": "white",
                        "hover_color": "#7ea5e8", "corner_radius": 0}

        yt_button = ctk.CTkButton(self, text="Watch on YouTube",
                                  **button_style,
                                  command=lambda: self.show_progress_bar("youtube"))
        yt_button.place(relx=0.22, rely=0.67, anchor="center")

        github_button = ctk.CTkButton(self, text="Visit GitHub",
                                      **button_style,
                                      command=lambda: self.show_progress_bar("github"))
        github_button.place(relx=0.5, rely=0.67, anchor="center")

    def show_progress_bar(self, button):
        """ Show the progress bar before leading the user to the YouTube link. """

        yt_button = self.children["!ctkbutton"]
        github_button = self.children["!ctkbutton"]

        progress = ctk.CTkProgressBar(self, mode="indeterminate", width=300, height=20,
                                      progress_color="#ff61c2", fg_color="#2a406d", corner_radius=0)

        progress.place(relx=0.22, rely=0.75, anchor="center")

        progress.start()

        if button == "youtube":
            self.after(2000, self.open_youtube, progress, yt_button)
        elif button == "github":
            self.after(2000, self.open_github, progress, github_button)

    @staticmethod
    def check_internet_connection():
        """ Check for internet connection by attempting to connect to google.com """

        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False

    def open_youtube(self, progress, yt_button):
        """ Open the YouTube link and destroy the progress bar. """

        if not self.check_internet_connection():
            messagebox.showerror("Error", "No internet connection.")
            progress.destroy()
            yt_button.configure(state="normal")
            return

        url = "https://youtu.be/qPPtqwabqyU"

        webbrowser.open_new(url)
        progress.destroy()
        yt_button.configure(state="normal")

    def open_github(self, progress, github_button):
        """ Open the GitHub link and destroy the progress bar. """

        if not self.check_internet_connection():
            messagebox.showerror("Error", "No internet connection.")
            progress.destroy()
            github_button.configure(state="normal")
            return

        url = "https://github.com/Yanatg"

        webbrowser.open_new(url)
        progress.destroy()
        github_button.configure(state="normal")


class NetworkPage(FramePage):
    """ The network graph page of the app. """

    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_bg("pics/default_bg.png")
        self.progress_bar = None
        self.task = None
        self.set_button()
        self.set_label()
        self.show_progress()

    def set_label(self):
        """ Set the labels of the page. """

        title_label = ctk.CTkLabel(self, text="Network Graph Visualization",
                                   font=("PK Maehongson", 30, "bold"),
                                   text_color="white", fg_color="#0a2151")
        title_label.place(relx=0.085, rely=0.11, anchor="nw")

        description_label = ctk.CTkLabel(self,
                                         text="The graph show the relationship between the country.",
                                         font=("PK Maehongson", 20, "bold"),
                                         text_color="#3fe0fa", fg_color="#0a2252")
        description_label.place(relx=0.085, rely=0.2, anchor="nw")

    def plot_graph(self):
        """ plot the network graph. """

        g = self.facade.network_graph()
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.set_facecolor('#081b42')
        # set the color of the axis and the background
        sns.set_style("whitegrid", {'axes.grid': False, 'axes.facecolor': '#081b42',
                                    'figure.facecolor': '#081b42'})

        pos = nx.circular_layout(g)
        nx.draw_networkx_nodes(g, pos, node_size=100, node_color='#ffc661')
        nx.draw_networkx_edges(g, pos, edgelist=list(g.edges), edge_color='#40f281')
        nx.draw_networkx_labels(g, pos, font_size=8, font_color='white')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.6, anchor="center")
        plt.close(fig)

    def show_progress(self):
        """ Show the progress bar while plotting the network graph """

        loading_label = ctk.CTkLabel(self, text="Loading", font=("PK Maehongson", 25, "bold"),
                                     text_color="#3fe0fa", fg_color="#0e2e6c")
        loading_label.place(relx=0.5, rely=0.5, anchor="center")

        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate", width=300, height=20,
                                               progress_color="#ff61c2", fg_color="#2a406d",
                                               corner_radius=0)
        self.progress_bar.place(relx=0.5, rely=0.6, anchor="center")
        self.progress_bar.start()
        self.task = Thread(target=self.plot_graph)
        self.progress_bar.start()
        self.task.start()
        self.after(100, self.check_progress)

    def check_progress(self):
        """ Check the progress of the task. """

        if self.task.is_alive():
            self.after(100, self.check_progress)
        else:
            self.progress_bar.destroy()
            self.task.join()
            self.task = None
