"""
End of Dayz
Assignment 2
Semester 1, 2021
CSSE1001/CSSE7030

A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List

from a2_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Hizam Alaklbi>, <46127679>"
__email__ = "<s4612767@student.uq.edu.au>"

TRACKING_OFFSETS = [(-1, 0), (0, 1), (0, -1), (1, 0)]

# Implement your classes here.
class Entity:
    """
    This class used to represent anything that can
    appear on the game’s grid.
    """
    
    def step(self, position: Position, game) -> None:
        """
        This method is called on every entity in the game grid after each move
        made by the player,it controls what actions an entity will perform during the step event.
        
        This method should do nothing.
        """
        pass

    def display(self) -> str:
        """ Return the character used to represent this entity in a text-based grid """
        raise NotImplementedError()

    def __repr__(self) -> str:
        """ Return a representation of this entity."""
        return "Entity()"


class Player(Entity):
    """
    A player is a subclass of the entity class that represents
    the player that the user controls on the game grid.
    
    It inherits from Entity.
    """
    
    def __repr__(self) -> str:
        """ Return a representation of this entity."""
        return "Player()"

    def display(self) -> str:
        """ Return the character used to represent this entity in a text-based grid "P" """
        return PLAYER


class Hospital(Entity):
    """
    This is a subclass of the entity class that represents the hospital in the grid.
    
    It inherits from Entity.
    """

    def __repr__(self) -> str:
        """ Return a representation of this entity."""
        return "Hospital()"

    def display(self) -> str:
        """ Return the character used to represent this entity in a text-based grid "H" """
        return HOSPITAL


class Grid:
    """
    This class is used to represent the 2D grid of entities.
    
    The grid can vary in size but it is always a square.
    
    Each (x, y) position in the grid can only contain one entity at a time.
    """
    
    def __init__(self, size: int):
        """
        A grid is constructed with a size that dictates
        the length and width of the grid.
        
        Initially a grid does not contain any entities.

        Parameters:
            size: The length and width of the grid.
        """
        self._grid_size = size
        self._entities = dict()

    def get_size(self):
        """ Returns the size of the grid """
        return self._grid_size

    def in_bounds(self, position: Position):
        """
        Return True if the given position is within the bounds of the grid.
        
        For a position to be within the bounds of the grid, both the x and y coordinates
        have to be greater than or equal to zero but less than the size of the grid.

        Parameters:
            position: An (x, y) position that we want to check is within the bounds of the grid.
        """
        return position.get_x() in range(0, self._grid_size) and \
               position.get_y() in range(0, self._grid_size)

    def add_entity(self, position: Position, entity: Entity):
        """
        Place a given entity at a given position of the grid.
        
        If there is already an entity at the given position,
        the given entity will replace the existing entity.
        
        If the given position is outside the bounds of the grid,
        the entity will not be added

        Parameters:
            position: An (x, y) position in the grid to place the entity.
            entity: The entity to place on the grid.
        """
        self._entities[position] = entity

    def get_entity(self, position: Position):
        """
        Return the entity that is at the given position in the grid.
        
        If there is no entity at the given position, returns None.
        If the given position is out of bounds, returns None.

        Parameters:
            position: The (x, y) position in the grid to check for an entity.
        """
        if position in self._entities:
            return self._entities[position]

        return None

    def get_mapping(self):
        """
        Return a dictionary with position instances as the keys and
        entity instances as the values.
        
        For every position in the grid that has an entity, the returned
        dictionary should contain an entry with the position instance
        mapped to the entity instance.
        
        """
        return self._entities.copy()

    def remove_entity(self, position: Position):
        """ Remove the entity, if any, at the given position.

        Parameters:
            position: An (x, y) position in the grid from which the entity is removed.
        """
        self._entities.pop(position)

    def get_entities(self):
        """ Return a list of all the entities in the grid. """
        tmp_list = []

        for pos in self._entities:
            tmp_list.append(self._entities[pos])

        return tmp_list

    def move_entity(self, start: Position, end: Position):
        """
        Move an entity from the given start position to the given end position.

        Parameters:
            start: The position the entity is in initially.
            end: The position to which the entity will be moved.
        """
        
        if 0 <= end.get_x() < self._grid_size and \
                0 <= end.get_y() < self._grid_size:
                entity = self.get_entity(start)
                if entity != None:
                    self.remove_entity(start)
                    self.add_entity(end,entity) 
                else :
                    return None
            
    def find_player(self):
        """
        Return the position of the player within the grid.
        
        Return None if there is no player in the grid. 
        """
        
        for k, v in self._entities.items():
            if v.display() == PLAYER:
                return k
        return None 

    def serialize(self):
        """ Serialize the grid into a dictionary that maps tuples to characters. """
        tmp: dict = dict()
        for item in self._entities.items():
            pos: Position = item[0]
            val: Entity = item[1]
            tmp[(pos.get_x(), pos.get_y())] = val.display()
        return tmp
        

class MapLoader:
    """
    This class is used to read a map file and create an appropriate
    grid instance which stores all the map file entities.

    It is an abstract class to allow for extensible map definitions.
    The BasicMapLoader class described below is a very simple implementation
    of the MapLoader which only handles the player and hospital entities.
    """
    def load(self, filename: str) -> Grid:
        """
        Load a new Grid instance from a map file.

        Parameters:
            filename: Path where the map file should be found.
        """
        serialised_map, size = load_map(filename)
        grid = Grid(size)
        for result in serialised_map:
            x,y = result
            pos = Position(x, y)
            entity = serialised_map[result]
            #create entity depending on what the value is
            val = self.create_entity(entity) 
            grid.add_entity(pos, val)
        return grid

    def create_entity(self, token: str):
        """
        Create and return a new instance of the Entity class
        based on the provided token.

        Parameters:
            token: Character representing the Entity subtype.
        """
        
        raise NotImplementedError()


class BasicMapLoader(MapLoader):
    """
    Inherits from MapLoader
    It is a subclass of MapLoader which can handle
    loading map files which include the entities [Player , Hospital]:  
    """
    def create_entity(self, token: str):
        """
        Create and return a new instance of the Entity class
        based on the provided token.

        Parameters:
            token: Character representing the Entity subtype.
        """
        
        if token == HOSPITAL:
            return Hospital()
        if token == PLAYER:
            return Player()
        else:
            raise ValueError(f"{token} not a valid Token")


class Game():
    """
    It handles some of the logic for controlling
    the actions of the player within the grid.
    It stores an instance of the Grid and
    keeps track of the player within the grid so that
    the player can be controlled.
    """
    def __init__(self, grid: Grid):
        """
        The construction of a Game instance takes
        the grid upon which the game is being played.

        Parameters:
            grid: The game’s grid.
            
        Preconditions:
             grid.find_player() is not None.
        """
        self._grid = grid
        self._step_count = 0
 
    def get_grid(self):
        """ Return the grid on which this game is being played. """
        return self._grid

    def get_player(self):
        """
        Return the instance of the Player class in the grid.
        If there is no player in the grid, return None.
        If there are multiple players in the grid, returning
        any player is sufficient.
        """
        position = self._grid.find_player()
        return self._grid.get_entity(position)

    def step(self):
        """
        This method of the game will be
        called after every action performed by the player.
        """
        self._step_count += 1
        mapping = self._grid.get_mapping()
        for position,entity in mapping.items():
            
            entity.step(position,self)

    def get_steps(self):
        """ Return the amount of steps made in the game. """ 
        return self._step_count

    def move_player(self, offset: Position):
        """
        Move the player entity in the grid by a given offset.

        Parameters :
            offset: A position to add to the player’s current position
                    to produce the player’s new desired position.
        """
        pos = self._grid.find_player()
        new_pos = pos.add(offset)
        self._grid.move_entity(pos, new_pos)
            
    def direction_to_offset(self, direction):
        """
        Convert a direction, as a string, to a offset position.

        Parameters:
            direction: Character representing the direction
                        in which the player should be moved.
        """
        if direction == UP:
            return Position(0, -1)
        elif direction == DOWN:
            return Position(0, 1)
        elif direction == LEFT:
            return Position(-1, 0)
        elif direction == RIGHT:
            return Position(1, 0)
            
    def has_won(self) -> bool:
        """ Return true if the player has won the game. """
        filter_lambda = lambda entity: entity.display() == HOSPITAL
        hospitals = list(filter(filter_lambda, self._grid.get_entities()))
        return len(hospitals) == 0

    def has_lost(self) -> bool:
        """ Return true if the player has lost the game."""
        return False
        return not self.has_won()


class TextInterface(GameInterface):
    """
    A text-based interface between the user and the game instance.
    """
    def __init__(self, size: int):
        """
        The text-interface is constructed knowing the size of the game to be
        played, this allows the draw method to correctly print the
        right sized grid.

        Parameters:
            size: The size of the game to be displayed and played.
        """
        self._grid_size = size
        
    def draw(self, game: Game) -> None:
        """
        The draw method will print out the given game surrounded by
        ‘#’ characters representing the border of the game.

        Parameters:
            game: An instance of the game class that is to be
                  displayed to the user by printing the grid.
        """
        print(BORDER * (self._grid_size + 2))
        for y in range(self._grid_size):
            print(BORDER, end="")
            for x in range(self._grid_size):
                entity = game._grid.get_entity(Position(x, y))
                if entity is None:
                    print(" ", end="")
                else:
                    print(entity.display(), end="")
            print(BORDER)

        print(BORDER * (self._grid_size + 2))

    def play(self, game: Game) -> None:
        """
        It implements the game loop, constantly
        prompting the user for their action, performing the
        action and printing the game until the game is over.

        Parameters
            game: The game to start playing.
        """
        while 1:
            self.draw(game)
            action = input(ACTION_PROMPT)
            self.handle_action(game, action)
            if game.has_won():
                print(WIN_MESSAGE)
                break
            elif game.has_lost():
                print(LOSE_MESSAGE)
                break

    def handle_action(self, game: Game, action: str):
        """
        This method is used to process the actions
        entered by the user during the game loop in the play method.

        Parameters:
            game: The game that is currently being played.
            action: An action entered by the player during the game loop.
        """
        pos = game.direction_to_offset(action)
        if pos != None :
            game.move_player(pos)
        game.step()
        
                
class VulnerablePlayer(Player):
    """
    This class is a subclass of the Player, this class
    extends the player by allowing them to become infected.
    """
    def __init__(self):
        """
        When an object of the VulnerablePlayer class is
        constructed, the player should not be infected.
        """
        super().__init__()
        self._is_infected = False

    def is_infected(self):
        """ Return the current infected state of the player """
        return self._is_infected

    def infect(self):
        """
        When the infect method is called, the player
        becomes infected and subsequent calls to is_infected return
        true.
        """
        self._is_infected = True


class Zombie(Entity):
    """
    This entity will wander the grid at random.
    The movement of a zombie is triggered by the player performing
    an action, i.e. the zombie moves during each step event.
    """        
    def step(self, position: Position, game) -> None:
        """
        This method for the zombie entity will move the
        zombie in a random direction.

        Parameters:
            position: The position of this zombie when the step event is triggered.
            game: The current game being played.
        """
        rand_dir = random_directions()
        for x, y in rand_dir:
            new_pos = position.add(Position(x, y))
            if game._grid.in_bounds(new_pos):                
                # get position by adding pos (direction) to position (current position)
                if game._grid.get_entity(new_pos) == None:
                    game._grid.move_entity(position,new_pos)
                    break
                elif game._grid.get_entity(new_pos).display() == PLAYER: 
                    game._grid.get_entity(new_pos).infect()
                    break

    def display(self) -> str:
        """ Return the character used to represent the zombie entity "Z". """
        return ZOMBIE
    
    def __repr__(self):
        """ Return a representation of this entity."""
        return "Zombie()"

    
class IntermediateGame(Game):
    """ An intermediate game extends some of the functionality of the basic game."""
    def __init__(self, grid: Grid):
        super().__init__(grid)

    def has_lost(self) -> bool:
        """
        Return true if the player has lost the game.
        The player loses the game if they become infected by a zombie
        """
        player = self.get_player()
        return player.is_infected()


class IntermediateMapLoader(BasicMapLoader):
    """
    This class extends BasicMapLoader to
    add support for new entities that are being added [VulnerablePlayer, Zombie].
    """
    def __init__(self):
        super(IntermediateMapLoader, self).__init__()

    def create_entity(self, token: str):
        """
        When a player token, ‘P’, is found, a VulnerablePlayer
        instance should be created instead of a Player.
        the IntermediateMapLoader should be able to load "Zombie" entity.
        """
        if token == PLAYER:
            return VulnerablePlayer()
        elif token == HOSPITAL:
            return Hospital()
        elif token == ZOMBIE:
            return Zombie()
        else:
            raise ValueError(f"{token} not a valid Token")


class TrackingZombie(Zombie):
    """
    The TrackingZombie is a more intelligent type of zombie
    which is able to see the player and move towards them.
    """
    def step(self, position: Position, game) -> None:
        """
        The step method for the tracking zombie will move the
        tracking zombie in the best possible direction to move closer to the player.

        Parameters:
            position: The position of this zombie when the step event is triggered.
            game: The current game being played.
        """
        min_move = None
        min_dist = None
        player_pos = game.get_grid().find_player()
        
        for x,y in TRACKING_OFFSETS:
            offset = Position(x, y)
            new_position = position.add(offset)
            if new_position == player_pos:
                game._grid.get_entity(new_position).infect()
                return
            # check if any entity is at new position
            #     if there is, then skip current loop
            current_entity = game.get_grid().get_entity(new_position)
            if current_entity is not None and current_entity.display() in PICKUP_ITEMS:
                continue
            if min_move is None:
                min_move = new_position
                min_dist = new_position.distance(player_pos)
                continue 
        # check whetehr distance between x, y and player pos less than saved min_dist
            elif new_position.distance(player_pos) < min_dist:
                min_move = new_position
                min_dist = new_position.distance(player_pos)
                break

        game.get_grid().move_entity(position,min_move)

    def display(self) -> str:
        """ Return the character used to represent this entity in a text-based grid "T" """
        return TRACKING_ZOMBIE

    
class Pickup(Entity):
    """
    A Pickup is a special type of entity that the player is able to pickup and hold
    in their inventory. The Pickup class is an abstract class.
    """
    
    def __init__(self):
        """
        When a Pickup entity is created, the lifetime of the entity
        should be equal to its maximum lifetime (durability).
        """
        super(Pickup, self).__init__()
        self._lifetime = self.get_durability() 
        
    def get_durability(self):
        """
        Return the maximum amount of steps the player is able
        to take while holding this item. After the player takes
        this many steps, the item disappears.
        """
        raise NotImplementedError

    def get_lifetime(self):
        """
        Return the remaining steps a player can take with this
        instance of the item before the item disappears from the
        player’s inventory.
        """
        return self._lifetime

    def hold(self):
        """
        The hold method is called on every pickup entity that
        the player is holding each time the player takes a
        step.
        """
        self._lifetime -= 1

    def __repr__(self):
        """ Return a representation of this entity."""
        return "Pickup()"


class Garlic(Pickup):
    """
    Garlic is an entity which the player can pickup.
    While the player is holding a garlic entity they cannot be infected by a zombie.
    If they collide with a zombie while holding a garlic, the zombie will perish.
    """
    def get_durability(self):
        """ Return the durability of a garlic. """
        return 10

    def display(self) -> str:
        """ Return the character used to represent the garlic entity in a text-based grid. "G" """
        return GARLIC

    def __repr__(self):
        """ Return a representation of this entity."""
        return f"Garlic({self._lifetime})"


class Crossbow(Pickup):
    """ Crossbow is an entity which the player can pickup. """
    def __init__(self):
        super(Crossbow, self).__init__()

    def get_durability(self):
        """ Return the durability of a crossbow. """
        return 5

    def display(self) -> str:
        """ Return the character used to represent the crossbow entity in a text-based grid. "C" """
        return CROSSBOW

    def __repr__(self):
        """ Return a representation of this entity."""
        return f"Crossbow({self._lifetime})"


class Inventory:
    """
    It holds a collection of entities
    which the player can pickup, i.e. Pickup subclasses.
    """
    def __init__(self):
        """ When an inventory is constructed, it should not contain any items. """
        self._items = []
         
        
    def step(self):
        """
        The step method will be called every
        time the player steps as a part of the player’s step method.

        When this method is called, the lifetime of every item stored
        within the inventory should decrease
        """
        for entity in self.get_items():
            entity.hold()
            if entity.get_lifetime() == 0:
                self._items.remove(entity)
                
                
    def add_item(self, entity):
        """
        This method should take a pickup entity and add it to the inventory.

        Parameters:
            item: The pickup entity to add to the inventory.
        """
        self._items.append(entity)

    def get_items(self):
        """ Return the pickup entity instances currently stored in the inventory. """
        return self._items.copy()

    def contains(self, pickup_id):
        """
        Return true if the inventory contains any entities
        which return the given pickup_id from the entity’s display
        method.
        """
        for item in self._items:
            if item.display() == pickup_id:
                return True

        return False


class HoldingPlayer(VulnerablePlayer):
    """
    This is a subclass of VulnerablePlayer
    that extends the existing functionality of the player.
    """
    def __init__(self):
        """ """
        super().__init__()
        self._inventory = Inventory()

    def get_inventory(self):
        """ Return the instance of the Inventory class that represents the player’s inventory. """
        return self._inventory

    def infect(self):
        """
        Extend the existing infect method so that the player
        is immune to becoming infected if they are holding
        garlic.
        """
        if self._inventory.contains(GARLIC) == False:
            super().infect()
           
    def step(self, position: Position, game) -> None:
        """
        This method for a holding player will
        notify its inventory that a step event has occurred.

        Parameters:
            position: The position of this entity when the step event is triggered.
            game: The current game being played.
        """
        self._inventory.step()


class AdvancedGame(IntermediateGame):
    """
    This class extends IntermediateGame to add support for the player
    picking up a Pickup item when they come into contact with it.
    """
    def __init__(self, grid: Grid):
        super().__init__(grid)

    def move_player(self, offset: Position):
        """
        Move the player entity in the grid by a given offset.

        Parameters:
            offset: A position to add to the player’s current position to
                    produce the player’s new desired position.
        """
        player_pos = self._grid.find_player()
        player = self.get_player()
        
        if player is not None and player_pos is not None:
            new_pos = player_pos.add(offset)
            in_pos = self._grid.get_entity(new_pos)
            if in_pos is not None:
        #if there is a Pickup item, it should be added to the player’s inventory and being removed.
                if in_pos.display() in PICKUP_ITEMS:
                    self._grid.remove_entity(new_pos)
                    if isinstance(player, HoldingPlayer):
                        entity = self._grid.get_entity(in_pos.display())
                        player._inventory.add_item(in_pos)

        for k in self._grid._entities:
            pos: Position = k
            val: Entity = self._grid._entities[pos]
            if val.display() == PLAYER:
                new_pos = pos.add(offset)
                self._grid.move_entity(pos, new_pos)
                break

    
class AdvancedMapLoader(IntermediateMapLoader):
    """
    This class extends IntermediateMapLoader to
    add support for new entities that are added in task 3 of the assignment.

    The AdvancedMapLoader should be able to load the following entities:
        • TrackingZombie
        • Garlic
        • Crossbow
    """
    def create_entity(self, token: str):
        """
        Create and return a new instance of the Entity class
        based on the provided token.

        Parameters:
            token: Character representing the Entity subtype.
        """
        if token == PLAYER:
            return HoldingPlayer()
        if token == CROSSBOW:
            return Crossbow()
        if token == GARLIC:
            return Garlic()
        if token == TRACKING_ZOMBIE:
            return TrackingZombie()
        else:
            return super().create_entity(token)
            
            raise ValueError(f"{token} not a valid Token")


class AdvancedTextInterface(TextInterface):
    """ A text-based interface between the user and the game instance. """
    def __init__(self, grid):
        """ """
        super().__init__(grid)
        
    def draw(self, game: Game) -> None:
        """
        This method should print out the given game
        surrounded by ‘#’ characters representing the border of the game.

        Parameters:
            game: An instance of the game class that is to be displayed to
                  the user by printing the grid.
        """
        super().draw(game)
        player = game.get_player()
        if isinstance(player, HoldingPlayer):
            if len(player._inventory.get_items()) != 0:
                print(HOLDING_MESSAGE)
                for i in player._inventory.get_items():
                    print(repr(i))

    def handle_action(self, game: Game, action: str):
        """
        The handle_action method for AdvancedTextInterface should
        extend the interface to be able to handle the fire
        action for a crossbow.

        Parameters:
            game: The game that is currently being played.
            action: An action entered by the player during the game loop.
        """
        if action == FIRE:
            player = game.get_player()
            if isinstance(player, HoldingPlayer):
                if player._inventory.contains(CROSSBOW):
                    direction = input(FIRE_PROMPT)
                    if direction not in [UP, LEFT, DOWN, RIGHT]:
                        print(INVALID_FIRING_MESSAGE)
                    else:
                        fire_offset = game.direction_to_offset(direction)
                        fire_pos = game._grid.find_player()

                        no_zombie = True
                        while game._grid.in_bounds(fire_pos):
                            fire_pos = fire_pos.add(fire_offset)
                            entity_in_pos = game._grid.get_entity(fire_pos)
                            if entity_in_pos is not None:
                                
                                if entity_in_pos.display() == HOSPITAL:
                                    break
                        # If the first entity in that direction is a zombie, remove the zombie.
                                if entity_in_pos.display() in ZOMBIES:
                                    game._grid.remove_entity(fire_pos)
                                    no_zombie = False
                                    break

                        if no_zombie:    
                            print(NO_ZOMBIE_MESSAGE)
                    
                else:
                    print(NO_WEAPON_MESSAGE)
           
        super().handle_action(game,action)
        
def main():
    """Entry point to gameplay."""
    mapLoader = AdvancedMapLoader()
    grid = mapLoader.load("maps/basic4.txt")
    game = AdvancedGame(grid)
    textInteface = AdvancedTextInterface(grid._grid_size)
    textInteface.draw(game)
    textInteface.play(game)



if __name__ == "__main__":
    main()
