from drafter import *
from bakery import assert_equal
from dataclasses import dataclass

hide_debug_information()
set_website_title("Live Scoring Calculator")
set_site_information(author= "Jack Sarno",
                     description="Allows figure skating coachs to score practice programs live",
                     sources= "Gemini",
                     planning="",
                     links=["https://github.com/jack-sarno/live-scoring-calculator"]
                    )
set_website_framed(False)

NUMBERS = ["1", "2", "3", "4"]

@dataclass
class Element:
    num: str
    type: str
    name: str
    extra: list[str]
    goe: int
    extra2: list[str]
    
@dataclass
class State:
    elements: list[Element]
    str_elements: str
    element_num: int
    total_score: float
    tec: float
    pcs: float
    falls: int
    bonuses: float
    list_str: ""

def parse_single_jump(jump_str: str) -> dict:
    """Helper to parse a single jump within a combination or solo jump."""
    num = jump_str[0]
    extra = []
    
    # Check for second half bonus flag 'x' at the end
    if jump_str.endswith("x"):
        extra.append("x")
        jump_body = jump_str[1:-1]
    else:
        jump_body = jump_str[1:]
        
    name = jump_body
    return {"num": num, "name": name, "extra": extra}

def parse_jump_str(jump_str: str) -> Element:
    # Split combination jumps separated by '+'
    sub_jumps = jump_str.split("+")
    
    nums = []
    names = []
    extras = []
    
    for sub in sub_jumps:
        parsed = parse_single_jump(sub)
        nums.append(parsed["num"])
        names.append(parsed["name"])
        extras.extend(parsed["extra"])
        
    # Combine parsed jump elements
    combined_num = "+".join(nums) if len(nums) > 1 else nums[0]
    combined_name = "+".join(names) if len(names) > 1 else names[0]
    
    # Remove duplicate extra flags if any
    unique_extras = list(dict.fromkeys(extras))
    
    return Element(combined_num, "jump", combined_name, unique_extras, 0, [])

def parse_jump_str(jump_str: str) -> Element:
    # Split combination jumps separated by '+'
    sub_jumps = jump_str.split("+")
    
    nums = []
    names = []
    extras = []
    
    for sub in sub_jumps:
        parsed = parse_single_jump(sub)
        nums.append(parsed["num"])
        names.append(parsed["name"])
        extras.extend(parsed["extra"])
        
    # Combine parsed jump elements
    combined_num = "+".join(nums) if len(nums) > 1 else nums[0]
    combined_name = "+".join(names) if len(names) > 1 else names[0]
    
    # Remove duplicate extra flags if any
    unique_extras = list(dict.fromkeys(extras))
    
    return Element(combined_num, "jump", combined_name, unique_extras, 0, [])
    

def parse_element_str(element_str: str) -> list[Element]:
    element_list = []
    split_list = element_str.split(", ")
    for element in split_list:
        if element[0] in NUMBERS:
            parsed_jump = parse_jump_str(element)
            current_num = parsed_jump.num
            current_type = parsed_jump.type
            current_name = parsed_jump.name
            current_extra = parsed_jump.extra
        elif "Sp" in element:
            current_num = ""
            current_type = "spin"
            current_extra = []
            current_name = ""
            if element == "ChSp":
                current_name = "ChSp"
            else:
                if "F" in element:
                    current_name += "F"
                if any(tag in element for tag in ["CC", "CU", "CL", "CSS"]):
                    current_name += "C"
                if "CoSp" in element:
                    current_name += "CoSp"
                elif "USp" in element:
                    current_name += "USp"
                elif "LSp" in element:
                    current_name += "LSp"
                elif "SSp" in element:
                    current_name += "SSp"
                elif "CSp" in element:
                    current_name += "CSp"
        else:
            current_num = ""
            current_type = "step"
            current_extra = []
            current_name = ""
            if element in ["ChSq", "ChSt", "StSq"]:
                current_name = element
        element_list.append(Element(current_num, current_type, current_name, current_extra, 0, []))
    return element_list
                    
assert_equal(parse_element_str("2Lz, 4Fx"), [Element("2", "jump", "Lz", [], 0, []), Element("4", "jump", "F", ["x"], 0, [])])
assert_equal(parse_element_str("FCSp, CCoSp"), [Element("", "spin", "FCSp", [], 0, []), Element("", "spin", "CCoSp", [], 0, [])])
assert_equal(parse_element_str("3Lz+3T, 2A+1Eu+3S"), [Element("3+3", "jump", "Lz+T", [], 0, []), Element("2+1+3", "jump", "A+Eu+S", [], 0, [])])
assert_equal(parse_element_str("3F+2T+2Lox"), [Element("3+2+2", "jump", "F+T+Lo", ["x"], 0, [])])
assert_equal(parse_element_str("ChSq, 2Lo+2T, FCUSp"), [Element("", "step", "ChSq", [], 0, []), Element("2+2", "jump", "Lo+T", [], 0, []), Element("", "spin", "FCUSp", [], 0, [])])
   
@route
def index(state: State) -> Page:
    state.element_num = -1
    return Page(
        state,
        [
             Header("Live Scoring Calculator"),
             "Enter element list:", TextBox("element_list_str", state.str_elements), "\n",
             "or", Button("Enter Manually", "go_to_jumps"), "instead"
         ],
    )

@route
def go_to_jumps(state: State) -> Page:
    return Page(
        state,
        [
             Header("Jumps"), "\n",
             Button("Spins", "go_to_spins"), Button("Steps", "go_to_steps"), "\n",
             Button("2 Jump Combos", "go_to_2jump"), Button("3 Jump Combos", "go_to_3jump"), Button("4 Jump Combos", "go_to_4jump"), "\n",
             "Rotations:", SelectBox("rotations", ["0", "1", "2", "3", "4"], "0"),
             "Type:", SelectBox("name", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "Bonus:", SelectBox("bonus", ["No bonus", "x"], "No bonus"), "\n",
             Button("Add", "add_jump"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_spins(state: State) -> Page:
    return Page(
        state,
        [
             Header("Spins"), "\n",
             Button("Jumps", "go_to_jumps"), Button("Steps", "go_to_steps"), "\n",
             "Spin Type:", SelectBox("variation", ["CSp", "ChSp", "CoSp", "LSp", "SSp", "USp"], "CSp"), "\n",
             CheckBox("flying"), "Flying ", CheckBox("change"), "Change Foot", "\n",
             Button("Add", "add_spin"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_steps(state: State) -> Page:
    return Page(
        state,
        [
             Header("Steps"), "\n",
             Button("Jumps", "go_to_jumps"), Button("Spins", "go_to_spins"), "\n",
             "Step Type:", SelectBox("variation", ["StSq", "ChSq", "ChSt"], "StSq"), "\n",
             Button("Add", "add_step"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_2jump(state: State) -> Page:
    return Page(
        state,
        [
             Header("2 Jump Combos"), "\n",
             Button("Spins", "go_to_spins"), Button("Steps", "go_to_steps"), "\n",
             Button("Jumps", "go_to_jumps"), Button("3 Jump Combos", "go_to_3jump"), Button("4 Jump Combos", "go_to_4jump"), "\n",
             "1st Jump Rotations:", SelectBox("rotations1", ["0", "1", "2", "3", "4"], "0"),
             "1st Jump Type:", SelectBox("name1", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "2nd Jump Rotations:", SelectBox("rotations2", ["0", "1", "2", "3", "4"], "0"),
             "2nd Jump Type:", SelectBox("name2", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "Bonus:", SelectBox("bonus", ["No bonus", "x"], "No bonus"), "\n",
             Button("Add", "add_2jump"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_3jump(state: State) -> Page:
    return Page(
        state,
        [
             Header("2 Jump Combos"), "\n",
             Button("Spins", "go_to_spins"), Button("Steps", "go_to_steps"), "\n",
             Button("Jumps", "go_to_jumps"), Button("2 Jump Combos", "go_to_2jump"), Button("4 Jump Combos", "go_to_4jump"), "\n",
             "1st Jump Rotations:", SelectBox("rotations1", ["0", "1", "2", "3", "4"], "0"),
             "1st Jump Type:", SelectBox("name1", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "2nd Jump Rotations:", SelectBox("rotations2", ["0", "1", "2", "3", "4"], "1"),
             "2nd Jump Type:", SelectBox("name2", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "Eu"), "\n",
             "3rd Jump Rotations:", SelectBox("rotations3", ["0", "1", "2", "3", "4"], "0"),
             "3rd Jump Type:", SelectBox("name3", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "Bonus:", SelectBox("bonus", ["No bonus", "x"], "No bonus"), "\n",
             Button("Add", "add_3jump"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_4jump(state: State) -> Page:
    return Page(
        state,
        [
             Header("2 Jump Combos"), "\n",
             Button("Spins", "go_to_spins"), Button("Steps", "go_to_steps"), "\n",
             Button("Jumps", "go_to_jumps"), Button("2 Jump Combos", "go_to_2jump"), Button("3 Jump Combos", "go_to_3jump"), "\n",
             "1st Jump Rotations:", SelectBox("rotations1", ["0", "1", "2", "3", "4"], "0"),
             "1st Jump Type:", SelectBox("name1", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "2nd Jump Rotations:", SelectBox("rotations2", ["0", "1", "2", "3", "4"], "1"),
             "2nd Jump Type:", SelectBox("name2", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "Eu"), "\n",
             "3rd Jump Rotations:", SelectBox("rotations3", ["0", "1", "2", "3", "4"], "1"),
             "3rd Jump Type:", SelectBox("name3", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "Eu"),
             "4th Jump Rotations:", SelectBox("rotations4", ["0", "1", "2", "3", "4"], "0"),
             "4th Jump Type:", SelectBox("name4", ["S", "T", "Lo", "F", "Lz", "A", "Eu", "Wz"], "S"),
             "Bonus:", SelectBox("bonus", ["No bonus", "x"], "No bonus"), "\n",
             Button("Add", "add_4jump"), "\n",
             Button("Finish", "go_to_next_element"), "\n",
             "List of elements so far: " + state.list_str
         ],
    )

@route
def go_to_next_element(state: State) -> Page:
    state.element_num += 1
    if state.element_num >= len(state.elements):
        return final_page(state)
    if state.elements[state.element_num].type == "jump":
        return score_jump(state)
    if state.elements[state.element_num].type == "spin":
        return score_spin(state)
    if state.elements[state.element_num].type == "step":
        return score_spin(state)
    
@route
def score_jump(state: State) -> Page:
    return Page(
        state,
        [
             Header("Live Scoring"), "\n",
             "Element: ", state.list_str.split(", ")[state.element_num], "\n",
             " Element number: ", state.element_num + 1, "\n",
             "GOE:", SelectBox("goe", [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 0),
             "Edge:", SelectBox("edge", ["clean", "!", "e"], "clean"),
             "Rotation:", SelectBox("rotation", ["clean", "q", "<", "<<"], "clean"), "\n",
             CheckBox("rep"), "+REP ", CheckBox("bonus"), "b ", CheckBox("invalid"), "* ", CheckBox("fall"), "F", "\n",
             Button("Next", "jump_next_element")
         ],
    )

@route
def jump_next_element(state: State, goe: int, edge: str, rotation: str, rep: bool, bonus: bool, invalid: bool, fall: bool) -> Page:
    state.elements[state.element_num].goe = goe
    if edge != "clean":
        state.elements[state.element_num].extra2.append(edge)
    if rotation != "clean":
        state.elements[state.element_num].extra2.append(rotation)
    if rep:
        state.elements[state.element_num].extra2.append("+REP")
    if bonus:
        state.elements[state.element_num].extra2.append("b")
        state.bonuses += 1.0
    if invalid:
        state.elements[state.element_num].extra2.append("*")
    if fall:
        state.elements[state.element_num].extra2.append("F")
        state.falls += 1
    return go_to_next_element(state)

@route
def score_spin(state: State):
    return Page(
        state,
        [
             Header("Live Scoring"), "\n",
             "Element: ", state.list_str.split(", ")[state.element_num], "\n",
             " Element number: ", state.element_num + 1, "\n",
             "GOE:", SelectBox("goe", [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 0),
             "Level:", SelectBox("level", ["B", "1", "2", "3", "4"], "B"),
             CheckBox("missing_variation"), "V ", CheckBox("invalid"), "* ", CheckBox("fall"), "F", "\n",
             Button("Next", "spin_next_element")
         ],
    )

@route
def spin_next_element(state: State, goe: int, level: str, missing_variation: bool, invalid: bool, fall: bool) -> Page:
    state.elements[state.element_num].goe = goe
    state.elements[state.element_num].num = level
    if missing_variation:
        state.elements[state.element_num].extra2.append("V")
    if invalid:
        state.elements[state.element_num].extra2.append("*")
    if fall:
        state.elements[state.element_num].extra2.append("F")
        state.falls += 1
    return go_to_next_element(state)

@route
def score_step(state: State):
    return Page(
        state,
        [
             Header("Live Scoring"), "\n",
             "Element: ", state.list_str.split(", ")[state.element_num], "\n",
             " Element number: ", state.element_num + 1, "\n",
             "GOE:", SelectBox("goe", [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 0),
             "Level (if step sequence, otherwise leave as 1):", SelectBox("level", ["B", "1", "2", "3", "4"], "1"),
             CheckBox("bonus"), "b ", CheckBox("invalid"), "* ", CheckBox("fall"), "F", "\n",
             Button("Next", "step_next_element")
         ],
    )

@route
def step_next_element(state: State):
    state.elements[state.element_num].goe = goe
    state.elements[state.element_num].num = level
    if bonus:
        state.elements[state.element_num].extra2.append("b")
        state.bonuses += 0.5
    if invalid:
        state.elements[state.element_num].extra2.append("*")
    if fall:
        state.elements[state.element_num].extra2.append("F")
        state.falls += 1
    return go_to_next_element(state)

@route
def final_page(state):
    return Page(
        state,
        [
             Header("Final Score"), "\n",
         ],
    )

@route
def add_jump(state: State, rotations: str, name: str, bonus: str) -> Page:
    if bonus == "x":
        state.elements.append(Element(rotations, "jump", name, ["x"], 0, []))
        if not state.list_str:
            state.list_str += rotations + name + bonus
        else:
            state.list_str += ", " + rotations + name + bonus
    else:
        state.elements.append(Element(rotations, "jump", name, [], 0, []))
        if not state.list_str:
            state.list_str += rotations + name
        else:
            state.list_str += ", " + rotations + name
    return go_to_jumps(state)

@route
def add_2jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, bonus: str) -> Page:
    if bonus == "x":
        state.elements.append(Element(rotations1 + "+" + rotations2, "jump", name1 + "+" + name2, ["x"], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2 + bonus
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2 + bonus
    else:
        state.elements.append(Element(rotations1 + "+" + rotations2, "jump", name1 + "+" + name2, [], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2
    return go_to_jumps(state)

@route
def add_3jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, rotations3: str, name3: str, bonus: str) -> Page:
    if bonus == "x":
        state.elements.append(Element(rotations1+"+"+rotations2+"+"+rotations3, "jump", name1+"+"+name2+"+"+name3, ["x"], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3 + bonus
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3 + bonus
    else:
        state.elements.append(Element(rotations1+"+"+rotations2+"+"+rotations3, "jump", name1+"+"+name2+"+"+name3, [], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3
    return go_to_jumps(state)

@route
def add_4jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, rotations3: str, name3: str, rotations4: str, name4: str, bonus: str) -> Page:
    if bonus == "x":
        state.elements.append(Element(rotations1+"+"+rotations2+"+"+rotations3+"+"+rotations4, "jump", name1+"+"+name2+"+"+name3+"+"+name4, ["x"], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3 + "+" + rotations4 + name4 + bonus
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3+ "+" + rotations4 + name4 + bonus
    else:
        state.elements.append(Element(rotations1+"+"+rotations2+"+"+rotations3+"+"+rotations4, "jump", name1+"+"+name2+"+"+name3+"+"+name4, [], 0, []))
        if not state.list_str:
            state.list_str += rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3 + "+" + rotations4 + name4
        else:
            state.list_str += ", " + rotations1 + name1 + "+" + rotations2 + name2 + "+" + rotations3 + name3 + "+" + rotations4 + name4
    return go_to_jumps(state)

@route
def add_spin(state: State, variation: str, flying: bool, change: bool) -> Page:
    if flying:
        if change:
            state.elements.append(Element("", "spin", "FC" + variation, [], 0, []))
            if not state.list_str:
                state.list_str += "FC" + variation
            else:
                state.list_str += ", FC" + variation
        else:
            state.elements.append(Element("", "spin", "F" + variation, [], 0, []))
            if not state.list_str:
                state.list_str += "F" + variation
            else:
                state.list_str += ", F" + variation
    else:
        if change:
            state.elements.append(Element("", "spin", "C" + variation, [], 0, []))
            if not state.list_str:
                state.list_str += "C" + variation
            else:
                state.list_str += ", C" + variation
        else:
            state.elements.append(Element("", "spin", variation, [], 0, []))
            if not state.list_str:
                state.list_str += variation
            else:
                state.list_str += ", " + variation
    return go_to_jumps(state)
        
@route
def add_step(state: State, variation: str) -> Page:
        state.elements.append(Element("", "step", variation, [], 0, []))
        if not state.list_str:
            state.list_str += variation
        else:
            state.list_str += ", " + variation
        return go_to_jumps(state)

start_server(State([], "", 0, 0.0, 0.0, 0.0, 0, 0.0, ""))
