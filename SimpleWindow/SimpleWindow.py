from ctypes import c_int, windll, sizeof, byref
import win32gui, win32con
import OpenGL.GL as gl
import ctypes
import numpy
import glfw
import cv2
import os


RED = "\033[91m"
NORMAL = "\033[0m"


class Window:
    # MARK: __init__()
    def __init__(self,
                 name: str,
                 size: tuple = (None, None),
                 position: tuple = (None, None),
                 title_bar_color: tuple = (None, None, None),
                 border_color: tuple = (None, None, None),
                 resizable: bool = True,
                 topmost: bool = False,
                 foreground: bool = True,
                 minimized: bool = False,
                 undestroyable: bool = False,
                 icon: str = "",
                 no_warnings: bool = False):
        """
        Initialize a new window
        The window will be shown when calling create_window() or when showing the first frame with show()

        Parameters
        ----------
        name : str
            The name of the window
        size : tuple
            The size of the window
        position : tuple
            The position of the window
        title_bar_color : tuple, optional
            The color of the title bar
        border_color : tuple, optional
            The color of the window border
        resizable : bool, optional
            If the window should be resizable
        topmost : bool, optional
            If the window should be always on top
        foreground : bool, optional
            If the window should be in the foreground on creation
        minimized : bool, optional
            If the window should be minimized on creation
        undestroyable : bool, optional
            If the window should be undestroyable
        icon : str, optional
            The path to the .ico icon
        no_warnings : bool, optional
            If warnings should be printed
        """
        glfw.init()

        self._name = name
        self._size = size
        self._position = position
        self._title_bar_color = title_bar_color
        self._border_color = border_color
        self._resizable = resizable
        self._topmost = topmost
        self._foreground = foreground
        self._minimized = minimized            
        self._undestroyable = undestroyable
        self._icon = icon
        self._no_warnings = no_warnings

        self._open = False
        self._hwnd = None
        self._window = None
        self._texture_id = None


    # MARK: create_window()
    def create_window(self):
        """
        Create the window

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._size[0] == None:
            self._size = 150, self._size[1]
        if self._size[1] == None:
            self._size = self._size[0], 50

        if self._position[0] == None:
            self._position = 0, self._position[1]
        if self._position[1] == None:
            self._position = self._position[0], 0

        # some windows magic so that the icon is also shown int the taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Python.Pip.Modules.SimpleWindow.PyPI.GitHub.OleFranz")

        self._window = glfw.create_window(self._size[0], self._size[1], self._name, None, None)
        glfw.make_context_current(self._window)
        glfw.set_window_size_limits(self._window, 150, 50, glfw.DONT_CARE, glfw.DONT_CARE)
        glfw.set_window_pos(self._window, self._position[0], self._position[1])

        self._hwnd = glfw.get_win32_window(self._window)
        self._open = True

        if None not in self._title_bar_color:
            self.set_title_bar_color(self._title_bar_color)
        if None not in self._border_color:
            self.set_border_color(self._border_color)
        if self._resizable == False:
            glfw.set_window_attrib(self._window, glfw.RESIZABLE, glfw.FALSE)
        if self._topmost:
            glfw.set_window_attrib(self._window, glfw.FLOATING, glfw.TRUE)
        if self._foreground:
            self.set_foreground(state=True)
        if self._minimized:
            self.set_minimized(state=True)
        if self._icon != "":
            self.set_icon(self._icon)

        self._texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGB8,
            self._size[0],
            self._size[1],
            0,
            gl.GL_BGR,
            gl.GL_UNSIGNED_BYTE,
            None
        )


    # MARK: close()
    def close(self):
        """
        Close the window

        Parameters
        ----------
        None

        Returns
        -------
        None"""
        if self._open:
            glfw.destroy_window(self._window)
            self._open = False


    # MARK: set_name()
    def set_name(self, name: str):
        """
        Set the name of the window

        Parameters
        ----------
        name : str
            The name of the window

        Returns
        -------
        None
        """
        glfw.set_window_title(self._window, name)
        self._name = name


    # MARK: get_name()
    def get_name(self):
        """
        Get the name of the window

        Parameters
        ----------
        None

        Returns
        -------
        str
            The name of the window
        """
        return self._name


    # MARK: set_size()
    def set_size(self, size: tuple):
        """
        Set the size of the window

        Parameters
        ----------
        size : tuple
            The size of the window

        Returns
        -------
        None
        """
        if size != self._size and self._open:
            if len(size) != 2 or isinstance(size[0], (int, type(None))) == False or isinstance(size[1], (int, type(None))) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: size must be a tuple of (int, int)" + NORMAL)
                return
        if size[0] == None:
            size = (self._size[0], size[1])
        if size[1] == None:
            size = (size[0], self._size[1])
        if None in size:
            if self._no_warnings != True:
                print(RED + "SimpleWindow: size not valid, found None value" + NORMAL)
            return
        size = max(150, round(size[0])), max(50, round(size[1]))
        glfw.set_window_size(self._window, size[0], size[1])
        self._size = size


    # MARK: get_size()
    def get_size(self):
        """
        Get the size of the window

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            The size of the window
        """
        if self._open:
            return glfw.get_window_size(self._window)
        return self._size


    # MARK: set_position()
    def set_position(self, position: tuple):
        """
        Set the position of the window

        Parameters
        ----------
        position : tuple
            The position of the window

        Returns
        -------
        None
        """
        if position != self._position and self._open:
            if len(position) != 2 or isinstance(position[0], (int, type(None))) == False or isinstance(position[1], (int, type(None))) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: position must be a tuple of (int, int)" + NORMAL)
                return
        if position[0] == None:
            position = (self._position[0], position[1])
        if position[1] == None:
            position = (position[0], self._position[1])
        if None in position:
            if self._no_warnings != True:
                print(RED + "SimpleWindow: position not valid, found None value" + NORMAL)
            return
        glfw.set_window_pos(self._window, position[0], position[1])
        self._position = position


    # MARK: get_position()
    def get_position(self):
        """
        Get the position of the window

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            The position of the window
        """
        if self._open:
            return glfw.get_window_pos(self._window)
        return self._position


    # MARK: set_title_bar_color()
    def set_title_bar_color(self, color: tuple):
        """
        Set the title bar color of the window

        Parameters
        ----------
        color : tuple
            The color of the title bar, must be a tuple of (int, int, int)

        Returns
        -------
        None
        """
        if self._open:
            if len(color) != 3 or isinstance(color[0], int) == False or isinstance(color[1], int) == False or isinstance(color[2], int) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: title_bar_color must be a tuple of (int, int, int)" + NORMAL)
                return
            windll.dwmapi.DwmSetWindowAttribute(self._hwnd, 35, byref(c_int((max(0, min(255, round(color[0]))) << 16) | (max(0, min(255, round(color[1]))) << 8) | max(0, min(255, round(color[2]))))), sizeof(c_int))
        self._title_bar_color = color


    # MARK: get_title_bar_color()
    def get_title_bar_color(self):
        """
        Get the title bar color of the window

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            The title bar color of the window
        """
        return self._title_bar_color


    # MARK: set_border_color()
    def set_border_color(self, color: tuple):
        """
        Set the border color of the window

        Parameters
        ----------
        color : tuple
            The color of the border, must be a tuple of (int, int, int)

        Returns
        -------
        None
        """
        if self._open:
            if len(color) != 3 or isinstance(color[0], int) == False or isinstance(color[1], int) == False or isinstance(color[2], int) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: border_color must be a tuple of (int, int, int)" + NORMAL)
                return
            windll.dwmapi.DwmSetWindowAttribute(self._hwnd, 34, byref(c_int((max(0, min(255, round(color[0]))) << 16) | (max(0, min(255, round(color[1]))) << 8) | max(0, min(255, round(color[2]))))), sizeof(c_int))
        self._border_color = color


    # MARK: get_border_color()
    def get_border_color(self):
        """
        Get the border color of the window

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            The border color of the window
        """
        return self._border_color


    # MARK: set_resizable()
    def set_resizable(self, state: bool):
        """
        Set the resizable state of the window

        Parameters
        ----------
        state : bool
            If the window should be resizable

        Returns
        -------
        None
        """
        glfw.set_window_attrib(self._window, glfw.RESIZABLE, glfw.TRUE if state else glfw.FALSE)
        self._resizable = state


    # MARK: get_resizable()
    def get_resizable(self):
        """
        Get the resizable state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is resizable
        """
        return self._resizable


    # MARK: set_topmost()
    def set_topmost(self, state: bool):
        """
        Set the window to be always on top of other windows

        Parameters
        ----------
        state : bool
            If the window should be always on top of other windows

        Returns
        -------
        None
        """
        if self._window != None:
            glfw.set_window_attrib(self._window, glfw.FLOATING, glfw.TRUE if state else glfw.FALSE)
        self._topmost = state


    # MARK: get_topmost()
    def get_topmost(self):
        """
        Get the topmost state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is on top of other windows
        """
        return self._topmost


    # MARK: set_foreground()
    def set_foreground(self, state: bool):
        """
        Set the window to be in the foreground

        Parameters
        ----------
        state : bool
            If the window should be in the foreground

        Returns
        -------
        None
        """
        if self._open:
            if state:
                win32gui.SetWindowPos(self._hwnd, win32con.HWND_TOPMOST if self._topmost else win32con.HWND_TOP, self.get_size()[0], self.get_size()[1], 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            else:
                win32gui.SetWindowPos(self._hwnd, win32con.HWND_BOTTOM, self.get_size()[0], self.get_size()[1], 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        self._foreground = state


    # MARK: get_foreground()
    def get_foreground(self):
        """
        Get the foreground state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is in the foreground
        """
        if self._open:
            self._foreground = self._hwnd == win32gui.GetForegroundWindow()
        return self._foreground


    # MARK: set_minimized()
    def set_minimized(self, state: bool):
        """
        Set the window to be minimized

        Parameters
        ----------
        state : bool
            If the window should be minimized

        Returns
        -------
        None
        """
        if self._open:
            win32gui.ShowWindow(self._hwnd, win32con.SW_MINIMIZE if state else win32con.SW_RESTORE)
        self._minimized = state


    # MARK: get_minimized()
    def get_minimized(self):
        """
        Get the minimized state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is minimized
        """
        if self._open:
            self._minimized = int(win32gui.IsIconic(self._hwnd)) == 1
        return self._minimized


    # MARK: set_undestroyable()
    def set_undestroyable(self, state: bool):
        """
        Set the window to be undestroyable
        Undestroyable windows will automatically reopen when the user closes the window

        Parameters
        ----------
        state : bool
            If the window should be undestroyable

        Returns
        -------
        None
        """
        self._undestroyable = state


    # MARK: get_undestroyable()
    def get_undestroyable(self):
        """
        Get the undestroyable state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is undestroyable
        """
        return self._undestroyable


    # MARK: set_icon()
    def set_icon(self, icon: str):
        """
        Set the window icon of the window

        Parameters
        ----------
        icon : str
            The path to the .ico icon

        Returns
        -------
        None
        """
        if self._open:
            if isinstance(icon, str) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: icon must be a string, the path to the .ico file" + NORMAL)
                return
            if os.path.exists(icon) == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: invalid icon path" + NORMAL)
                return
            if icon.endswith(".ico") == False:
                if self._no_warnings != True:
                    print(RED + "SimpleWindow: icon must be an .ico file" + NORMAL)
                return
            icon_handle = win32gui.LoadImage(None, icon, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
            win32gui.SendMessage(self._hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon_handle)
            win32gui.SendMessage(self._hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon_handle)
        self._icon = icon


    # MARK: get_icon()
    def get_icon(self):
        """
        Get the icon path of the window

        Parameters
        ----------
        None

        Returns
        -------
        str
            The path to the .ico icon
        """
        return self._icon


    # MARK: set_open()
    def set_open(self, state: bool):
        """
        Set the open state of the window

        Parameters
        ----------
        state : bool
            If the window should be open

        Returns
        -------
        None
        """
        if state and self._open != True:
            self.create_window()
        elif state == False and self._open:
            self.close()


    # MARK: get_open()
    def get_open(self):
        """
        Get the open state of the window

        Parameters
        ----------
        None

        Returns
        -------
        bool
            If the window is open
        """
        return self._open == True


    # MARK: get_handle()
    def get_handle(self):
        """
        Get the handle (HWND) of the window

        Parameters
        ----------
        None

        Returns
        -------
        int
            The handle of the window
        """
        return self._hwnd


    # MARK: show()
    def show(self, frame: numpy.ndarray):
        """
        Show the frame in the window

        Parameters
        ----------
        frame : numpy.ndarray
            The frame to show

        Returns
        -------
        None
        """
        if self._open == False:
            self.create_window()

        if self._open == False and self._undestroyable == False:
            return

        if glfw.window_should_close(self._window):
            if self._open == True:
                self.close()
                self._open = "user_closed"
            if self._undestroyable:
                self.create_window()
            return

        self._minimized = self.get_minimized()

        if self._minimized:
            glfw.poll_events()
            return

        glfw.make_context_current(self._window)

        width, height = glfw.get_framebuffer_size(self._window)
        if (width != gl.glGetTexLevelParameteriv(gl.GL_TEXTURE_2D, 0, gl.GL_TEXTURE_WIDTH) or
            height != gl.glGetTexLevelParameteriv(gl.GL_TEXTURE_2D, 0, gl.GL_TEXTURE_HEIGHT)):
            gl.glTexImage2D(
                gl.GL_TEXTURE_2D,
                0,
                gl.GL_RGB8,
                width,
                height,
                0,
                gl.GL_BGR,
                gl.GL_UNSIGNED_BYTE,
                None
            )

        gl.glViewport(0, 0, width, height)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if len(frame.shape) == 2 or frame.shape[2] == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        if frame.shape[0] != height or frame.shape[1] != width:
            frame = cv2.resize(frame, (width, height))

        frame = numpy.ascontiguousarray(frame, dtype=numpy.uint8)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexSubImage2D(
            gl.GL_TEXTURE_2D,
            0, 0, 0,
            width, height,
            gl.GL_BGR,
            gl.GL_UNSIGNED_BYTE,
            frame.tobytes()
        )

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0.0, 1.0); gl.glVertex2f(-1.0, -1.0)
        gl.glTexCoord2f(1.0, 1.0); gl.glVertex2f( 1.0, -1.0)
        gl.glTexCoord2f(1.0, 0.0); gl.glVertex2f( 1.0,  1.0)
        gl.glTexCoord2f(0.0, 0.0); gl.glVertex2f(-1.0,  1.0)
        gl.glEnd()
        gl.glDisable(gl.GL_TEXTURE_2D)

        glfw.swap_buffers(self._window)

        glfw.poll_events()