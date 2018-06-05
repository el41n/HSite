from bs4 import BeautifulSoup
import urllib.request
import re

from ..hardware import Vendor
from ..cpu.cpu import Architecture, CodeName, CPU
from ..motherboard.motherboard import Socket, FormFactor, Chipset, Motherboard
from ..memory.memory import Memory, MemoryType
from ..power_block.power_block import PowerBlock


class Parser():
    def __init__(self, base_url="https://komp.1k.by", cpu_url="https://komp.1k.by/utility-cpu/",
                 moth_url="https://komp.1k.by/utility-motherboards/", mem_url="https://komp.1k.by/utility-memory/",
                 power_url="https://komp.1k.by/utility-powermodules/"):
        self._base_url = base_url
        self._cpu_url = cpu_url
        self._moth_url = moth_url
        self._mem_url = mem_url
        self._power_url = power_url

    def start(self):
        self.links = self.make_links_list(self.cpu_url)
        self.find_info(self.proc_parse)
        self.links = self.make_links_list(self.moth_url)
        self.find_info(self.moth_parse)
        self.links = self.make_links_list(self.mem_url)
        self.find_info(self.mem_parse)
        self.links = self.make_links_list(self.power_url)
        self.find_info(self.power_parse)

    def make_links_list(self, url):
        html = self.request(url)
        soup = BeautifulSoup(html, "html.parser")
        links_field = soup.findAll('fieldset', class_='prod-list_body')
        links_tag = links_field[0].find_all('a', class_='pr-line_link')
        for link in links_tag:
            yield self.base_url + link.get('href')

    def find_info(self, function):
        for link in self.links:
            html = self.request(link)
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.findAll('table', class_='b-pr-tech')
            table_list = list()
            for section in table:
                info_tag = section.find_all('td')
                info_list = list()
                for info in info_tag:
                    info_list.append(info.text)
                table_list.append(info_list)
            model = soup.findAll('span', class_='crumbs_current')
            table_list.append(model[0].text)

            price = soup.findAll('div', class_='pr-price_cash')
            price = re.findall('\d+,\d+', price[0].text)
            price = [float(pr.replace(',', '.')) for pr in price]
            price = sum(price) / len(price)
            table_list.append(price)

            function(table_list)

    def proc_parse(self, info_table):
        info_map = dict()
        info_map['vendor'] = info_table[0][0].split(' ')[0]
        info_map['architecture'] = ''.join(info_table[0][0].split(' ')[1:])
        info_map['socket'] = info_table[0][1]
        info_map['codename'] = info_table[1][0]
        info_map['cores'] = info_table[1][1]
        info_map['clock_speed'] = "".join(re.findall('\d', info_table[2][0]))
        info_map['cache'] = "".join(re.findall('\d', info_table[3][-1]))
        info_map['power'] = "".join(re.findall('\d', info_table[6][0]))
        info_map['model'] = info_table[-2]
        info_map['price'] = info_table[-1]

        vendor = Vendor(vendor=info_map['vendor'])
        vid = vendor.save()

        architecture = Architecture(architecture=info_map['architecture'])
        aid = architecture.save()

        socket = Socket(socket=info_map['socket'])
        sid = socket.save()

        codename = CodeName(codename=info_map['codename'])
        cid = codename.save()

        cpu = CPU(vendor_id=vid,
                  model=info_map['model'],
                  architecture_id=aid,
                  socket_id=sid,
                  codename_id=cid,
                  cores=info_map['cores'],
                  clock_speed=info_map['clock_speed'],
                  cache=info_map['cache'],
                  power=info_map['power'],
                  price=info_map['price']
                  )
        cpu.save()

    def moth_parse(self, info_table):
        info_map = dict()
        info_map['vendor'] = info_table[-2].split(' ')[0]
        info_map['model'] = ''.join(info_table[-2].split(' ')[1:])
        info_map['socket'] = info_table[0][1]
        info_map['mem_type'] = info_table[1][0]
        info_map['chipset'] = info_table[5][0]
        info_map['form'] = info_table[14][-2]
        info_map['price'] = info_table[-1]

        vendor = Vendor(vendor=info_map['vendor'])
        vid = vendor.save()

        socket = Socket(socket=info_map['socket'])
        sid = socket.save()

        mem_type = MemoryType(type=info_map['mem_type'])
        mid = mem_type.save()

        chipset = Chipset(chipset=info_map['chipset'])
        cid = chipset.save()

        form = FormFactor(form_factor=info_map['form'])
        fid = form.save()


        moth = Motherboard(vendor_id=vid,
                           model=info_map['model'],
                           socket_id=sid,
                           memory_type_id=mid,
                           chipset_id=cid,
                           price=info_map['price'],
                           form_factor_id=fid
                  )
        moth.save()

    def mem_parse(self, info_table):
        info_map = dict()
        info_map['vendor'] = info_table[-2].split(' ')[0]
        info_map['model'] = ''.join(info_table[-2].split(' ')[1:])
        info_map['mem_type'] = info_table[0][0] + ' ' + info_table[0][1]
        info_map['volume'] = "".join(re.findall('\d', info_table[0][2]))
        info_map['price'] = info_table[-1]

        vendor = Vendor(vendor=info_map['vendor'])
        vid = vendor.save()

        mem_type = MemoryType(type=info_map['mem_type'])
        mid = mem_type.save()

        mem = Memory(vendor_id=vid,
                           model=info_map['model'],
                           type_id=mid,
                           price=info_map['price'],
                           volume=info_map['volume']
                           )
        mem.save()

    def power_parse(self, info_table):
        info_map = dict()
        info_map['vendor'] = info_table[-2].split(' ')[0]
        info_map['model'] = ''.join(info_table[-2].split(' ')[1:])
        info_map['capacity'] = "".join(re.findall('\d', info_table[0][1]))
        if info_map['capacity'] == '1':
            info_map['capacity'] = "".join(re.findall('\d', info_table[0][0]))
        info_map['price'] = info_table[-1]

        vendor = Vendor(vendor=info_map['vendor'])
        vid = vendor.save()

        power = PowerBlock(vendor_id=vid,
                           model=info_map['model'],
                           price=info_map['price'],
                           power_capacity=info_map['capacity']
                           )
        power.save()


    def request(self, url):
        response = urllib.request.urlopen(url)
        return response


