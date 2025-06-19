import importlib
import logging

from handlers.interfaces import IHandler


log = logging.getLogger(__name__)


class HandlerMainConfig:
    def __init__(self):
        self.aliases = {}
        self.src_path_prefix = None

    def register_alias(self, from_, to_):
        self.aliases[from_] = to_


class HandlerMain:
    def __init__(self, config: HandlerMainConfig):
        self._config = config

    def get_action_handler(self, mode_type, action_type) -> IHandler.__class__:

        import_path = self._to_import_path(mode_type, action_type)
        handler_name = self._to_handler_name(mode_type, action_type)

        log.info(f"Trying to import: {import_path}.{handler_name}")
        mode_module = importlib.import_module(import_path)
        return getattr(mode_module, handler_name)

    def _to_import_path(self, mode_type, action_type):
        mode_type_s = mode_type.__str__()
        action_type_s = action_type.__str__().replace('-', "_")
        action_type_s = self._apply_aliases(action_type_s)

        path = f"handlers.{mode_type_s}.handler_{mode_type_s}_{action_type_s}"
        src_path_prefix = self._config.src_path_prefix
        if src_path_prefix:
            path = f"{src_path_prefix}.{path}"

        return path

    def _to_handler_name(self, mode_type, action_type):
        mode_type_camel_s = ""
        for x in self._apply_aliases(mode_type.__str__()).split("-"):
            mode_type_camel_s += x[0].upper() + x[1:]
        action_type_camel_s = ""
        for x in self._apply_aliases(action_type.__str__()).split("-"):
            action_type_camel_s += x[0].upper() + x[1:]
        path = f"Handler{mode_type_camel_s}{action_type_camel_s}"
        print(path)
        return path

    def _apply_aliases(self, string):
        for from_, to_ in self._config.aliases.items():
            if string == from_:
                return to_
            elif string.endswith(f"-{from_}"):
                return string.endswith(f"-{to_}")
        return string
