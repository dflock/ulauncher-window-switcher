from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess


class X11WindowSwitcherExtension(Extension):
    def __init__(self):
        # Check that wmctrl is installed
        import shutil

        # Check that we have wmctrl before continuing
        if shutil.which("wmctrl"):
            # We have wmctrl, hook up extension
            super(X11WindowSwitcherExtension, self).__init__()
            self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        else:
            # No wmctrl, so bail
            import logging

            logger = logging.getLogger(__name__)
            logger.error("Missing Dependency: wmctrl not found on $PATH")
            import sys

            sys.exit()


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        keyword = event.get_keyword()
        search = str(event.get_argument() or "").lower().strip()

        items = []

        # Get list of all windows, and process into a dictionary that looks like this:
        # {<window_id>: {ws: <workspace_id>, name: <window_name>}}
        result = subprocess.run(
            ['wmctrl -l | awk \'{ if( $2 != "-1") { $3="";  print $0} }\''],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # equivalent to capture_output=True
            shell=True,
            universal_newlines=True,  # equivalent to text=True
        ).stdout
        w_list = [y for y in (x.strip() for x in result.splitlines()) if y]
        w_dict = {
            x[1].split(maxsplit=2)[0]: {
                "ws": int(x[1].split(maxsplit=2)[1]),
                "name": x[1].split(maxsplit=2)[2],
            }
            for x in enumerate(w_list)
        }

        # Get list of all workspaces and process into a dictionary that looks like this:
        # {<workspace_id>: <workspace_name>}
        result = subprocess.run(
            [
                "wmctrl -d | sed -n -E -e 's/^.*WA: (N\/A|.,. [[:digit:]]+x[[:digit:]]+)  //p'"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # equivalent to capture_output=True
            shell=True,
            universal_newlines=True,  # equivalent to text=True
        ).stdout
        ws_list = [y for y in (x.strip() for x in result.splitlines()) if y]
        ws_dict = {i: x for i, x in enumerate(ws_list)}

        for w_idx, window in w_dict.items():
            if search == "" or search in window["name"].lower():
                items.append(
                    ExtensionResultItem(
                        icon="images/window.svg",
                        # Workaround for https://github.com/Ulauncher/Ulauncher/issues/587
                        name=window["name"].replace("&", "&amp;")
                        if search
                        else window["name"],
                        description="Workspace {}: {}, Window Id: {}".format(
                            window["ws"], ws_dict[window["ws"]], w_idx
                        ),
                        on_enter=RunScriptAction("wmctrl -ia {}".format(w_idx)),
                    )
                )

        return RenderResultListAction(items)


if __name__ == "__main__":
    X11WindowSwitcherExtension().run()
