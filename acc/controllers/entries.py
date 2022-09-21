from cement import Controller, ex, fs
import csv

class Entries(Controller):
    class Meta:
        label = 'entries'
        stacked_type = 'nested'
        stacked_on = 'base'
    @ex(
            help='list all entries',
            arguments=[(['input_file'],{'help':'a CSV file with transactions'})]
    )
    def list(self):
        fs.backup(self.app.pargs.input_file)
        with open(self.app.pargs.input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            date_column = 1
            account_column = 2
            amount_column = 3
            description_column = 4
            first_row = True
            for row in csv_reader:
                if first_row:
                    account_column = row.index('Full Account Name')
                    amount_column = row.index('Amount Num.')
                    date_column = row.index("Date")
                    description_column = row.index("Description")
                    first_row = False
                    continue
                account = row[account_column]
                amount = row[amount_column]
                date = row[date_column]
                description = row[description_column]

                print('%s\t%s\t%s\t%s' % (date, description, amount, account))
