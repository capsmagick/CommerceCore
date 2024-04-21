from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import StringPreference

from setup.dtynamic_preferences_type_registry import EmailPreference


section = Section('integrations')


@global_preferences_registry.register
class ShipRocketEMAIL(EmailPreference):
    section = section
    name = 'SHIP_ROCKET_EMAIL'
    default = 'rmuwork51@gmail.com'
    required = False


@global_preferences_registry.register
class ShipRocketPassword(StringPreference):
    section = section
    name = 'SHIP_ROCKET_PASSWORD'
    default = 'rmuKnowbinTech'
    required = False


