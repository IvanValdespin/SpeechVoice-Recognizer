import json
import time
from app import data_base 


class StringTemporal(data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    data = data_base.Column(data_base.String(255), nullable=False)



class Lamp():

    def __init__(self,status,nlp,sentence,patterns,matcher,lamp_ins,lamp_actions,lamp_properties) -> None:
        
        self.status = status
        self.nlp = nlp
        self.sentence = sentence
        self.patterns = patterns
        self.matcher = matcher
        self.lamp_ins = lamp_ins
        self.lamp_actions = lamp_actions
        self.lamp_properties = lamp_properties
        
    
    def get_status(self):

        self.lamp_ins['on'] = self.status['on']
        self.lamp_ins['color'] = self.status['color']
        self.lamp_ins['brightness'] = self.status['brightness']
    
    def getOnOff(self):
        

        on_off = self.get_matches(self.patterns[16],self.matcher)
        color = self.get_matches(self.patterns[3], self.matcher)


        if on_off:

            action = self.sentence[on_off[0][2]-1].text

            if action == self.lamp_properties[0]:
                self.lamp_ins['on'] = True
            else:
                self.lamp_ins['on'] = False

        elif self.get_matches(self.patterns[1],self.matcher):
            self.lamp_ins['on'] = True

        elif self.get_matches(self.patterns[2],self.matcher):
            self.lamp_ins['on'] = False

        else:
            pass

        if color:

            color = self.sentence[color[0][1]].text
            self.lamp_ins['color'] = color

        return self.lamp_ins['on']

    def getColor(self):
        
        change = self.get_matches(self.patterns[4], self.matcher)

        if change: 
            color = self.get_matches(self.patterns[3], self.matcher)
            if color:
                color = self.sentence[color[0][1]].text
                self.lamp_ins['color'] = color
        else:
                pass
        
    
    def getBrightness(self):

        
        increase = self.get_matches(self.patterns[5],self.matcher)
        decrease = self.get_matches(self.patterns[6],self.matcher)
        percentage = self.get_matches(self.patterns[18],self.matcher)

        brightness_value = self.status['brightness']

        if percentage:

            if len(percentage)==1:
                value = int(self.sentence[percentage[0][1]:percentage[0][2]].text)
                current_value = int(self.lamp_ins['brightness'])
                
                if increase:
                    if current_value == 100:
                        pass
                    elif (current_value + value) > 100:
                        self.lamp_ins['brightness'] = 100
                    else:
                        self.lamp_ins['brightness'] = current_value + value

                elif decrease:
                    if current_value == 0:
                        pass
                    elif (current_value - value) < 0:
                        self.lamp_ins['brightness'] = 0
                    else: 
                        self.lamp_ins['brightness'] = current_value - value
            
            elif len(percentage)==2:
                value = int(self.sentence[percentage[0][2]-1].text)
                self.lamp_ins['brightness']=int(value)

        else:

            if increase:  
                if brightness_value < 100 and (brightness_value+10) <= 100:
                    self.lamp_ins['brightness'] = brightness_value + 10
                else:
                    self.lamp_ins['brightness'] = 100

            elif decrease:
                if (brightness_value-10 > 0):
                    self.lamp_ins['brightness'] = brightness_value - 10
                else:
                    self.lamp_ins['brightness'] = 0
            else:
                pass
    
    def get_matches(self,patterns,matcher):

        matches = [match for match in matcher if self.nlp.vocab.strings[match[0]] in patterns]
        return matches
    
    def getInstructions(self):
        
        self.get_status()

        if self.lamp_ins['on']:

            if self.getOnOff() == False:

                self.lamp_ins['color'] = ''
                self.lamp_ins['brightness'] = 0
            else:
                self.getColor()
                self.getBrightness()
        else:
            
            if self.getOnOff() == True:
                self.getColor()
                self.getBrightness()

                if self.lamp_ins['color']== "":
                    self.lamp_ins['color'] = 'tan'

                    if self.lamp_ins['brightness'] == 0 or self.lamp_ins['brightness'] == "":
                        self.lamp_ins['brightness'] = 100 
            else:
                self.lamp_ins['brightness'] = 0
                self.lamp_ins['color']== ""
                    
        return self.lamp_ins
        self.patterns = json_lgconfig['PATTERNS']['pattern_names']
        self.instructuions = json_lgconfig['INSTRUCTIONS']
        self.urls = json_lgconfig['URLS']
        self.actions = json_lgconfig['OBJECTS']
        

    #def get_intention(self):

        

class Blind():

    def __init__(self,nlp,sentence,patterns,matcher,blind_ins,blinds_actions,blind_properties) -> None:
        self.nlp = nlp
        self.sentence = sentence
        self.patterns = patterns
        self.matcher = matcher
        self.blind_ins = blind_ins
        self.blind_actions = blinds_actions
        self.blind_properties = blind_properties

    def getUpDown(self):

        up_down = self.get_matches(self.patterns[17],self.matcher)

        if up_down:
            action = self.sentence[up_down[0][2]-1].text
            
            if action in self.blind_actions['up']:
                self.blind_ins['state'] = self.blind_properties[0]

            elif action in self.blind_actions['down']:
                self.blind_ins['state'] = self.blind_properties[1]
    
        elif self.get_matches(self.patterns[8],self.matcher):
            self.blind_ins['state'] = self.blind_properties[0]

        elif self.get_matches(self.patterns[9],self.matcher):
            self.blind_ins['state'] = self.blind_properties[1]

        elif self.get_matches(self.patterns[10],self.matcher):
            self.blind_ins['state'] = self.blind_properties[2]

        else:
            pass

        return self.blind_ins
    
    def get_matches(self,patterns,matcher):

        matches = [match for match in matcher if self.nlp.vocab.strings[match[0]] in patterns]
        return matches




class Robot():

    def __init__(self,nlp,matcher,urls,sentence,actions,init_coord,request,patterns) -> None:
        self.nlp = nlp
        self.urls = urls        
        self.matcher = matcher
        self.sentence = sentence
        self.actions = actions
        self.init_coord = init_coord
        self.request = request
        self.patterns = patterns
        self.token = self.getToken()
        




    def saveToken(self,token):
    
        string_temporal = StringTemporal(data=token)
        data_base.session.add(string_temporal)
        data_base.session.commit()

    def deleteToken(self):
        StringTemporal.query.delete()
        data_base.session.commit()
    
    def getToken(self):

        return StringTemporal.query.first().data
    
    
    
    def startRobot(self):

        url = self.urls['post']['operator']

        operator = {
            "name": "user_name",   
            "email": "user_mail"
        }

        status = self.request.sendPost(url, operator)

        if status.status_code == 200:
            header = status.headers
            new_token = header['location'][57::]
            self.deleteToken()
            self.saveToken(new_token)

            time.sleep(1)
            response = self.sendCoordenates(self.init_coord)
            if response == 200:
                return self.actions['messages']['init_success']
            else:
                return response
        
        elif status.status_code == 403:
            return self.actions['messages']['taken']
        
        else:
            return self.actions['messages']['error']
        
    def desconnectRobot(self):

        url = self.urls['delete']['operator'] + self.getToken()
        status = self.request.sendDelete(url)
        if status.status_code == 200:
            return self.actions['messages']['delete_user']
        elif status.status_code == 404:
            return self.actions['messages']['bad_token']
        else:
            return self.actions['messages']['issue']
            
    def taken(self):
        try:
            url = self.urls['get']['operator']
            status = self.request.sendGetStatus(url)
            status = status.status_code

            if status == 204:
                answer = self.actions['messages']['free']       
            elif status == 200:
                answer = self.actions['messages']['taken']
            else: 
                answer = self.actions['messages'] ['error']
        except Exception as e:
            print(e)
            answer = e

        return answer
            
    def initialize(self):

        url = self.urls['put']['initialize']
        status = self.request.sendPut(url,self.token)
        return status.status_code
    
    def resetRobot(self):
            
        response = self.sendCoordenates(self.init_coord)
        if response == 200:
            return self.actions['messages']['init_success']
        else:
            return self.actions['messages']['not_reset']
    
    def getGripperData(self):

        url = self.urls['get']['gripper']    
        token = self.getToken() 
        status = self.request.sendGetMovements(url,token)
        return status
        
    def openGripper(self):

        response = self.getGripperData() 

        if response.status_code == 200:

            current_distance = int(response.content.decode('utf-8'))

            if current_distance == 800:
                return self.actions['messages']['max_distance_gripper']
            else: 
                distance = self.get_matches(self.patterns[18],self.matcher)
                
                if len(distance) == 0:
                    return self.actions['messages']['not_distance']


                if len(distance) == 1:
                    distance = float(self.sentence[distance[0][1]:distance[0][2]].text)

                    if self.get_matches(self.patterns[20],self.matcher):

                        final_distance = (distance * 100) + current_distance
                    else: 
                        final_distance = current_distance + distance

                elif len(distance) == 2:

                    distance = float(self.sentence[distance[0][2]-1].text)

                    if self.get_matches(self.patterns[20],self.matcher):
                        final_distance = distance * 100
                    else:
                        final_distance = distance
                else:
                    final_distance = distance

                if final_distance > 800:
                    return self.actions['messages']['distance_exceeded']
                else:
                    time.sleep(1)
                    response = self.sendGripperDistance(int(final_distance))

                    return response
        else:
            return self.actions['messages']['bad_gripper_get']
        
    def closeGripper(self):

        response = self.getGripperData() 

        if response.status_code == 200:

            current_distance = int(response.content.decode('utf-8'))

            if current_distance == 0:
                return self.actions['messages']['min_gripper_distance']

            else: 
                distance = self.get_matches(self.patterns[18],self.matcher)

                if len(distance) == 0:
                    return self.actions['messages']['not_distance']
                
                if len(distance) == 1:
                    distance = float(self.sentence[distance[0][1]:distance[0][2]].text)

                    if self.get_matches(self.patterns[20],self.matcher):

                        final_distance = current_distance - (distance * 100)
                    else: 
                        final_distance = current_distance - distance

                elif len(distance) == 2:

                    distance = float(self.sentence[distance[0][2]-1].text)

                    if self.get_matches(self.patterns[20],self.matcher):
                        final_distance = distance * 100
                    else:
                        final_distance = distance
                else:
                    final_distance = distance

                if final_distance < 0:
                    return self.actions['messages']['bad_parameter']
                else:
                    time.sleep(1)
                    response = self.sendGripperDistance(int(final_distance))
                    return response
        else:
            return self.actions['messages']['bad_gripper_get']
    
    def getCoordinates(self):

        url = self.urls['get']['tcp']
        token = self.getToken()
        status = self.request.sendGetMovements(url,token)
        return status
        
    
    def moveRobot(self,movement):

        response = self.getCoordinates()

        if response.status_code != 200:
            return self.actions['messages']['get_error']

        else:

            coordenates = response.json()

            actions = self.actions['actions']['actions'][::2]

            if self.sentence[movement[0][1]:movement[0][2]].text.lower() in actions:
                
                direction = self.get_matches(self.patterns[21],self.matcher)
                distance = self.get_matches(self.patterns[18],self.matcher)

                if len(distance) == 0:
                    return self.actions['messages']['not_distance']
                elif len(direction) == 0:
                    return self.actions['messages']['not_direction']
                
                else:
                    distance = self.sentence[distance[0][1]:distance[0][2]].text

                    try:
                        distance = float(distance)

                        if self.get_matches(self.patterns[20],self.matcher):
                            distance *= 10

                        if direction:

                            directions = self.actions['properties']['movement']

                            """right"""
                            if self.sentence[direction[0][1]:direction[0][2]].text == directions[0]:

                                if type(self.yAxis(float(coordenates['coordinate']['y']),distance,directions[0])) is float:
                                    coordenates['coordinate']['y'] = self.yAxis(float(coordenates['coordinate']['y']),distance,directions[0])
                                else:
                                    return self.yAxis(float(coordenates['coordinate']['y']),distance,directions[0])
                                """left"""
                            elif self.sentence[direction[0][1]:direction[0][2]].text == directions[1]:
                                if type(self.yAxis(float(coordenates['coordinate']['y']),distance,directions[1])) is float:
                                    coordenates['coordinate']['y'] = self.yAxis(float(coordenates['coordinate']['y']),distance,directions[1])
                                else:
                                    return self.yAxis(float(coordenates['coordinate']['y']),distance,directions[1])

                                """up"""
                            elif self.sentence[direction[0][1]:direction[0][2]].text == directions[2]:
                                if type(self.zAxis(float(coordenates['coordinate']['z']),distance,directions[2])) is float:
                                    coordenates['coordinate']['z'] = self.zAxis(float(coordenates['coordinate']['z']),distance,directions[2])
                                else:
                                    return self.zAxis(float(coordenates['coordinate']['z']),distance,directions[2])
                                """down"""
                            elif self.sentence[direction[0][1]:direction[0][2]].text == directions[3]:
                                if type(self.zAxis(float(coordenates['coordinate']['z']),distance,directions[3]))is float:
                                    coordenates['coordinate']['z'] = self.zAxis(float(coordenates['coordinate']['z']),distance,directions[3])
                                else:
                                    return self.zAxis(float(coordenates['coordinate']['z']),distance,directions[3])
                                """forward"""
                            elif self.sentence[direction[0][1]:direction[0][2]].text in directions[4:6]:
                                if type(self.xAxis(float(coordenates['coordinate']['x']),distance,'forward')) is float:
                                    coordenates['coordinate']['x'] = self.xAxis(float(coordenates['coordinate']['x']),distance,'forward')
                                else:
                                    return self.xAxis(float(coordenates['coordinate']['x']),distance,'forward')
                                """backward"""
                            elif self.sentence[direction[0][1]:direction[0][2]].text in directions[6::]:
                                if type(self.xAxis(float(coordenates['coordinate']['x']),distance,'backward')) is float:
                                    coordenates['coordinate']['x'] = self.xAxis(float(coordenates['coordinate']['x']),distance,'backward')
                                else:
                                    return self.xAxis(float(coordenates['coordinate']['x']),distance,'backward')
                    except:
                        return "Something was wrong"
            
                    time.sleep(1)
                    final_coordenates = {
                        "target": coordenates,
                        "speed":50
                    }
                    response = self.sendCoordenates(final_coordenates)
                    return self.actions['messages']['success']
            else:
                return self.actions['messages']['fail']

    def sendCoordenates(self,coordenates):
        try:
            token = self.getToken()
            url_put = self.urls['put']['target']
            response = self.request.send_put(url_put,token,coordenates)

            if response.status_code == 200:
                return self.actions['messages']['success']
            else:
                return self.actions['messages']['bad_parameter']
        except Exception as e:
            return e
        
    def sendGripperDistance(self,distance):
        try:
            token = self.getToken()
            url_put = self.urls['put']['gripper']
            response = self.request.send_put(url_put,token,distance)

            if response.status_code == 200:
                return self.actions['messages']['success']
            else:
                return self.actions['messages']['bad_parameter']
        except Exception as e:
            return e
    
    
    def xAxis(self,current_x,x,direction):

        if direction == "forward":
            final_x = current_x + x
        else: 
            final_x = current_x - x

        if final_x > 720 or final_x < -720:
            return self.actions['messages']['distance_exceeded']
        else:
            return round(final_x,2)
        


    def yAxis(self,current_y,y,direction):

        if direction == "right":
            final_y = current_y + y
        else:
            final_y = current_y - y
        
        if final_y > 720 or final_y < -720:            
            return self.actions['messages']['distance_exceeded']
        else:
            return round(final_y,2)
    
    def zAxis(self,current_z,z,direction):

        if direction == 'up':
            final_z = current_z + z
        else:
            final_z = current_z - z

        if final_z < -178 or final_z > 1010:
            return self.actions['messages']['distance_exceeded']
        else:
            return round(final_z,2)
    
    def roll(self,current_roll,roll):

        final_roll = current_roll + roll
        final_roll = current_roll - roll
        if final_roll > 180 or final_roll < -180:
            bad_input = 'Bad input. Dregrees exceeded'
            print(bad_input)
            return round(current_roll,2)
        else:
            return round(final_roll,2)
    
    def pitch(self,current_pitch,pitch):

        final_pitch = current_pitch + pitch
        final_pitch = current_pitch - pitch

        if final_pitch > 180 or final_pitch < -180:
            final_pitch = 'error'
        else:
            return round(current_pitch,2)

    def yaw(self,current_yaw,yaw):
        
        final_yaw = current_yaw + yaw
        final_yaw = current_yaw - yaw

        if final_yaw > 180 or final_yaw < -180:
            final_yaw = 'error'

        return final_yaw
        

        
    def getIntention(self):

        movement = self.get_matches(self.patterns[13],self.matcher)
        """Move, shift and rotate"""
        if movement:
            return self.moveRobot(movement)

            """Robot status"""   
        if self.get_matches(self.patterns[12],self.matcher):
            return  self.taken()
        
            """Initializing the robot"""
        elif self.get_matches(self.patterns[15],self.matcher):
            return self.startRobot()
        
        gripper = self.get_matches(self.patterns[14],self.matcher)

        if len(gripper) > 0:
            if self.sentence[gripper[0][1]:gripper[0][2]].text.lower() == self.actions['actions']['gripper'][0]:
                return self.openGripper()
            else:
                return self.closeGripper()
        
        if self.get_matches(self.patterns[22],self.matcher):
            return self.desconnectRobot()
        
        elif self.get_matches(self.patterns[23],self.matcher):
            return self.resetRobot()
    
        else:
            return "Action not identified"
                

    def get_matches(self,patterns,matcher):

        matches = [match for match in matcher if self.nlp.vocab.strings[match[0]] in patterns]
        return matches


