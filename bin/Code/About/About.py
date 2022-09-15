from PySide2 import QtCore, QtWidgets

import Code
from Code.About import AboutBase
from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import QTUtil


class WAbout(QtWidgets.QDialog):
    def __init__(self, procesador):
        super(WAbout, self).__init__(procesador.main_window)

        # gen_web_bootstrap()

        self.setWindowTitle(_("About"))
        self.setWindowIcon(Iconos.Aplicacion64())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        self.setMaximumWidth(QTUtil.anchoEscritorio())

        f = Controles.TipoLetra(puntos=10)  # 0, peso=75 )

        head = (
            '<span style="font-size:30pt; font-weight="700"; font-family:arial; color:#2D2B2B">%s</span><br>'
            % Code.lucas_chess
        )
        head += '<span style="font-size:15pt;">%s</span><br>' % _X(_("version %1"), procesador.version)
        head += '<span style="font-size:10pt;color:2D2B2B">%s: %s</span>' % (
            _("Author"),
            '<a href="mailto:lukasmonk@gmail.com">Lucas Monge</a>',
        )
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">%s</a>' % (procesador.web, procesador.web)
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">Blog : Fresh news</a>' % (procesador.blog,)
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">Sources: github</a>' % (procesador.github,)
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">Wiki</a><br>' % (procesador.wiki,)
        head += (
            ' - %s <a style="font-size:10pt; color:2D2B2B" href="http://www.gnu.org/copyleft/gpl.html"> GPL</a>'
            % _("License")
        )

        lb_ico = Controles.LB(self).ponImagen(Iconos.pmAplicacion64())
        lb_titulo = Controles.LB(self, head)

        # Tabs
        tab = Controles.Tab()
        tab.ponFuente(f)

        ib = AboutBase.ThanksTo()

        sub_tab = None
        for k, titulo in ib.dic.items():
            txt = ib.texto(k)
            lb = Controles.LB(self, txt)
            lb.set_background("#F6F3EE")
            lb.ponFuente(f)
            if "-" in k:
                base, num = k.split("-")
                if num == "1":
                    sub_tab = Controles.Tab()
                    sub_tab.ponFuente(f)
                    sub_tab.set_position("S")
                    tab.addTab(sub_tab, _("Engines"))
                lm = ib.list_engines(num)
                titulo = lm[0][0].split(" ")[1] + " - " + lm[-1][0].split(" ")[1]
                sub_tab.addTab(lb, titulo)
            else:
                tab.addTab(lb, titulo)

        ly_v1 = Colocacion.H().control(lb_ico).espacio(15).control(lb_titulo).relleno()
        layout = Colocacion.V().otro(ly_v1).espacio(10).control(tab).margen(10)

        self.setLayout(layout)


# def gen_web_bootstrap():
#     """
#     <nav>
#   <div class="nav nav-tabs" id="nav-tab" role="tablist">
#     <a class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" href="#nav-home" role="tab" aria-controls="nav-home" aria-selected="true">Home</a>
#     <a class="nav-link" id="nav-profile-tab" data-bs-toggle="tab" href="#nav-profile" role="tab" aria-controls="nav-profile" aria-selected="false">Profile</a>
#     <a class="nav-link" id="nav-contact-tab" data-bs-toggle="tab" href="#nav-contact" role="tab" aria-controls="nav-contact" aria-selected="false">Contact</a>
#   </div>
# </nav>
# <div class="tab-content" id="nav-tabContent">
#   <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">...</div>
#   <div class="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">...</div>
#   <div class="tab-pane fade" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">...</div>
# </div>
#     """
#     ib = AboutBase.ThanksTo()
#
#     dic = ib.dic
#
#     with open(r"c:\lucaschess\_WEB_R\mysite\templates\Thanksto.html", "wt", encoding="utf-8") as q:
#
#         li = ['{% extends "base.html" %}',
#               '{% block contenido %}',
#               "<nav>",
#               '<div class="nav nav-tabs" id="nav-tab" role="tablist">'
#               ]
#         first = True
#         for clave, rotulo in dic.items():
#             if first:
#                 first = False
#                 active = " active"
#                 selected = "true"
#             else:
#                 active = ""
#                 selected = "false"
#
#             # engines
#             if "-" in clave:
#                 if not clave.endswith("-1"):
#                     continue
#                 clave = clave[:-2]
#                 rotulo = rotulo[:-2]
#             html = (
#                 '<a class="nav-link%s" id="nav-%s-tab" '
#                 'data-bs-toggle="tab" href="#nav-%s" role="tab" '
#                 'aria-controls="nav-%s" aria-selected="%s"><h5 class="mb-0 text-secondary">{{_("%s")}}</h5></a>' % (active, clave, clave, clave, selected, rotulo)
#             )
#             li.append(html)
#
#         li.extend(["</div>", "</nav>", "<br>"])
#
#         li.append('<div class="tab-content" id="nav-tabContent">')
#         first = True
#         for clave, rotulo in dic.items():
#             if first:
#                 first = False
#                 active = " show active"
#             else:
#                 active = ""
#
#             # engines
#             if "-" in clave:
#                 if not clave.endswith("-1"):
#                     continue
#                 clave = clave[:-2]
#                 li_eng_txt = []
#                 li_eng_txt.append('<table class="table table-bordered">')
#                 li_eng_txt.append('<tr>')
#                 li_eng_txt.append('<th>{{_("Engine")}}</th>')
#                 li_eng_txt.append('<th>OS</th>')
#                 li_eng_txt.append('<th>{{_("Author")}}</th>')
#                 li_eng_txt.append('<th>{{_("Web")}}</th>')
#                 li_eng_txt.append('</tr>')
#
#                 li_eng = Code.configuration.list_engines(si_externos=False)
#
#                 lix = []
#                 so = "Windows"
#                 for (name, autor, url) in li_eng:
#                     if name == "Maia-1100":
#                         name = "Maia-1100/1900"
#                     elif name.startswith("Maia"):
#                         continue
#                     if "-bmi2" in name:
#                         name = name.replace("-bmi2", "")
#                     if name.endswith("64"):
#                         name = name.replace("64", "")
#                     lix.append((name, autor, url, so))
#                 li_eng = lix
#                 with open(r".\OS\linux\OSEngines.py", "rt", encoding="utf-8") as flnx:
#                     for linea in flnx:
#                         linea = linea.strip()
#                         if linea.startswith("cm = mas(") or linea.startswith("mas("):
#                             lir = linea.split('"')
#                             x, alias, x, autor, x, version, x, url, x, nombre, x = lir
#                             if alias == "Maia-%d":
#                                 nombre = "Maia-1100/1900"
#                             if "{bmi2}" in nombre:
#                                 nombre = nombre.replace("{bmi2}", "")
#                             li_eng.append((nombre, autor, url, "Linux"))
#                 li_eng.sort(key=lambda xt: xt[0])
#
#                 for pos, (name, autor, url, so) in enumerate(li_eng, 1):
#                     li_eng_txt.append("<tr>")
#                     li_eng_txt.append("<td>%s</td>" % name)
#                     li_eng_txt.append("<td>%s</td>" % so)
#                     li_eng_txt.append("<td>%s</td>" % autor)
#                     li_eng_txt.append('<td><a href="%s">%s</a></td>' % (url, url))
#                     li_eng_txt.append("</tr>")
#                 li_eng_txt.append('</table>')
#                 txt = "\n".join(li_eng_txt)
#             else:
#                 txt = ib.texto(clave)
#                 if clave == "contributors":
#                     txt = txt.replace("<br>", "")
#
#             html = '<div class="tab-pane fade%s" id="nav-%s" role="tabpanel" aria-labelledby="nav-%s-tab">%s</div>' % (active, clave, clave, txt)
#             li.append(html)
#
#         li.append("</div>")
#         li.append("{% endblock contenido %}")
#
#         q.write("\n".join(li))
#


class WInfo(QtWidgets.QDialog):
    def __init__(self, wparent, titulo, head, txt, min_tam, pm_icon):
        super(WInfo, self).__init__(wparent)

        self.setWindowTitle(titulo)
        self.setWindowIcon(Iconos.Aplicacion64())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)

        f = Controles.TipoLetra(puntos=20)

        lb_ico = Controles.LB(self).ponImagen(pm_icon)
        lb_titulo = Controles.LB(self, head).align_center().ponFuente(f)
        lb_texto = Controles.LB(self, txt)
        lb_texto.setMinimumWidth(min_tam - 84)
        lb_texto.setWordWrap(True)
        lb_texto.setTextFormat(QtCore.Qt.RichText)
        bt_seguir = Controles.PB(self, _("Continue"), self.seguir).ponPlano(False)

        ly_v1 = Colocacion.V().control(lb_ico).relleno()
        ly_v2 = Colocacion.V().control(lb_titulo).control(lb_texto).espacio(10).control(bt_seguir)
        ly_h = Colocacion.H().otro(ly_v1).otro(ly_v2).margen(10)

        self.setLayout(ly_h)

    def seguir(self):
        self.close()


def info(parent, titulo, head, txt, min_tam, pm_icon):
    w = WInfo(parent, titulo, head, txt, min_tam, pm_icon)
    w.exec_()
