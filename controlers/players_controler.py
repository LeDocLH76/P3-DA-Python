
from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import ORDER_ALPHA
from views import views_input, views_menu, views_output, views_utility


def players_controler():
    """ Controler for the player submenu

    """
    from models.player import Player
    manager_player_obj = Db_manager_player()
    manager_tournament_obj = Db_manager_tournament()

    while True:
        action = views_menu.players_action_choice()
        # Create new player
        if action == 1:
            new_player(manager_player_obj)

        # Update a player in database
        if action == 2:
            views_utility.clear_screen()
            views_utility.crlf()
            views_output.players_list(ORDER_ALPHA)
            views_utility.crlf()
            player_to_update = views_input.player_choice()
            if player_to_update is False:
                continue
            response: Player | None = manager_player_obj.get_by_id(
                player_to_update)
            # player exist on db ?
            if response is not None:
                player_db_obj = response
                players_set = (
                    manager_tournament_obj.get_players_all_tournaments())
                # If player is in one tournament on db
                if player_to_update in players_set:
                    # Do NOT update
                    views_output.forbiden_delete()
                    views_input.wait_for_enter()
                    continue
                views_utility.crlf()
                views_output.print_player(player_db_obj)
                player_dict = views_input.new_player()
                new_player_obj = Player(
                    player_dict["name"],
                    player_dict["surname"],
                    player_dict["birth_date"],
                    player_dict["gender"],
                    player_dict["classification"])
                # Update player in database
                manager_player_obj.add_one(new_player_obj, player_to_update)
            else:
                # Not in database
                views_output.input_error()
                views_input.wait_for_enter()

        # Delete a player in database
        if action == 3:
            views_utility.clear_screen()
            views_utility.crlf()
            views_output.players_list(ORDER_ALPHA)
            views_utility.crlf()
            player_to_delete = views_input.player_choice()
            if player_to_delete is False:
                continue
            response: Player | None = manager_player_obj.get_by_id(
                player_to_delete)
            if response is not None:
                player_db_obj = response
                players_set = (
                    manager_tournament_obj.get_players_all_tournaments())
                # If player is in a tournament
                if player_to_delete in players_set:
                    # Do NOT delete
                    views_output.forbiden_delete()
                    views_input.wait_for_enter()
                    continue
                # Confirm ?
                views_utility.crlf()
                views_output.confirm_delete()
                views_output.print_player(player_db_obj)
                views_utility.crlf()
                response = views_input.y_or_n()
                if response is False:
                    continue
                else:
                    manager_player_obj = Db_manager_player()
                    manager_player_obj.delete_one(player_to_delete)
            else:
                # Not in database
                views_output.input_error()
                views_input.wait_for_enter()

        # Display player list
        if action == 4:
            display_player_list()
            views_input.wait_for_enter()

        # Change player classification
        if action == 5:
            display_player_list()
            player_to_update = views_input.player_choice()
            if player_to_update is False:
                continue
            response: Player | None = manager_player_obj.get_by_id(
                player_to_update)
            # player exist on db ?
            if response is not None:
                views_utility.crlf()
                views_output.print_player(response)
                views_utility.crlf()
                new_classification = views_input.new_classification()
                if not new_classification:
                    continue
                response.set_classification(new_classification)
            else:
                # Not in database
                views_output.input_error()
                views_input.wait_for_enter()

        # Exit
        if action == 6:
            break

# -------------------------------
# Functions used in this controler
# -------------------------------


def display_player_list() -> None:
    # Ask user for sort type and display list of players
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.player_sort_type()
    sort_choice = views_menu.sort_choice()
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.players_list(sort_choice)
    views_utility.crlf()


def new_player(manager_player_obj: Db_manager_player) -> None:
    # Get player's infos from the user and save them in in database
    from models.player import Player
    views_utility.clear_screen()
    views_utility.crlf()
    player_dict = views_input.new_player()
    player_obj = Player(
        player_dict["name"],
        player_dict["surname"],
        player_dict["birth_date"],
        player_dict["gender"],
        player_dict["classification"])
    response = manager_player_obj.add_one(player_obj)
    if response is not True:
        views_output.player_exist(response)
        views_utility.crlf()
        views_input.wait_for_enter()
