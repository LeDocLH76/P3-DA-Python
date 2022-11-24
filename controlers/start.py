
from controlers.players_controler import players_controler
from controlers.tournament_ctrl import tournament_controler
from views import views_input, views_menu, views_output, views_utility
from models.db_manager_tournaments import Db_manager_tournament


def begin():
    """Controler for root menu"""
    manager_tournament_obj = Db_manager_tournament()
    # Chess tournament splash screen
    views_output.splash_screen()
    while True:
        # Main menu
        views_utility.clear_screen()
        views_utility.crlf()
        res_root_menu = views_menu.root_menu()
        # Display all tournaments on database
        if res_root_menu == 1:
            views_utility.clear_screen()
            views_utility.crlf()
            views_output.tournament_list()
            views_utility.crlf()
            views_input.wait_for_enter()

        # Display all players on database
        if res_root_menu == 2:
            views_utility.clear_screen()
            views_utility.crlf()
            sort_type = views_menu.sort_choice()
            views_utility.clear_screen()
            views_utility.crlf()
            views_output.players_list(sort_type)
            views_utility.crlf()
            views_input.wait_for_enter()

        # Display one tournament results
        if res_root_menu == 3:
            views_utility.clear_screen()
            views_utility.crlf()
            tournament_quantity = views_output.tournament_list()
            views_utility.crlf()
            tournament_id = views_input.tournament_choice(tournament_quantity)
            views_utility.clear_screen()
            views_utility.crlf()
            result_type = views_menu.result_type()
            if result_type == 3:
                tournament = manager_tournament_obj.get_one_from_db(
                    tournament_id)
                views_utility.clear_screen()
                views_utility.crlf()
                views_output.player_result(tournament)
            else:
                views_utility.clear_screen()
                views_utility.crlf()
                views_output.tournament_results(tournament_id, result_type)
            views_utility.crlf()
            views_input.wait_for_enter()

        # Diplay one tournament players
        if res_root_menu == 4:
            views_utility.clear_screen()
            views_utility.crlf()
            tournament_quantity = views_output.tournament_list()
            views_utility.crlf()
            tournament_id = views_input.tournament_choice(tournament_quantity)
            views_utility.clear_screen()
            views_utility.crlf()
            sort_type = views_menu.sort_choice()
            views_utility.clear_screen()
            views_utility.crlf()
            tournament = manager_tournament_obj.get_one_from_db(tournament_id)
            views_output.tournament_players(tournament, sort_type)
            views_utility.crlf()
            views_input.wait_for_enter()

        # Displayer player menu
        if res_root_menu == 5:
            players_controler()

        # Jump in a non closed tournament
        if res_root_menu == 6:
            tournament_controler(True)

        # Begin a new tournament
        if res_root_menu == 7:
            tournament_controler(False)

        # Exit
        if res_root_menu == 8:
            views_output.bye_screen()
            break
