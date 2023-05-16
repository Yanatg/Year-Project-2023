from data import CountryDatabase
from matplotlib import pyplot as plt
import seaborn as sns
import networkx as nx


class GraphManage:
    """ This class is used to manage the graphs. """

    def __init__(self):
        self.df = CountryDatabase().get_df()
        self.color_chart = ['#9e8efd', '#3fe0fa', '#40f281', '#e9e283', '#e8ab6e', '#ff61c2']

    def distribution_graph(self, attribute):
        """ This method is used to plot the distribution graph of the given attribute. """

        plt.clf()
        df = self.df
        data = df[df[attribute] != 0][attribute]
        # set the size of the graph
        plt.figure(figsize=(9, 4))
        # set the color of the axis and the background
        sns.set_style("whitegrid", {'axes.grid': False, 'axes.facecolor': '#081b42',
                                    'figure.facecolor': '#081b42'})
        graph = sns.histplot(data=data, kde=True, alpha=.8, color='#ffc661')
        graph.figure.set_facecolor('#081b42')
        # set the axis color
        graph.tick_params(colors='white', which='both')
        # set the title of the graph
        graph.set_title(f'{attribute} Histogram', color='white')
        graph.set_xlabel(attribute, color='white')
        graph.set_ylabel('Count', color='white')
        return graph

    def everyday_graph(self, attribute):
        """ This method is used to plot the everyday graph of the given attribute. """

        df = self.df[self.df[attribute] != 0]
        # group the data by region
        data = df.groupby('Region')[attribute].sum()
        labels = data.index
        # set the size of the graph
        plt.figure(figsize=(9, 4))
        # plot the pie chart
        graph = data.plot.pie(autopct='%1.1f%%', startangle=90,
                              labels=['', '', '', '', '', '', '', '', '', '', '', ''],
                              colors=self.color_chart, )
        # set the graph background color to black
        graph.figure.set_facecolor('#081b42')
        # set the axis color
        graph.tick_params(colors='white', which='both')
        # set the title of the graph
        graph.set_title(attribute, color='white')
        # remove the attribute name from the graph
        graph.set_ylabel('')
        # add the labels to the left corner of the graph and not overlapping
        graph.legend(labels=labels, bbox_to_anchor=(1.1, 1), ncol=1, title='Region',
                     facecolor='#081b42', edgecolor='#081b42')
        # set the text color to white
        plt.setp(graph.get_legend().get_title(), color='white')
        plt.setp(graph.get_legend().get_texts(), color='white')
        return graph

    def correlation_graph(self, attribute1, attribute2):
        """ This method is used to plot the correlation graph between the two attributes. """

        df = self.df
        # set the size of the graph
        plt.figure(figsize=(9, 4))
        sns.set_style("whitegrid", {'axes.grid': False, 'axes.facecolor': '#081b42',
                                    'figure.facecolor': '#081b42'})
        # plot the correlation graph between the two attributes hue is the region
        graph = sns.relplot(data=df, x=attribute1, y=attribute2, hue='Region',
                            size=attribute2, sizes=(40, 400),
                            alpha=.8, palette=self.color_chart, height=4.5, aspect=1.5)
        # set the axis color
        graph.ax.tick_params(colors='white', which='both')
        graph.set_xlabels(attribute1, color='white')
        graph.set_ylabels(attribute2, color='white')
        # set the text color to white
        graph.legend.set_title('Region')
        plt.setp(graph.legend.get_texts(), color='white')

        return graph

    def descriptive_stat(self):
        """ This method is used to get the descriptive statistics of the data. """

        df = self.df
        # get the descriptive statistics of the data
        data = df.describe()
        # transpose the data to make it easier to read
        data = data.transpose()
        data = data.drop(['count', '25%', '50%', '75%'], axis=1)
        data_index = list(data.index)
        data_col = list(data.columns)
        # set the value to 2 decimal places
        data = data.round(2)
        data_list = []
        for col in data.columns:
            data_list.append(data[col].values)
        return data_list, data_index, data_col

    def bar_graph(self, attribute):
        """ This method is used to plot the bar graph of the given attribute. """

        df = self.df
        data = df.groupby('Region')[attribute].sum()
        x = data.index
        y = data.values
        # set the size of the graph
        plt.figure(figsize=(9, 4))
        # set the color of the axis and the background
        sns.set_style("whitegrid", {'axes.grid': False, 'axes.facecolor': '#081b42',
                                    'figure.facecolor': '#081b42'})
        graph = sns.barplot(x=x, y=y, palette=self.color_chart)
        graph.figure.set_facecolor('#081b42')
        # set the axis color
        graph.tick_params(colors='white', which='both')
        # set the title of the graph
        graph.set_title(f'{attribute} Bar Chart', color='white')
        graph.set_xlabel('Region', color='white')
        graph.set_ylabel(attribute, color='white')
        return graph

    def network_graph(self):
        """ This method is used to plot the network graph of the data. """

        df = self.df
        g = nx.Graph()
        # add the nodes to the graph using the country name as the nodes
        g.add_nodes_from(df['Country'].values)
        # add the edges to the graph
        for i in range(0, len(df['Country']) - 1):
            pop1 = df.iloc[i]['Population']
            for j in range(i + 1, len(df['Country'])):
                pop2 = df.iloc[j]['Population']
                # if the population of the two countries are close and both are in the same
                # continent add an edge between them
                if abs(pop1 - pop2) <= 10000 and df.iloc[i]['Region'] == df.iloc[j]['Region']:
                    g.add_edge(df.iloc[i]['Country'], df.iloc[j]['Country'], weight=0)
                elif abs(pop1 - pop2) <= 10000 and df.iloc[i]['Region'] != df.iloc[j]['Region']:
                    g.add_edge(df.iloc[i]['Country'], df.iloc[j]['Country'], weight=1)

        edge_weight_list = []
        for (u, v, wt) in g.edges.data('weight'):
            edge_weight_list.append(wt)
        # set the size of the graph
        plt.figure(figsize=(9, 4))
        fig = plt.figure()
        fig.set_facecolor('#081b42')
        # set the color of the axis and the background
        sns.set_style("whitegrid", {'axes.grid': False, 'axes.facecolor': '#081b42',
                                    'figure.facecolor': '#081b42'})

        pos = nx.circular_layout(g)
        nx.draw_networkx_nodes(g, pos, node_size=100, node_color='#ffc661')
        nx.draw_networkx_edges(g, pos, edgelist=list(g.edges), width=edge_weight_list,
                               edge_color='#40f281')
        nx.draw_networkx_labels(g, pos, font_size=8, font_color='white')
        return g
