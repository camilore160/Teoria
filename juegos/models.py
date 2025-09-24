from otree.api import *
from otree.api import widgets  # para usar RadioSelect

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
        if self.accepted:
            p1.payoff = C.ENDOWMENT - self.offer
            p2.payoff = self.offer
        else:
            p1.payoff = cu(0)
            p2.payoff = cu(0)

    # -------------------
    # DICTADOR (estándar)
    # -------------------
    def set_payoffs_dictador(self):
        p1, p2 = self.get_players()  # p1 es el dictador (id 1)
        p1.payoff = C.ENDOWMENT - p1.dictador_oferta
        p2.payoff = p1.dictador_oferta

    # ===============================
    # NUEVO: ULTIMÁTUM con información
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
        if self.accepted_info:
            p1.payoff = C.ENDOWMENT - self.offer_info
            p2.payoff = self.offer_info
        else:
            p1.payoff = cu(0)
            p2.payoff = cu(0)

    # ==================================
    # NUEVO: DICTADOR con información
    # ==================================
    def set_payoffs_dictador_info(self):
        p1, p2 = self.get_players()  # p1 es el dictador (id 1)
        p1.payoff = C.ENDOWMENT - p1.dictador_oferta_info
        p2.payoff = p1.dictador_oferta_info


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
        choices=["Hombre", "Mujer", "Otro", "Prefiero no decir"],
        widget=widgets.RadioSelect
    )
    # NUEVO: universidad
    universidad = models.StringField(
        label="¿Tu universidad es pública o privada?",
        choices=["Pública", "Privada", "No aplicable", "Prefiero no decir"],
        widget=widgets.RadioSelect
    )

    # Decisión del dictador (estándar)
    dictador_oferta = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador?"
    )

    # NUEVO: Dictador con información
    dictador_oferta_info = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador? (con información)"
    )