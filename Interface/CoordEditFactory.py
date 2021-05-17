from re import search
from tkinter import *
from tkinter.ttk import Treeview

from numpy import clip

from Coord import Coord


class CoordEditFactory:
    def __init__(self, parent: Treeview):
        self._parent = parent
        self._edit_widget = None
        self.get_coord_callback = None
        self.set_coord_callback = None
        self.paint_marker_from_coord_callback = None

    def close_widget(self):
        if self._edit_widget:
            self._edit_widget.destroy()

    def edit(self, row, column):
        self.close_widget()

        try:
            if column == "name":
                self._edit_widget = TextEditWidget(
                    self._parent,
                    self.get_coord_callback,
                    self.set_coord_callback,
                    row,
                    column
                )
            else:
                self._edit_widget = NumericEditWidget(
                    self._parent,
                    self.get_coord_callback,
                    self.set_coord_callback,
                    row,
                    column,
                    self.paint_marker_from_coord_callback
                )

            x, y, width, height = self._parent.bbox(row, column)
            self._edit_widget.place(x=x, y=y, anchor=NW, width=width, height=height)
        except BaseEditWidget.UneditableField:
            pass


class BaseEditWidget(Frame):
    class UneditableField(Exception):
        pass

    def __init__(self, parent, set_coord_callback, row, column, **kw):
        super().__init__(parent, **kw)

        self._parent = parent
        self._set_coord_callback = set_coord_callback
        self._row = row
        self._column = column

        self.bind("<Escape>", lambda *_: self.destroy())

        self.focus_force()


class TextEditWidget(BaseEditWidget):
    def __init__(self, parent, get_coord_callback, set_coord_callback, row, column, **kw):
        super().__init__(parent, set_coord_callback, row, column, **kw)

        self._text = StringVar()
        self._coord: Coord = get_coord_callback(row)
        text = self._coord.column_data(self._column)
        if text is None:
            raise self.UneditableField()
        self._text.set(text)

        self._widget = Entry(self)
        self._widget.pack(fill=BOTH, expand=YES)
        # exportselection = automatic copying selected text to clipboard
        self._widget.config(textvariable=self._text, exportselection=False)
        self._widget.focus_set()

        self._widget.bind("<Return>", self._on_return)
        self._widget.bind("<Control-a>", lambda *_: self.select_all())
        self._widget.bind("<Escape>", lambda *_: self.destroy())

    def _on_return(self, event):
        value = self._text.get()
        self._coord.column_data(self._column, value)
        self._set_coord_callback(self._row, self._coord)
        self.destroy()

    def select_all(self):
        self._widget.selection_range(0, 'end')
        # returns 'break' to interrupt default key-bindings
        return 'break'


class NumericEditWidget(TextEditWidget):
    drag_icon = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\t\x00\x00\x00\x10\x08\x06\x00\x00\x00\xc4HUC\x00\x00\n0iCCPICC Profile\x00\x00x\x9c\x9d\x96wTT\xd7\x16\x87\xcf\xbdwz\xa1\xcd0\x14)C\xef\xbd\r \xbd7\xa9\xd2Da\x98\x19`(\x03\x0e34\xb1!\xa2\x02\x11ED\x04\x15A\x82"\x06\x8c\x86"\xb1"\x8a\x85\x80`\xc1\x1e\x90 \xa0\xc4`\x14QQy3\xb2Vt\xe5\xe5\xbd\x97\x97\xdf\x1fg}k\x9f\xbd\xf7=g\xef}\xd6\xba\x00\x90\xbc\xfd\xb9\xbctX\n\x804\x9e\x80\x1f\xe2\xe5J\x8f\x8c\x8a\xa6c\xfb\x01\x0c\xf0\x00\x03\xcc\x00`\xb223\x02B=\xc3\x80H>\x1en\xf4L\x91\x13\xf8"\x08\x807w\xc4+\x007\x8d\xbc\x83\xe8t\xf0\xffI\x9a\x95\xc1\x17\x88\xd2\x04\x89\xd8\x82\xcd\xc9d\x89\xb8P\xc4\xa9\xd9\x82\x0c\xb1}F\xc4\xd4\xf8\x141\xc3(1\xf3E\x07\x14\xb1\xbc\x98\x13\x17\xd9\xf0\xb3\xcf";\x8b\x99\x9d\xc6c\x8bX|\xe6\x0cv\x1a[\xcc="\xde\x9a%\xe4\x88\x18\xf1\x17qQ\x16\x97\x93-\xe2["\xd6L\x15\xa6qE\xfcV\x1c\x9b\xc6af\x02\x80"\x89\xed\x02\x0e+I\xc4\xa6"&\xf1\xc3B\xdcD\xbc\x14\x00\x1c)\xf1+\x8e\xff\x8a\x05\x9c\x1c\x81\xf8Rn\xe9\x19\xb9|nb\x92\x80\xae\xcb\xd2\xa3\x9b\xd9\xda2\xe8\xde\x9c\xecT\x8e@`\x14\xc4d\xa50\xf9l\xba[zZ\x06\x93\x97\x0b\xc0\xe2\x9d?KF\\[\xba\xa8\xc8\xd6f\xb6\xd6\xd6F\xe6\xc6f_\x15\xea\xbfn\xfeM\x89{\xbbH\xaf\x82?\xf7\x0c\xa2\xf5}\xb1\xfd\x95_z=\x00\x8cYQmv|\xb1\xc5\xef\x05\xa0c3\x00\xf2\xf7\xbf\xd84\x0f\x02 )\xea[\xfb\xc0W\xf7\xa1\x89\xe7%I \xc8\xb031\xc9\xce\xce6\xe6rX\xc6\xe2\x82\xfe\xa1\xff\xe9\xf07\xf4\xd5\xf7\x8c\xc5\xe9\xfe(\x0f\xdd\x9d\x93\xc0\x14\xa6\n\xe8\xe2\xba\xb1\xd2S\xd3\x85|zf\x06\x93\xc5\xa1\x1b\xfdy\x88\xffq\xe0_\x9f\xc30\x84\x93\xc0\xe1sx\xa2\x88p\xd1\x94qy\x89\xa2v\xf3\xd8\\\x017\x9dG\xe7\xf2\xfeS\x13\xffa\xd8\x9f\xb48\xd7"Q\x1a>\x01j\xac1\x90\x1a\xa0\x02\xe4\xd7>\x80\xa2\x10\x01\x12s@\xb4\x03\xfd\xd17\x7f|8\x10\xbf\xbc\x08\xd5\x89\xc5\xb9\xff,\xe8\xdf\xb3\xc2e\xe2%\x93\x9b\xf89\xce-$\x8c\xce\x12\xf2\xb3\x16\xf7\xc4\xcf\x12\xa0\x01\x01H\x02*P\x00*@\x03\xe8\x02#`\x0el\x80=p\x06\x1e\xc0\x17\x04\x820\x10\x05V\x01\x16H\x02i\x80\x0f\xb2A>\xd8\x08\x8a@\t\xd8\x01v\x83jP\x0b\x1a@\x13h\x01\'@\x078\r.\x80\xcb\xe0:\xb8\x01n\x83\x07`\x04\x8c\x83\xe7`\x06\xbc\x01\xf3\x10\x04a!2D\x81\x14 UH\x0b2\x80\xcc!\x06\xe4\x08y@\xfeP\x08\x14\x05\xc5A\x89\x10\x0f\x12B\xf9\xd0&\xa8\x04*\x87\xaa\xa1:\xa8\t\xfa\x1e:\x05]\x80\xaeB\x83\xd0=h\x14\x9a\x82~\x87\xde\xc3\x08L\x82\xa9\xb02\xac\r\x9b\xc0\x0c\xd8\x05\xf6\x83\xc3\xe0\x95p"\xbc\x1a\xce\x83\x0b\xe1\xedp\x15\\\x0f\x1f\x83\xdb\xe1\x0b\xf0u\xf86<\x02?\x87g\x11\x80\x10\x11\x1a\xa2\x86\x18!\x0c\xc4\r\tD\xa2\x91\x04\x84\x8f\xacC\x8a\x91J\xa4\x1eiA\xba\x90^\xe4&2\x82L#\xefP\x18\x14\x05EG\x19\xa1\xecQ\xde\xa8\xe5(\x16j5j\x1d\xaa\x14U\x8d:\x82jG\xf5\xa0n\xa2FQ3\xa8Oh2Z\tm\x80\xb6C\xfb\xa0#\xd1\x89\xe8lt\x11\xba\x12\xdd\x88nC_B\xdfF\x8f\xa3\xdf`0\x18\x1aF\x07c\x83\xf1\xc6Da\x921k0\xa5\x98\xfd\x98V\xccy\xcc f\x0c3\x8b\xc5b\x15\xb0\x06X\x07l \x96\x89\x15`\x8b\xb0{\xb1\xc7\xb0\xe7\xb0C\xd8q\xec[\x1c\x11\xa7\x8a3\xc7y\xe2\xa2q<\\\x01\xae\x12w\x14w\x167\x84\x9b\xc0\xcd\xe3\xa5\xf0Zx;| \x9e\x8d\xcf\xc5\x97\xe1\x1b\xf0]\xf8\x01\xfc8~\x9e M\xd0!8\x10\xc2\x08\xc9\x84\x8d\x84*B\x0b\xe1\x12\xe1!\xe1\x15\x91HT\'\xda\x12\x83\x89\\\xe2\x06b\x15\xf18\xf1\nq\x94\xf8\x8e$C\xd2\'\xb9\x91bHB\xd2v\xd2a\xd2y\xd2=\xd2+2\x99\xacMv&G\x93\x05\xe4\xed\xe4&\xf2E\xf2c\xf2[\t\x8a\x84\xb1\x84\x8f\x04[b\xbdD\x8dD\xbb\xc4\x90\xc4\x0bI\xbc\xa4\x96\xa4\x8b\xe4*\xc9<\xc9J\xc9\x93\x92\x03\x92\xd3Rx)m)7)\xa6\xd4:\xa9\x1a\xa9SR\xc3R\xb3\xd2\x14i3\xe9@\xe94\xe9R\xe9\xa3\xd2W\xa5\'e\xb02\xda2\x1e2l\x99B\x99C2\x17e\xc6(\x08E\x83\xe2FaQ6Q\x1a(\x97(\xe3T\x0cU\x87\xeaCM\xa6\x96P\xbf\xa3\xf6Sgded-e\xc3esdkd\xcf\xc8\x8e\xd0\x10\x9a6\xcd\x87\x96J+\xa3\x9d\xa0\xdd\xa1\xbd\x97S\x96s\x91\xe3\xc8m\x93k\x91\x1b\x92\x9b\x93_"\xef,\xcf\x91/\x96o\x95\xbf-\xff^\x81\xae\xe0\xa1\x90\xa2\xb0S\xa1C\xe1\x91"JQ_1X1[\xf1\x80\xe2%\xc5\xe9%\xd4%\xf6KXK\x8a\x97\x9cXr_\tV\xd2W\nQZ\xa3tH\xa9OiVYE\xd9K9Cy\xaf\xf2E\xe5i\x15\x9a\x8a\xb3J\xb2J\x85\xcaY\x95)U\x8a\xaa\xa3*W\xb5B\xf5\x9c\xea3\xba,\xdd\x85\x9eJ\xaf\xa2\xf7\xd0g\xd4\x94\xd4\xbc\xd5\x84juj\xfdj\xf3\xea:\xea\xcb\xd5\x0b\xd4[\xd5\x1fi\x104\x18\x1a\t\x1a\x15\x1a\xdd\x1a3\x9a\xaa\x9a\x01\x9a\xf9\x9a\xcd\x9a\xf7\xb5\xf0Z\x0c\xad$\xad=Z\xbdZs\xda:\xda\x11\xda[\xb4;\xb4\'u\xe4u|t\xf2t\x9au\x1e\xea\x92u\x9dtW\xeb\xd6\xeb\xde\xd2\xc3\xe81\xf4R\xf4\xf6\xeb\xdd\xd0\x87\xf5\xad\xf4\x93\xf4k\xf4\x07\x0c`\x03k\x03\xae\xc1~\x83AC\xb4\xa1\xad!\xcf\xb0\xdep\xd8\x88d\xe4b\x94e\xd4l4jL3\xf67.0\xee0~a\xa2i\x12m\xb2\xd3\xa4\xd7\xe4\x93\xa9\x95i\xaai\x83\xe9\x033\x193_\xb3\x02\xb3.\xb3\xdf\xcd\xf5\xcdY\xe65\xe6\xb7,\xc8\x16\x9e\x16\xeb-:-^Z\x1aXr,\x0fX\xde\xb5\xa2X\x05Xm\xb1\xea\xb6\xfahmc\xcd\xb7n\xb1\x9e\xb2\xd1\xb4\x89\xb3\xd9g3\xcc\xa02\x82\x18\xa5\x8c+\xb6h[W\xdb\xf5\xb6\xa7m\xdf\xd9Y\xdb\t\xecN\xd8\xfdfod\x9fb\x7f\xd4~r\xa9\xceR\xce\xd2\x86\xa5c\x0e\xea\x0eL\x87:\x87\x11G\xbac\x9c\xe3A\xc7\x11\'5\'\xa6S\xbd\xd3\x13g\rg\xb6s\xa3\xf3\x84\x8b\x9eK\xb2\xcb1\x97\x17\xae\xa6\xae|\xd76\xd797;\xb7\xb5n\xe7\xdd\x11w/\xf7b\xf7~\x0f\x19\x8f\xe5\x1e\xd5\x1e\x8f=\xd5=\x13=\x9b=g\xbc\xac\xbc\xd6x\x9d\xf7F{\xfby\xef\xf4\x1e\xf6Q\xf6a\xf94\xf9\xcc\xf8\xda\xf8\xae\xf5\xed\xf1#\xf9\x85\xfaU\xfb=\xf1\xd7\xf7\xe7\xfbw\x05\xc0\x01\xbe\x01\xbb\x02\x1e.\xd3Z\xc6[\xd6\x11\x08\x02}\x02w\x05>\n\xd2\tZ\x1d\xf4c0&8(\xb8&\xf8i\x88YH~Ho(%46\xf4h\xe8\x9b0\xd7\xb0\xb2\xb0\x07\xcbu\x97\x0b\x97w\x87K\x86\xc7\x847\x85\xcfE\xb8G\x94G\x8cD\x9aD\xae\x8d\xbc\x1e\xa5\x18\xc5\x8d\xea\x8c\xc6F\x87G7F\xcf\xae\xf0X\xb1{\xc5x\x8cULQ\xcc\x9d\x95:+sV^]\xa5\xb8*u\xd5\x99X\xc9Xf\xec\xc98t\\D\xdc\xd1\xb8\x0f\xcc@f=s6\xde\'~_\xfc\x0c\xcb\x8d\xb5\x87\xf5\x9c\xed\xcc\xae`Oq\x1c8\xe5\x9c\x89\x04\x87\x84\xf2\x84\xc9D\x87\xc4]\x89SINI\x95I\xd3\\7n5\xf7e\xb2wrm\xf2\\J`\xca\xe1\x94\x85\xd4\x88\xd4\xd64\\Z\\\xda)\x9e\x0c/\x85\xd7\x93\xae\x92\x9e\x93>\x98a\x90Q\x941\xb2\xdan\xf5\xee\xd53|?~c&\x94\xb92\xb3S@\x15\xfdL\xf5\tu\x85\x9b\x85\xa3Y\x8eY5Yo\xb3\xc3\xb3O\xe6H\xe7\xf0r\xfar\xf5s\xb7\xe5N\xe4y\xe6}\xbb\x06\xb5\x86\xb5\xa6;_-\x7fc\xfe\xe8Z\x97\xb5u\xeb\xa0u\xf1\xeb\xba\xd7k\xac/\\?\xbe\xc1k\xc3\x91\x8d\x84\x8d)\x1b\x7f*0-(/x\xbd)bSW\xa1r\xe1\x86\xc2\xb1\xcd^\x9b\x9b\x8b$\x8a\xf8E\xc3[\xec\xb7\xd4nEm\xe5n\xed\xdff\xb1m\xef\xb6O\xc5\xec\xe2k%\xa6%\x95%\x1fJY\xa5\xd7\xbe1\xfb\xa6\xea\x9b\x85\xed\t\xdb\xfb\xcb\xac\xcb\x0e\xec\xc0\xec\xe0\xed\xb8\xb3\xd3i\xe7\x91r\xe9\xf2\xbc\xf2\xb1]\x01\xbb\xda+\xe8\x15\xc5\x15\xafw\xc7\xee\xbeZiYY\xbb\x87\xb0G\xb8g\xa4\xca\xbf\xaas\xaf\xe6\xde\x1d{?T\'U\xdf\xaeq\xadi\xdd\xa7\xb4o\xdb\xbe\xb9\xfd\xec\xfdC\x07\x9c\x0f\xb4\xd4*\xd7\x96\xd4\xbe?\xc8=x\xb7\xce\xab\xae\xbd^\xbb\xbe\xf2\x10\xe6P\xd6\xa1\xa7\r\xe1\r\xbd\xdf2\xbemjTl,i\xfcx\x98wx\xe4H\xc8\x91\x9e&\x9b\xa6\xa6\xa3JG\xcb\x9a\xe1fa\xf3\xd4\xb1\x98c7\xbes\xff\xae\xb3\xc5\xa8\xa5\xae\x95\xd6Zr\x1c\x1c\x17\x1e\x7f\xf6}\xdc\xf7wN\xf8\x9d\xe8>\xc98\xd9\xf2\x83\xd6\x0f\xfb\xda(m\xc5\xedP{n\xfbLGR\xc7HgT\xe7\xe0)\xdfS\xdd]\xf6]m?\x1a\xffx\xf8\xb4\xda\xe9\x9a3\xb2g\xca\xce\x12\xce\x16\x9e]8\x97wn\xf6|\xc6\xf9\xe9\x0b\x89\x17\xc6\xbac\xbb\x1f\\\x8c\xbcx\xab\'\xb8\xa7\xff\x92\xdf\xa5+\x97=/_\xecu\xe9=w\xc5\xe1\xca\xe9\xabvWO]c\\\xeb\xb8n}\xbd\xbd\xcf\xaa\xaf\xed\'\xab\x9f\xda\xfa\xad\xfb\xdb\x07l\x06:o\xd8\xde\xe8\x1a\\:xv\xc8i\xe8\xc2M\xf7\x9b\x97o\xf9\xdc\xba~{\xd9\xed\xc1;\xcb\xef\xdc\x1d\x8e\x19\x1e\xb9\xcb\xbe;y/\xf5\xde\xcb\xfbY\xf7\xe7\x1flx\x88~X\xfcH\xeaQ\xe5c\xa5\xc7\xf5?\xeb\xfd\xdc:b=rf\xd4}\xb4\xefI\xe8\x93\x07c\xac\xb1\xe7\xbfd\xfe\xf2a\xbc\xf0)\xf9i\xe5\x84\xeaD\xd3\xa4\xf9\xe4\xe9)\xcf\xa9\x1b\xcfV<\x1b\x7f\x9e\xf1|~\xba\xe8W\xe9_\xf7\xbd\xd0}\xf1\xc3o\xce\xbf\xf5\xcdD\xce\x8c\xbf\xe4\xbf\\\xf8\xbd\xf4\x95\xc2\xab\xc3\xaf-_w\xcf\x06\xcd>~\x93\xf6f~\xae\xf8\xad\xc2\xdb#\xef\x18\xefz\xdfG\xbc\x9f\x98\xcf\xfe\x80\xfdP\xf5Q\xefc\xd7\'\xbfO\x0f\x17\xd2\x16\x16\xfe\x05\x03\x98\xf3\xfc\xb9\xacs\x19\x00\x00\x01\x05IDATx\x9c\xc5\x911\x8a\x83@\x18\x85_\xf4\x166z\x94\xa4M\x15\xb0\xb3\x8a\x85\x82\x17\x08hc\x9f\xce\x1b\xc4\x13\x04\xb1\x88\xd8Dob\x1aKG\xf4\x9fa4\xe2\xa4Y\x96]\xd8%\xb0\xcd~\xf0\x8a\xf7\xf8\xba\xb7QJ\xe1\x1d\xda[\xe3OR\x9a\xa6&\x00$Ib\xfd(eYf\xea\xba^}\xd4{\x1c\xc7\xd67\xa9(\n\x13@\xb5\xae\xab\x01\x00\xcf\xe7\xd3\x90R\xde\x83 \xb0\x00@\xcb\xf3\xdc\\\x96\xa5\x92R\x1a\x9c\xf3\x03\x00p\xce\x0f\x9cs\x83\x88*\xc7q,M\x08q!"\x8b\x88\xceA\x10\xdc\x00 \x8e\xe3\x1b\x11\x9d\xc7q4\x89\xe8\xa2\r\xc3pd\x8c5]\xd7\x9d\xc20\xdc\x03\x80\xef\xfb\xfba\x18NB\x88FJy\xd4<\xcf{0\xc6\xb6]\xd7\xb5\x8c\xb1+\x00\xf4}\x7f%\xa2v\x9a\xa6]Y\x96\x8d\x06\x00Q\x14=\x84\x10[)e\x0b\x00\xf3<\xb7\xeb\xba\xee\xea\xban\x00\x00J\xa9\xcf\xb8\xaek*\xa5`\xdb\xb6\xf5u\xdf\xfc\xe3w\xbf\xf1\x02\x93V\xa8\x83\x16\xb7\x17,\x00\x00\x00\x00IEND\xaeB`\x82'

    def __init__(self, parent, get_coord_callback, set_coord_callback, row, column, paint_marker_from_coord_callback,
                 **kw):
        super().__init__(parent, get_coord_callback, set_coord_callback, row, column, **kw)

        self._paint_marker_from_coord_callback = paint_marker_from_coord_callback
        self._coord: Coord = get_coord_callback(row)
        self._original_value = self._coord.column_data(self._column)
        self._last_event = 0

        input_validation_callback = (self.register(self._input_validation), '%P', "%s")
        self._widget.config(validate='key', validatecommand=input_validation_callback, exportselection=True)

        self._photo_image = PhotoImage(data=self.drag_icon)
        self._drag_icon = Label(self._widget, image=self._photo_image, cursor="sb_h_double_arrow")
        self._drag_icon.pack(side=RIGHT, anchor=W)

        self._text.trace("w", self._on_modify_variable)
        self._widget.bind('<Double-1>', self._on_double_click)
        self._drag_icon.bind("<B1-Motion>", self._on_drag)
        self._drag_icon.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Destroy>", self._on_destroy)

    def _on_modify_variable(self, *_):
        """
        Modifies the Coord existing in the model,
        Draws the updated marker with MenuView._on_list_mouseover function
        """
        self._coord.column_data(self._column, float(self._text.get()))
        self._paint_marker_from_coord_callback(self._coord)

    def _on_double_click(self, event):
        index = self._text.get().find(".")
        if self._widget.index(INSERT) <= index:
            self._widget.selection_range(0, index)
        else:
            self._widget.selection_range(index + 1, "end")
        return "break"

    def _on_drag(self, event):
        new_event = event.x / 1000
        delta = new_event - self._last_event
        self._last_event = new_event
        new_value = float(self._text.get()) + delta

        position = clip(new_value, 0, 1)
        self._text.set(position)

    def _on_release(self, event):
        self._last_event = 0

    def _on_destroy(self, event):
        """
        Revert uncommited changes.
        """
        self._coord.column_data(self._column, self._original_value)

    def _on_return(self, event):
        value = float(self._text.get())
        self.destroy()
        self._coord.column_data(self._column, value)
        self._set_coord_callback(self._row, self._coord)

    def _input_validation(self, new_value, old_value):
        pattern = r"^(0\.\d+|1\.0+)$"

        if self._widget.selection_present():
            if "." not in self._widget.selection_get():
                # We can allow any edits excluding "." as long as
                # the other half of the number hasn't been already deleted via selection:
                result = search(pattern, old_value)
                return bool(result)
            else:
                return False

        result = search(pattern, new_value)
        return bool(result)
