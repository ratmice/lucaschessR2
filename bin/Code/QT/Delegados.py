"""
Rutinas basicas para la edicion en las listas de registros.
"""

from PySide2 import QtCore, QtGui, QtWidgets

import Code
from Code.Nags.Nags import dic_symbol_nags

from Code.QT import Iconos

dicPM = {}
dicPZ = {}


# dicNG = {}


def generaPM(piezas):
    # dicPM["V"] = Iconos.pmComentario()
    dicPM["R"] = Iconos.pmOpening()
    dicPM["M"] = Iconos.pmComentarioMas()
    dicPM["S"] = Iconos.pmOpeningComentario()

    dicPM["O"] = Iconos.pmOpening()
    dicPM["C"] = Iconos.pmComment()
    dicPM["V"] = Iconos.pmVariation()
    dicPM["OC"] = Iconos.pmOpeningComment()
    dicPM["OV"] = Iconos.pmOpeningVariation()
    dicPM["VC"] = Iconos.pmVariationComment()
    dicPM["OVC"] = Iconos.pmOpeningVariationComment()
    dicPM["T"] = Iconos.pmThemes()

    for k in "KQRNBkqrnb":
        dicPZ[k] = piezas.render(k)

    # nags_folder = Code.path_resource("IntFiles", "NAGs")
    # for f in os.listdir(nags_folder):
    #     if f.endswith(".svg") and f.startswith("$") and len(f) > 5:
    #         nag = f[1:-4]
    #         if nag.isdigit():
    #             fsvg = nags_folder + "/" + f
    #             dicNG[nag] = QtSvg.QSvgRenderer(fsvg)


class ComboBox(QtWidgets.QItemDelegate):
    def __init__(self, liTextos):
        QtWidgets.QItemDelegate.__init__(self)
        self.li_textos = liTextos

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self.li_textos)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, cb, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        num = self.li_textos.index(value)
        cb.setCurrentIndex(num)

    def setModelData(self, cb, model, index):
        num = cb.currentIndex()
        model.setData(index, self.li_textos[num])

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LineaTexto(QtWidgets.QItemDelegate):
    def __init__(self, parent=None, siPassword=False, siEntero=False, rx=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.siPassword = siPassword
        self.siEntero = siEntero
        self.rx = rx

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        if self.siPassword:
            editor.setEchoMode(QtWidgets.QLineEdit.Password)
        if self.siEntero:
            editor.setValidator(QtGui.QIntValidator(self))
            editor.setAlignment(QtCore.Qt.AlignRight)
        if self.rx:
            xrx = QtCore.QRegExp(self.rx)
            validator = QtGui.QRegExpValidator(xrx, self)
            editor.setValidator(validator)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, sle, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        sle.setText(value)

    def setModelData(self, sle, model, index):
        value = str(sle.text())
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LineaTextoUTF8(QtWidgets.QItemDelegate):
    def __init__(self, parent=None, siPassword=False):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.siPassword = siPassword

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        if self.siPassword:
            editor.setEchoMode(QtWidgets.QLineEdit.Password)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, sle, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        sle.setText(value)

    def setModelData(self, sle, model, index):
        value = sle.text()
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class EtiquetaPGN(QtWidgets.QStyledItemDelegate):
    def __init__(self, is_white, si_alineacion=False, si_fondo=False):
        self.is_white = is_white  # None = no hacer
        self.with_figurines = is_white is not None
        self.si_alineacion = si_alineacion
        self.si_fondo = si_fondo
        QtWidgets.QStyledItemDelegate.__init__(self, None)

    def setWhite(self, is_white):
        self.is_white = is_white
        self.with_figurines = is_white is not None

    def rehazPosicion(self):
        position = self.bloquePieza.position
        self.setPos(position.x, position.y)

    def paint(self, painter, option, index):
        data = index.model().data(index, QtCore.Qt.DisplayRole)
        if type(data) == tuple:
            pgn, color, txt_analysis, indicadorInicial, li_nags = data
            if li_nags:
                li = []
                st = set()
                for x in li_nags:
                    x = str(x)
                    if x in st:
                        continue
                    st.add(x)
                    if x.isdigit():
                        x = int(x)
                        symbol = dic_symbol_nags(x)
                        if symbol :
                            li.append(symbol)
                li_nags = li
        else:
            pgn, color, txt_analysis, indicadorInicial, li_nags = data, None, None, None, None

        ini_pz = None
        fin_pz = None
        post_pz = None
        salto_fin_pz = 0
        if self.with_figurines and len(pgn) > 2:
            if pgn[0] in "QBKRN":
                ini_pz = pgn[0] if self.is_white else pgn[0].lower()
                pgn = pgn[1:]
            elif pgn[-1] in "QBRN":
                fin_pz = pgn[-1] if self.is_white else pgn[-1].lower()
                pgn = pgn[:-1]
            elif pgn[-2] in "QBRN":
                fin_pz = pgn[-2] if self.is_white else pgn[-2].lower()
                post_pz = pgn[-1]
                pgn = pgn[:-2]
                salto_fin_pz = -6

        if li_nags:
            if post_pz is None:
                post_pz = ""
            post_pz += " " + " ".join(li_nags)

        rect = option.rect
        w_total = rect.width()
        h_total = rect.height()
        x_total = rect.x()
        y_total = rect.y()

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(rect, QtGui.QColor(Code.configuration.pgn_selbackground()))
            color = Code.configuration.pgn_selforeground()
        elif self.si_fondo:
            fondo = index.model().getFondo(index)
            if fondo:
                painter.fillRect(rect, fondo)

        if indicadorInicial:
            painter.save()
            painter.translate(x_total, y_total)
            painter.drawPixmap(0, 0, dicPM[indicadorInicial])
            painter.restore()

        document_pgn = QtGui.QTextDocument()
        document_pgn.setDefaultFont(option.font)
        if color:
            pgn = '<font color="%s"><b>%s</b></font>' % (color, pgn)
        document_pgn.setHtml(pgn)
        w_pgn = document_pgn.idealWidth()
        h_pgn = document_pgn.size().height()
        hx = h_pgn * 80 / 100
        wpz = int(hx * 0.8)

        ancho = w_pgn
        if ini_pz:
            ancho += wpz
        if fin_pz:
            ancho += wpz + salto_fin_pz
        # if li_nags:
        #     ancho += wpz * len(li_nags)

        # x = x_total + (w_total - ancho) / 2
        # if self.si_alineacion:
        #     alineacion = index.model().getAlineacion(index)
        #     if alineacion == "i":
        #         x = x_total + 3
        #     elif alineacion == "d":
        #         x = x_total + (w_total - ancho - 3)

        x = x_total + 20
        y = y_total + (h_total - h_pgn * 0.9) / 2

        if ini_pz:
            painter.save()
            painter.translate(x, y + 1)
            pm = dicPZ[ini_pz]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz

        painter.save()
        painter.translate(x, y)
        document_pgn.drawContents(painter)
        painter.restore()
        x += w_pgn

        if fin_pz:
            painter.save()
            painter.translate(x - 0.3 * wpz, y + 1)
            pm = dicPZ[fin_pz]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz + salto_fin_pz

        if post_pz:
            document_pgn = QtGui.QTextDocument()
            document_pgn.setDefaultFont(option.font)
            if color:
                post_pz = '<font color="%s"><b>%s</b></font>' % (color, post_pz)
            else:
                post_pz = "<b>%s</b>" % post_pz
            document_pgn.setHtml(post_pz)
            w_pgn = document_pgn.idealWidth()
            painter.save()
            painter.translate(x, y)
            document_pgn.drawContents(painter)
            painter.restore()
            x += w_pgn

        # if li_nags:
        #     for rndr in li_nags:
        #         painter.save()
        #         painter.translate(x - 0.2 * wpz, y - 1)
        #         df = hx * 0.2
        #         pmRect = QtCore.QRectF(df, df, hx - df, hx - df)
        #         rndr.render(painter, pmRect)
        #         painter.restore()
        #         x += wpz * 0.8

        if txt_analysis:
            document_analysis = QtGui.QTextDocument()
            document_analysis.setDefaultFont(option.font)
            if color:
                txt_analysis = '<font color="%s">%s</font>' % (color, txt_analysis)
            document_analysis.setHtml(txt_analysis)
            w_analysis = document_analysis.idealWidth()
            painter.save()
            painter.translate(x_total + (w_total - w_analysis), y)
            document_analysis.drawContents(painter)
            painter.restore()


class PmIconosBMT(QtWidgets.QStyledItemDelegate):
    """
    Delegado para la muestra con html
    """

    def __init__(self, parent=None, dicIconos=None, x=4):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.pos_x = x

        if dicIconos:
            self.dicIconos = dicIconos
        else:
            self.dicIconos = {
                "0": Iconos.pmPuntoBlanco(),
                "1": Iconos.pmPuntoNegro(),
                "2": Iconos.pmPuntoAmarillo(),
                "3": Iconos.pmPuntoNaranja(),
                "4": Iconos.pmPuntoVerde(),
                "5": Iconos.pmPuntoAzul(),
                "6": Iconos.pmPuntoMagenta(),
                "7": Iconos.pmPuntoRojo(),
                "8": Iconos.pmPuntoEstrella(),
            }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if "." in pos:
            pos = pos[: pos.index(".")]

        if not (pos in self.dicIconos):
            return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(self.pos_x, 1, self.dicIconos[pos])
        painter.restore()


class PmIconosColor(QtWidgets.QStyledItemDelegate):
    """Usado en TurnOnLigths"""

    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicpmIconos = {
            "0": Iconos.pmGris32(),
            "1": Iconos.pmAmarillo32(),
            "2": Iconos.pmNaranja32(),
            "3": Iconos.pmVerde32(),
            "4": Iconos.pmAzul32(),
            "5": Iconos.pmMagenta32(),
            "6": Iconos.pmRojo32(),
            "7": Iconos.pmLight32(),
        }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if not (pos in self.dicpmIconos):
            return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(4, 4, self.dicpmIconos[pos])
        painter.restore()


class PmIconosWeather(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicIconos = {
            "0": Iconos.pmInvierno(),
            "1": Iconos.pmLluvia(),
            "2": Iconos.pmSolNubesLluvia(),
            "3": Iconos.pmSolNubes(),
            "4": Iconos.pmSol(),
        }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if not (pos in self.dicIconos):
            if pos.isdigit():
                pos = "4" if int(pos) > 4 else "0"
            else:
                return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(4, 4, self.dicIconos[pos])
        painter.restore()


class PmIconosCheck(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicIconos = {True: Iconos.pmChecked(), False: Iconos.pmUnchecked()}

    def paint(self, painter, option, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole) is True

        rect = option.rect
        width = rect.width()
        height = rect.height()
        x = rect.x() + (width - 16) / 2
        y = rect.y() + (height - 16) / 2

        painter.save()
        painter.drawPixmap(x, y, self.dicIconos[value])
        painter.restore()

    def createEditor(self, parent, option, index):
        return None


class MultiEditor(QtWidgets.QItemDelegate):
    def __init__(self, wparent):
        QtWidgets.QItemDelegate.__init__(self, None)
        self.win_me = wparent

    def createEditor(self, parent, option, index):
        editor = self.win_me.me_set_editor(parent)
        if editor:
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        self.win_me.me_set_value(editor, value)

    def setModelData(self, editor, model, index):
        value = self.win_me.me_leeValor(editor)
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class EtiquetaPOS(QtWidgets.QStyledItemDelegate):
    def __init__(self, with_figurines, siFondo=False, siLineas=True):
        self.with_figurines = with_figurines
        self.siAlineacion = False
        self.siLineas = siLineas
        self.siFondo = siFondo
        QtWidgets.QStyledItemDelegate.__init__(self, None)

    def rehazPosicion(self):
        position = self.bloquePieza.position
        self.setPos(position.x, position.y)

    def paint(self, painter, option, index):
        data = index.model().data(index, QtCore.Qt.DisplayRole)
        pgn, is_white, color, txt_analysis, indicadorInicial, li_nags, agrisar, siLine = data
        if li_nags:
            li = []
            st = set()
            for x in li_nags:
                x = str(x)
                if x in st:
                    continue
                st.add(x)
                if x.isdigit():
                    symbol = dic_symbol_nags(int(x))
                    if symbol:
                        li.append(symbol)
            li_nags = li

        ini_pz = None
        fin_pz = None
        post_pz = None
        salto_fin_pz = 0
        if self.with_figurines and pgn:
            if pgn[0] in "QBKRN":
                ini_pz = pgn[0] if is_white else pgn[0].lower()
                pgn = pgn[1:]
            elif pgn[-1] in "QBRN":
                fin_pz = pgn[-1] if is_white else pgn[-1].lower()
                pgn = pgn[:-1]
            elif len(pgn) > 2 and pgn[-2] in "QBRN":
                fin_pz = pgn[-2] if is_white else pgn[-2].lower()
                post_pz = pgn[-1]
                pgn = pgn[:-2]
                salto_fin_pz = -6

        if li_nags:
            if post_pz is None:
                post_pz = ""
            post_pz += " " + " ".join(li_nags)

        rect = option.rect
        width = rect.width()
        height = rect.height()
        x0 = rect.x()
        y0 = rect.y()
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(
                rect, QtGui.QColor(Code.configuration.pgn_selbackground())
            )  # sino no se ve en CDE-Motif-Windows
            color = Code.configuration.pgn_selforeground()
        elif self.siFondo:
            fondo = index.model().getFondo(index)
            if fondo:
                painter.fillRect(rect, fondo)

        if agrisar:
            painter.setOpacity(0.18)

        if indicadorInicial:
            painter.save()
            painter.translate(x0, y0)
            painter.drawPixmap(0, 0, dicPM[indicadorInicial])
            painter.restore()

        documentPGN = QtGui.QTextDocument()
        documentPGN.setDefaultFont(option.font)
        if color:
            pgn = '<font color="%s"><b>%s</b></font>' % (color, pgn)
        documentPGN.setHtml(pgn)
        wPGN = documentPGN.idealWidth()
        hPGN = documentPGN.size().height()
        hx = hPGN * 80 / 100
        wpz = int(hx * 0.8)

        ancho = wPGN
        if ini_pz:
            ancho += wpz
        if fin_pz:
            ancho += wpz
        # if li_nags:
        #     ancho += wpz * len(li_nags)

        x = x0 + (width - ancho) / 2
        if self.siAlineacion:
            alineacion = index.model().getAlineacion(index)
            if alineacion == "i":
                x = x0 + 3
            elif alineacion == "d":
                x = x0 + (width - ancho - 3)

        y = y0 + (height - hPGN * 0.9) / 2

        if ini_pz:
            painter.save()
            painter.translate(x, y + 1)
            pm = dicPZ[ini_pz]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz

        painter.save()
        painter.translate(x, y)
        documentPGN.drawContents(painter)
        painter.restore()
        x += wPGN

        if fin_pz:
            painter.save()
            painter.translate(x - 0.3 * wpz, y + 1)
            pm = dicPZ[fin_pz]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz + salto_fin_pz

        if post_pz:
            document_pgn = QtGui.QTextDocument()
            document_pgn.setDefaultFont(option.font)
            if color:
                post_pz = '<font color="%s"><b>%s</b></font>' % (color, post_pz)
            else:
                post_pz = "<b>%s</b>" % post_pz
            document_pgn.setHtml(post_pz)
            w_pgn = document_pgn.idealWidth()
            painter.save()
            painter.translate(x, y)
            document_pgn.drawContents(painter)
            painter.restore()
            x += w_pgn

        # if li_nags:
        #     for rndr in li_nags:
        #         painter.save()
        #         painter.translate(x - 0.2 * wpz, y)
        #         pmRect = QtCore.QRectF(0, 0, hx, hx)
        #         rndr.render(painter, pmRect)
        #         painter.restore()
        #         x += wpz

        if txt_analysis:
            txt_analysis = txt_analysis.replace("(", "").replace(")", "")
            document_analysis = QtGui.QTextDocument()
            document_analysis.setDefaultFont(option.font)
            if color:
                txt_analysis = '<font color="%s"><b>%s</b></font>' % (color, txt_analysis)
            document_analysis.setHtml(txt_analysis)
            w_analysis = document_analysis.idealWidth()
            painter.save()
            painter.translate(x0 + (width - w_analysis), y)
            document_analysis.drawContents(painter)
            painter.restore()

        if agrisar:
            painter.setOpacity(1.0)

        if self.siLineas:
            if not is_white:
                pen = QtGui.QPen()
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(x0, y0 + height - 1, x0 + width, y0 + height - 1)

            if siLine:
                pen = QtGui.QPen()
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(x0 + width - 2, y0, x0 + width - 2, y0 + height)
