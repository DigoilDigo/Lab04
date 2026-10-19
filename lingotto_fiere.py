class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        return f"{self.codice}: {self.nome} {self.cognome}"

    def __repr__(self):
        return f"Espositore('{self.codice}', '{self.nome}', '{self.cognome}')"


class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def prezzo_finale(self):
        """Metodo base per il prezzo (Standard)"""
        return self.prezzo_base

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.prezzo_finale() < other.prezzo_finale()
        return NotImplemented

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice if self.espositore else 'N/D'}"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale():.2f}€ - {stato}"

    def __repr__(self):
        return f"Stand('{self.codice}', {self.superficie}, {self.padiglione}, {self.prezzo_base})"


class StandPreseElettriche(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def prezzo_finale(self):
        """Sovrascrive il prezzo applicando il sovrapprezzo per prese extra (+7% ciascuna)"""
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice if self.espositore else 'N/D'}"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        """Sovrascrive il prezzo applicando il sovrapprezzo fisso del 30%"""
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice if self.espositore else 'N/D'}"
        return f"{self.codice}: Premium ({self.posizione}) | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale():.2f}€ - {stato}"


class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self.stand = {}  # Dizionario per memorizzare gli stand
        self.espositori = {}  # Dizionario per memorizzare gli espositori


    def nome(self):
        return self._nome


    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati degli stand e degli espositori da un file CSV."""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                for riga in file:
                    riga = riga.strip()
                    if not riga:
                        continue

                    campi = [c.strip() for c in riga.split(',')]
                    codice = campi[0]

                    if codice.startswith('ST'):
                        superficie = float(campi[1])
                        padiglione = int(campi[2])
                        prezzo_base = float(campi[3])

                        if len(campi) == 4:
                            stand_obj = Stand(codice, superficie, padiglione, prezzo_base)
                        elif len(campi) == 5:
                            quinto_campo = campi[4]
                            try:
                                num_prese = int(quinto_campo)
                                stand_obj = StandPreseElettriche(codice, superficie, padiglione, prezzo_base, num_prese)
                            except ValueError:
                                stand_obj = StandPremium(codice, superficie, padiglione, prezzo_base, quinto_campo)
                        self.stand[codice] = stand_obj

                    elif codice.startswith('ES'):
                        nome_espositore = campi[1]
                        cognome_espositore = campi[2]
                        espositore_obj = Espositore(codice, nome_espositore, cognome_espositore)
                        self.espositori[codice] = espositore_obj

        except FileNotFoundError:
            raise FileNotFoundError(f"Il file {file_path} non è stato trovato.")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand:
            raise ValueError(f"Lo stand con codice {codice_stand} non esiste.")
        if codice_espositore not in self.espositori:
            raise ValueError(f"L'espositore con codice {codice_espositore} non esiste.")

        stand_obj = self.stand[codice_stand]
        espositore_obj = self.espositori[codice_espositore]

        if not stand_obj.disponibile:
            raise ValueError(f"Lo stand {codice_stand} risulta già occupato.")

        for s in self.stand.values():
            if s.espositore == espositore_obj:
                raise ValueError(f"L'espositore {codice_espositore} è già associato a un altro stand ({s.codice}).")

        stand_obj.disponibile = False
        stand_obj.espositore = espositore_obj

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando l'eventuale stand associato"""
        if not self.espositori:
            print("Nessun espositore registrato nel sistema.")
            return

        for espositore in self.espositori.values():
            stand_a = None
            for stand in self.stand.values():
                if stand.espositore == espositore:
                    stand_a = stand
                    break

            if stand_a:
                print(f"- {espositore} -> Stand: {stand_a.codice}")
            else:
                print(f"- {espositore} -> Nessuno stand assegnato")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista degli stand ordinata in base al prezzo finale"""
        return sorted(self.stand.values())