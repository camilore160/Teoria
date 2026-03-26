from otree.api import *
from otree.api import widgets


class C(BaseConstants):
    NAME_IN_URL = 'juegos'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ENDOWMENT = cu(20000)
    STEP = 1000
    OFFER_CHOICES = list(range(0, int(ENDOWMENT) + 1, STEP))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    # =====================
    # ULTIMÁTUM
    # =====================

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

        p1, p2 = self.get_players()

        offer = self.offer or cu(0)

        if self.accepted:
            p1.payoff = C.ENDOWMENT - offer
            p2.payoff = offer
        else:
            p1.payoff = cu(0)
            p2.payoff = cu(0)


    # =====================
    # DICTADOR
    # =====================

    def set_payoffs_dictador(self):

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        oferta = p1.dictador_oferta or cu(0)

        p1.payoff = C.ENDOWMENT - oferta
        p2.payoff = oferta


    # =====================
    # ULTIMÁTUM CON INFO
    # =====================

    offer_info = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto ofreces al otro jugador?"
    )

    accepted_info = models.BooleanField(
        label="¿Aceptas la oferta?",
        choices=[[True, 'Aceptar'], [False, 'Rechazar']],
        widget=widgets.RadioSelect
    )

    def set_payoffs_info(self):

        p1, p2 = self.get_players()

        offer = self.offer_info or cu(0)

        if self.accepted_info:
            p1.payoff = C.ENDOWMENT - offer
            p2.payoff = offer
        else:
            p1.payoff = cu(0)
            p2.payoff = cu(0)


    # =====================
    # DICTADOR CON INFO
    # =====================

    def set_payoffs_dictador_info(self):

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        oferta = p1.dictador_oferta_info or cu(0)

        p1.payoff = C.ENDOWMENT - oferta
        p2.payoff = oferta


class Player(BasePlayer):

    # =====================
    # DATOS SOCIODEMOGRÁFICOS
    # =====================

    edad = models.IntegerField(
        label="¿Cuál es tu edad?",
        min=16,
        max=100
    )

    sexo = models.StringField(
        label="Sexo",
        choices=["Hombre", "Mujer"],
        widget=widgets.RadioSelect
    )

    condicion_laboral = models.StringField(
        label="¿Cuál es tu condición laboral?",
        choices=[
            "Estudiante",
            "Estudiante que trabaja"
        ],
        widget=widgets.RadioSelect
    )


    # =====================
    # DECISIONES DICTADOR
    # =====================

    dictador_oferta = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador?"
    )

    dictador_oferta_info = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador?"
    )


    # =====================
    # OPINIÓN DE JUSTICIA
    # =====================

    dic_fairness_p2 = models.StringField(
        choices=[
            ('justo', 'Justo'),
            ('injusto', 'Injusto')
        ],
        label="¿El reparto te pareció justo o injusto?",
        widget=widgets.RadioSelect
    )

    dic_info_fairness_p2 = models.StringField(
        choices=[
            ('justo', 'Justo'),
            ('injusto', 'Injusto')
        ],
        label="¿El reparto te pareció justo o injusto?",
        widget=widgets.RadioSelect
    )
