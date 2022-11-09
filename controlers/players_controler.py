from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import ORDER_ALPHA
from views import views_input, views_menu, views_output, views_utility


def players_controler():
    from models.player import Player
    while True:
        action = views_menu.players_action_choice()
        if action == 1:
            # Add a player in database
            manager_player_obj = Db_manager_player()
            views_utility.clear_screen()
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
            views_input.wait_for_enter()

        if action == 2:
            # Update a player in database
            views_output.players_list(ORDER_ALPHA)
            player_to_update = views_input.player_choice()
            if player_to_update is False:
                continue
            manager_player_obj = Db_manager_player()
            player_db = manager_player_obj.get_by_id(player_to_update)
            # player exist on db ?
            if player_db is not None:
                manager_tournament_obj = Db_manager_tournament()
                players_set = manager_tournament_obj.get_players_all()
                # If player is in a tournament
                if player_to_update in players_set:
                    # Do NOT update
                    views_output.forbiden_delete()
                    views_input.wait_for_enter()
                    continue
                views_utility.clear_screen()
                views_output.print_player(player_db)
                player_dict = views_input.new_player()
                player_obj = Player(
                    player_dict["name"],
                    player_dict["surname"],
                    player_dict["birth_date"],
                    player_dict["gender"],
                    player_dict["classification"])
                response = manager_player_obj.add_one(
                    player_obj, player_to_update)
                if response is not True:
                    views_output.player_exist(response)
                    views_input.wait_for_enter()
            else:
                # Not in database
                views_output.input_error()
            views_input.wait_for_enter()

        if action == 3:
            # Delete a player in database
            views_output.players_list(ORDER_ALPHA)
            player_to_delete = views_input.player_choice()
            if player_to_delete is False:
                continue
            manager_player_obj = Db_manager_player()
            player_db = manager_player_obj.get_by_id(player_to_delete)
            if player_db is not None:
                manager_tournament_obj = Db_manager_tournament()
                players_set = manager_tournament_obj.get_players_all()
                # If player is in a tournament
                if player_to_delete in players_set:
                    # Do NOT delete
                    views_output.forbiden_delete()
                    views_input.wait_for_enter()
                    continue
                # Confirm ?
                views_utility.clear_screen()
                views_output.confirm_delete()
                views_output.print_player(player_db)
                response = views_input.y_or_n()
                if response is False:
                    continue
                else:
                    manager_player_obj = Db_manager_player()
                    manager_player_obj.delete_one(player_db.doc_id)
            else:
                # Not in database
                views_output.input_error()
                views_input.wait_for_enter()

        if action == 4:
            # View players in database order is alpha (1)
            views_output.players_list(1)
            views_input.wait_for_enter()
        if action == 5:
            break
