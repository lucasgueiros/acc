
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import AccError
from .controllers.base import Base
from .controllers.accounts import Accounts

# configuration defaults
CONFIG = init_defaults('acc')
CONFIG['acc']['foo'] = 'bar'


class Acc(App):
    """Contabilidade da Família Gueiros primary application."""

    class Meta:
        label = 'acc'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Accounts
        ]


class AccTest(TestApp,Acc):
    """A sub-class of Acc that is better suited for testing."""

    class Meta:
        label = 'acc'


def main():
    with Acc() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except AccError as e:
            print('AccError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
