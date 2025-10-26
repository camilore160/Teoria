


from otree.api import *
from otree.api import widgets  # para usar RadioSelect


class C(BaseConstants):
    NAME_IN_URL = 'juegos'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    # Dotación de 20 000 (en oTree, cu(...) crea Currency)
    ENDOWMENT = cu(20000)

    # Ofertas de 0 a 20 000 en saltos de 1 000
    STEP = 1000
    OFFER_CHOICES = list(range(0, int(ENDOWMENT) + 1, STEP))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # -------------------
    # ULTIMÁTUM (estándar)
    # -------------------
    offer = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto ofreces al otro jugador?"
    )
    accepted = models.BooleanField(
        label="¿Aceptas la oferta?",
        choices=[[True, 'Aceptar'], [False, 'Rechazar']],
        widget=widgets.RadioSelect
    )

    def set_payoffs(self):
        # p1 = proponente (id 1), p2 = receptor (id 2)
        p1, p2 = self.get_players()

        # Guardamos variables de export para este juego
        p1.ult_offer = self.offer
        p2.ult_offer = self.offer
        p1.ult_accepted = self.accepted
        p2.ult_accepted = self.accepted

        if self.accepted:
            p1.payoff_ult = C.ENDOWMENT - self.offer
            p2.payoff_ult = self.offer
            p1.ult_received_p2 = cu(0)
            p2.ult_received_p2 = self.offer
        else:
            p1.payoff_ult = cu(0)
            p2.payoff_ult = cu(0)
            p1.ult_received_p2 = cu(0)
            p2.ult_received_p2 = cu(0)

        # Para tus pantallas actuales (se sobreescribe más adelante)
        p1.payoff = p1.payoff_ult
        p2.payoff = p2.payoff_ult

    # -------------------
    # DICTADOR (estándar)
    # -------------------
    def set_payoffs_dictador(self):
        p1, p2 = self.get_players()  # p1 es el dictador (id 1)

        p1.payoff_dic = C.ENDOWMENT - p1.dictador_oferta
        p2.payoff_dic = p1.dictador_oferta

        p1.dic_received_p2 = cu(0)
        p2.dic_received_p2 = p1.dictador_oferta

        # Para tus pantallas actuales (se sobreescribe más adelante)
        p1.payoff = p1.payoff_dic
        p2.payoff = p2.payoff_dic

    # ===============================
    # ULTIMÁTUM con información
    # ===============================
    offer_info = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto ofreces al otro jugador? (con información)"
    )
    accepted_info = models.BooleanField(
        label="¿Aceptas la oferta? (con información)",
        choices=[[True, 'Aceptar'], [False, 'Rechazar']],
        widget=widgets.RadioSelect
    )

    def set_payoffs_info(self):
        p1, p2 = self.get_players()

        # Guardamos variables de export para este juego
        p1.ult_info_offer = self.offer_info
        p2.ult_info_offer = self.offer_info
        p1.ult_info_accepted = self.accepted_info
        p2.ult_info_accepted = self.accepted_info

        if self.accepted_info:
            p1.payoff_ult_info = C.ENDOWMENT - self.offer_info
            p2.payoff_ult_info = self.offer_info
            p1.ult_info_received_p2 = cu(0)
            p2.ult_info_received_p2 = self.offer_info
        else:
            p1.payoff_ult_info = cu(0)
            p2.payoff_ult_info = cu(0)
            p1.ult_info_received_p2 = cu(0)
            p2.ult_info_received_p2 = cu(0)

        # Para tus pantallas actuales (se sobreescribe más adelante)
        p1.payoff = p1.payoff_ult_info
        p2.payoff = p2.payoff_ult_info

    # ==================================
    # DICTADOR con información
    # ==================================
    def set_payoffs_dictador_info(self):
        p1, p2 = self.get_players()  # p1 es el dictador (id 1)

        p1.payoff_dic_info = C.ENDOWMENT - p1.dictador_oferta_info
        p2.payoff_dic_info = p1.dictador_oferta_info

        p1.dic_info_received_p2 = cu(0)
        p2.dic_info_received_p2 = p1.dictador_oferta_info

        # Al finalizar todos los juegos, dejamos payoff = suma de los 4.
        for pl in (p1, p2):
            pl.total_payoff = (
                (pl.payoff_ult or cu(0))
                + (pl.payoff_dic or cu(0))
                + (pl.payoff_ult_info or cu(0))
                + (pl.payoff_dic_info or cu(0))
            )
            pl.payoff = pl.total_payoff


class Player(BasePlayer):
    # Sociodemográficos
    estrato = models.IntegerField(
        label="¿Cuál es tu estrato socioeconómico?",
        choices=[1, 2, 3, 4, 5, 6],
        widget=widgets.RadioSelect
    )
    edad = models.IntegerField(
        label="¿Cuál es tu edad?",
        min=16, max=100
    )
    sexo = models.StringField(
        label="Sexo",
        choices=["Hombre", "Mujer"],
        widget=widgets.RadioSelect
    )
    universidad = models.StringField(
        label="¿Tu universidad es pública o privada?",
        choices=["Pública", "Privada"],
        widget=widgets.RadioSelect
    )

    # Decisión del dictador (estándar)
    dictador_oferta = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador?"
    )

    # Dictador con información
    dictador_oferta_info = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador? (con información)"
    )

    # ========= NUEVOS CAMPOS PARA EXPORTAR RESULTADOS =========
    # Ultimátum estándar
    ult_offer = models.CurrencyField()          # oferta propuesta por P1
    ult_accepted = models.BooleanField()        # 1/0 aceptada
    ult_received_p2 = models.CurrencyField()    # cuánto recibió P2
    payoff_ult = models.CurrencyField()         # payoff de este juego

    # Dictador estándar
    dic_received_p2 = models.CurrencyField()
    payoff_dic = models.CurrencyField()

    # Ultimátum con información
    ult_info_offer = models.CurrencyField()
    ult_info_accepted = models.BooleanField()
    ult_info_received_p2 = models.CurrencyField()
    payoff_ult_info = models.CurrencyField()

    # Dictador con información
    dic_info_received_p2 = models.CurrencyField()
    payoff_dic_info = models.CurrencyField()

    # Total final (suma de los 4 juegos)
    total_payoff = models.CurrencyField()

    # ===================== NUEVO: opinión de justicia (P2) =====================
    dic_fairness_p2 = models.StringField(
        choices=[('justo', 'Justo'), ('injusto', 'Injusto')],
        label="¿El reparto que recibiste te pareció justo o injusto?",
        widget=widgets.RadioSelect
    )

    dic_info_fairness_p2 = models.StringField(
        choices=[('justo', 'Justo'), ('injusto', 'Injusto')],
        label="(Con información) ¿El reparto te pareció justo o injusto?",
        widget=widgets.RadioSelect
    )