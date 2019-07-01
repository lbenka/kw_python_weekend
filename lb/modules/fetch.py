from lb.modules.alsa import Alsa
from lb.modules.arriva import Arriva
from lb.modules.regiojet import Regiojet

provider_config = {"ALSA": Alsa, "ARRIVA": Arriva, "REGIOJET": Regiojet}


def fetch_provider(provider_name: str):
    return provider_config.get(provider_name.upper())
