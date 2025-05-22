import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for i in [2015,2016,2017,2018]:
            self._view.ddyear.options.append(ft.dropdown.Option(i))

        for country in self._model.fillDD():
            self._view.ddcountry.options.append(
                ft.dropdown.Option(country))

    def read_retailer(self,e):
        self._country = e.control.data

    def handle_graph(self, e):
        self._model.buildGraph(self._view.ddyear.value,self._view.ddcountry.value)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {self._model._graph.number_of_nodes()} nodi e {self._model._graph.number_of_edges()} archi"))
        self._view.btn_volume.disabled=False
        self._view.update_page()


    def handle_volume(self, e):
        dict_vol = self._model.findVolumes()
        sorted_retailers = list(dict_vol.keys())
        for vol in sorted_retailers:
            if dict_vol[vol] != 0:
                self._view.txt_result.controls.append(ft.Text(f"{vol} ---> {dict_vol[vol]}"))
        self._view.txtN.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        if self._view.txtN.value == "" or self._view.txtN.value is None:
            self._view.create_alert(f"Inserire un valore per la lunghezza del percorso!!!")
            return

        try:
            int(self._view.txtN.value)
        except:
            self._view.create_alert(f"Inserire un valore numerico!!!")
            return

        if int(self._view.txtN.value) <= 2:
            self._view.create_alert(f"Inserire un valore maggiore di 2!!!")
            return
        self._model.getMaxWeight(int(self._view.txtN.value))