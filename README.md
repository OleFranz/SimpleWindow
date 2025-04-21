# SimpleWindow

A package to easily create and manage windows in Python

## Installation

```
pip install SimpleWindow
```

## Usage

```python
import SimpleWindow
import numpy as np

# initialize the window, the window wont be shown until show() is called
window = SimpleWindow.Window(name="Example Window",
                             size=(1280, 720),
                             position=(100, 100),
                             title_bar_color=(0, 0, 0),
                             border_color=(None, None, None), # None so we don't overwrite the windows default color
                             resizable=True,
                             topmost=False,
                             foreground=True,
                             minimized=False,
                             undestroyable=False,
                             icon="",
                             no_warnings=False)

# create an image
image = np.zeros((720, 1280, 3), dtype=np.uint8)

while True:
    # the window will be shown now since its the first call of show()
    window.show(frame=image)

    # check if the window is open
    if window.get_open() == False:
        break
```