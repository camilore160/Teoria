


from otree.api import *
from .models import C, Subsession, Group, Player


# =========================
# PANTALLA INICIAL
# =========================
class Intro(Page):
    """Pantalla de bienvenida e instrucciones."""
    pass


# =========================
# DATOS SOCIODEMOGRÁFICOS
# =========================
class Demographics(Page):
    form_model = 'player'
    form_fields = ['estrato', 'edad', 'sexo', 'universidad']


# ===============
# ULTIMÁTUM (ESTÁNDAR)
# ===============
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
    def is_displayed(player: Player):
        return player.session.config.get('show_results', True)

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        return dict(
            offer=g.offer,
            accepted=g.accepted,
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# ===============
# DICTADOR (ESTÁNDAR)
# ===============
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
    def is_displayed(player: Player):
        # ⬇️ P2 la ve siempre; P1 solo si show_results=True
        return player.id_in_group == 2 or player.session.config.get('show_results', True)

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        dictator = g.get_player_by_id(1)
        oferta = dictator.dictador_oferta or cu(0)
        return dict(
            oferta=oferta,
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# =========================
# OPINIÓN DE JUSTICIA (DICTADOR estándar)  ⬅️ NUEVA
# =========================
class DictadorFairness(Page):
    form_model = 'player'
    form_fields = ['dic_fairness_p2']

    @staticmethod
    def is_displayed(player: Player):
        # Solo responde el Jugador 2
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        dictator = g.get_player_by_id(1)
        return dict(
            oferta=dictator.dictador_oferta or cu(0),
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# ==========================================================
# ULTIMÁTUM CON INFORMACIÓN (P2 ve datos de P1)
# ==========================================================
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
        g = player.group
        p1 = g.get_player_by_id(1)
        return dict(
            offer=g.offer_info,
            p1_estrato=p1.estrato,
            p1_edad=p1.edad,
            p1_sexo=p1.sexo,
            p1_universidad=getattr(p1, 'universidad', '—'),
            endowment=C.ENDOWMENT,
        )


class UltimatumInfoResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_info()


class UltimatumInfoResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config.get('show_results', True)

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        return dict(
            offer=g.offer_info,
            accepted=g.accepted_info,
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# ==========================================================
# DICTADOR CON INFORMACIÓN (P2 ve datos de P1)
# ==========================================================
class DictadorInfoDecision(Page):
    form_model = 'player'
    form_fields = ['dictador_oferta_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class DictadorInfoView(Page):
    """Muestra la info de P1 al Jugador 2 mientras P1 decide."""
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        p1 = g.get_player_by_id(1)
        return dict(
            p1_estrato=p1.estrato,
            p1_edad=p1.edad,
            p1_sexo=p1.sexo,
            p1_universidad=getattr(p1, 'universidad', '—'),
            endowment=C.ENDOWMENT,
        )


class DictadorInfoResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_dictador_info()


class DictadorInfoResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        # ⬇️ P2 la ve siempre; P1 solo si show_results=True
        return player.id_in_group == 2 or player.session.config.get('show_results', True)

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        dictator = g.get_player_by_id(1)
        return dict(
            oferta=dictator.dictador_oferta_info,
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# =========================
# OPINIÓN DE JUSTICIA (DICTADOR con información)  ⬅️ NUEVA
# =========================
class DictadorInfoFairness(Page):
    form_model = 'player'
    form_fields = ['dic_info_fairness_p2']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        dictator = g.get_player_by_id(1)
        return dict(
            oferta=dictator.dictador_oferta_info or cu(0),
            payoff=player.payoff,
            endowment=C.ENDOWMENT,
        )


# =========================
# PANTALLA FINAL
# =========================
class Gracias(Page):
    """Pantalla de cierre/agradecimiento."""
    pass


# =================
# SECUENCIA DE PÁGINAS
# =================
page_sequence = [
    Intro,
    Demographics,
    # Ultimátum (estándar)
    UltimatumOffer, WaitForOffer, UltimatumResponse, UltimatumResultsWaitPage, UltimatumResults,
    # Dictador (estándar)
    Dictador, DictadorResultsWaitPage, DictadorResults, DictadorFairness,   # ⬅️ nueva
    # Nuevos con información revelada
    UltimatumInfoOffer, WaitForOfferInfo, UltimatumInfoResponse, UltimatumInfoResultsWaitPage, UltimatumInfoResults,
    DictadorInfoDecision, DictadorInfoView, DictadorInfoResultsWaitPage, DictadorInfoResults, DictadorInfoFairness,  # ⬅️ nueva
    Gracias,
]

