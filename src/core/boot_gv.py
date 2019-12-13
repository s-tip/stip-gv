from django.apps import AppConfig
from django.core.management import call_command
from stip.common.boot import is_skip_sequence


class StipGvBoot(AppConfig):
    name = 'core.boot_gv'

    def ready(self):
        from ctirs.models import Config

        is_skip_sequnece = is_skip_sequence()
        if not is_skip_sequnece:
            print('>>> Start Auto Deploy')
            print('>>> Start collcect static --noinput')
            # collectstatic
            call_command('collectstatic', '--noinput')

            # loaddata (gv_system)
            config_count = Config.objects.count()
            print('>>> gv_system record count: ' + str(config_count))
            if config_count == 0:
                print('>>> Start loaddata gv_system')
                call_command('loaddata', 'gv_system')
                print('>>> users record count: ' + str(Config.objects.count()))
            else:
                print('>>> Skip loaddata gv_system')
