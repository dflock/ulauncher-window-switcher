# Window Switcher plugin for Ulauncher

This is a plugin for [uLauncher](https://ulauncher.io/) that lets you search & switch between Linux/X11 Windows by name:

![](./screenshots/search.png)

The default keyword in `w`, so just run Ulauncher, then type `w <query>` to filter the window list, then select a window from the list to switch to that window.

I used window icons from the [Obsidian Icon pack](https://github.com/madmaxms/iconpack-obsidian)

## Requirements

You need `wmctrl` installed. See: https://www.freedesktop.org/wiki/Software/wmctrl/

For Debian/Ubuntu, you can do:

```shell
$ sudo apt install wmctrl
```
