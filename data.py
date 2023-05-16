import pandas as pd


class CountryDatabase:

    def __init__(self):
        """ This class is used to create a database of countries and their attributes."""

        self.df = self.set_df()
        self.countries = [i for i in self.df['Country']]

    def set_df(self):
        """ This method is used to set the dataframe of the countries. """

        self.df = pd.read_csv('countries_of_the_world.csv')
        self.df = self.df.drop(
            ['Agriculture', 'Industry', 'Service', 'Climate', 'Other (%)', 'Crops (%)',
             'Arable (%)', 'Phones (per 1000)', 'Literacy (%)', 'Coastline (coast/area ratio)'],
            axis=1)
        self.df = self.df.dropna()
        return self.df

    def get_df(self):
        """ This method is used to get the dataframe of the countries. """

        return self.df

    def get_countries(self):
        """ This method is used to get the list of the countries. """

        return self.countries

    @staticmethod
    def get_all_attributes():
        """ This method is used to get all the attributes of the countries. """
        return ['Population', 'Area(sq. km.)', 'Pop. Density (per sq. km.)', 'Net migration',
                'Infant mortality (per 1000 births)', 'GDP ($ per capital)', 'Birthrate',
                'Deathrate']

    @staticmethod
    def get_everyday_attributes():
        return ['Population', 'Area(sq. km.)', 'Pop. Density (per sq. km.)',
                'Infant mortality (per 1000 births)', 'GDP ($ per capital)']

    def region_list(self):
        """ This method is used to get the regions. """

        dict_region = {}
        for region in self.df['Region'].unique():
            dict_region[region] = []
            for country in self.df[self.df['Region'] == region]['Country']:
                dict_region[region].append(country)
        return dict_region


class Country(CountryDatabase):
    """ This class is used to create a country object. """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.region = self.set_region()
        self.population = self.set_population()
        self.area = self.set_area()
        self.pop_den = self.set_pop_den()
        self.net_migration = self.set_net_migration()
        self.infant_mortal = self.set_infant_mortal()
        self.gdp = self.set_gdp()

    def set_name(self, name):
        """ This method is used to set the name of the country. """
        self.name = name

    def set_region(self):
        """ This method is used to set the region of the country. """

        self.region = self.df[self.df['Country'] == self.name]['Region'].values[0]
        return self.region

    def set_population(self):
        """ This method is used to set the population of the country. """

        self.population = self.df[self.df['Country'] == self.name]['Population'].values[0]
        return self.population if self.population != 0 else "-"

    def set_area(self):
        """ This method is used to set the area of the country. """

        self.area = self.df[self.df['Country'] == self.name]['Area(sq. km.)'].values[0]
        return self.area if self.area != 0 else "-"

    def set_pop_den(self):
        """ This method is used to set the population density of the country. """

        self.pop_den = \
            self.df[self.df['Country'] == self.name]['Pop. Density (per sq. km.)'].values[0]
        return self.pop_den if self.pop_den != 0 else "-"

    def set_net_migration(self):
        """ This method is used to set the net migration of the country. """

        self.net_migration = self.df[self.df['Country'] == self.name]['Net migration'].values[0]
        return self.net_migration if self.net_migration != 0 else "-"

    def set_infant_mortal(self):
        """ This method is used to set the infant mortality of the country. """

        self.infant_mortal = \
            self.df[self.df['Country'] == self.name]['Infant mortality (per 1000 births)'].values[0]
        return self.infant_mortal if self.infant_mortal != 0 else "-"

    def set_gdp(self):
        """ This method is used to set the GDP of the country. """

        self.gdp = self.df[self.df['Country'] == self.name]['GDP ($ per capital)'].values[0]
        return self.gdp if self.gdp != 0 else "-"

    def search_name_data(self):
        """ This method is used to search the name of the country. """

        return {"Name": self.name, "Region": self.region, "Population": self.population,
                "Area": self.area, "Population density": self.pop_den,
                "Net migration": self.net_migration,
                "Infant mortal": self.infant_mortal, "GDP": self.gdp}
