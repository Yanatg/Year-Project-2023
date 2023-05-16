from data import CountryDatabase, Country
from graph import GraphManage


class CountryFacade:
    """ This class is used to create a facade object. """

    def __init__(self):
        self.data = CountryDatabase()
        self.graph = GraphManage()

    def get_all_countries(self):
        """ This method is used to get all the countries. """

        return self.data.get_countries()

    def get_all_attributes(self):
        """ This method is used to get all the attributes. """

        return self.data.get_all_attributes()

    def get_everyday_attributes(self):
        """ This method is used to get the everyday attributes. """

        return self.data.get_everyday_attributes()

    @staticmethod
    def search_by_name(name):
        """ This method is used to search the country by name. """

        country = Country(name)
        return country.search_name_data()

    def distribution_graph(self, attribute):
        """ This method is used to get the distribution graph. """

        return self.graph.distribution_graph(attribute)

    def everyday_graph(self, attribute):
        """ This method is used to get the everyday graph. """

        return self.graph.everyday_graph(attribute)

    def correlation_graph(self, attribute1, attribute2):
        """ This method is used to get the correlation graph. """

        return self.graph.correlation_graph(attribute1, attribute2)

    def default_graph(self):
        """ This method is used to get the default graph. """

        return self.graph.bar_graph("Population")

    @staticmethod
    def att_dict():
        """ This method is used to get the attributes dictionary. """

        return {'Population': 'Population', 'Area(sq. km.)': 'Area',
                'Pop. Density (per sq. km.)': 'Population density',
                'Net migration': 'Net migration',
                'Infant mortality (per 1000 births)': 'Infant mortality',
                'GDP ($ per capital)': 'GDP', 'Birthrate': 'Birthrate',
                'Deathrate': 'Deathrate'}

    def descriptive_stat(self):
        """ This method is used to get the descriptive statistics. """

        return self.graph.descriptive_stat()

    def region_list(self):
        """ This method is used to get the region list. """

        return self.data.region_list()

    def network_graph(self):
        """ This method is used to get the network graph. """

        return self.graph.network_graph()
