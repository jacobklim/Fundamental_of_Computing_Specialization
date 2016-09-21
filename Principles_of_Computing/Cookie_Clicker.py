"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
        Init method that initiates the variables
        """
        self._total_number_cookies = 0.0
        self._current_number_cookies = 0.0
        self._current_time_sec = 0.0
        self._current_cps = 1.0
        #history list is a list of tuples.
        #Each tuple contains: a time, an item that was bought at that time (or None), 
        #the cost of the item, and the total number of cookies produced by that time
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total Cookies: " + str(self._total_number_cookies) + "\n"\
        + "Current Cookies: " + str(self._current_number_cookies) + "\n"\
        + "Current Time: " + str(self._current_time_sec) + "\n"\
        + "Current CPS: " + str(self._current_cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_number_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time_sec
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies >= self.get_cookies():
            time = (cookies - self.get_cookies()) / self.get_cps()
            return math.ceil(time)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_time_sec += time
            self._current_number_cookies += time * self.get_cps()
            self._total_number_cookies += time * self.get_cps()
        else:
            pass
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self.get_cookies():
            self._current_number_cookies -= cost
            self._current_cps += additional_cps
            self._history_list.append((self.get_time(), item_name, cost, self._total_number_cookies))
        else:
            pass
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    cloned_build_info = build_info.clone()
    new_action = ClickerState()
    
    while new_action.get_time() <= duration:
        
        time_left = duration - new_action.get_time()
        item = strategy(new_action.get_cookies(), new_action.get_cps(), 
                        new_action.get_history(), time_left, cloned_build_info)
        
        if item == None:
            break
        
        time_must_elapse = new_action.time_until(cloned_build_info.get_cost(item))
        
        if time_must_elapse > time_left:
            break
        else:
            new_action.wait(time_must_elapse)
            new_action.buy_item(item, cloned_build_info.get_cost(item), cloned_build_info.get_cps(item))
            cloned_build_info.update_item(item)
            
    new_action.wait(time_left)    
        
    
    return new_action


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_list = build_info.build_items()
    item_cost_list = []
    
    for item in item_list:
        item_cost_list.append(build_info.get_cost(item))
    
    cheapest_price = min(item_cost_list)
    cheapest_item_index = item_cost_list.index(cheapest_price)
    cheapest_item = item_list[cheapest_item_index]
    if cheapest_price > cookies + cps * time_left:
        return None
    else:
        return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_list = build_info.build_items()
    print item_list
    
    item_cost_list = map(build_info.get_cost, item_list)
    print item_cost_list    
    affordable_price_list = []
    for price in item_cost_list:
        if cookies + cps*time_left >= price:
            affordable_price_list.append(price)
    if affordable_price_list == []:
        return None
    else:
        expensive_price = max(affordable_price_list)
        expensive_item_index = item_cost_list.index(expensive_price)
        most_expensive_item = item_list[expensive_item_index]
        return most_expensive_item
    
   
        

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_list = build_info.build_items()
    
    item_cost_list = map(build_info.get_cost, item_list)
    
    cost_item_dict = dict(zip(item_cost_list, item_list))
    
    item_cps_list = map(build_info.get_cps, item_list)
    
    choice_list = []
       
    for index in range(len(item_list)):
        choice_list.append(item_cps_list[index] / item_cost_list[index])
    
    choice_cost_dict = dict(zip(choice_list, item_cost_list))
    choice_list.sort(reverse= True)
    for index in choice_list:       
        if cookies + cps*time_left >= choice_cost_dict[index]:
            best_item = cost_item_dict[choice_cost_dict[index]]    
            return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
