from PIL import Image, ImageDraw
import math
import re



class LSystemConfig:
  def __init__(self,axioms,rules,iterations,length,angle,direction,startPos,color,imagesize,commands=None,filename=None):
    self.axioms = axioms
    self.rules = rules
    self.instructions = ""

    self.iterations = iterations
    self.filename = self.defaultFilename(filename)

    self.length = self.startingLength(length)
    self.angle = angle
    self.direction = self.startingDirection(direction)

    self.color=self.startingColor(color)

    self.imagesize = self.startingImageSize(imagesize)
    self.startPos = self.startPoint(startPos)

  def defaultFilename(self,filename):
    return filename if filename is not None else "Fractals.png"
    
  def startingDirection(self,direction):
    return direction if direction is not None else 0

  def startingLength(self,length):
    return length if length is not None else 5
   
  def startingImageSize(self,imagesize):
    if imagesize is None:
      return (800,800)
    return imagesize

  def startingColor(self,color):
    return color if color is not None else (0,0,0)

  def startPoint(self,pos):
    startingPoints = {
      'topLeft': (0,0),
      'topright': (self.imagesize[0],0),
      'middle': (self.imagesize[0]//2,self.imagesize[1]//2),
      'bottommiddle':(self.imagesize[0]//2,self.imagesize[1]),
      'topmiddle':(self.imagesize[0]//2,0),
      'bottomleft': (0,self.imagesize[1]),
      'bottomright':(self.imagesize[0],self.imagesize[1])
    }

    if isinstance(pos, str) and pos in startingPoints:
      return startingPoints[pos]
    elif pos is None:
       return (self.imagesize[0]//2,self.imagesize[1])
    else:
      return pos


class MultiBatchLSystem:
  def __init__(self,LSystemConfigs):
      self.configs = LSystemConfigs

  def runAll(self):
    for config in self.configs:
      lsystem=LSystem(config)
      lsystem.run()
    

class LSystem:
  def __init__(self,LSystemConfig):
    self.axioms = LSystemConfig.axioms
    self.rules = LSystemConfig.rules
    self.iterations = LSystemConfig.iterations
    self.filename =LSystemConfig.filename
    self.startPos = LSystemConfig.startPos
    self.angle= LSystemConfig.angle
    self.direction = LSystemConfig.direction
    self.imagesize = LSystemConfig.imagesize
    self.length=LSystemConfig.length
    self.color=LSystemConfig.color
    self.instructions = LSystemConfig.instructions
    self.image = Image.new("RGB", LSystemConfig.imagesize, "white")
    self.commandsActions = self.getCommands()
    self.stack = []
    self.xlen = LSystemConfig.length
    self.ylen = LSystemConfig.length
    self.x = LSystemConfig.startPos[0]
    self.y = LSystemConfig.startPos[1] 

  def generateLSystemStringSingleLetterAxioms(self):
    self.instructions = self.axioms
    #print("Initial Axioms:", self.instructions)
    #print("Rules:", self.rules)
    #print("Rules Keys:", self.rules.keys())
    for _ in range(self.iterations):
      string = ""
      for axiom in self.instructions:
        string += self.rules.get(axiom,axiom)
        #print(f"Iteration {self.iterations + 1}, Char: {axiom}, Applied Rule: {self.rules.get(axiom, axiom)}")
      self.instructions = string

  def generateLSystemStringMultiNumberAxioms(self):
    self.instructions = self.axioms
    #maxkey = max(len(key) for key in self.rules.keys())
    print("Initial Axioms:", self.instructions)
    print("Rules:", self.rules)
    #print("Max Key:", maxkey)
    for index in range(self.iterations):
      string = ""
      i = 0
      while i < len(self.instructions):
        if self.instructions[i].isalpha():
            j = i +1
            while j < len(self.instructions) and self.instructions[j].isdigit():
               j+=1
            axiom = self.instructions[i:j] 
            string += self.rules.get(axiom,axiom)
            #print(f"Iteration {index + 1}, Axiom: {axiom}, Applied Rule: {self.rules.get(axiom, axiom)}")
            i=j
        else:
          axiom = self.instructions[i] 
          string += self.rules.get(axiom,axiom)
          #print(f"Iteration {index + 1}, Axiom: {axiom}, Applied Rule: {self.rules.get(axiom, axiom)}")
          i+=1
      self.instructions = string

  def generateLSystemStringMultiAxioms(self):
    self.instructions = self.axioms
    print("Multi Axioms Initial Axioms:", self.instructions)
    print("Multi Axioms Rules:", self.rules)
    print(list(self.commandsActions.keys() | self.rules.keys()))
    for index in range(self.iterations):
      string = ""
      i = 0
      while i < len(self.instructions):
        matches = None
        keys = None

        # check all rules for substring
        for key in self.commandsActions.keys() | self.rules.keys():
           if self.instructions.startswith(key,i):
              if matches is None or len(key) > len(matches):
                 matches = key
                 keys = key
        #print(f"i {i} key {keys} len key {len(keys)} match {matches} ")
        if matches is not None:
          axiom = keys
          string += self.rules.get(axiom,axiom)#self.rules[keys]
          i+=len(keys)
          print(f"Iteration {index + 1}, i {i}, Axiom: {axiom}, Applied Rule: {self.rules.get(axiom,axiom)}") 
        else:
          if (j := i+1) < len(self.instructions):
            while j < len(self.instructions) and self.instructions[j].isdigit():
              j += 1
            axiom = axiom = self.instructions[i:j] 
            string += self.rules.get(axiom,axiom)#self.rules[keys]
            if j>i+1:
              i += j
            else:
              i += 1
          else:
            axiom = self.instructions[i]
            string += self.rules.get(axiom, axiom)
            i += 1
          print(f"Iteration {index + 1}, i {i}, j {j}, Axiom: {axiom}, Applied Rule: {self.rules.get(axiom,axiom)}") 
      self.instructions = string
     

  def simplifyInstructions(self):
    if isinstance(self.instructions,str):
      self.instructions = re.sub(r'([A-Za-z])\d+', r'\1', self.instructions)
    elif isinstance(self.instructions,list):
      self.instructions = [re.sub(r'([A-Za-z])\d+', r'\1', instruct) for instruct in self.instructions]


  def getCommands(self):
    draw = ImageDraw.Draw(self.image)
    x,y=self.startPos
    direction = self.direction
    angle = self.angle
    length = self.length
    xlen = self.length
    ylen = self.length
    color = self.color
    stack = []

    def moveFocus():
      nonlocal x, y
      newX = x + length * math.cos(math.radians(direction))
      newY = y - length * math.sin(math.radians(direction))
      x, y = newX, newY

    def drawLine():
        nonlocal x, y
        newX = x + length * math.cos(math.radians(direction))
        newY = y - length * math.sin(math.radians(direction))
        draw.line((x, y, newX, newY), fill=color, width=1)
        x, y = newX, newY

    def drawCircle():
       nonlocal x,y
       draw.ellipse((x-length,y-length,x+length,y+length),outline=color)

    def drawSquare():
       nonlocal x,y
       draw.rectangle((x-length//2,y-length//2,x+length//2,y+length//2),outline=color)

    def changeAllLength(newlength,newxlen,newylen):
      nonlocal length,xlen,ylen
      print(f"length {length}, newlength {newlength}, xlen{xlen}, ylen {ylen}, newxlen {newxlen}, newylen {newylen}")
      length = newlength
      xlen = newxlen
      ylen = newylen

    def changeLength(newlength):
      nonlocal length
      print(f"length {length}, newlength {newlength}")
      length = newlength

    def changexyLen(newxlen,newylen):
      nonlocal xlen,ylen
      print(f"xlen{xlen}, ylen {ylen}, newxlen {newxlen}, newylen {newylen}")
      xlen = newxlen
      ylen = newylen
    
    def drawEllipse():
       nonlocal x,y
       draw.ellipse((x-xlen,y-ylen,x+xlen,y+ylen),outline=color)
    
    def drawRectangle():
       nonlocal x,y
       draw.rectangle((x-xlen//2,y-ylen//2,x+xlen//2,y+ylen//2),outline=color)
    
    def drawNothing():
       pass

    def updateDirection(angle):
      nonlocal direction
      direction +=  angle
    
    def popStack():
      nonlocal x, y, direction, color, length, xlen, ylen, stack
      x, y, direction, color, length, xlen, ylen = stack.pop()
    
    def pushStack():
      nonlocal stack
      stack.append((x,y,direction,color,length,xlen,ylen))

    def changeColor(newColor):
      nonlocal color
      color = newColor

    colorMatching = {
      'R': (255,0,0),
      'G':(0,255,0),
      'B':(0,0,255)   
    }
    
    commandsActions = {
      'L': drawLine,
      'C': drawCircle,
      'S': drawSquare,
      'E': drawEllipse,
      'M': moveFocus,
      'N': drawNothing,
      'CL': lambda: changeLength(30),
      'CLXL': lambda: changexyLen(45,35),
      'CAL': lambda: changeAllLength(20,55,75),
      '+': lambda: updateDirection(angle),
      '-': lambda: updateDirection(-angle),
      '[': pushStack,
      ']': popStack,

      # Colors
      'R': lambda: changeColor(colorMatching['R']),
      'G': lambda: changeColor(colorMatching['G']),
      'B': lambda: changeColor(colorMatching['B']) 
    } 
    return commandsActions 

  def executeCommands(self):
    '''
    draw = ImageDraw.Draw(self.image)
    
    x,y=self.startPos
    direction = self.direction
    angle = self.angle
    length = self.length
    xlen = self.length
    ylen = self.length
    color = self.color
    stack = []

    def moveFocus():
      nonlocal x, y
      newX = x + length * math.cos(math.radians(direction))
      newY = y - length * math.sin(math.radians(direction))
      x, y = newX, newY

    def drawLine():
        nonlocal x, y
        newX = x + length * math.cos(math.radians(direction))
        newY = y - length * math.sin(math.radians(direction))
        draw.line((x, y, newX, newY), fill=color, width=1)
        x, y = newX, newY

    def drawCircle():
       nonlocal x,y
       draw.ellipse((x-length,y-length,x+length,y+length),outline=color)

    def drawSquare():
       nonlocal x,y
       draw.rectangle((x-length//2,y-length//2,x+length//2,y+length//2),outline=color)

    def changeAllLength(newlength,newxlen,newylen):
      nonlocal length,xlen,ylen
      length = newlength
      xlen = newxlen
      ylen = newylen

    def changeLength(newlength):
      nonlocal length
      length = newlength

    def changexyLen(newxlen,newylen):
      nonlocal xlen,ylen
      xlen = newxlen
      ylen = newylen
    
    def drawEllipse():
       nonlocal x,y
       draw.ellipse((x-xlen,y-ylen,x+xlen,y+ylen),outline=color)
    
    def drawRectangle():
       nonlocal x,y
       draw.rectangle((x-xlen//2,y-ylen//2,x+xlen//2,y+ylen//2),outline=color)
    
    def drawNothing():
       pass

    def updateDirection(angle):
      nonlocal direction
      direction +=  angle
    
    def popStack():
      nonlocal x, y, direction, color, length, xlen, ylen, stack
      x, y, direction, color, length, xlen, ylen = stack.pop()
    
    def pushStack():
      nonlocal stack
      stack.append((x,y,direction,color,length,xlen,ylen))

    def changeColor(newColor):
      nonlocal color
      color = newColor

    colorMatching = {
      'R': (255,0,0),
      'G':(0,255,0),
      'B':(0,0,255)   
    }
    
    commandsActions = {
      'L': drawLine,
      'C': drawCircle,
      'S': drawSquare,
      'E': drawEllipse,
      'M': moveFocus,
      'N': drawNothing,
      'CL': lambda: changeLength(10),
      'CLXL': lambda: changexyLen(5,5),
      'CAL': lambda: changeAllLength(10,5,5),
      '+': lambda: updateDirection(angle),
      '-': lambda: updateDirection(-angle),
      '[': pushStack(),
      ']': popStack,

      # Colors
      'R': lambda: changeColor(colorMatching['R']),
      'G': lambda: changeColor(colorMatching['G']),
      'B': lambda: changeColor(colorMatching['B']) 
    } 
    '''
    i = 0
    while i < len(self.instructions):
      matches = None
      keys = None
      command = None
      # check all rules for substring
      for key in self.commandsActions.keys() | self.rules.keys():
         if self.instructions.startswith(key,i):
            if matches is None or len(key) > len(matches):
               matches = key
               keys = key
              
      command = keys
      i+=len(keys)
    #for command in self.instructions:
      #print(f"command {command}")
      if isinstance(command,str):
        try: 
          if command in self.commandsActions:
            self.commandsActions[command]()
          else:
             print(f"Error: Command {command} is not recognized")
        except Exception as e:
           print(f"An error happened executing command {command}: {str(e)}")
      elif isinstance(command,list) and len(command) == 0:
        command = command[0]
        try: 
          if command in self.commandsActions:
            self.commandsActions[command]()
          else:
             print(f"Error: Command {command} is not recognized")
        except Exception as e:
           print(f"An error happened executing command {command}: {str(e)}")
      else:
         print("Failure")
      #elif command in colorMatching:
      #  color = colorMatching[command]


  def executeCommands2(self):
    draw = ImageDraw.Draw(self.image)

    x,y=self.startPos
    direction = self.direction
    angle = self.angle
    length = self.length

    stack = []
    color = (0, 0, 0)


    def moveFocus():
      nonlocal x, y
      newX = x + length * math.cos(math.radians(direction))
      newY = y - length * math.sin(math.radians(direction))
      x, y = newX, newY

    def drawLine():
        nonlocal x, y
        newX = x + length * math.cos(math.radians(direction))
        newY = y - length * math.sin(math.radians(direction))
        draw.line((x, y, newX, newY), fill=color, width=1)
        x, y = newX, newY

    def drawCircle():
       nonlocal x,y
       draw.ellipse((x-length,y-length,x+length,y+length),outline=color)

    def drawSquare():
       nonlocal x,y
       draw.rectangle((x-length//2,y-length//2,x+length//2,y+length//2),outline=color)
    
    def drawEllipse():
       pass
    
    def drawRectangle():
       pass
    
    def drawNothing():
       pass

    def updateDirection(angle):
      nonlocal direction
      direction +=  angle
    
    def popStack():
      nonlocal x,y,direction,color
      x,y,direction,color = stack.pop()

    
    colorMatching = {
        'R': (255,0,0),
        'G':(0,255,0),
        'B':(0,0,255)   
    }

    for command in self.instructions:
        if command in ('L','X','Y') :
            drawLine()
        elif command == 'M':
           moveFocus()
        elif command == 'C':
           drawCircle()
        elif command == 'S':
           drawSquare()
        elif command == '+':
            direction += angle
        elif command == '-':
            direction -= angle
        elif command == '[':
            stack.append((x, y, direction, color))
        elif command == ']':
            x, y, direction, color = stack.pop()

        # Handle color-changing commands
        elif command in colorMatching:
          color = colorMatching[command]
    
    
  def save(self,filename = None):
    if filename is not None:
       self.filename = filename 
    self.image.save(self.filename)
    print("L-System image saved as " + self.filename)


  def run(self):

    #Generate the L-system instructions
    #self.generateLSystemStringAxiom1()
    #print("L-system instructions:", self.instructions)
    #self.simplifyInstructions()
    #print("L-system instructions:", self.instructions)

    #self.generateLSystemStringMultiNumberAxioms()
    #print("L-system instructions:", self.instructions)
    #self.simplifyInstructions()
    #print("L-system instructions:", self.instructions)

    self.generateLSystemStringMultiAxioms()
    print("L-system Instructions:", self.instructions)
    self.simplifyInstructions()
    print("Simplify L-system Instructions:", self.instructions)

    # Draw the L-system on an image
    self.executeCommands()
    #self.executeCommands2()
    #self.Draw()

    # Save the image to a file
    self.save()


# Main function to set up the L-system parameters and create the image
def main():
    

    # Configuration for the L-system
    configFractalTree = LSystemConfig(
        axioms="L",  # Starting axiom
        rules={
            "L": "LL+[+LG-LB-LR]-[-LB+LR+LG]",  # Rule for fractal with color-changing commands
        },
        iterations=5,  # Number of iterations
        length=10,  # Length of each line segment
        angle=35,  # Angle to turn
        direction=90,  # Initial direction (facing upwards)
        startPos= "bottommiddle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="FractalTree.png" # Filename
    )
    '''
     axioms="L1",  # Starting axiom
        rules={
            "L1": "L2-[[L1]]+L1+L2[+L2L1]-L1",  
            "L2": "L2L2"
        },
        axioms="L",  # Starting axiom
        rules={
            "L": "X-[[L]]+L+X[+XL]-L",  
            "X": "XX"
        },
    '''
    # Configuration for the L-system
    configFractalPlant = LSystemConfig(
        axioms="L1",  # Starting axiom
        rules={
            "L1": "L2-[[L1]]+L1+L2[+L2L1]-L1",  
            "L2": "L2L2"
        },
        iterations=4,  # Number of iterations
        length=10,  # Length of each line segment
        angle=25,  # Angle to turn
        direction=90,  # Initial direction (facing upwards)
        startPos="bottommiddle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="FractalPlant.png" # Filename
    )

    # Configuration for the L-system
    configSierpinskiTriangle = LSystemConfig(
        axioms="L",  # Starting axiom
        rules={
            "L": "L-M+L+M-L",
            "M":"MM"  
        },
        iterations=6,  # Number of iterations
        length=5,  # Length of each line segment
        angle=120,  # Angle to turn
        direction=0,  # Initial direction (facing upwards)
        startPos="middle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="SierpinskiTriangle.png" # Filename
    )

    '''
      axioms="LX",  # Starting axiom
        rules={
            "X": "X+YL+",
            "Y":"-LX-Y"  
        },
    '''

    # Configuration for the L-system
    configDragonCurve = LSystemConfig(
        axioms="L1L2",  # Starting axiom
        rules={
            #"L1": "L1",
            "L2": "L2+L3L1+",
            "L3":"-L1L2-L3"  
        },
        iterations=10,  # Number of iterations
        length=10,  # Length of each line segment
        angle=90,  # Angle to turn
        direction=0,  # Initial direction (facing upwards)
        startPos="middle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="DragonCurve.png" # Filename
    )

    # Configuration for the L-system
    configKochSnowflake = LSystemConfig(
        axioms="L",  # Starting axiom
        rules={
            "L": "L+L--L+L",
        },
        iterations=6,  # Number of iterations
        length=4,  # Length of each line segment
        angle=60,  # Angle to turn
        direction=90,  # Initial direction (facing upwards)
        startPos="bottommiddle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="KochSnowflake.png" # Filename
    )


    # Configuration for the L-system
    configCirclesSquares = LSystemConfig(
        axioms="LL",  # Starting axiom
        rules={
            "L": "L+RC-BS+LCAL",
        },
        iterations=2,  # Number of iterations
        length=55,  # Length of each line segment
        angle=30,  # Angle to turn
        direction=0,  # Initial direction (facing upwards)
        startPos="middle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="CirclesSquares.png" # Filename
    )

    # Configuration for the L-system
    configCirclesSquaresChangeLength = LSystemConfig(
        axioms="CNL",  # Starting axiom
        rules={
            "L": "L+RC-+BS+LCL",
        },
        iterations=2,  # Number of iterations
        length=55,  # Length of each line segment
        angle=30,  # Angle to turn
        direction=0,  # Initial direction (facing upwards)
        startPos="middle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="CirclesSquaresChange1.png" # Filename
    )

    # Configuration for the L-system
    configCirclesSquaresChangeLength2 = LSystemConfig(
        axioms="L",  # Starting axiom
        rules={
            "L": "L+RC-BS+CLL",
        },
        iterations=2,  # Number of iterations
        length=55,  # Length of each line segment
        angle=30,  # Angle to turn
        direction=0,  # Initial direction (facing upwards)
        startPos="middle",  # Start from the bottom middle of the image
        color=(0, 0, 0),  # Default color
        imagesize=(800, 800),  # Image size
        filename="CirclesSquaresChange2.png" # Filename
    )
    configs = [configSierpinskiTriangle,configDragonCurve,configKochSnowflake,configFractalTree,configFractalPlant,configCirclesSquares,configCirclesSquaresChangeLength,configCirclesSquaresChangeLength2]
    #configs = [configDragonCurve]
    batch = MultiBatchLSystem(configs)
    batch.runAll()

if __name__ == "__main__":
    main()
