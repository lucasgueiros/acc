from cement import Controller, ex, fs
import csv
from anytree import Node, RenderTree

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
        radix = Node('Radix')
        accounts = {'radix': radix}
        with open(self.app.pargs.input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    complete_name = row[4]
                    path = complete_name.split(':')
                    last= radix
                    name = ''
                    for part_name in path:
                        if name == '':
                            name = part_name
                        else:
                            name = ':'.join([name,part_name])

                        if not (name in accounts):
                            node = Node(name,parent=last)
                            accounts[name] = node
                            last = node
                        else:
                            last = accounts[name]
                    line_count += 1
            print(f'Processed {line_count} lines.')
        for pre, fill, node in RenderTree(radix):
            print("%s%s" % (pre, node.name))
