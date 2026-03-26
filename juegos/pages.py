from otree.api import *
from .models import C, Subsession, Group, Player


# =========================
# PANTALLA INICIAL
# =========================
class Intro(Page):
    pass


# =========================
# DATOS SOCIODEMOGRÁFICOS
# =========================
class Demographics(Page):

    form_model = 'player'
    form_fields = ['sexo', 'edad', 'condicion_laboral']


# =========================
# ULTIMÁTUM (ESTÁNDAR)
# =========================
class UltimatumOffer(Page):

    form_model = 'group'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForOffer(WaitPage):
    pass


class UltimatumResponse(Page):

    form_model = 'group'
    form_fields = ['accepted']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class UltimatumResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()


class UltimatumResults(Page):

    @staticmethod
    def vars_for_template(player: Player):

        g = player.group

        return dict(
            offer=g.offer or cu(0),
            accepted=g.accepted,
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# DICTADOR
# =========================
class Dictador(Page):

    form_model = 'player'
    form_fields = ['dictador_oferta']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class DictadorResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_dictador()


class DictadorResults(Page):

    @staticmethod
    def vars_for_template(player: Player):

        dictator = player.group.get_player_by_id(1)

        return dict(
            oferta=dictator.dictador_oferta or cu(0),
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# FAIRNESS DICTADOR
# =========================
class DictadorFairness(Page):

    form_model = 'player'
    form_fields = ['dic_fairness_p2']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):

        dictator = player.group.get_player_by_id(1)

        return dict(
            oferta=dictator.dictador_oferta or cu(0),
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# ULTIMÁTUM CON INFORMACIÓN
# =========================
class UltimatumInfoOffer(Page):

    form_model = 'group'
    form_fields = ['offer_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForOfferInfo(WaitPage):
    pass


class UltimatumInfoResponse(Page):

    form_model = 'group'
    form_fields = ['accepted_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):

        p1 = player.group.get_player_by_id(1)

        return dict(
            p1_edad=p1.edad,
            p1_sexo=p1.sexo,
            p1_condicion_laboral=p1.condicion_laboral,
            offer=player.group.offer_info or cu(0),
            endowment=C.ENDOWMENT,
        )


class UltimatumInfoResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_info()


class UltimatumInfoResults(Page):

    @staticmethod
    def vars_for_template(player: Player):

        g = player.group

        return dict(
            offer=g.offer_info or cu(0),
            accepted=g.accepted_info,
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# DICTADOR CON INFORMACIÓN
# =========================
class DictadorInfoDecision(Page):

    form_model = 'player'
    form_fields = ['dictador_oferta_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class DictadorInfoResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_dictador_info()


class DictadorInfoResults(Page):

    @staticmethod
    def vars_for_template(player: Player):

        dictator = player.group.get_player_by_id(1)

        return dict(
            oferta=dictator.dictador_oferta_info or cu(0),
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# FAIRNESS DICTADOR INFO
# =========================
class DictadorInfoFairness(Page):

    form_model = 'player'
    form_fields = ['dic_info_fairness_p2']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):

        dictator = player.group.get_player_by_id(1)

        return dict(
            oferta=dictator.dictador_oferta_info or cu(0),
            payoff=player.payoff or cu(0),
            endowment=C.ENDOWMENT,
        )


# =========================
# FINAL
# =========================
class Gracias(Page):
    pass


# =========================
# SECUENCIA
# =========================
page_sequence = [

    Intro,
    Demographics,

    UltimatumOffer,
    WaitForOffer,
    UltimatumResponse,
    UltimatumResultsWaitPage,
    UltimatumResults,

    Dictador,
    DictadorResultsWaitPage,
    DictadorResults,
    DictadorFairness,

    UltimatumInfoOffer,
    WaitForOfferInfo,
    UltimatumInfoResponse,
    UltimatumInfoResultsWaitPage,
    UltimatumInfoResults,

    DictadorInfoDecision,
    DictadorInfoResultsWaitPage,
    DictadorInfoResults,
    DictadorInfoFairness,

    Gracias,
]
