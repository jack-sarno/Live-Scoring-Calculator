from drafter import *
from bakery import assert_equal
from dataclasses import dataclass

hide_debug_information()
set_website_title("Live Scoring Calculator")
'''
set_site_information(author= "Jack Sarno",
                     description="Allows figure skating coachs to score practice programs live",
                     sources= "Gemini", "ChatGPT"
                     planning="Planning.png",
                     links=["https://github.com/jack-sarno/live-scoring-calculator", "https://github.com/jack-sarno/Live-Scoring-Calculator/blob/main/Figure%20Skating%20Jump%20Scoring%20Update.pdf",
                     "https://github.com/jack-sarno/Live-Scoring-Calculator/blob/main/Figure%20Skating%20Scoring%20Program%20Implementation.pdf",
                     "https://github.com/jack-sarno/Live-Scoring-Calculator/blob/main/Find%20Program%20Bugs.pdf", "https://github.com/jack-sarno/Live-Scoring-Calculator/blob/main/Find%20Program%20Bugs.pdf, https://github.com/jack-sarno/Live-Scoring-Calculator/blob/main/Parsing%20Figure%20Skating%20Jump%20Combinations.pdf"]
                    )
'''
set_site_information(author= "Jack Sarno",
                     description="Allows figure skating coachs to score practice programs live",
                     sources= "Gemini", "ChatGPT"
                     planning="Planning.png",
                     links=["https://github.com/jack-sarno/live-scoring-calculator"])
set_website_framed(False)

from drafter import *
from bakery import assert_equal
from dataclasses import dataclass

@dataclass
class Element:
    '''
    Represents an element with its details
    
    Attributes:
        num (str): for jumps it represents revolutions and for spins and steps it represents level
        type (str): jump, spin, or step
        name (str): specific type of the element
        extra (list[str]): extra info about the element that you can get before the element is performed. Ex: "x"
        goe (int): from -5 to 5, it represents how well the element is performed
        extra2 (list[str]): extra info that you can only get after the element is performed. Ex: "V"
    '''
    num: str
    type: str
    name: str
    extra: list[str]
    goe: int
    extra2: list[str]
    
@dataclass
class State:
    '''
    Represents the state of the Live Scoring Calculator
    
    Attributes:
        elements (list[Element]): the list of all the elements in the program
        element_num (int): While iterating through elements, represents the current element being modified from the list
        tes (float): Technical score for the program
        pcs (float): Components score for the program
        falls (int): Amount of times the skater fell in the program
        deductions (float): Deductions that are applied at the very end to the final score
        bonuses (float): Keeps track of elements that recieve a bonuse (b)
        list_str (float): elements in str form that is readable by the user
    '''
    elements: list[Element]
    element_num: int
    tes: float
    pcs: float
    falls: int
    deductions: float
    bonuses: float
    list_str: str
    
@dataclass
class Multiplier:
    '''
    Keeps track of the pcs multipliers for that specific level
    
    Attributes:
        level (str): the level of that specific modifier
        composition_and_presentation (float): composition and presentation always have the same modifier
        skating(skills): the modifier for the skating skills score
    '''
    level: str
    composition_and_presentation: float
    skating_skills: float
    
@dataclass
class Jump_BV:
    '''
    Holds the base values for a specific jump type and all of its rotations
    
    Attributes:
        type (str): the type of jump. (There are 8 types: A, S, T, Lo, F, Lz, Wz, Eu)
        zero (float): Value if the takeoff is clear but the skater didn't jump. Will always be 0.00
        single (float): Single jump value
        double (float): Double jump value
        triple (float): Triple jump value
        quadruple (float): Quadruple jump value
    '''
    type: str
    zero: float
    single: float
    double: float
    triple: float
    quadruple: float
    
@dataclass
class Spin_BV:
    '''
    Holds the base values for a specific spin type and all of its possible levels
    
    Attributes:
        type (str): The specific code for that spin
        base (float): Level B value
        one (float): Level 1 value
        two (float): Level 2 value
        three (float): Level 3 value
        four (float): Level 4 value
    '''
    type: str
    base: float
    one: float
    two: float
    three: float
    four: float
    
NUMBERS = ["1", "2", "3", "4"]

PCS_MULTIPLIERS = [Multiplier("Championship Pre-Juvenile Freeskate", 0.96, 2.88), Multiplier("Championship Juvenile Freeskate", 1.25, 3.75),
                   Multiplier("Championship Intermediate Freeskate", 1.80, 3.60), Multiplier("Championship Novice Freeskate", 2.28, 3.04),
                   Multiplier("Championship Junior Women Freeskate", 2.67, 2.67), Multiplier("Championship Junior Men Freeskate", 3.33, 3.33),
                   Multiplier("Championship Senior Women Freeskate", 2.67, 2.67), Multiplier("Championship Senior Men Freeskate", 3.33, 3.33),
                   Multiplier("Championship Intermediate Short Program", 0.90, 1.80), Multiplier("Championship Novice Short Program", 1.14, 1.52),
                   Multiplier("Championship Junior Women Short Program", 1.33, 1.33), Multiplier("Championship Junior Men Short Program", 1.67, 1.67),
                   Multiplier("Championship Senior Women Short Program", 1.33, 1.33), Multiplier("Championship Senior Men Short Program", 1.67, 1.67),
                   Multiplier("Excel Pre-Preliminary Freeskate", 0.90, 2.70), Multiplier("Excel Preliminary Plus Freeskate", 0.92, 2.76),
                   Multiplier("Excel Pre-Juvenile Plus Freeskate", 0.96, 2.88), Multiplier("Excel Juvenile Freeskate", 1.25, 3.75),
                   Multiplier("Excel Juvenile Plus Freeskate", 1.25, 3.75), Multiplier("Excel Intermediate Freeskate", 1.80, 3.60),
                   Multiplier("Excel Intermediate Plus Freeskate", 1.80, 3.60), Multiplier("Excel Novice Freeskate", 2.28, 3.04),
                   Multiplier("Excel Junior Freeskate", 2.67, 2.67), Multiplier("Excel Senior Freeskate", 2.67, 2.67)]

JUMP_BVS = [Jump_BV("A", 0.00, 1.10, 3.30, 8.00, 12.50), Jump_BV("S", 0.00, 0.40, 1.30, 4.30, 9.70), Jump_BV("T", 0.00, 0.40, 1.30, 4.20, 9.50),
            Jump_BV("Lo", 0.00, 0.50, 1.70, 4.90, 10.50), Jump_BV("F", 0.00, 0.50, 1.80, 5.30, 11.00), Jump_BV("Lz", 0.00, 0.60, 2.10, 5.90, 11.50),
            Jump_BV("Wz", 0.30, 0.30, 0.30, 0.30, 0.30), Jump_BV("Eu", 0.00, 0.00, 0.00, 0.00, 0.00)]

SPIN_BVS = [Spin_BV("USp", 1.20, 1.40, 1.80, 2.30, 2.90), Spin_BV("FUSp", 1.80, 2.00, 2.40, 2.90, 3.50), Spin_BV("CUSp", 1.80, 2.00, 2.40, 2.90, 3.50),
            Spin_BV("FCUSp", 1.80, 2.00, 2.40, 2.90, 3.50), Spin_BV("LSp", 1.40, 1.80, 2.30, 2.90, 3.20), Spin_BV("FLSp", 2.00, 2.40, 2.90, 3.50, 3.80),
            Spin_BV("CLSp", 2.00, 2.40, 2.90, 3.50, 3.80), Spin_BV("FCLSp", 2.00, 2.40, 2.90, 3.50, 3.80), Spin_BV("CSp", 1.30, 1.70, 2.20, 2.80, 3.10),
            Spin_BV("FCSp", 1.90, 2.30, 2.80, 3.40, 3.80), Spin_BV("CCSp", 2.00, 2.40, 2.80, 3.40, 3.80), Spin_BV("FCCSp", 2.00, 2.40, 2.80, 3.40, 3.80),
            Spin_BV("SSp", 1.30, 1.60, 1.90, 2.50, 3.00), Spin_BV("FSSp", 2.00, 2.40, 2.80, 3.40, 3.80), Spin_BV("CSSp", 1.90, 2.30, 2.80, 3.10, 3.60),
            Spin_BV("FCSSp", 1.90, 2.30, 2.80, 3.10, 3.60), Spin_BV("CoSp", 1.80, 2.00, 2.40, 3.00, 3.60), Spin_BV("FCoSp", 1.80, 2.00, 2.40, 3.00, 3.60),
            Spin_BV("CCoSp", 2.00, 2.40, 3.00, 3.60, 4.20), Spin_BV("FCCoSp", 2.00, 2.40, 3.00, 3.60, 4.20), Spin_BV("ChSp", 3.50, 3.50, 3.50, 3.50, 3.50)]

def calculate_pcs(level: str, composition: float, presentation: float, skating_skills: float) -> float:
    '''
    Calculates the total Program Component Score (PCS) using
    the multipliers assigned to the selected skating level.

    Args:
        level (str): The skating level and program type used
            to determine the PCS multipliers.
        composition (float): The judge's Composition score.
        presentation (float): The judge's Presentation score.
        skating_skills (float): The judge's Skating Skills score.

    Returns:
        float: The total PCS, rounded to two decimal places.
    '''
    index = 0
    pcs_total = 0.0
    for i in range(len(PCS_MULTIPLIERS)):
        if PCS_MULTIPLIERS[i].level == level:
            index = i
    pcs_total += PCS_MULTIPLIERS[index].composition_and_presentation * composition
    pcs_total += PCS_MULTIPLIERS[index].composition_and_presentation * presentation
    pcs_total += PCS_MULTIPLIERS[index].skating_skills * skating_skills
    return round(pcs_total, 2)

assert_equal(calculate_pcs("Championship Pre-Juvenile Freeskate", 1, 2, 3), 11.52)
assert_equal(calculate_pcs("Championship Junior Women Freeskate", 5, 5, 5), 40.05)
assert_equal(calculate_pcs("Championship Junior Men Freeskate", 3, 4, 5), 39.96)
assert_equal(calculate_pcs("Championship Juvenile Freeskate", 0, 0, 0), 0.00)
assert_equal(calculate_pcs("Excel Pre-Preliminary Freeskate", 2, 2, 2), 9.00)

def parse_single_jump(jump_str: str) -> dict:
    '''
    Parses an individual jump string and separates its
    rotation count, jump type, bonus, and rotation call.

    Args:
        jump_str (str): A string representing one jump,
            including its rotation count and any modifiers.

    Returns:
        dict: A dictionary containing the jump's rotation
            count, name, extra modifiers, and rotation call.
    '''
    num = jump_str[0]
    extra = []
    rotation_call = "clean"

    # Strip trailing second-half bonus 'x'
    if jump_str.endswith("x"):
        extra.append("x")
        jump_body = jump_str[1:-1]
    else:
        jump_body = jump_str[1:]

    # Check for per-jump rotation calls at the end of the jump
    if jump_body.endswith("<<"):
        rotation_call = "<<"
        jump_body = jump_body[:-2]
    elif jump_body.endswith("<"):
        rotation_call = "<"
        jump_body = jump_body[:-1]
    elif jump_body.endswith("q"):
        rotation_call = "q"
        jump_body = jump_body[:-1]

    return {"num": num, "name": jump_body, "extra": extra, "rotation": rotation_call}

assert_equal(parse_single_jump("3Lz"), {"num": "3", "name": "Lz", "extra": [], "rotation": "clean"})
assert_equal(parse_single_jump("2A"), {"num": "2", "name": "A", "extra": [], "rotation": "clean"})
assert_equal(parse_single_jump("4Fx"), {"num": "4", "name": "F", "extra": ["x"], "rotation": "clean"})
assert_equal(parse_single_jump("3Lz<"), {"num": "3", "name": "Lz", "extra": [], "rotation": "<"})
assert_equal(parse_single_jump("3A<<"), {"num": "3", "name": "A", "extra": [], "rotation": "<<"})
assert_equal(parse_single_jump("2Loq"), {"num": "2", "name": "Lo", "extra": [], "rotation": "q"})
assert_equal(parse_single_jump("3Tx"), {"num": "3", "name": "T", "extra": ["x"], "rotation": "clean"})

def parse_jump_str(jump_str: str) -> Element:
    '''
    Parses a single jump or jump combination and separates
    its rotations, jump types, bonuses, and rotation calls.

    Args:
        jump_str (str): A string representing a jump or
            combination of jumps separated by plus signs.

    Returns:
        Element: An Element object containing the combined
            rotations, jump types, modifiers, and rotation calls.
    '''
    sub_jumps = jump_str.split("+")

    nums = []
    names = []
    extras = []
    rotations = []

    for sub in sub_jumps:
        parsed = parse_single_jump(sub)
        nums.append(parsed["num"])
        names.append(parsed["name"])
        extras.extend(parsed["extra"])
        rotations.append(parsed["rotation"])

    combined_num = "+".join(nums) if len(nums) > 1 else nums[0]
    combined_name = "+".join(names) if len(names) > 1 else names[0]
    unique_extras = list(dict.fromkeys(extras))

    # Store per-jump rotation calls in extra2
    return Element(combined_num, "jump", combined_name, unique_extras, 0, rotations)

assert_equal(parse_jump_str("3Lz"), Element("3", "jump", "Lz", [], 0, ["clean"]))
assert_equal(parse_jump_str("4Fx"), Element("4", "jump", "F", ["x"], 0, ["clean"]))
assert_equal(parse_jump_str("3Lz+3T"), Element("3+3", "jump", "Lz+T", [], 0, ["clean", "clean"]))
assert_equal(parse_jump_str("2A+1Eu+3S"), Element("2+1+3", "jump", "A+Eu+S", [], 0, ["clean", "clean", "clean"]))
assert_equal(parse_jump_str("3Lz<+2T<<"), Element("3+2", "jump", "Lz+T", [], 0, ["<", "<<"]))
assert_equal(parse_jump_str("3Fx+2Tx"), Element("3+2", "jump", "F+T", ["x"], 0, ["clean", "clean"]))

def parse_element_str(element_str: str) -> list[Element]:
    '''
    Parses a complete planned program element string and identifies
    each element as a jump, spin, or step sequence.

    Args:
        element_str (str): A string containing the program's
            elements separated by commas and spaces.

    Returns:
        list[Element]: A list of Element objects containing
            the parsed information for every program element.
    '''
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

def get_single_jump_bv(rotations: str, jump_type: str) -> float:
    '''
    Looks up the base value of an individual jump using
    its rotation count and jump type.

    Args:
        rotations (str): The number of rotations completed
            by the jump, represented as a string.
        jump_type (str): The type of jump, such as S, T,
            Lo, F, Lz, A, Wz, or Eu.

    Returns:
        float: The base value assigned to the specified jump.
            Returns 0.0 if the jump type or rotation count
            does not match an available base value.
    '''
    for bv in JUMP_BVS:
        if bv.type == jump_type:
            if rotations == "0":
                return bv.zero
            elif rotations == "1":
                return bv.single
            elif rotations == "2":
                return bv.double
            elif rotations == "3":
                return bv.triple
            elif rotations == "4":
                return bv.quadruple
    return 0.0

assert_equal(get_single_jump_bv("0", "A"), 0.00)
assert_equal(get_single_jump_bv("1", "A"), 1.10)
assert_equal(get_single_jump_bv("2", "A"), 3.30)
assert_equal(get_single_jump_bv("3", "A"), 8.00)
assert_equal(get_single_jump_bv("4", "A"), 12.50)

assert_equal(get_single_jump_bv("1", "S"), 0.40)
assert_equal(get_single_jump_bv("2", "T"), 1.30)
assert_equal(get_single_jump_bv("3", "Lo"), 4.90)
assert_equal(get_single_jump_bv("3", "F"), 5.30)
assert_equal(get_single_jump_bv("3", "Lz"), 5.90)
assert_equal(get_single_jump_bv("3", "Wz"), 0.30)
assert_equal(get_single_jump_bv("3", "Eu"), 0.00)

assert_equal(get_single_jump_bv("5", "A"), 0.00)
assert_equal(get_single_jump_bv("3", "Invalid"), 0.00)

def downgrade_rotation(rot: str) -> str:
    '''
    Reduces a jump's rotation count by one when the jump
    receives a downgrade call.

    Args:
        rot (str): The original number of rotations completed
            by the jump, represented as a string.

    Returns:
        str: The downgraded rotation count, represented
            as a string.
    '''
    if rot == "4":
        return "3"
    elif rot == "3":
        return "2"
    elif rot == "2":
        return "1"
    else:
        return "0"

assert_equal(downgrade_rotation("4"), "3")
assert_equal(downgrade_rotation("3"), "2")
assert_equal(downgrade_rotation("2"), "1")
assert_equal(downgrade_rotation("1"), "0")
assert_equal(downgrade_rotation("0"), "0")

def score_jump_element(element: Element) -> float:
    '''
    Calculates the total score of a jump or jump combination
    by applying base values, rotation calls, modifiers, and GOE.

    Args:
        element (Element): The jump element containing its
            rotations, jump types, modifiers, GOE, and
            additional rotation information.

    Returns:
        float: The total jump score, including applicable
            base values, deductions, bonuses, and GOE,
            rounded to two decimal places.
    '''
    if "*" in element.extra2:
        return 0.00

    rotations_list = element.num.split("+")
    names_list = element.name.split("+")
    num_jumps = len(rotations_list)

    # Extract the per-jump rotation calls (defaulting to "clean" if missing)
    jump_rot_calls = element.extra2[:num_jumps]
    while len(jump_rot_calls) < num_jumps:
        jump_rot_calls.append("clean")

    # Element-level flags ("e", "!", "+REP", "b", "F") stored after rotation calls
    flags = element.extra2[num_jumps:]

    total_bv = 0.0
    highest_single_bv = 0.0

    for i, (rot, name, rot_call) in enumerate(zip(rotations_list, names_list, jump_rot_calls)):
        if rot_call == "<<":
            rot = downgrade_rotation(rot)

        bv = get_single_jump_bv(rot, name)

        # Under-rotated ('<') reduces the individual jump's BV to 80%
        if rot_call == "<":
            bv *= 0.8

        # Wrong edge ('e') applies to the takeoff (first) jump, reducing its BV to 80%
        if i == 0 and "e" in flags:
            bv *= 0.8

        total_bv += bv
        if bv > highest_single_bv:
            highest_single_bv = bv

    if "+REP" in flags:
        total_bv *= 0.8
    if "x" in element.extra:
        total_bv *= 1.1

    goe_value = highest_single_bv * (element.goe * 0.10)
    return round(total_bv + goe_value, 2)

assert_equal(score_jump_element(Element("3", "jump", "A", [], 0, ["clean"])), 8.00)
assert_equal(score_jump_element(Element("3", "jump", "A", [], 1, ["clean"])), 8.80)
assert_equal(score_jump_element(Element("3", "jump", "A", ["x"], 0, ["clean"])), 8.80)

assert_equal(score_jump_element(Element("3", "jump", "A", [], 0, ["<<"])), 3.30)
assert_equal(score_jump_element(Element("3", "jump", "A", [], 0, ["<"])), 6.40)
assert_equal(score_jump_element(Element("3", "jump", "A", [], 0, ["q"])), 8.00)

assert_equal(score_jump_element(Element("3", "jump", "Lz", [], 0, ["clean", "e"])), 4.72)
assert_equal(score_jump_element(Element("3+3", "jump", "Lz+T", [], 0, ["clean", "clean"])), 10.10)
assert_equal(score_jump_element(Element("3+3", "jump", "Lz+T", ["x"], 0, ["clean", "clean"])), 11.11)
assert_equal(score_jump_element(Element("3+3", "jump", "Lz+T", [], 0, ["clean", "clean", "+REP"])), 8.08)
assert_equal(score_jump_element(Element("3", "jump", "A", [], 0, ["clean", "*"])), 0.00)

def score_spin_element(element: Element) -> float:
    '''
    Calculates the total score of a spin using its base value,
    difficulty level, missing variation status, and GOE.

    Args:
        element (Element): The spin element containing its
            spin type, difficulty level, modifiers, and GOE.

    Returns:
        float: The total spin score, including its base value
            and GOE, rounded to two decimal places.
    '''
    if "*" in element.extra2:
        return 0.00
    bv = 0.00
    for spin in SPIN_BVS:
        if spin.type == element.name:
            if not "V" in element.extra2:
                if element.num == "B":
                    bv = spin.base
                elif element.num == "1":
                    bv = spin.one
                elif element.num == "2":
                    bv = spin.two
                elif element.num == "3":
                    bv = spin.three
                elif element.num == "4":
                    bv = spin.four
            else:
                if element.num == "B":
                    bv = spin.base
                elif element.num == "1":
                    bv = spin.base
                elif element.num == "2":
                    bv = spin.one
                elif element.num == "3":
                    bv = spin.two
                elif element.num == "4":
                    bv = spin.three
    goe_value = bv * (element.goe * 0.10)
    return round(bv + goe_value, 2)

assert_equal(score_spin_element(Element("B", "spin", "USp", [], 0, [])), 1.20)
assert_equal(score_spin_element(Element("1", "spin", "USp", [], 0, [])), 1.40)
assert_equal(score_spin_element(Element("2", "spin", "USp", [], 0, [])), 1.80)
assert_equal(score_spin_element(Element("3", "spin", "USp", [], 0, [])), 2.30)
assert_equal(score_spin_element(Element("4", "spin", "USp", [], 0, [])), 2.90)

assert_equal(score_spin_element(Element("B", "spin", "FCSp", [], 0, [])), 1.90)
assert_equal(score_spin_element(Element("4", "spin", "FCSp", [], 0, [])), 3.80)
assert_equal(score_spin_element(Element("4", "spin", "USp", [], 0, ["V"])), 2.30)

assert_equal(score_spin_element(Element("4", "spin", "USp", [], 1, [])), 3.19)
assert_equal(score_spin_element(Element("B", "spin", "ChSp", [], 0, [])), 3.50)
assert_equal(score_spin_element(Element("4", "spin", "USp", [], 0, ["*"])), 0.00)
assert_equal(score_spin_element(Element("", "spin", "USp", [], 0, [])), 0.00)

def score_step_element(element: Element) -> float:
    '''
    Calculates the total score of a step sequence, choreographic
    step sequence, or a choreographic sequence using its base value,
    level, and GOE.

    Args:
        element (Element): The step element containing its
            sequence type, difficulty level, modifiers, and GOE.

    Returns:
        float: The total step sequence score, including its
            base value and GOE where applicable.
    '''
    if "*" in element.extra2:
        return 0.00
    bv = 0.00
    if element.name == "StSq" or element.name == "ChSt":
        if element.name == "ChSt":
            bv = 2.00
        else:
            if element.num == "B":
                bv = 1.60
            elif element.num == "1":
                bv = 1.90
            elif element.num == "2":
                bv = 2.70
            elif element.num == "3":
                bv = 3.50
            elif element.num == "4":
                bv = 4.10
        goe_value = bv * (element.goe * 0.10)
        return round(bv + goe_value, 2)
    else:
        #return ChSq base value because that is the only element not checked to return
        bv = 3.50
        return bv + element.goe * 0.5
    
assert_equal(score_step_element(Element("B", "step", "StSq", [], 0, [])), 1.60)
assert_equal(score_step_element(Element("1", "step", "StSq", [], 0, [])), 1.90)
assert_equal(score_step_element(Element("2", "step", "StSq", [], 0, [])), 2.70)
assert_equal(score_step_element(Element("3", "step", "StSq", [], 0, [])), 3.50)
assert_equal(score_step_element(Element("4", "step", "StSq", [], 0, [])), 4.10)

assert_equal(score_step_element(Element("1", "step", "StSq", [], 1, [])), 2.09)
assert_equal(score_step_element(Element("4", "step", "StSq", [], -1, [])), 3.69)

assert_equal(score_step_element(Element("", "step", "ChSt", [], 0, [])), 2.00)
assert_equal(score_step_element(Element("", "step", "ChSt", [], 1, [])), 2.20)

assert_equal(score_step_element(Element("1", "step", "ChSq", [], 0, [])), 3.50)
assert_equal(score_step_element(Element("1", "step", "ChSq", [], 1, [])), 4.00)

assert_equal(score_step_element(Element("1", "step", "StSq", [], 0, ["*"])), 0.00)
assert_equal(score_step_element(Element("1", "step", "ChSq", [], 0, ["*"])), 0.00)
   
@route
def index(state: State) -> Page:
    '''
    Displays the main page of the live skating score calculator
    and allows the user to enter a program or enter elements manually.

    Args:
        state (State): The current program state containing
            the elements, scores, and program information.

    Returns:
        Page: The main calculator page with options to enter
            a program element list or manually add elements.
    '''
    state.element_num = -1
    return Page(
        state,
        [
             Header("Live Scoring Calculator"), 
             "Enter element list:", TextBox("element_list_str", ""), Button("Go", "setup_live_from_str"), "\n",
             "or", Button("Enter Manually", "go_to_jumps"), "instead"
         ],
    )

assert_equal(index(State(elements=[], element_num=0, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='')),
    Page(State(elements=[],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str=''), [
        Header('Live Scoring Calculator'),
        'Enter element list:',
        TextBox('element_list_str'),
        Button('Go', 'setup_live_from_str'),
        '\n',
        'or',
        Button('Enter Manually', 'go_to_jumps'),
        'instead',
    ]))




@route
def go_to_jumps(state: State) -> Page:
    '''
    Displays the jump entry page and allows the user to add
    individual jumps or navigate to other element categories.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The jump entry page with controls for selecting
            jump rotations, types, and second-half bonuses.
    '''
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

assert_equal(go_to_jumps(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='')),
    Page(State(elements=[],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str=''), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: ',
    ]))

@route
def go_to_spins(state: State) -> Page:
    '''
    Displays the spin entry page and allows the user to select
    spin variations, flying entries, and changes of foot.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The spin entry page with controls for selecting
            spin characteristics and adding spins.
    '''
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
    '''
    Displays the step sequence entry page and allows the user
    to select and add different types of step elements.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The step entry page with controls for selecting
            and adding step sequences.
    '''
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
    '''
    Displays the two-jump combination entry page and allows
    the user to select the rotations and types of both jumps.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The two-jump combination entry page with
            controls for selecting both jumps and a bonus.
    '''
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

assert_equal(go_to_2jump(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='')),
    Page(State(elements=[],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str=''), [
        Header('2 Jump Combos'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('Jumps', 'go_to_jumps'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        '1st Jump Rotations:',
        SelectBox('rotations1', ['0', '1', '2', '3', '4'], '0'),
        '1st Jump Type:',
        SelectBox('name1', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        '2nd Jump Rotations:',
        SelectBox('rotations2', ['0', '1', '2', '3', '4'], '0'),
        '2nd Jump Type:',
        SelectBox('name2', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_2jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: ',
    ]))


@route
def go_to_3jump(state: State) -> Page:
    '''
    Displays the three-jump combination entry page and allows
    the user to select the rotations and types of all three jumps.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The three-jump combination entry page with
            controls for selecting all three jumps and a bonus.
    '''
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

assert_equal(go_to_3jump(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='')),
    Page(State(elements=[],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str=''), [
        Header('2 Jump Combos'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('Jumps', 'go_to_jumps'),
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        '1st Jump Rotations:',
        SelectBox('rotations1', ['0', '1', '2', '3', '4'], '0'),
        '1st Jump Type:',
        SelectBox('name1', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        '2nd Jump Rotations:',
        SelectBox('rotations2', ['0', '1', '2', '3', '4'], '1'),
        '2nd Jump Type:',
        SelectBox('name2', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'Eu'),
        '\n',
        '3rd Jump Rotations:',
        SelectBox('rotations3', ['0', '1', '2', '3', '4'], '0'),
        '3rd Jump Type:',
        SelectBox('name3', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_3jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: ',
    ]))


@route
def go_to_4jump(state: State) -> Page:
    '''
    Displays the four-jump combination entry page and allows
    the user to select the rotations and types of all four jumps.

    Args:
        state (State): The current program state containing
            the elements entered so far.

    Returns:
        Page: The four-jump combination entry page with
            controls for selecting all four jumps and a bonus.
    '''
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

assert_equal(go_to_4jump(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='')),
    Page(State(elements=[],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str=''), [
        Header('2 Jump Combos'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('Jumps', 'go_to_jumps'),
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        '\n',
        '1st Jump Rotations:',
        SelectBox('rotations1', ['0', '1', '2', '3', '4'], '0'),
        '1st Jump Type:',
        SelectBox('name1', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        '2nd Jump Rotations:',
        SelectBox('rotations2', ['0', '1', '2', '3', '4'], '1'),
        '2nd Jump Type:',
        SelectBox('name2', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'Eu'),
        '\n',
        '3rd Jump Rotations:',
        SelectBox('rotations3', ['0', '1', '2', '3', '4'], '1'),
        '3rd Jump Type:',
        SelectBox('name3', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'Eu'),
        '4th Jump Rotations:',
        SelectBox('rotations4', ['0', '1', '2', '3', '4'], '0'),
        '4th Jump Type:',
        SelectBox('name4', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_4jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: ',
    ]))
    
@route
def score_jump(state: State) -> Page:
    '''
    Displays the live scoring page for a jump or jump combination
    and allows the user to enter GOE, edge calls, and rotation calls.

    Args:
        state (State): The current program state containing
            the elements and the index of the current element.

    Returns:
        Page: The jump scoring page with controls for entering
            GOE, edge calls, rotation calls, bonuses, invalid
            element status, and falls.
    '''
    current_el = state.elements[state.element_num]
    sub_jumps = state.list_str.split(", ")[state.element_num].split("+")
    existing_rots = current_el.extra2 if current_el.extra2 else ["clean"] * len(sub_jumps)

    page_items = [
        Header("Live Scoring"), "\n",
        "Element: ", state.list_str.split(", ")[state.element_num], "\n",
        " Element number: ", state.element_num + 1, "\n",
        "GOE:", SelectBox("goe", [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 0),
        "Edge:", SelectBox("edge", ["clean", "!", "e"], "clean"), "\n",
    ]

    # Add a rotation dropdown for each jump in the solo or combination
    for i, jump_label in enumerate(sub_jumps):
        default_rot = existing_rots[i] if i < len(existing_rots) else "clean"
        page_items.extend([
            f"{jump_label} Rotation:",
            SelectBox(f"rot_{i}", ["clean", "q", "<", "<<"], default_rot),
        ])

    page_items.extend([
        "\n",
        CheckBox("rep"), "+REP ", CheckBox("bonus"), "b ", CheckBox("invalid"), "* ", CheckBox("fall"), "F", "\n",
        Button("Next", "jump_next_element")
    ])

    return Page(state, page_items)




@route
def score_spin(state: State) -> Page:
    '''
    Displays the live scoring page for the current spin and
    allows the user to enter its GOE, level, and modifiers.

    Args:
        state (State): The current program state containing
            the elements and the index of the current element.

    Returns:
        Page: The spin scoring page with controls for entering
            GOE, difficulty level, missing variation status,
            invalid element status, and falls.
    '''
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
def score_step(state: State) -> Page:
    '''
    Displays the live scoring page for the current step sequence
    and allows the user to enter its GOE, level, and modifiers.

    Args:
        state (State): The current program state containing
            the elements and the index of the current element.

    Returns:
        Page: The step scoring page with controls for entering
            GOE, difficulty level, bonuses, invalid element
            status, and falls.
    '''
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
def score_pcs(state):
    '''
    Displays the Program Component Score entry page and allows
    the user to select the skating level and enter PCS marks.

    Args:
        state (State): The current program state containing
            all scored elements and accumulated scores.

    Returns:
        Page: The PCS entry page with controls for selecting
            the program level and entering Composition,
            Presentation, and Skating Skills scores.
    '''
    return Page(
        state,
        [
             Header("PCS Scores"), "\n",
             "Level:", SelectBox("level", ["Championship Pre-Juvenile Freeskate", "Championship Juvenile Freeskate", "Championship Intermediate Freeskate",
                                           "Championship Novice Freeskate", "Championship Junior Women Freeskate", "Championship Junior Men Freeskate",
                                           "Championship Senior Women Freeskate", "Championship Senior Men Freeskate", "Championship Intermediate Short Program",
                                           "Championship Novice Short Program", "Championship Junior Women Short Program", "Championship Junior Men Short Program",
                                           "Championship Senior Women Short Program", "Championship Senior Men Short Program", "Excel Pre-Preliminary Freeskate",
                                           "Excel Preliminary Plus Freeskate", "Excel Pre-Juvenile Plus Freeskate", "Excel Juvenile Freeskate",
                                           "Excel Juvenile Plus Freeskate", "Excel Intermediate Freeskate", "Excel Intermediate Plus Freeskate",
                                           "Excel Novice Freeskate", "Excel Junior Freeskate", "Excel Senior Freeskate"], "Championship Pre-Juvenile Freeskate"), "\n",
             "Composition:", SelectBox("composition", [0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00,
                                                       4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00,
                                                       8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75, 10.00], 0.00), "\n",
             "Presentation:", SelectBox("presentation", [0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00,
                                                       4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00,
                                                       8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75, 10.00], 0.00), "\n",
             "Skating Skills:", SelectBox("skating_skills", [0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00,
                                                       4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00,
                                                       8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75, 10.00], 0.00),"\n",
             Button("Finish", "score_program")                             
         ],
    )

@route
def final_page(state) -> Page:
    '''
    Displays the completed skating program score, including
    TES, PCS, bonuses, deductions, and the final total.

    Args:
        state (State): The completed program state containing
            all calculated scores and accumulated deductions.

    Returns:
        Page: The final results page showing the program's
            individual score components and overall total.
    '''
    return Page(
        state,
        [
             Header("Final Score"), "\n",
             "TES: ", state.tes, "\n",
             "PCS: ", state.pcs, "\n",
             "Bonuses: ", state.bonuses, "\n",
             "Deductions: ", state.deductions, "\n",
             "Total: ", state.tes + state.pcs + state.bonuses + state.deductions
         ],
    )

@route
def score_program(state: State, level: str, composition: float, presentation: float, skating_skills: float) -> Page:
    '''
    Calculates the final program score by adding the Technical
    Element Score, Program Component Score, bonuses, and deductions.

    Args:
        state (State): The current program state containing
            the elements, bonuses, and fall count.
        level (str): The skating level and program type used
            to determine PCS multipliers and fall deductions.
        composition (float): The judge's Composition score.
        presentation (float): The judge's Presentation score.
        skating_skills (float): The judge's Skating Skills score.

    Returns:
        Page: The final results page displaying the calculated
            TES, PCS, bonuses, deductions, and total score.
    '''
    tes_score = 0.0
    for element in state.elements:
        if element.type == "jump":
            tes_score += score_jump_element(element)
        elif element.type == "spin":
            tes_score += score_spin_element(element)
        elif element.type == "step":
            tes_score += score_step_element(element)
    state.tes = round(tes_score, 2)
    state.pcs = calculate_pcs(level, composition, presentation, skating_skills)
    if "Junior" in level or "Senior" in level:
        state.deductions = -1 * state.falls
    else:
        state.deductions = -0.5 * state.falls
    return final_page(state)

assert_equal(score_program(State(elements=[Element(num='4', type='spin', name='CCoSp', extra=[], goe=2, extra2=['V']), Element(num='4', type='jump', name='Lo', extra=[], goe=-3, extra2=['<']), Element(num='1', type='step', name='ChSq', extra=[], goe=4, extra2=[])], element_num=3, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='CCoSp, 4Lo, ChSq'), 'Championship Senior Men Freeskate', 8.75, 7.75, 8.75),
    Page(State(elements=[Element(num='4',
                            type='spin',
                            name='CCoSp',
                            extra=[],
                            goe=2,
                            extra2=['V']),
                    Element(num='4',
                            type='jump',
                            name='Lo',
                            extra=[],
                            goe=-3,
                            extra2=['<']),
                    Element(num='1',
                            type='step',
                            name='ChSq',
                            extra=[],
                            goe=4,
                            extra2=[])],
          element_num=3,
          tes=15.7,
          pcs=84.08,
          falls=0,
          deductions=0,
          bonuses=0.0,
          list_str='CCoSp, 4Lo, ChSq'), [
        Header('Final Score'),
        '\n',
        'TES: ',
        15.7,
        '\n',
        'PCS: ',
        84.08,
        '\n',
        'Bonuses: ',
        0.0,
        '\n',
        'Deductions: ',
        0,
        '\n',
        'Total: ',
        99.78,
    ]))

@route
def add_jump(state: State, rotations: str, name: str, bonus: str) -> Page:
    '''
    Creates a new individual jump element using the selected
    rotations, jump type, and second-half bonus.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        rotations (str): The number of rotations completed
            by the jump, represented as a string.
        name (str): The type of jump being added.
        bonus (str): Indicates whether the jump receives
            a second-half bonus, represented by x or No bonus.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
    extra = ["x"] if bonus == "x" else []
    state.elements.append(Element(rotations, "jump", name, extra, 0, ["clean"]))
    label = rotations + name + (bonus if bonus == "x" else "")
    state.list_str = label if not state.list_str else state.list_str + ", " + label
    return go_to_jumps(state)

assert_equal(add_jump(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str=''), '1', 'S', 'No bonus'),
    Page(State(elements=[Element(num='1',
                            type='jump',
                            name='S',
                            extra=[],
                            goe=0,
                            extra2=['clean'])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S',
    ]))


@route
def add_2jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, bonus: str) -> Page:
    '''
    Creates a new two-jump combination using the selected
    rotations and jump types for both jumps.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        rotations1 (str): The rotation count of the first jump.
        name1 (str): The type of the first jump.
        rotations2 (str): The rotation count of the second jump.
        name2 (str): The type of the second jump.
        bonus (str): Indicates whether the combination receives
            a second-half bonus, represented by x or No bonus.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
    extra = ["x"] if bonus == "x" else []
    state.elements.append(Element(f"{rotations1}+{rotations2}", "jump", f"{name1}+{name2}", extra, 0, ["clean", "clean"]))
    label = f"{rotations1}{name1}+{rotations2}{name2}" + (bonus if bonus == "x" else "")
    state.list_str = label if not state.list_str else state.list_str + ", " + label
    return go_to_jumps(state)

assert_equal(add_2jump(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str=''), '1', 'S', '1', 'Lo', 'x'),
    Page(State(elements=[Element(num='1+1',
                            type='jump',
                            name='S+Lo',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean'])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S+1Lox'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S+1Lox',
    ]))


@route
def add_3jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, rotations3: str, name3: str, bonus: str) -> Page:
    '''
    Creates a new three-jump combination using the selected
    rotations and jump types for all three jumps.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        rotations1 (str): The rotation count of the first jump.
        name1 (str): The type of the first jump.
        rotations2 (str): The rotation count of the second jump.
        name2 (str): The type of the second jump.
        rotations3 (str): The rotation count of the third jump.
        name3 (str): The type of the third jump.
        bonus (str): Indicates whether the combination receives
            a second-half bonus, represented by x or No bonus.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
    extra = ["x"] if bonus == "x" else []
    state.elements.append(Element(f"{rotations1}+{rotations2}+{rotations3}", "jump", f"{name1}+{name2}+{name3}", extra, 0, ["clean", "clean", "clean"]))
    label = f"{rotations1}{name1}+{rotations2}{name2}+{rotations3}{name3}" + (bonus if bonus == "x" else "")
    state.list_str = label if not state.list_str else state.list_str + ", " + label
    return go_to_jumps(state)

assert_equal(add_3jump(State(elements=[Element(num='1+1', type='jump', name='S+Lo', extra=['x'], goe=0, extra2=['clean', 'clean'])], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='1S+1Lox'), '1', 'S', '1', 'Eu', '1', 'F', 'No bonus'),
    Page(State(elements=[Element(num='1+1',
                            type='jump',
                            name='S+Lo',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean']),
                    Element(num='1+1+1',
                            type='jump',
                            name='S+Eu+F',
                            extra=[],
                            goe=0,
                            extra2=['clean', 'clean', 'clean'])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S+1Lox, 1S+1Eu+1F'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S+1Lox, 1S+1Eu+1F',
    ]))

@route
def add_4jump(state: State, rotations1: str, name1: str, rotations2: str, name2: str, rotations3: str, name3: str, rotations4: str, name4: str, bonus: str) -> Page:
    '''
    Creates a new four-jump combination using the selected
    rotations and jump types for all four jumps.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        rotations1 (str): The rotation count of the first jump.
        name1 (str): The type of the first jump.
        rotations2 (str): The rotation count of the second jump.
        name2 (str): The type of the second jump.
        rotations3 (str): The rotation count of the third jump.
        name3 (str): The type of the third jump.
        rotations4 (str): The rotation count of the fourth jump.
        name4 (str): The type of the fourth jump.
        bonus (str): Indicates whether the combination receives
            a second-half bonus, represented by x or No bonus.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
    extra = ["x"] if bonus == "x" else []
    state.elements.append(Element(f"{rotations1}+{rotations2}+{rotations3}+{rotations4}", "jump", f"{name1}+{name2}+{name3}+{name4}", extra, 0, ["clean", "clean", "clean", "clean"]))
    label = f"{rotations1}{name1}+{rotations2}{name2}+{rotations3}{name3}+{rotations4}{name4}" + (bonus if bonus == "x" else "")
    state.list_str = label if not state.list_str else state.list_str + ", " + label
    return go_to_jumps(state)

assert_equal(add_4jump(State(elements=[Element(num='1+1', type='jump', name='S+Lo', extra=['x'], goe=0, extra2=['clean', 'clean']), Element(num='1+1+1', type='jump', name='S+Eu+F', extra=[], goe=0, extra2=['clean', 'clean', 'clean'])], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='1S+1Lox, 1S+1Eu+1F'), '3', 'A', '1', 'Eu', '3', 'S', '2', 'A', 'x'),
    Page(State(elements=[Element(num='1+1',
                            type='jump',
                            name='S+Lo',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean']),
                    Element(num='1+1+1',
                            type='jump',
                            name='S+Eu+F',
                            extra=[],
                            goe=0,
                            extra2=['clean', 'clean', 'clean']),
                    Element(num='3+1+3+2',
                            type='jump',
                            name='A+Eu+S+A',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean', 'clean', 'clean'])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax',
    ]))

@route
def add_spin(state: State, variation: str, flying: bool, change: bool) -> Page:
    '''
    Creates a new spin element using the selected spin variation,
    flying entry, and change-of-foot characteristics.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        variation (str): The type of spin being added, such
            as CSp, CoSp, LSp, SSp, USp, or ChSp.
        flying (bool): Indicates whether the spin has
            a flying entry.
        change (bool): Indicates whether the spin includes
            a change of foot.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
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

assert_equal(add_spin(State(elements=[Element(num='1+1', type='jump', name='S+Lo', extra=['x'], goe=0, extra2=['clean', 'clean']), Element(num='1+1+1', type='jump', name='S+Eu+F', extra=[], goe=0, extra2=['clean', 'clean', 'clean']), Element(num='3+1+3+2', type='jump', name='A+Eu+S+A', extra=['x'], goe=0, extra2=['clean', 'clean', 'clean', 'clean'])], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax'), 'SSp', True, False),
    Page(State(elements=[Element(num='1+1',
                            type='jump',
                            name='S+Lo',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean']),
                    Element(num='1+1+1',
                            type='jump',
                            name='S+Eu+F',
                            extra=[],
                            goe=0,
                            extra2=['clean', 'clean', 'clean']),
                    Element(num='3+1+3+2',
                            type='jump',
                            name='A+Eu+S+A',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean', 'clean', 'clean']),
                    Element(num='',
                            type='spin',
                            name='FSSp',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax, FSSp'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax, FSSp',
    ]))
        
@route
def add_step(state: State, variation: str) -> Page:
    '''
    Creates a new step or choreographic sequence element
    using the selected sequence variation.

    Args:
        state (State): The current program state containing
            the existing elements and element list.
        variation (str): The type of step sequence being added,
            such as StSq, ChSq, or ChSt.

    Returns:
        Page: The jump entry page with the updated program
            element list.
    '''
    state.elements.append(Element("", "step", variation, [], 0, []))
    if not state.list_str:
        state.list_str += variation
    else:
        state.list_str += ", " + variation
    return go_to_jumps(state)

assert_equal(add_step(State(elements=[Element(num='1', type='jump', name='S', extra=[], goe=0, extra2=['clean'])], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='1S'), 'StSq'),
    Page(State(elements=[Element(num='1',
                            type='jump',
                            name='S',
                            extra=[],
                            goe=0,
                            extra2=['clean']),
                    Element(num='',
                            type='step',
                            name='StSq',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=-1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S, StSq'), [
        Header('Jumps'),
        '\n',
        Button('Spins', 'go_to_spins'),
        Button('Steps', 'go_to_steps'),
        '\n',
        Button('2 Jump Combos', 'go_to_2jump'),
        Button('3 Jump Combos', 'go_to_3jump'),
        Button('4 Jump Combos', 'go_to_4jump'),
        '\n',
        'Rotations:',
        SelectBox('rotations', ['0', '1', '2', '3', '4'], '0'),
        'Type:',
        SelectBox('name', ['S', 'T', 'Lo', 'F', 'Lz', 'A', 'Eu', 'Wz'], 'S'),
        'Bonus:',
        SelectBox('bonus', ['No bonus', 'x'], 'No bonus'),
        '\n',
        Button('Add', 'add_jump'),
        '\n',
        Button('Finish', 'go_to_next_element'),
        '\n',
        'List of elements so far: 1S, StSq',
    ]))

@route
def go_to_next_element(state: State) -> Page:
    '''
    Advances the program to the next element that needs to be
    scored and determines which scoring page should be displayed.

    Args:
        state (State): The current program state containing
            the elements, current element number, and scores.

    Returns:
        Page: The scoring page for the next jump, spin, or
            step sequence, or the PCS page when all elements
            have been scored.
    '''
    state.element_num += 1
    if state.element_num >= len(state.elements):
        return score_pcs(state)
    if state.elements[state.element_num].type == "jump":
        return score_jump(state)
    if state.elements[state.element_num].type == "spin":
        return score_spin(state)
    if state.elements[state.element_num].type == "step":
        return score_step(state)
    
assert_equal(go_to_next_element(State(elements=[Element(num='1+1', type='jump', name='S+Lo', extra=['x'], goe=0, extra2=['clean', 'clean']), Element(num='1+1+1', type='jump', name='S+Eu+F', extra=[], goe=0, extra2=['clean', 'clean', 'clean']), Element(num='3+1+3+2', type='jump', name='A+Eu+S+A', extra=['x'], goe=0, extra2=['clean', 'clean', 'clean', 'clean']), Element(num='', type='spin', name='FSSp', extra=[], goe=0, extra2=[])], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax, FSSp')),
    Page(State(elements=[Element(num='1+1',
                            type='jump',
                            name='S+Lo',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean']),
                    Element(num='1+1+1',
                            type='jump',
                            name='S+Eu+F',
                            extra=[],
                            goe=0,
                            extra2=['clean', 'clean', 'clean']),
                    Element(num='3+1+3+2',
                            type='jump',
                            name='A+Eu+S+A',
                            extra=['x'],
                            goe=0,
                            extra2=['clean', 'clean', 'clean', 'clean']),
                    Element(num='',
                            type='spin',
                            name='FSSp',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=0,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='1S+1Lox, 1S+1Eu+1F, 3A+1Eu+3S+2Ax, FSSp'), [
        Header('Live Scoring'),
        '\n',
        'Element: ',
        '1S+1Lox',
        '\n',
        ' Element number: ',
        1,
        '\n',
        'GOE:',
        SelectBox('goe', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], '0'),
        'Edge:',
        SelectBox('edge', ['clean', '!', 'e'], 'clean'),
        '\n',
        '1S Rotation:',
        SelectBox('rot_0', ['clean', 'q', '<', '<<'], 'clean'),
        '1Lox Rotation:',
        SelectBox('rot_1', ['clean', 'q', '<', '<<'], 'clean'),
        '\n',
        CheckBox('rep'),
        '+REP ',
        CheckBox('bonus'),
        'b ',
        CheckBox('invalid'),
        '* ',
        CheckBox('fall'),
        'F',
        '\n',
        Button('Next', 'jump_next_element'),
    ]))

@route
def setup_live_from_str(state: State, element_list_str: str) -> Page:
    '''
    Parses the user's complete program element string,
    saves the elements, and begins the live scoring process.

    Args:
        state (State): The current program state.
        element_list_str (str): The complete list of program
            elements entered by the user.

    Returns:
        Page: The scoring page for the first program element,
            or the PCS page if there are no elements to score.
    '''
    state.elements = parse_element_str(element_list_str)
    state.list_str = element_list_str
    return go_to_next_element(state)

assert_equal(setup_live_from_str(State(elements=[], element_num=-1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str=''), 'CCoSp, 4Lo, ChSq'),
    Page(State(elements=[Element(num='',
                            type='spin',
                            name='CCoSp',
                            extra=[],
                            goe=0,
                            extra2=[]),
                    Element(num='4',
                            type='jump',
                            name='Lo',
                            extra=[],
                            goe=0,
                            extra2=[]),
                    Element(num='',
                            type='step',
                            name='ChSq',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=0,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='CCoSp, 4Lo, ChSq'), [
        Header('Live Scoring'),
        '\n',
        'Element: ',
        'CCoSp',
        '\n',
        ' Element number: ',
        1,
        '\n',
        'GOE:',
        SelectBox('goe', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], '0'),
        'Level:',
        SelectBox('level', ['B', '1', '2', '3', '4'], 'B'),
        CheckBox('missing_variation'),
        'V ',
        CheckBox('invalid'),
        '* ',
        CheckBox('fall'),
        'F',
        '\n',
        Button('Next', 'spin_next_element'),
    ]))

@route
def jump_next_element(
    state: State,
    goe: int,
    edge: str,
    rep: bool,
    bonus: bool,
    invalid: bool,
    fall: bool,
    rot_0: str = "clean",
    rot_1: str = "clean",
    rot_2: str = "clean",
    rot_3: str = "clean",
) -> Page:
    '''
    Saves the judge's scoring information for the current jump
    and advances the program to the next element.

    Args:
        state (State): The current program state containing
            the elements, bonuses, and fall count.
        goe (int): The Grade of Execution score assigned
            to the jump.
        edge (str): The edge call assigned to the jump,
            such as clean, !, or e.
        rep (bool): Indicates whether the jump combination
            receives a repetition deduction.
        bonus (bool): Indicates whether the jump receives
            an additional bonus.
        invalid (bool): Indicates whether the jump is invalid
            and should receive no base value.
        fall (bool): Indicates whether the skater fell
            during the jump.
        rot_0 (str): The rotation call for the first jump.
        rot_1 (str): The rotation call for the second jump.
        rot_2 (str): The rotation call for the third jump.
        rot_3 (str): The rotation call for the fourth jump.

    Returns:
        Page: The scoring page for the next element or the
            PCS page if all elements have been scored.
    '''
    current_el = state.elements[state.element_num]
    current_el.goe = goe

    num_jumps = len(current_el.num.split("+"))
    per_jump_rots = [rot_0, rot_1, rot_2, rot_3][:num_jumps]

    # Store per-jump rotations first, followed by element-level flags
    updated_extra2 = list(per_jump_rots)
    if edge != "clean":
        updated_extra2.append(edge)
    if rep:
        updated_extra2.append("+REP")
    if bonus:
        updated_extra2.append("b")
        state.bonuses += 1.0
    if invalid:
        updated_extra2.append("*")
    if fall:
        updated_extra2.append("F")
        state.falls += 1

    current_el.extra2 = updated_extra2
    return go_to_next_element(state)

assert_equal(jump_next_element(State(elements=[Element(num='4', type='spin', name='CCoSp', extra=[], goe=2, extra2=['V']), Element(num='4', type='jump', name='Lo', extra=[], goe=0, extra2=[]), Element(num='', type='step', name='ChSq', extra=[], goe=0, extra2=[])], element_num=1, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='CCoSp, 4Lo, ChSq'), -3, 'clean', False, False, False, False, '<'),
    Page(State(elements=[Element(num='4',
                            type='spin',
                            name='CCoSp',
                            extra=[],
                            goe=2,
                            extra2=['V']),
                    Element(num='4',
                            type='jump',
                            name='Lo',
                            extra=[],
                            goe=-3,
                            extra2=['<']),
                    Element(num='',
                            type='step',
                            name='ChSq',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=2,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='CCoSp, 4Lo, ChSq'), [
        Header('Live Scoring'),
        '\n',
        'Element: ',
        'ChSq',
        '\n',
        ' Element number: ',
        3,
        '\n',
        'GOE:',
        SelectBox('goe', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], '0'),
        'Level (if step sequence, otherwise leave as 1):',
        SelectBox('level', ['B', '1', '2', '3', '4'], '1'),
        CheckBox('bonus'),
        'b ',
        CheckBox('invalid'),
        '* ',
        CheckBox('fall'),
        'F',
        '\n',
        Button('Next', 'step_next_element'),
    ]))

@route
def spin_next_element(state: State, goe: int, level: str, missing_variation: bool, invalid: bool, fall: bool) -> Page:
    '''
    Saves the judge's scoring information for the current spin
    and advances the program to the next element.

    Args:
        state (State): The current program state containing
            the elements and the fall count.
        goe (int): The Grade of Execution score assigned
            to the spin.
        level (str): The difficulty level of the spin,
            represented as B, 1, 2, 3, or 4.
        missing_variation (bool): Indicates whether the spin
            is missing a required variation.
        invalid (bool): Indicates whether the spin is invalid
            and should receive no base value.
        fall (bool): Indicates whether the skater fell
            during the spin.

    Returns:
        Page: The scoring page for the next element or the
            PCS page if all elements have been scored.
    '''
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

assert_equal(spin_next_element(State(elements=[Element(num='', type='spin', name='CCoSp', extra=[], goe=0, extra2=[]), Element(num='4', type='jump', name='Lo', extra=[], goe=0, extra2=[]), Element(num='', type='step', name='ChSq', extra=[], goe=0, extra2=[])], element_num=0, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='CCoSp, 4Lo, ChSq'), 2, '4', True, False, False),
    Page(State(elements=[Element(num='4',
                            type='spin',
                            name='CCoSp',
                            extra=[],
                            goe=2,
                            extra2=['V']),
                    Element(num='4',
                            type='jump',
                            name='Lo',
                            extra=[],
                            goe=0,
                            extra2=[]),
                    Element(num='',
                            type='step',
                            name='ChSq',
                            extra=[],
                            goe=0,
                            extra2=[])],
          element_num=1,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='CCoSp, 4Lo, ChSq'), [
        Header('Live Scoring'),
        '\n',
        'Element: ',
        '4Lo',
        '\n',
        ' Element number: ',
        2,
        '\n',
        'GOE:',
        SelectBox('goe', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], '0'),
        'Edge:',
        SelectBox('edge', ['clean', '!', 'e'], 'clean'),
        '\n',
        '4Lo Rotation:',
        SelectBox('rot_0', ['clean', 'q', '<', '<<'], 'clean'),
        '\n',
        CheckBox('rep'),
        '+REP ',
        CheckBox('bonus'),
        'b ',
        CheckBox('invalid'),
        '* ',
        CheckBox('fall'),
        'F',
        '\n',
        Button('Next', 'jump_next_element'),
    ]))

@route
def step_next_element(state: State, goe: int, level: str, bonus: bool, invalid: bool, fall: bool):
    '''
    Saves the judge's scoring information for the current step
    sequence and advances the program to the next element.

    Args:
        state (State): The current program state containing
            the elements, bonuses, and fall count.
        goe (int): The Grade of Execution score assigned
            to the step sequence.
        level (str): The difficulty level of the step sequence,
            represented as B, 1, 2, 3, or 4.
        bonus (bool): Indicates whether the step sequence
            receives an additional bonus.
        invalid (bool): Indicates whether the step sequence
            is invalid and should receive no base value.
        fall (bool): Indicates whether the skater fell
            during the step sequence.

    Returns:
        Page: The scoring page for the next element or the
            PCS page if all elements have been scored.
    '''
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

assert_equal(step_next_element(State(elements=[Element(num='4', type='spin', name='CCoSp', extra=[], goe=2, extra2=['V']), Element(num='4', type='jump', name='Lo', extra=[], goe=-3, extra2=['<']), Element(num='', type='step', name='ChSq', extra=[], goe=0, extra2=[])], element_num=2, tes=0.0, pcs=0.0, falls=0, deductions=0.0, bonuses=0.0, list_str='CCoSp, 4Lo, ChSq'), 4, '1', False, False, False),
    Page(State(elements=[Element(num='4',
                            type='spin',
                            name='CCoSp',
                            extra=[],
                            goe=2,
                            extra2=['V']),
                    Element(num='4',
                            type='jump',
                            name='Lo',
                            extra=[],
                            goe=-3,
                            extra2=['<']),
                    Element(num='1',
                            type='step',
                            name='ChSq',
                            extra=[],
                            goe=4,
                            extra2=[])],
          element_num=3,
          tes=0.0,
          pcs=0.0,
          falls=0,
          deductions=0.0,
          bonuses=0.0,
          list_str='CCoSp, 4Lo, ChSq'), [
        Header('PCS Scores'),
        '\n',
        'Level:',
        SelectBox('level', ['Championship Pre-Juvenile Freeskate', 'Championship Juvenile Freeskate', 'Championship Intermediate Freeskate', 'Championship Novice Freeskate', 'Championship Junior Women Freeskate', 'Championship Junior Men Freeskate', 'Championship Senior Women Freeskate', 'Championship Senior Men Freeskate', 'Championship Intermediate Short Program', 'Championship Novice Short Program', 'Championship Junior Women Short Program', 'Championship Junior Men Short Program', 'Championship Senior Women Short Program', 'Championship Senior Men Short Program', 'Excel Pre-Preliminary Freeskate', 'Excel Preliminary Plus Freeskate', 'Excel Pre-Juvenile Plus Freeskate', 'Excel Juvenile Freeskate', 'Excel Juvenile Plus Freeskate', 'Excel Intermediate Freeskate', 'Excel Intermediate Plus Freeskate', 'Excel Novice Freeskate', 'Excel Junior Freeskate', 'Excel Senior Freeskate'], 'Championship Pre-Juvenile Freeskate'),
        '\n',
        'Composition:',
        SelectBox('composition', ['0.0', '0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0', '2.25', '2.5', '2.75', '3.0', '3.25', '3.5', '3.75', '4.0', '4.25', '4.5', '4.75', '5.0', '5.25', '5.5', '5.75', '6.0', '6.25', '6.5', '6.75', '7.0', '7.25', '7.5', '7.75', '8.0', '8.25', '8.5', '8.75', '9.0', '9.25', '9.5', '9.75', '10.0'], '0.0'),
        '\n',
        'Presentation:',
        SelectBox('presentation', ['0.0', '0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0', '2.25', '2.5', '2.75', '3.0', '3.25', '3.5', '3.75', '4.0', '4.25', '4.5', '4.75', '5.0', '5.25', '5.5', '5.75', '6.0', '6.25', '6.5', '6.75', '7.0', '7.25', '7.5', '7.75', '8.0', '8.25', '8.5', '8.75', '9.0', '9.25', '9.5', '9.75', '10.0'], '0.0'),
        '\n',
        'Skating Skills:',
        SelectBox('skating_skills', ['0.0', '0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0', '2.25', '2.5', '2.75', '3.0', '3.25', '3.5', '3.75', '4.0', '4.25', '4.5', '4.75', '5.0', '5.25', '5.5', '5.75', '6.0', '6.25', '6.5', '6.75', '7.0', '7.25', '7.5', '7.75', '8.0', '8.25', '8.5', '8.75', '9.0', '9.25', '9.5', '9.75', '10.0'], '0.0'),
        '\n',
        Button('Finish', 'score_program'),
    ]))

start_server(State([], 0, 0.0, 0.0, 0, 0.0, 0.0, ""))
