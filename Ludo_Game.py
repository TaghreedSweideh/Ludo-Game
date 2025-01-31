import random

BLUE = "\033[1;34m"
RED = "\033[1;31m"
YELLOW = "\033[1;93m"
GREEN = "\033[1;32m"
RESET = "\033[0m"
#كلاس توكن يقوم بتعريف حجر من خلال لونه،رقمه،موقعه،وحالته الحالية 
class Token:
    def __init__(self, color, token_id):
        self.color = color
        self.token_id = token_id
        self.position = None
        self.is_in_home = False
        self.is_finished = False
        self.current_area = "start"
        self.is_in_safe_zone = False
        self.is_in_wall = False
        self.can_kill = False
        self.can_be_killed = False

    def deepcopy(self):
        new_token = Token(self.color, self.token_id)
        new_token.position = self.position
        new_token.is_in_home = self.is_in_home
        new_token.is_finished = self.is_finished
        new_token.current_area = self.current_area
        new_token.is_in_safe_zone = self.is_in_safe_zone
        new_token.is_in_wall = self.is_in_wall
        new_token.can_kill = self.can_kill
        new_token.can_be_killed = self.can_be_killed
        return new_token

    def is_equal(self, other_token):
        return (
            self.color == other_token.color
            and self.position == other_token.position
            and self.current_area == other_token.current_area
            and self.is_in_safe_zone == other_token.is_in_safe_zone
            and self.is_in_wall == other_token.is_in_wall
            and self.can_kill == other_token.can_kill
            and self.can_be_killed == other_token.can_be_killed
        )
    def repr(self):
        return f"{self.color} Token {self.token_id}"
#كلاس لاعب يقوم بتعريف لاعب له الخصائص التالية الاسم ،اللون،نوع اللاعب هل هو انسان او كومبيوتر ومصفوفة للاحجار التي وصلت للنهاية والرقعة الحالية 
#تابع get_movable_tokens يقوم بالبحث عن الاحجار التي يمكن تحريكها للاعب معين ويقوم بارجاع مصفوفة احجار
class Player:
    def __init__(self, name, color,board, is_human=True):
        self.name = name  
        self.color = color
        self.is_human = is_human 
        self.board = board
        self.finished_tokens = []
        
    def get_movable_tokens(self, dice_value, board):
        movable_tokens = []
        
        if dice_value == 6:
            for token in self.board.start_areas[self.color]:
                if token.position is None: 
                    movable_tokens.append(token)

        for tokens_at_position in self.board.circular_path:
            for token in tokens_at_position: 
                if token and token.color == self.color:
                    next_position = (token.position + dice_value) % 52 
                    movable_tokens.append(token)

        for tokens_at_position in self.board.home_paths[self.color]:
            for token in tokens_at_position:  
                if token:
                    current_index = token.position
                    target_index = current_index + dice_value
                    if target_index < len(board.home_paths[self.color]): 
                        movable_tokens.append(token)

        return movable_tokens

    def add_finished_token(self, token):
        if token not in self.finished_tokens:
            self.finished_tokens.append(token)
            print(f"{token.repr()} added to {self.name}'s finished tokens!")

        
    def __str__(self):
        return f"Player {self.name} ({'Human' if self.is_human else 'Computer'})"
    
#كلاس يقوم بطباعة الرقعة وفيه جميع المصفوفات التي تعرف بنية اللعبة
class LudoBoard: 
    def __init__(self): 
        self.circular_path = [[] for _ in range(52)]  
        self.color_target_indices = {"Green": 50, "Yellow": 11, "Blue": 24, "Red": 37}
        self.starting_positions = {"Green": 0, "Yellow": 13, "Blue": 26, "Red": 39}         
        self.home_paths = { 
            "Red": [[] for _ in range(6)], 
            "Blue": [[] for _ in range(6)], 
            "Green": [[] for _ in range(6)], 
            "Yellow": [[] for _ in range(6)], 
        } 
        self.start_areas = {
        "Red": [Token("Red", i + 1) for i in range(4)],
        "Blue": [Token("Blue", i + 1) for i in range(4)],
        "Green": [Token("Green", i + 1) for i in range(4)],
        "Yellow": [Token("Yellow", i + 1) for i in range(4)],
        } 
        self.safe_zones = [0, 8, 13, 21, 26, 34, 39, 47] 
        self.path_to_grid = { 
            0: (8, 13),  1: (8, 12),  2: (8, 11),  3: (8, 10),  4: (8, 9), 
            5: (9, 8),   6: (10, 8),  7: (11, 8),  8: (12, 8),  9: (13, 8), 
            10: (14, 8), 11: (14, 7), 12: (14, 6), 13: (13, 6), 14: (12, 6), 
            15: (11, 6), 16: (10, 6), 17: (9, 6),  18: (8, 5),  19: (8, 4), 
            20: (8, 3),  21: (8, 2),  22: (8, 1),  23: (8, 0),  24: (7, 0), 
            25: (6, 0),  26: (6, 1),  27: (6, 2),  28: (6, 3),  29: (6, 4), 
            30: (6, 5),  31: (5, 6),  32: (4, 6),  33: (3, 6),  34: (2, 6), 
            35: (1, 6),  36: (0, 6),  37: (0, 7),  38: (0, 8),  39: (1, 8), 
            40: (2, 8),  41: (3, 8),  42: (4, 8),  43: (5, 8),  44: (6, 9), 
            45: (6, 10), 46: (6, 11), 47: (6, 12), 48: (6, 13), 49: (6, 14), 
            50: (7, 14), 51: (8, 14) 
        } 
        self.grid_to_path = {value: key for key, value in self.path_to_grid.items()} 
 
    def get_grid_coordinates(self, path_index): 
        return self.path_to_grid.get(path_index) 
 
    def get_path_index(self, row, col): 
        return self.grid_to_path.get((row, col)) 
          
    def print_visual_board(self):
        for i in range(15):
            for j in range(15):
                if 0 <= i <= 5 and 0 <= j <= 5:  #blue zone
                    blue_positions = {(2, 2): 0, (2, 3): 1, (3, 2): 2, (3, 3): 3}
                    if (i, j) in blue_positions:
                        index = blue_positions[(i, j)]
                        token = self.start_areas["Blue"][index] if index < len(self.start_areas["Blue"]) else None
                        print(f" {BLUE}{token.token_id if token else '*'}{RESET}", end='')
                    else:
                        print(f" {BLUE}*{RESET}", end='')

                elif 0 <= i <= 5 and 9 <= j <= 14:  #red zone
                    red_positions = {(2, 11): 0, (2, 12): 1, (3, 11): 2, (3, 12): 3}
                    if (i, j) in red_positions:
                        index = red_positions[(i, j)]
                        token = self.start_areas["Red"][index] if index < len(self.start_areas["Red"]) else None
                        print(f" {RED}{token.token_id if token else '*'}{RESET}", end='')
                    else:
                        print(f" {RED}*{RESET}", end='')

                elif 9 <= i <= 14 and 0 <= j <= 5:  #yellow zone
                    yellow_positions = {(11, 2): 0, (11, 3): 1, (12, 2): 2, (12, 3): 3}
                    if (i, j) in yellow_positions:
                        index = yellow_positions[(i, j)]
                        token = self.start_areas["Yellow"][index] if index < len(self.start_areas["Yellow"]) else None
                        print(f" {YELLOW}{token.token_id if token else '*'}{RESET}", end='')
                    else:
                        print(f" {YELLOW}*{RESET}", end='')

                elif 9 <= i <= 14 and 9 <= j <= 14:  #green zone
                    green_positions = {(11, 11): 0, (11, 12): 1, (12, 11): 2, (12, 12): 3}
                    if (i, j) in green_positions:
                        index = green_positions[(i, j)]
                        token = self.start_areas["Green"][index] if index < len(self.start_areas["Green"]) else None
                        print(f" {GREEN}{token.token_id if token else '*'}{RESET}", end='')
                    else:
                        print(f" {GREEN}*{RESET}", end='')

                elif 1 <= i <= 6 and j == 7:  #red home path
                    tokens = self.home_paths["Red"][i - 1]
                    if not tokens:
                        print(f" {RED}*{RESET}", end='')
                    elif len(tokens) == 1: 
                        print(f" {RED}{tokens[0].token_id}{RESET}", end='')
                    else: 
                        print(f" {RED}R{RESET}", end='')
                        

                elif 8 <= i <= 13 and j == 7:  #yellow home path
                    tokens = self.home_paths["Yellow"][i - 8]
                    if not tokens:
                        print(f" {YELLOW}*{RESET}", end='')
                    elif len(tokens) == 1:
                        print(f" {YELLOW}{tokens[0].token_id}{RESET}", end='')
                    else:
                        print(f" {YELLOW}Y{RESET}", end='')
                        
                        
                elif i == 7 and 1 <= j <= 6:  #blue home path
                    tokens = self.home_paths["Blue"][j - 1]
                    if not tokens:
                        print(f" {BLUE}*{RESET}", end='')
                    elif len(tokens) == 1:
                        print(f" {BLUE}{tokens[0].token_id}{RESET}", end='')
                    else:
                        print(f" {BLUE}B{RESET}", end='')


                elif i == 7 and 8 <= j <= 13:  #green home path
                    tokens = self.home_paths["Green"][j - 8]
                    if not tokens:
                        print(f" {GREEN}*{RESET}", end='')
                    elif len(tokens) == 1:
                        print(f" {GREEN}{tokens[0].token_id}{RESET}", end='')
                    else:
                        print(f" {GREEN}G{RESET}", end='')


                elif (i, j) == (7, 7):
                    print(" *", end='')
                else: 
                    path_index = self.get_path_index(i, j)

                    if path_index is not None:
                        tokens = self.circular_path[path_index]
                        if not tokens:
                            if path_index in self.safe_zones:
                                print(f" {RESET}S{RESET}", end='')
                            else:
                                print(" *", end='')
                        elif len(tokens) == 1: 
                            token = tokens[0]
                            color_code = {"Red": RED, "Blue": BLUE, "Green": GREEN, "Yellow": YELLOW}[token.color]
                            print(f" {color_code}{token.token_id}{RESET}", end='')
                        else: 
                            first_token = tokens[0]
                            color_code = {"Red": RED, "Blue": BLUE, "Green": GREEN, "Yellow": YELLOW}[first_token.color]
                            print(f" {color_code}M{RESET}", end='')
                    else:
                        print(" *", end='')

            print()

    
    
    def deepcopy(self):
        new_board = LudoBoard()
        new_board.circular_path = [
            [token.deepcopy() for token in cell] 
            for cell in self.circular_path
        ]
        for color in self.home_paths:
            new_board.home_paths[color] = [
                [token.deepcopy() for token in cell]
                for cell in self.home_paths[color]
            ]
        for color in self.start_areas:
            new_board.start_areas[color] = [
                token.deepcopy() for token in self.start_areas[color]
            ]
        new_board.safe_zones = self.safe_zones.copy()
        new_board.path_to_grid = self.path_to_grid.copy()
        new_board.grid_to_path = self.grid_to_path.copy()
        
        return new_board
    def is_safe(self, index):
        return index in self.safe_zones

    def equal(self, other):
        if not isinstance(other, LudoBoard):
            return False
        for idx, cell in enumerate(self.circular_path):
            other_cell = other.circular_path[idx]
            if len(cell) != len(other_cell):
                return False
            for token, other_token in zip(cell, other_cell):
                if not token.is_equal(other_token):
                    return False
        for color in self.home_paths:
            for idx, cell in enumerate(self.home_paths[color]):
                other_cell = other.home_paths[color][idx]
                if len(cell) != len(other_cell):
                    return False
                for token, other_token in zip(cell, other_cell):
                    if not token.is_equal(other_token):
                        return False
        for color in self.start_areas:
            if len(self.start_areas[color]) != len(other.start_areas[color]):
                return False
            for token, other_token in zip(self.start_areas[color], other.start_areas[color]):
                if not token.is_equal(other_token):
                    return False
        return (
            self.safe_zones == other.safe_zones
            and self.path_to_grid == other.path_to_grid
            and self.grid_to_path == other.grid_to_path
        )
    def update_token_state(self, token):
        token.is_in_safe_zone = token.position in self.safe_zones if token.position is not None else False
        if token.current_area == "circular":
            cell = self.circular_path[token.position]
            token.is_in_wall = len(cell) >= 2 and any(t.color == token.color for t in cell)
        token.can_be_killed = False
        if token.current_area == "circular" and not token.is_in_safe_zone and not token.is_in_wall:
            for idx, cell in enumerate(self.circular_path):
                for attacker in cell:
                    if attacker.color == token.color or attacker.current_area != "circular":
                        continue
                    attacker_start = self.starting_positions[attacker.color]
                    attacker_target = self.color_target_indices[attacker.color]
                    attacker_pos = attacker.position
                    if attacker_start <= attacker_target:
                        attacker_in_segment = attacker_start <= attacker_pos < attacker_target
                    else:
                        attacker_in_segment = attacker_pos >= attacker_start or attacker_pos < attacker_target

                    if attacker_in_segment and self._is_position_ahead(attacker_pos, token.position, attacker.color):
                        token.can_be_killed = True
                        break
                if token.can_be_killed:
                    break
        token.can_kill = False
        if token.current_area == "circular" and not token.is_in_safe_zone:
            color = token.color
            start_pos = self.starting_positions[color]
            target_pos = self.color_target_indices[color]
            current_pos = token.position
            if start_pos <= target_pos:
                in_segment = start_pos <= current_pos < target_pos
            else:
                in_segment = current_pos >= start_pos or current_pos < target_pos
            token.can_kill = in_segment

    def _is_position_ahead(self, attacker_pos, victim_pos, attacker_color):
        target = self.color_target_indices[attacker_color]
        start = self.starting_positions[attacker_color]
        if start <= target:
            return attacker_pos < victim_pos <= target
        else:
            return (attacker_pos < victim_pos) or (victim_pos <= target)  
 
#كلاس يقوم بادارة الحركة على الرقعة حسب موقعه في اي مصفوفة اذا كان بالطريق المشترك او الطريق الخاص به للوصول للنهاية        
# بالاضافة الى توابع لقتل الخصم وتحقيق الجدار وعدم القدرة على التحرك في حال وجود جدار 
class Movement:
    def __init__(self, board,players):
        self.board = board
        self.players = players
        
    def move_token_in_start_area(self, token):
        # print('in starting area')
        starting_positions = {"Green": 0, "Yellow": 13, "Blue": 26, "Red": 39}
        start_position = starting_positions[token.color]

        self.board.start_areas[token.color].remove(token)
        
        self.board.circular_path[start_position].append(token)
        token.position = start_position

        # print(f"{token.repr()} moved to position {token.position} on the circular path.")
        
        

    def move_token_in_home_path(self, token, dice_value):
        # print('in home path')
        one_token_reched_end=False
        if token in self.board.home_paths[token.color][token.position]:
            self.board.home_paths[token.color][token.position].remove(token)
            
        token.position += dice_value
        if token.position < len(self.board.home_paths[token.color]) - 1:
            self.board.home_paths[token.color][token.position].append(token)
            token.current_area = "home" 
            # print(f"{token.repr()} moved to position {token.position} on the home path.")
        else:
            one_token_reched_end=True
            token.current_area = "finished"           
            # print(f"{token.repr()} reached the end of the home path!")
            token.position = len(self.board.home_paths[token.color]) - 1
                
        return one_token_reched_end



    def move_token_in_path(self, token, dice_value):
        # print('in circular path')
        iskilled=False

        old_position = token.position
        new_position = (token.position + dice_value) % len(self.board.circular_path)
        if self.is_wall_on_path(old_position, new_position, token):
            # print("There is a wall in your way!")
            return 
        if token in self.board.circular_path[old_position]:
            self.board.circular_path[old_position].remove(token)
        color_target_indices = {"Green": 50, "Yellow": 11, "Blue": 24, "Red": 37}
        target_index = color_target_indices[token.color]
        if (old_position <= target_index <= new_position) or (
            new_position < old_position and (target_index > old_position or target_index <= new_position)
        ):
            remaining_dice_value = (new_position - target_index) % len(self.board.circular_path)
            if remaining_dice_value < 0:
                remaining_dice_value += len(self.board.circular_path)
            token.position = 0  
            token.is_in_home = True  
            self.board.home_paths[token.color][token.position].append(token)
            if remaining_dice_value > 0:
                self.move_token_in_home_path(token, remaining_dice_value-1)
        else:
            token.position = new_position
            self.board.circular_path[new_position].append(token)
            if not self.is_safe(new_position):
                iskilled=self.check_and_kill(new_position,token)
        # print(f"{token.repr()} moved to position {token.position} on the circular path.")
        
        return iskilled

    def is_safe(self, index):
        return index in self.board.safe_zones
    
    def is_wall(self, path_index ,token):
            cell = self.board.circular_path[path_index]
            if len(cell) >= 2:
                color_counts = {}
                for t in cell:
                    if t.color != token.color:
                        color_counts[t.color] = color_counts.get(t.color, 0) + 1
                        
                for count in color_counts.values():
                    if count >= 2:
                        return True
            return False

    
    def is_wall_on_path(self, old_position, new_position, token):
        positions_to_check = []
        
        color_target_indices = {"Green": 50, "Yellow": 11, "Blue": 24, "Red": 37}
        target_index = color_target_indices[token.color]
        
        
        if old_position < new_position:
            positions_to_check = range(old_position + 1, new_position)
        else:
            positions_to_check = list(range(old_position + 1, len(self.board.circular_path))) + list(range(0, new_position))
        for pos in positions_to_check:
            if (old_position <= target_index < new_position and pos > target_index) or (
                target_index < old_position and (pos > target_index and pos < old_position)
            ):
                break
            if self.is_wall(pos, token):
                return True  
        return False  
    
    def check_and_kill(self, path_index, moving_token):
        target_cell = self.board.circular_path[path_index]
        token_killed = False

        for token in target_cell[:]:
            if token.color != moving_token.color:
                token.position = None
                token.current_area = "start"
                token.is_in_home = False
                token.is_in_safe_zone = False
                token.is_in_wall = False
                token.can_kill = False
                token.can_be_killed = False
                target_cell.remove(token)
                self.board.start_areas[token.color].append(token)
                # print(f"{token.repr()} has been sent back to the starting area.")
                token_killed = True

        return token_killed


    def move_one_token(self, token, dice_value):
        if not token: 
            print("Error: Tried to move None token!")
            return {"killed": False, "finished": False}
        
        iskilled = False
        one_token_reched_end = False
        
        if token.is_in_home:
            one_token_reched_end = self.move_token_in_home_path(token, dice_value)
        elif token.position is None:
            self.move_token_in_start_area(token)
        else:
            iskilled = self.move_token_in_path(token, dice_value)
        
        return {
            "killed": iskilled,
            "finished": one_token_reched_end
        }
   


# كلاس يقوم بادارة حالة الرقعة واللعب وادارة الدور بين اللاعبين اذا كانو لاعبين او اربعة  
#بالاضافة الى توابع الربح ونهاية اللعبة وتابع لاستدعاء خوارزمية لعب الكومبيوتر
class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_player_index = 0 
        self.movement = Movement(self.board,self.players)
        self.dice_value = None 
        self.expectimax_agent = Expectimax(self.board, self.players, max_depth=4)


    def roll_dice(self):
        return random.randint(1, 6)
    
    def next_turn(self):
        if len(self.players) > 0: 
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    
    def game_over(self):
        return len(self.players) == 1

    def check_win(self, player):
        if len(player.finished_tokens) == 4:
            print(f"Player {player.color} has won and is removed from the game!")
            winning_player_index = self.current_player_index  
            self.players.remove(player)  
            if winning_player_index == len(self.players):  
                self.current_player_index = 0
            else:
                self.current_player_index = winning_player_index
            return True 
        return False 

    def play(self):
        self.board.print_visual_board()

        while True:
            current_player = self.players[self.current_player_index]
            # if self.check_win(current_player):
            #     print(f"{current_player.name} has won the game!")
            #     break
            if self.game_over():
                print("Game over!")
                break
            if current_player.is_human:
                print(f"_____Human's Turn ({current_player.color})_____")
                self.human_play()
            else:
                print(f"_____Computer's Turn ({current_player.color})_____")
                self.computer_play()
            self.board.print_visual_board()

            # if self.check_win(current_player):
            #     print(f"{current_player.name} has won the game!")
            #     break
            if self.game_over():
                print("Game over!")
                break            
    def perform_turn(self, player, is_human, counter_six=0):
        if counter_six >= 3:
            print("Maximum consecutive rolls of 6 reached. Turn ends.")
            return False
        if self.check_win(player):
            return False
        if is_human:
            input(f"Press enter to roll dice...")
        else:
            print(f"Rolling dice...")
        self.dice_value = self.roll_dice()
        print(f"Player {player.color}'s turn. Dice rolled: {self.dice_value}")
        # next_states = self.get_next_states(self.board, self.dice_value)
        # print(f"Possible next states: {len(next_states)}") 
        
        movable_tokens = player.get_movable_tokens(self.dice_value, self.board)
        if not movable_tokens:
            print(f"Player {player.color} has no valid moves.")
            return False
        
        if is_human:
            chosen_token = self.choose_token_human(movable_tokens)
        else:
            chosen_token = self.choose_token_computer(movable_tokens)

        # self.print_token_states() 
        got_extra_turn = False
        move_result = self.movement.move_one_token(chosen_token, self.dice_value)
        if move_result.get("finished"):
            print(f"Player {player.color}'s {chosen_token.token_id} has reached the end!")
            player.add_finished_token(chosen_token)
        got_extra_turn = (
                move_result["killed"] or 
                move_result["finished"]
            )
        if got_extra_turn:
            print(f"Player {player.color} gets an extra turn for their move!")
            self.board.print_visual_board()
            
        if self.dice_value == 6:
            print(f"{player.color} rolled a 6! Gets another turn.")
            self.board.print_visual_board()
            counter_six += 1
            got_extra_turn = True
        else:
            counter_six = 0    
        return got_extra_turn
            

    def human_play(self):
        counter_six = 0
        while True: 
            extra_turn = self.perform_turn(self.players[self.current_player_index], is_human=True, counter_six=counter_six)
            if not extra_turn:
                break
            counter_six += 1
        self.next_turn() 
        
    def computer_play(self):
        counter_six = 0
        while True:  
            extra_turn = self.perform_turn(self.players[self.current_player_index], is_human=False, counter_six=counter_six)
            if not extra_turn:
                break
            counter_six+=1
        self.next_turn()
        
        
    def choose_token_human(self, movable_tokens):
        print("Movable tokens:")
        for i, token in enumerate(movable_tokens):
            print(f"{i + 1}: Token {token.token_id}")
        while True:
            try:
                choice = int(input("Choose a token to move: ")) - 1
                if 0 <= choice < len(movable_tokens):
                    return movable_tokens[choice]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")


    def choose_token_computer(self, movable_tokens):
        if not movable_tokens:
            return None

        best_move = None
        max_value = float('-inf')

        for token in movable_tokens:
            if token.is_finished: 
                continue

            simulated_state = self.board.deepcopy()
            movement = Movement(simulated_state, self.players)
            def find_token():
                new_token = next((t for t in simulated_state.start_areas[token.color] 
                                if t.token_id == token.token_id), None)
                if new_token: return new_token
                for idx, cell in enumerate(simulated_state.circular_path):
                    new_token = next((t for t in cell 
                                    if t.color == token.color and t.token_id == token.token_id), None)
                    if new_token: return new_token
                for idx, cell in enumerate(simulated_state.home_paths[token.color]):
                    new_token = next((t for t in cell 
                                    if t.color == token.color and t.token_id == token.token_id), None)
                    if new_token: return new_token
                return None

            new_token = find_token() 
            if not new_token: 
                print(f"Token {token.token_id} not found in any area, skipping")
                continue
            movement.move_one_token(new_token, self.dice_value)
            eval_value = self.expectimax_agent.expectimax(
                simulated_state, 
                depth=2, 
                is_maximizing_player=False,
                dice_value=self.dice_value,
                players=self.players,
                current_player_index=self.current_player_index
            )
            
            if eval_value > max_value:
                max_value = eval_value
                best_move = token

        return best_move if best_move else movable_tokens[0] 

#كلاس للخوارزمية فيه تابع التقييم للحركات الممكنة القادمة حيث ترتب اولويتها كالتالي
#عدد الاحجار القادرة على القتل
#عدد الاحجار التي ستخرجت من منطقة البداية
#الجدران المكونة لنفس اللاعب
#الاحجار في المناطق الامنة
#الاحجار التي اقتربت من الهدف النهائي
#يوجد ايضا التابع الذي يرجع الحالات التالية

class Expectimax:
    def __init__(self, board, players, max_depth=5):
        self.board = board
        self.players = players
        self.MAX_DEPTH = max_depth 
    def heuristic_function(self, board, players, current_player_color):
        """Calculate heuristic value with new priority order."""
        heuristic_value = 0
        current_player = next((p for p in players if p.color == current_player_color), None)
        if not current_player:
            return 0
        for cell in board.circular_path:
            for token in cell:
                if token.color == current_player_color and token.can_kill:
                    heuristic_value += 200  
        tokens_in_start = len(board.start_areas[current_player_color])
        tokens_exited = 4 - tokens_in_start - len(current_player.finished_tokens)
        heuristic_value += tokens_exited * 150
        for cell in board.circular_path:
            same_color_tokens = [t for t in cell if t.color == current_player_color]
            if len(same_color_tokens) >= 2:
                heuristic_value += 100 * (len(same_color_tokens) - 1) 
        for idx, cell in enumerate(board.circular_path):
            if board.is_safe(idx):
                for token in cell:
                    if token.color == current_player_color:
                        heuristic_value += 80
        for cell in board.home_paths[current_player_color]:
            for token in cell:
                heuristic_value += 60
        heuristic_value += len(current_player.finished_tokens) * 40
        target_indices = {"Green": 50, "Yellow": 11, "Blue": 24, "Red": 37}
        target = target_indices[current_player_color]
        for idx, cell in enumerate(board.circular_path):
            for token in cell:
                if token.color == current_player_color and token.current_area == "circular":
                    distance = (target - idx) % 52
                    proximity = (52 - distance) / 52 * 20  
                    heuristic_value += proximity
      # print(f"Heuristic for {current_player_color}: {heuristic_value}")
        return heuristic_value

    def get_next_states(self, state, dice_value, players, current_player_index):
        current_player = players[current_player_index]
        movable_tokens = current_player.get_movable_tokens(dice_value, state)
        next_states = []

        for token in movable_tokens:
            if token.is_finished:  
                continue
            new_board = state.deepcopy()
            new_players = [Player(p.name, p.color, new_board, p.is_human) for p in players]
            movement = Movement(new_board, new_players)
            def find_token_in_all_areas():
                new_token = next((t for t in new_board.start_areas[token.color] 
                                if t.token_id == token.token_id), None)
                if new_token: return new_token
                for cell in new_board.circular_path:
                    new_token = next((t for t in cell 
                                    if t.color == token.color and t.token_id == token.token_id), None)
                    if new_token: return new_token
                for cell in new_board.home_paths[token.color]:
                    new_token = next((t for t in cell 
                                    if t.color == token.color and t.token_id == token.token_id), None)
                    if new_token: return new_token
                return None
                
            new_token = find_token_in_all_areas()
            
            if not new_token:
                # print(f"Token {token.token_id} not found in simulation, skipping")
                continue

            move_result = movement.move_one_token(new_token, dice_value)
            extra_turn = (
                dice_value == 6 or 
                move_result["killed"] or 
                move_result["finished"]
            )
            
            if not any(new_board.equal(existing) for existing in next_states):
                next_states.append((new_board, extra_turn))
                
        return next_states

    def expectimax(self, state, depth, is_maximizing_player, dice_value, players, current_player_index, counter_six=3):
        if depth == 0 or any(len(player.finished_tokens) == 4 for player in players):
            return self.heuristic_function(state, players, players[current_player_index].color)

        if is_maximizing_player:
            max_eval = float('-inf')
            next_states = self.get_next_states(state, dice_value, players, current_player_index)

            for new_state, extra_turn in next_states:
                if extra_turn and counter_six > 0: 
                    eval = self.expectimax(
                        new_state, depth, True, dice_value, players, current_player_index, counter_six - 1
                    )
                else:
                    eval = self.expectimax(
                        new_state, depth - 1, False, dice_value, players, (current_player_index + 1) % len(players)
                    )
                max_eval = max(max_eval, eval)

            return max_eval
        else:
            expected_value = 0
            for dice_roll in range(1, 7):
                prob = 1 / 6
                next_states = self.get_next_states(state, dice_roll, players, current_player_index)
                if next_states:
                    eval = sum(
                        self.expectimax(new_state, depth - 1, True, dice_roll, players, (current_player_index + 1) % len(players))
                        for new_state, _ in next_states
                    ) / len(next_states)
                else:
                    eval = self.heuristic_function(state, players, players[current_player_index].color)
                expected_value += prob * eval

            return expected_value
#تابع لتخيير المستخدم اذا كان يريد اللعب كلاعبين او 4 كومبيوترات 
def setup_game():
    board = LudoBoard()
    
    print("Choose Game Mode:")
    print("1: Human vs Computer")
    print("2: Four Computers")
    
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice == 1 or choice == 2:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    if choice == 1: 
        players = [
            Player(name="Human Player", color="Red", board=board, is_human=True),
            Player(name="Computer Player", color="Yellow", board=board, is_human=False)
        ]
    else:  
        players = [
            Player(name="Computer 1", color="Red", board=board, is_human=False),
            Player(name="Computer 2", color="Blue", board=board, is_human=False),
            Player(name="Computer 3", color="Green", board=board, is_human=False),
            Player(name="Computer 4", color="Yellow", board=board, is_human=False)
        ]
    
    return Game(board, players)

game = setup_game()
game.play()

