from spacy.matcher import Matcher
from Interfaces import IPatterns

class EnglishConfig(IPatterns):

    def __init__(self,nlp,english_config) -> None:
        
        self.nlp = nlp
        self.matcher = Matcher(self.nlp.vocab)
        self.english_objects = english_config
    

    def createPatterns(self):

        objects = self.english_objects['OBJECTS']

        lamp_sinonyms = [{'LOWER':{"FUZZY1":{"IN":objects['LAMP']['sinonyms']}},'OP':'+'}]
        lamp_on = [{'LOWER':{"FUZZY1":{"IN":objects['LAMP']['actions']['turnon']}},'OP':'+'}]
        lamp_off = [{'LOWER':{"FUZZY1":{"IN":objects['LAMP']['actions']['turnoff']}},'OP':'+'}]
        colors = [{'LOWER':{'IN':objects['LAMP']['colors']},'OP':'+'}]
        color_verbs = [{'LOWER':{'FUZZY':{'IN':objects['LAMP']['actions']['color']}},'OP':'?'}] 
        rise_brightness = [{'LOWER':{'FUZZY1':{'IN':objects['LAMP']['actions']['brightness_up']}},'OP':'+'}]
        reduce_brightness = [{'LOWER':{'FUZZY1':{'IN':objects['LAMP']['actions']['brightness_down']}},'OP':'+'}]

        blind_sinonyms = [{"LOWER":{"FUZZY":{"IN":objects['BLINDS']['sinonyms']}},'OP':'+'}]
        blind_actions_up = [{"LOWER":{"FUZZY1":{"IN":objects['BLINDS']['actions']['up']}},'OP':'+'}]
        blind_actions_down = [{"LOWER":{"FUZZY1":{"IN":objects['BLINDS']['actions']['down']}},'OP':'+'}]
        blind_actions_stop = [{"LOWER":{"FUZZY1":{"IN":objects['BLINDS']['actions']['stop']}},'OP':'+'}]

        robot_sinonyms = [{"LOWER":{"FUZZY":{"IN":objects['ROBOT']['sinonyms']}},'OP':'+'}]
        robot_status = [{'LOWER':{'FUZZY':{'IN':objects['ROBOT']['actions']['status']}},'OP':'+'}]
        robot_start = [{'LOWER':{'FUZZY':{'IN':objects['ROBOT']['actions']['actions'][4:6]}},'OP':'+'}]
        robot_movements = [{'LOWER':{'FUZZY1':{'IN':objects['ROBOT']['actions']['actions'][0:3]}},'OP':'+'}]
        robot_direction = [{'LOWER':{'FUZZY1':{'IN':objects['ROBOT']['properties']['movement']}},'OP':'+'}]
        robot_desconnect = [{'LOWER':{'FUZZY1':objects['ROBOT']['actions']['actions'][6]},'OP':'+'}]
        robot_reset = [{'LOWER':{'FUZZY1':objects['ROBOT']['actions']['actions'][3]},'OP':'+'}]
        gripper_movements = [{'LOWER':{'FUZZY':{'IN':objects['ROBOT']['actions']['gripper']}},'OP':'+'}]


        onoff = [{'POS':'VERB','LEMMA':{'IN':['turn','switch']},'OP':'?'},{'LOWER':'the','OP':'?'},
                    {"LOWER":{"FUZZY":{"IN":objects['LAMP']['sinonyms']}},'OP':'?'},{'LOWER':{'IN':['on','off']},'OP':'+'}]
        
        updown = [{'POS':'VERB','LEMMA':'turn','OP':'?'},{'LOWER':'the','OP':'?'},
                    {"LOWER":{"FUZZY":{"IN":objects['BLINDS']['sinonyms']}},'OP':'?'},{'LOWER':{'IN':['up','down']},'OP':'+'}]


        numbers_pattern = [{'LOWER':{'IN':['at','to']},'OP':'?'},{'POS':'NUM','OP':'+'}]

        mm_pattern = [{'LOWER':{'IN':objects['ROBOT']['properties']['distance'][0:3]}}]
        cm_pattern = [{'LOWER':{'IN':objects['ROBOT']['properties']['distance'][3::]}}]

        wakeword = [{"LOWER":{"FUZZY1":{"IN":objects['ESP32']['wakeword']}},'OP':'+'}]

        patterns = [lamp_sinonyms,lamp_on,lamp_off,colors,color_verbs, rise_brightness,reduce_brightness,
                    blind_sinonyms,blind_actions_up,blind_actions_down,blind_actions_stop,
                    robot_sinonyms, robot_status, robot_movements, gripper_movements,robot_start,
                    onoff,updown,numbers_pattern,mm_pattern,cm_pattern,robot_direction,robot_desconnect,robot_reset,
                    wakeword]
        return patterns

    def chargePatterns(self):
        
        patterns = self.createPatterns()
        pattern_names = self.english_objects['PATTERNS']
        counter = 0        
        
        for name in pattern_names['pattern_names']:
            self.matcher.add(name,[patterns[counter]])
            counter += 1

        return self.matcher

