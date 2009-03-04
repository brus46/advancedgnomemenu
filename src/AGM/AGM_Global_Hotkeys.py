import gconf

keys={"<Alt>F1":"advancedgnomemenu -s",
      "<Alt>F2":"advancedgnomemenu -s -m"}

def enable_global_hotkeys():
    c = gconf.client_get_default()
    i=20
    for key in keys:
        # key binding
        c.set_string('/apps/metacity/global_keybindings/run_command_'+str(i),key)

        # key command
        c.set_string('/apps/metacity/keybinding_commands/command_'+str(i), keys[key])
        i+=1

def disable_global_hotkeys():
    pass