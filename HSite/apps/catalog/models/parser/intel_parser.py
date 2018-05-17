from bs4 import BeautifulSoup
import urllib.request
import re
import itertools
from .cpu_parser import Parser
from ..motherboard.socket import Socket

class IntelParser(Parser):
    def __init__(self):
        self.base = 'https://ark.intel.com'
        self.base_url = 'https://ark.intel.com/ru#@Processors'
        self.processor_links = None

    def start(self):
        """
        Start executing parsing.
        :return:
        """
        self.processor_links = self.find_processor_list()
        #print(self.processor_links)
        self.find_processor_info()
        #self.base_response = self.request()
        #a = self.find_processor_list(self.base_response)

    def request(self, url):
        """
        Sends request for getting html file.
        :param url: url of file
        :return: opened html file
        """
        response = urllib.request.urlopen(url)
        return response

    def find_processor_list(self):
        """
        Finds all links for searching Intel processors.
        :return: map with {processor family: link for getting info}
        """
        html = self.request(self.base_url)
        soup = BeautifulSoup(html,  'html.parser')
        processor_list = soup.find('div', class_="products processors")
        links_list = processor_list.find_all('a')
        maps = []
        for link in links_list:
            html = self.request(self.base+link.get('href'))
            soup = BeautifulSoup(html, 'html.parser')
            processor_list = soup.find('tbody')
            processor_links = processor_list.find_all('a')
            for processor_link in processor_links:
                maps.append(self.base+processor_link.get('href'))
        return maps
                #yield self.base + processor_link.get('href')
            #print(processor_list)
            #yield self.base + processor_links.get('href')
        #return {links_list[0].text: self.base + links_list[0].get('href')}
        # for link in links_list:
        #     print(link.get('href'))

    def find_processor_info(self):
        """
        Finds processors inside families and gets info about 'em.
        Creates new db object.
        :return:
        """

        #architecture

        def find_architecture(string):
            """
            Searches for architecture instance.
            :param string:
            :return:
            """
            architecture = IntelArchitecture.objects.values_list('architecture', flat=True).order_by('architecture')
            architecture_re = re.compile('(Core™ i9)+|(Core™ i7)+|(Core™ i5)+|(Core™ i3)+|(Core™ m)+|(Pentium™ M)+')
            arch = tuple(filter(lambda x: x is not None, architecture_re.search(string).groups()))
            #d = architecaaure.values()
            #print(architecture)
            if architecture.filter(architecture=arch[0]).exists():
                pass
            else:
                new_arch = IntelArchitecture(architecture=arch[0])
                new_arch.save()
            return IntelArchitecture.objects.get(architecture=arch[0]).id

        def find_socket(sock):
            socket = Socket.objects.values_list('socket', flat=True).order_by('socket')
            if socket.filter(socket=sock).exists():
                pass
            else:
                new_socket = Socket(socket=sock)
                new_socket.save()
            return Socket.objects.get(socket=sock).id
        #
        # def find_codename(string):
        #     cdn = string.split()[-1]


        def to_normal_float(string):
            float_number = re.compile(r'[\d,\d]+')
            if string == '':
                return 0
            float_str = float_number.findall(string)
            return float('.'.join(float_str[0].split(',')))

        def price_found(string):
            price = re.compile(r'\d+.\d+')
            price_str = price.findall(string)
            if len(price_str) == 0:
                return 0
            return float(price_str[0])

        for processors_family in self.processor_links:
            html = self.request(processors_family)
            #print(html)
            soup = BeautifulSoup(html, 'html.parser')

            info = dict()

            name = soup.find('h1', class_='h1')
            name = name.text
            info['architecture'] = find_architecture(name)

            model = soup.find('li', class_="ProcessorNumber")
            model = model.find('span', class_="value").text.strip()
            info['model'] = model

            status = soup.find('li', class_="StatusCodeText")
            status = status.find('span', class_="value").text.strip()
            info['status'] = status

            date = soup.find('li', class_="BornOnDate")
            date = date.find('span', class_="value").text.strip()
            info['date'] = date

            price = soup.find('li', class_="Price1KUnits")
            price = price.find('span', class_="value").text.strip()
            info['price'] = price_found(price)

            cores = soup.find('li', class_="CoreCount")
            cores = cores.find('span', class_="value").text.strip()
            info['cores'] = cores

            try:
                max_clock = soup.find('li', class_="ClockSpeedMax")
                max_clock = max_clock.find('span', class_="value").text.strip()
                info['max_clock'] = to_normal_float(max_clock)
            except AttributeError:
                print(info['model']+' error max clock')
                info['max_clock'] = 0

            clock = soup.find('li', class_="ClockSpeed")
            clock = clock.find('span', class_="value").text.strip()
            info['clock'] = to_normal_float(clock)

            cache = soup.find('li', class_="Cache")
            cache = cache.find('span', class_="value").text.strip()
            info['cache'] = to_normal_float(cache)

            try:
                socket = soup.find('li', class_="SocketsSupported")
                socket = socket.find('span', class_="value").text.strip()
                info['socket'] = find_socket(socket)
            except AttributeError:
                print(info['model']+' error socket')
                info['socket'] = None


            cpu = IntelCPU(model=info['model'],
                           status=info['status'],
                           date=info['date'],
                           cores=info['cores'],
                           max_clock_speed=info['max_clock'],
                           clock_speed=info['clock'],
                           cache=info['cache'],
                           price=info['price'],
                           architecture_id=info['architecture'],
                           socket_id=info['socket']
                           )
            cpu.save()




            # processor_table = soup.findAll('table', class_="table support-table table-sorter collapsible")
            # #print(processor_table[0])
            # processors = processor_table[0].find_all('tr', class_="blank-table-row seg-desktop ")
            # for processor in processors:
            #     Information = tuple(processor.text.split('\n')[1:10])
            #
            #
            #
            #
            #
            #     cpu = IntelCPU(model=Information[0],
            #                    status=Information[1],
            #                    date=Information[2],
            #                    cores=Information[3],
            #                    max_clock_speed=to_normal_float(Information[4]),
            #                    clock_speed=to_normal_float(Information[5]),
            #                    cash=to_normal_float(Information[6]),
            #                    price=price_found(Information[8]))
            #     cpu.save()
            #     break
