from cement import Controller, ex, fs
import csv
from anytree import Node, RenderTree, NodeMixin
from decimal import Decimal

class Account(NodeMixin):
    def __init__(self, name, saldo = Decimal(0), parent=None, children=None):
        super(Account,self).__init__()
        self.name = name
        self.saldo = saldo
        self.parent = parent
        if children:
            self.children = children

    def sum_saldo(self, valor):
        self.saldo = self.saldo + valor

    def saldo_subcontas(self):
        saldo_subcontas = self.saldo
        for child in self.children:
            saldo_subcontas = saldo_subcontas + child.saldo_subcontas() 
        return saldo_subcontas

class Accounts(Controller):
    class Meta:
        label = 'accounts'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(
            help='lista all accounts',
            arguments=[
                (['input_file'],{'help': 'arquivo com transações'})
                ]
            )
    def list(self):
        fs.backup(self.app.pargs.input_file)
        radix = Account('Radix')
        accounts = {'radix': radix}
        with open(self.app.pargs.input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            account_column = 1
            amount_column = 2
            first_row = True
            for row in csv_reader:
                if first_row:
                    account_column = row.index("Full Account Name")
                    amount_column = row.index("Amount Num.")
                    first_row = False
                    continue
                complete_name = row[account_column]
                path = complete_name.split(':')
                last= radix
                name = ''
                for part_name in path:
                    if name == '':
                        name = part_name
                    else:
                        name = ':'.join([name,part_name])

                    if not (name in accounts):
                        node = Account(name, parent=last)
                        accounts[name] = node
                        last = node
                    else:
                        last = accounts[name]
                valor = Decimal(row[amount_column].replace(',','.'))
                last.sum_saldo(valor)
        for pre, fill, node in RenderTree(radix):
            print("%s%s\t%s" % (pre, node.name, node.saldo))
