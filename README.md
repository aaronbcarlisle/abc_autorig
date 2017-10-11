# ABC Autorigger
Not feature complete. There's three modules currently, leg, arm and main.
You must create a main module for it to build properly.

Both Leg and Arm Modules include:
- Space Switching
- IkFk Blending
- Hook System (for modularity)

Mostly for learning purposes.

## To Use:
Download and unzip into your Scripts folder, then run the following.
~~~ python
from abc_autorig.ui import autorig_ui
ui_instance = autorig_ui.AutorigUI()
ui_instance.ui()

# for reloading
from abc_autorig import main_reload
main_reload.reload_main()
~~~
## NOTE:
All modules can be built without the UI. I'll update the unit test file later.
