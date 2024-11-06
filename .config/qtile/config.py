# [import]
import os
import re
import json
import psutil
import socket
import subprocess

from subprocess import Popen
from typing import List
from pathlib import Path
from libqtile import bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.widget.decorations import BorderDecoration

# [variables]
mod = "mod4"
terminal = guess_terminal()
#home = os.path.expanduser("~")
home = str(Path.home())
conf = home + "/.config/qtile/"
lbin = home + "/.local/bin/"
astart = conf + "autostart.sh"
colordict = json.load(open(conf + "colors.json"))

# MyPallete Dracula Gruvbox Monokai Nord Palenight Solarized
colorscheme = colordict["MyPallete"]
Color0=(colorscheme["Color0"])
Color1=(colorscheme["Color1"])
Color2=(colorscheme["Color2"])
Color3=(colorscheme["Color3"])
Color4=(colorscheme["Color4"])
Color5=(colorscheme["Color5"])
Color6=(colorscheme["Color6"])
Color7=(colorscheme["Color7"])
Color8=(colorscheme["Color8"])

# [keys]
keys = [
    # Switch between windows.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "w", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),
    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow/shrink windows.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split/unsplit"),
    # Lauch default terminal emulator.
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below.
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Kill active window.
    Key([mod], "escape", lazy.window.kill(), desc="Kill focused window"),
    # Toggle fullsreen/floating  mode on the focused window.
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    # Main qtile commands.
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# [groups]
#groups = [Group(i) for i in "12345"]
groups = []
group_names = ["1", "2", "3", "4", "5",]
group_labels = ["1", "2", "3", "4", "5",]
group_layouts = ["bsp", "bsp", "bsp", "bsp", "bsp"]

groups.append(ScratchPad("6", [
    DropDown("peek", "peek", x=0.3, y=-0.04, width=0.40, height=0.4, on_focus_lost_hide=False),
    DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False),
]))

keys.extend([
    Key([mod], "F9", lazy.group["6"].dropdown_toggle("peek")),
    Key([mod], 'F10', lazy.group["6"].dropdown_toggle("terminal")),
])

for i in range(len(group_names)):
    groups.append(
            Group(
                name=group_names[i],
                layout=group_layouts[i].lower(),
                label=group_labels[i],
            ))

for i in groups:
    keys.extend(
        [   # mod + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name)),
            # mod + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)),
            # mod + ctrl + letter of group = switch focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=False),
                desc="Switch focused window to group {}".format(i.name)),
        ]
    )

# [layouts]
def init_layout_theme():
    return {
        "border_width": 2,
        "margin": 5,
        "border_focus": Color2,
        "border_normal": Color8,
    }
layout_theme = init_layout_theme()

layouts = [
	layout.Bsp(**layout_theme),
	layout.Tile(**layout_theme),
    layout.Floating(),
#	layout.Columns(),
#	layout.Matrix(),
#	layout.Max(),
#	layout.MonadTall(),
#	layout.MonadWide(),
#	layout.RatioTile(),
#	layout.Stack(num_stacks=2),
#	layout.TreeTab(),
#	layout.VerticalTile(),
#	layout.Zoomy(),
]

# [decorations]
def init_widgets_defaults():
    return dict(
        font="FiraCode Nerd Font SemBd",
        fontsize=14,
        padding=5,
    )
widget_defaults = init_widgets_defaults()    
extension_defaults = widget_defaults.copy()

rect = {
    "decorations": [
        RectDecoration(
            use_widget_background=True,
            line_colour=Color3,
            line_width=2,
            padding_y=2,
            clip=True,
            radius=13,
            group=True
        )
    ]
}
border = {
    "decorations": [
        BorderDecoration(
            border_width=[0,0,2,0],
            padding_y=3,
            colour=Color7
        )
    ]
}
left = {
   "decorations": [
        PowerLineDecoration(
#            path="arrow_left"
            path="rounded_left"
#            path="forward_slash"
        )
    ]
}
right = {
    "decorations": [
        PowerLineDecoration(
#            path="arrow_right"
            path="rounded_right"
#            path="back_slash"
        )
    ]
}

# [widgets_list]
def init_widgets_list():
    widgets_list = [
        widget.TextBox(
            background=Color0,
            fontsize=20,
            text="",
            foreground=Color3,
            fontshadow=Color1,
            desc="",
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn("rofi -show drun")},
        ),
        widget.CurrentLayoutIcon(
            use_mask=True,
            foreground=Color5,
            fontshadow=Color1,
            scale=0.5,
        ),
        widget.GroupBox(
            highlight_method="line",
            active=Color6,
            inactive=Color4,
            fontshadow=Color1,
            borderwidth=2,
            font="Clockopia",
            fontsize=15,
            highlight_color=[Color0, Color0],
            this_current_screen_border=Color7,
            margin_x=0,
        ),
        widget.Sep(
            padding=10,
            linewidth=2,
            size_percent=55,
            foreground=Color4,
            fontshadow=Color1,
        ),
        widget.LaunchBar(
            foreground=Color4,
            fontshadow=Color1,
            progs=[("","vivaldi"), ("","alacritty -e vifm"), ("","telegram-desktop")],
        ),
        widget.TextBox(
            background=Color0,
            fontsize=15,
            text="",
            foreground=Color4,
            fontshadow=Color1,
            desc="",
            padding=6,
            mouse_callbacks={"Button1": lazy.spawn(lbin + "mpv.sh")},
        ),
        widget.TextBox(
            background=Color0,
            fontsize=15,
            text="",
            foreground=Color4,
            fontshadow=Color1,
            desc="",
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn(lbin + "screenshot.sh")},
        ),
        widget.TextBox(
            background=Color0,
            fontsize=15,
            text="",
            foreground=Color4,
            fontshadow=Color1,
            desc="",
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn(lbin + "script.sh")},
        ),
        widget.Spacer(5),
        widget.Prompt(),
        widget.TaskList(
            icon_size=16,
            fontsize=0,
            borderwidth=0,
            margin=10,
            padding=1,
        ),
        widget.Spacer(),
#        widget.OpenWeather(
#            location="Kaliningrad",
#            format="{location_city}: {icon}   {temp}°{units_temperature}   {humidity}%   {wind_speed}{units_wind_speed}",
#            language="ru",
#            mouse_callbacks={"Button1": lazy.spawn(
#                ["kitty", "--hold", "-e", "curl", "ru.wttr.in/Kaliningrad?format=v2d"]
#            )},
#            foreground=Color5,
#            fontshadow=Color1,
#        ),
        widget.Wttr(
            lang="ru",
            location={"Svetlogorsk, Russia":"Калининград:"},
            format="%C %t %w %h",
            units="M",
            mouse_callbacks={"Button1": lazy.spawn(
                ["kitty", "--hold", "-e", "curl", "ru.wttr.in/Kaliningrad?format=v2d"]
            )},
            foreground=Color5,
            fontshadow=Color1,
        ),
        widget.Spacer(),
        widget.CheckUpdates(
            distro="Gentoo_eix",
            update_interval=3600,
            display_format=" {updates}",
            colour_have_updates=Color6,
            fontshadow=Color1,
            execute="kitty -e sudo cl-update",
        ),
        widget.Spacer(5),
        widget.Systray(
            icon_size=16,
            padding=12,
        ),
        widget.Spacer(5),
        widget.Sep(
            padding=15,
            linewidth=2,
            size_percent=55,
            foreground=Color4,
            fontshadow=Color1,
        ),
        widget.KeyboardLayout(
            configured_keyboards=["us","ru"],
            foreground=Color6,
            fontshadow=Color1,
        ),
        widget.Sep(
            padding=10,
            linewidth=3,
            size_percent=10,
            foreground=Color4,
            fontshadow=Color1,
        ),
        widget.PulseVolume(
            step=5,
            foreground=Color6,
            fontshadow=Color1,
        ),
        widget.Sep(
            padding=10,
            linewidth=3,
            size_percent=10,
            foreground=Color4,
            fontshadow=Color1,
        ),
        widget.Clock(
            format="%d-%b %a %H:%M",
            mouse_callbacks={"Button1": lazy.spawn("kitty -e calcurse")},
            foreground=Color5,
            fontshadow=Color1,
        ),
        widget.Sep(
            padding=10,
            linewidth=3,
            size_percent=10,
            foreground=Color4,
            fontshadow=Color1,
        ),
        widget.TextBox(
            background=Color0,
            fontsize=20,
            text="",
            foreground=Color3,
            fontshadow=Color1,
            desc="",
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn(lbin + "powermenu.sh")},
        ),
        widget.Spacer(10),
    ]
    return widgets_list
widgets_list = init_widgets_list()

# [screens]
def init_widgets_screen():
    widgets_screen = widgets_list
    return widgets_screen
widgets_screen = init_widgets_screen()

def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=widgets_screen,
                size=32,
                opacity=0.8,
                background=Color0,
                border_width=[5, 5, 5, 5],
                border_color=[Color0, Color0, Color0, Color0],
            ),
        ),
    ]    
screens = init_screens()

# [floating_rules]
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = "floating_only"
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="blueman-manager"),  # blueman
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="kitty"),  # kitty
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="nm-connection-editor"),  # nm-editor
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Waypaper"),  # waypaper
    ]
)

no_float_rules = [
    Match(wm_class="mpv"),
]

# [miscellaneous]
auto_fullscreen = True # on app request
focus_on_window_activation = "focus" # or smart
reconfigure_screens = True
auto_minimize = True # on app request
wl_input_rules = None # used to configure input_devices in wayland
wmname = "Qtile"

# [hooks]
@hook.subscribe.startup_once
def autostart():
	Popen([astart])

@hook.subscribe.client_managed
def force_tile(window):
    for rule in no_float_rules:
        if rule.compare(window):
            window.floating = False
            break
