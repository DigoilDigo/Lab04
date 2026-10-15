class LingottoFiere:
    def __init__(self, nome):
        self.nome=nome

    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica gli strumenti da un file CSV.
                Solleva FileNotFoundError se il file non esiste.
                """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                for riga in file:
                    riga = riga.strip()
                    if not riga:
                        continue  # Salta eventuali righe vuote

                    campi = riga.split(',')
                    if len(campi) == 5:
                        id, metri, padiglione, prezzo, prese = campi
                        # Crea l'oggetto Strumento e lo memorizza nel dizionario
                        nuovo_str = Strumento(id, metri, padiglione, prezzo, prese)
                        self.stand[id] = nuovo_str
        except FileNotFoundError:
            raise FileNotFoundError(f"Il file {file_path} non è stato trovato.")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # TODO

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO