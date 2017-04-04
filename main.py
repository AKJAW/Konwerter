from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.animation import Animation
from navigationdrawer import NavigationDrawer
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from textinput import TextInput as ModuleTextInput
from kivy.uix.togglebutton import ToggleButton
import config as cfg
import os.path
from kivy.uix.slider import Slider

import kivy

kivy.require('1.9.1')
from kivy.app import App





class MyApp(App):
    def build(self):
        self.config = cfg.Config('settings.ini')
        try:
            configFont = self.getConfigFont('s')
        except:
            configFont = 22
        print(configFont)
        if platform == 'win' or platform == 'linux' or platform == 'macosx':
            arrow_size = 40
            self.defaultFont = 15.0
            if configFont == 0:
                self.buttonFontSize = 15
            else:
                self.buttonFontSize = configFont

        else:
            arrow_size = 160
            self.defaultFont = Window.width / 25
            if configFont == 0:
                self.buttonFontSize = Window.width / 25
            else:
                self.buttonFontSize = configFont

        print(self.buttonFontSize)


        self.createSpinners()
        self.navigationdrawer = NavigationDrawer()

        self.naviTopSidePanel = BoxLayout(orientation='vertical')
        self.naviTopSidePanel.add_widget(Label(text=str(platform)))

        self.naviOneOperationToggle = ToggleButton(group='layout', state='down', allow_no_selection=False,
                                                text = '      Dzialania\nna jednej liczbie', on_press = self.naviOptionOne,
                                                font_size = self.buttonFontSize)
        self.naviTopSidePanel.add_widget(self.naviOneOperationToggle)

        self.naviTwoOperationToggle = ToggleButton(group='layout', allow_no_selection=False,
                                                   text='        Dzialania\nna dwoch liczbach',
                                                   on_press=self.naviOptionTwo,
                                                   font_size=self.buttonFontSize)
        self.naviTopSidePanel.add_widget(self.naviTwoOperationToggle)
        self.naviFontButton = Button(text='Opcje czcionki', on_press = self.showFontSlider,
                                             font_size=self.buttonFontSize, background_color=(1, 1, 1, 1))

        self.naviBottomSidePanel = BoxLayout(orientation='vertical')
        self.naviBottomSidePanel.add_widget(Label(text='Dodatkowe\n     opcje'))
        self.pipeToggle = ToggleButton(text='Dodaj pionowa kreske', font_size=self.buttonFontSize)
        self.pipeToggle.bind(on_press=self.checkThePipe)
        self.naviBottomSidePanel.add_widget(self.pipeToggle)
        self.naviBottomSidePanel.add_widget(self.naviFontButton)


        drawerBar = InstructionGroup()
        drawer = Rectangle(size=(5, Window.height+1000))
        drawerBar.add(Color(10, 10, 10, 0.7))
        drawerBar.add(drawer)
        drawerImageLayout = RelativeLayout(
            pos_hint={'x': .999},


        )

        InvisibleButton = Button(size_hint=(1, .07), opacity=.1)
        InvisibleButton.bind(on_press=lambda j: self.navigationdrawer.toggle_state())


        drawerArrowLayout = RelativeLayout(
            pos_hint={'right': 1.503, 'y': 0},
        )
        drawerImageLayout.canvas.add(drawerBar)
        drawerArrowImage = Image(source=os.path.join(os.getcwd(), 'images', 'arrow.png'), size_hint_y=None, height=arrow_size)
        drawerArrowLayout.add_widget(drawerArrowImage)
        drawerArrowLayoutNest = RelativeLayout()

        drawerArrowLayoutNest.add_widget(drawerArrowLayout)
        drawerArrowLayoutNest.add_widget(drawerImageLayout)


        self.naviMainPanel = BoxLayout(orientation='vertical')
        self.naviMainPanel.add_widget(self.naviTopSidePanel)
        self.naviMainPanel.add_widget(BoxLayout())
        self.naviMainPanel.add_widget(self.naviBottomSidePanel)
        self.naviMainPanel.add_widget(drawerArrowLayoutNest)


        self.topWindow = FloatLayout()
        self.bottomWindow = FloatLayout(
            pos_hint={'x': 0}
        )

        #First Input
        self.firstTextInput = ModuleTextInput(multiline=False, size_hint=(.745, .1), use_bubble=True, bubble_pos=23,
                                   pos_hint={'top': self.firstNumberspinner.pos_hint['top'] + .001,  # bylo +.001
                                             'x': self.firstNumberspinner.pos_hint['right'] - .98},
                                   hint_text="Wprowadz liczbe")
        #Second Input
        self.secondTextInput = ModuleTextInput(multiline=False, size_hint=(.745, .1), use_bubble=True, bubble_pos=23,
                                          pos_hint={'top': self.firstTextInput.pos_hint['top'] - .105,
                                                    'x': self.firstNumberspinner.pos_hint['right'] - .98},
                                          hint_text="(opcjonalne)Wprowadz druga liczbe")
        #Two Operations Layout(HIDDEN)
        self.twoOperationLayout= FloatLayout(
            pos_hint={'x': 0}
        )
        self.twoOperationLayout.add_widget(self.secondTextInput)
        self.twoOperationLayout.add_widget(self.secondNumberspinner)
        self.mathSpinnerLabel = Label(text='Wybierz dzialanie', size_hint=(.33, .20),
                                        pos_hint={'top': self.firstTextInput.pos_hint['top'] - .13, 'x': .01})
        self.twoOperationLayout.add_widget(self.mathSpinnerLabel)
        self.twoOperationLayout.add_widget(self.mathSpinner)
        #Result
        self.resultTextOutput = ModuleTextInput(text='', size_hint=(.98, .30), readonly=True, use_bubble=True, bubble_pos=23,
                                           pos_hint={'top': self.firstTextInput.pos_hint['top'] - .5, 'x': .01})
        self.decButton = Button(text='DEC', on_press=self.buildTest, size_hint=(.325, .10),
                                 background_color=(1, 1, 1, 1), font_size=self.buttonFontSize,
                                 pos_hint={'top': self.resultTextOutput.pos_hint['top'] + .1,
                                           'x': .01})
        self.binButton = Button(text='BIN', on_press=self.buildTest, size_hint=(self.decButton.size_hint[0], .10),
                                 background_color=(1, 1, 1, 0.5), font_size=self.buttonFontSize,
                                 pos_hint={'top': self.resultTextOutput.pos_hint['top'] + .1,
                                           'x': self.decButton.pos_hint['x'] + .327})
        self.hexButton = Button(text='HEX', on_press=self.buildTest,
                                 size_hint=(self.binButton.size_hint[0], .10),
                                 background_color=(1, 1, 1, 0.5), font_size=self.buttonFontSize,
                                 pos_hint={'top': self.resultTextOutput.pos_hint['top'] + .1,
                                           'x': self.binButton.pos_hint['x'] + .327})
        self.resultDict = {'DEC':0, 'BIN':1, 'HEX':2}
        self.resultButtons = [self.decButton, self.binButton, self.hexButton]
        self.firstResultList = ['Nie podales liczby','Nie podales liczby','Nie podales liczby']
        self.secondResultList = ['Nie podales liczby','Nie podales liczby','Nie podales liczby']
        self.buttonPressed = 0
        self.bottomWindow.add_widget(self.decButton)
        self.bottomWindow.add_widget(self.binButton)
        self.bottomWindow.add_widget(self.hexButton)
        self.bottomWindow.add_widget(self.resultTextOutput)



        self.mainWindow = FloatLayout()
        self.mainWindow.add_widget(self.bottomWindow)
        self.mainWindow.add_widget(self.firstTextInput)
        self.mainWindow.add_widget(self.firstNumberspinner)
        while len(self.twoOperationLayout.children) != 0:
            self.twoOperationLayout.remove_widget(self.twoOperationLayout.children[0])
        self.mainWindow.add_widget(self.twoOperationLayout)
        self.mainWindow.add_widget(Label(text='Wyniki', size_hint=(.98, .20),
                                     pos_hint={'top': self.firstTextInput.pos_hint['top'] - .273, 'x': .01}))
        self.convertButton = Button(text='Konwertuj', on_press=self.manageFunctions, size_hint=(.2, .10),
                                      pos_hint={'top': 0.74, 'x': .40}, font_size=self.buttonFontSize)
        self.mainWindow.add_widget(self.convertButton)
        self.tutorialLayout = RelativeLayout()
        self.mainWindow.add_widget(self.tutorialLayout)
        self.mainWindow.add_widget(InvisibleButton)

        self.navigationdrawer.add_widget(self.naviMainPanel)
        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.mainWindow)


        return self.navigationdrawer

    def showFontSlider(self, btn):

        sliderLayout = BoxLayout(orientation='vertical')
        self.fontSlider = Slider(value_track=True, step=1, value=self.convertButton.font_size, size_hint=(1, 0.2))
        if platform == 'win' or platform == 'linux' or platform == 'macosx':
            self.fontSlider.max = 25
        else:
            self.fontSlider.max = 60
        self.some_label = Label(text='Rozmiar czcionki '+str(self.convertButton.font_size), size_hint=(1, 0.6), halign='left')
        self.fontSlider.bind(value=self.onSliderValueChange)
        self.sliderConfirmButton = Button(text="Zastosuj", font_size=self.buttonFontSize, size_hint=(1, 0.6))
        self.sliderDefaultButton = Button(text="Domyslne", font_size=self.buttonFontSize, size_hint=(1, 0.6))
        sliderButtonLayout = BoxLayout(orientation='horizontal')
        sliderButtonLayout.add_widget(self.sliderConfirmButton)
        sliderButtonLayout.add_widget(self.sliderDefaultButton)
        sliderLayout.add_widget(self.some_label)
        sliderLayout.add_widget(self.fontSlider)
        sliderLayout.add_widget(sliderButtonLayout)
        self.fontPopup = Popup(title='czcionka',auto_dismiss=False,
                      content=sliderLayout,
                      size_hint=(0.7, 0.3),
                      # size=(400, 200)
                      )
        self.sliderConfirmButton.bind(on_press=self.setConfigFont)
        self.sliderDefaultButton.bind(on_press=self.setDefaultFont)
        self.fontPopup.open()

    def onSliderValueChange(self, btn, value):
        self.buttonFontSize = value
        self.some_label.text = 'Rozmiar czcionki '+str(value)
        self.firstNumberspinner.font_size = value
        self.secondNumberspinner.font_size = value
        self.mathSpinner.font_size = value
        self.binButton.font_size = value
        self.decButton.font_size = value
        self.hexButton.font_size = value
        self.naviOneOperationToggle.font_size = value
        self.naviTwoOperationToggle.font_size = value
        self.convertButton.font_size = value
        self.pipeToggle.font_size = value
        self.naviFontButton.font_size = value
        self.sliderConfirmButton.font_size = value
        self.sliderDefaultButton.font_size = value

    def setDefaultFont(self, btn):
        value = self.defaultFont
        self.fontSlider.value = value
        self.some_label.text = 'Rozmiar czcionki ' + str(value)
        self.firstNumberspinner.font_size = value
        self.secondNumberspinner.font_size = value
        self.mathSpinner.font_size = value
        self.binButton.font_size = value
        self.decButton.font_size = value
        self.hexButton.font_size = value
        self.naviOneOperationToggle.font_size = value
        self.naviTwoOperationToggle.font_size = value
        self.convertButton.font_size = value
        self.pipeToggle.font_size = value
        self.naviFontButton.font_size = value
        self.sliderConfirmButton.font_size = value
        self.sliderDefaultButton.font_size = value


    def getConfigFont(self, btn):
        return self.config.getSettings('font_size')

    def setConfigFont(self, btn):
        self.config.setSettings('font_size', str(self.convertButton.font_size))
        self.fontPopup.dismiss()


    def layTheSpace(self):
        for index in xrange(len(self.firstResultList)):
            number = self.firstResultList[index]
            number = number[::-1]
            pipeNumber = ''
            for i in xrange(len(number)):
                pipeNumber += number[i]
                if (i + 1) % 4 == 0 and i != len(number) - 1:
                    pipeNumber += ' '
            # print (pipeNumber[::-1])
            self.firstResultList[index] = pipeNumber[::-1]

    def layThePipe(self):
        for index in xrange(1, len(self.firstResultList)):
            number = self.firstResultList[index].replace(' ','')
            number = number[::-1]
            pipeNumber = ''
            for i in xrange(len(number)):
                pipeNumber += number[i]
                if (i + 1) % 4 == 0 and i != len(number) - 1:
                    pipeNumber += ' | '
            # print (pipeNumber[::-1])
            self.firstResultList[index] = pipeNumber[::-1]

    def delThePipe(self, btn):
        for index in xrange(1, len(self.firstResultList)):
            self.firstResultList[index] = self.firstResultList[index].replace(' | ', ' ')

    def checkThePipe(self, btn):
        print (btn.state)
        # print (btn.background_color)
        if btn.state == 'down' and self.firstResultList[0] != 'Nie podales liczby':
            self.layThePipe()
        else:
            self.delThePipe(btn)
        self.buildTest(self.resultButtons[self.buttonPressed])

    def naviOptionOne(self, btn):
        # self.naviTwoOperationButton.background_color = (1, 1, 1, 0.15)
        # self.naviOneOperationButton.background_color = (1, 1, 1, 1)
        self.mathSpinner.text = 'brak'
        self.secondNumberspinner.choice = 'Wybierz'
        self.secondNumberspinner.text = 'Wybierz'
        self.secondTextInput = ''

        if len(self.twoOperationLayout.children) != 0:
            # self.secondTextInput.text = ''
            while len(self.twoOperationLayout.children) != 0:
                self.twoOperationLayout.remove_widget(self.twoOperationLayout.children[0])
            #self.math_spinner

        return


    def naviOptionTwo(self, btn):
        # self.naviTwoOperationButton.background_color = (1, 1, 1, 1)
        # self.naviOneOperationButton.background_color = (1, 1, 1, 0.15)

        self.mathSpinner.text = 'brak'

        if len(self.twoOperationLayout.children) == 0:
            self.secondTextInput = ''
            # while len(self.twoOperationLayout.children) != 0:
            #     self.twoOperationLayout.remove_widget(self.twoOperationLayout.children[0])
            #self.math_spinner
            self.secondTextInput = ModuleTextInput(multiline=False, size_hint=(.745, .1), use_bubble=True, bubble_pos=23,
                                             pos_hint={'top': self.firstTextInput.pos_hint['top'] - .105,
                                                       'x': self.firstNumberspinner.pos_hint['right'] - .98},
                                             hint_text="(opcjonalne)Wprowadz druga liczbe")
            self.twoOperationLayout.add_widget(self.secondTextInput)
            self.twoOperationLayout.add_widget(self.secondNumberspinner)
            self.mathSpinnerLabel = Label(text='Wybierz dzialanie', size_hint=(.33, .20),
                                          pos_hint={'top': self.firstTextInput.pos_hint['top'] - .13, 'x': .01})
            self.twoOperationLayout.add_widget(self.mathSpinnerLabel)
            self.twoOperationLayout.add_widget(self.mathSpinner)
        return


    def changeColor(self, btn):
        for button in self.resultButtons:
            if button == btn:
                button.background_color = (1, 1, 1, 1)
            else:
                button.background_color = (1, 1, 1, 0.5)
                button.background_color = (1, 1, 1, 0.5)



    def buildTest(self, btn):

        self.changeColor(btn)
        for name, number in self.resultDict.items():
            if btn.text == name:
                self.resultTextOutput.text = self.firstResultList[number]
                self.buttonPressed = number
                break

        #print buttonPressed
        return btn.text



    def createSpinners(self):
        self.firstNumberspinner = MySpinner(
            # default value shown
            text='System\nliczbowy',
            # available values
            values=('Dec', 'Bin', 'Hex'),
            text_align='center',
            font_size=self.buttonFontSize,
            # bold = True,
            # text_size= (spinner.width, None),
            # size: self.texture_size
            # just for positioning in our example
            size_hint=(.23, .1),
            pos_hint={'top': 0.99, 'right': .99})
        self.firstNumberspinner.choice = "Wybierz"
        self.firstNumberspinner.bind(text = self.firstNumberspinner.setChoice)

        self.secondNumberspinner = MySpinner(
            # default value shown
            text=' System\nliczbowy',
            # available values
            values=('Dec', 'Bin', 'Hex', 'Wybierz'),
            font_size=self.buttonFontSize,
            # just for positioning in our example
            size_hint=(.23, .1),
            pos_hint={'top': self.firstNumberspinner.pos_hint['top'] - .105, 'right': self.firstNumberspinner.pos_hint['right']})
        self.secondNumberspinner.choice = "Wybierz"
        self.secondNumberspinner.bind(text=self.secondNumberspinner.setChoice)

        self.mathSpinner = MySpinner(
            # default value shown
            text='brak',
            # available values
            font_size=self.buttonFontSize,
            values=('brak', '+', '-', '*', '/'),
            # just for positioning in our example
            size_hint=(.2, .10),
            pos_hint={'top': 0.74, 'x': .07})

    # def pause_tutorial_arrow(self, btn):
    #     while len(self.tutorialLayout.children) != 0:
    #         self.tutorialLayout.remove_widget(self.tutorialLayout.children[0])

    def on_pause(self):
        #self.textoutput_result.save(path=".", filename=PAUSE_FILE_NAME)
        return True  # app sleeps until resume return False to stop the app

    def on_stop(self):
        pass

    def on_resume(self):
        #self.textoutput_result.load(path=".", filename=PAUSE_FILE_NAME, store_save=False)
        pass

    def tutorial_arrow(self, btn):
        # print len(self.tutorialLayout.children), " lenght before"
        while len(self.tutorialLayout.children) != 0:
            self.tutorialLayout.remove_widget(self.tutorialLayout.children[0])

        if len(self.tutorialLayout.children) == 0:
            if platform == 'win' or platform == 'linux':
                self.tutorial_arrow_image = Image(source=os.path.join(os.getcwd(), 'images', 'tutorial_arrow.png'), size_hint_y=None, height=Window.width/16,
                                        pos_hint={'x': .46, 'top': self.firstNumberspinner.pos_hint['top'] - .22})
            else:
                self.tutorial_arrow_image = Image(source=os.path.join(os.getcwd(), 'images', 'tutorial_arrow.png'), size_hint_y=None,
                                                  height=Window.width / 9,
                                                  pos_hint={'x': .41, 'top': self.firstNumberspinner.pos_hint['top'] - .22})
            self.tutorialLayout.add_widget(self.tutorial_arrow_image)
            anim = Animation(y=-10, duration = .6) + Animation(y=10, duration = .4)
            anim.repeat = True
            anim.start(self.tutorialLayout)

    def playTutorial(self):
        # print len(self.tutorialLayout.children)
        while len(self.tutorialLayout.children) != 0:
            self.tutorialLayout.remove_widget(self.tutorialLayout.children[0])
        # print len(self.tutorialLayout.children)
        if len(self.tutorialLayout.children) == 0:
            # print "WCHODZI DO BUDOWY"
            self.tutorial_arrow(self)

    def checkDEC(self, number):
        try:
            int(number)
            return True
        except ValueError:
            self.showPopup('Nie poprawna liczba Decymalna', number)
            return False

    def checkBIN(self, number):
        try:
            int(number, 2)
            return True
        except ValueError:
            self.showPopup('Nie poprawna liczba Binarna', number)
            return False

    def checkHEX(self, number):
        try:
            int(number, 16)
            return True
        except ValueError:
            self.showPopup('Nie poprawna liczba Hexadecymalna', number)
            return False

    # def printResult(self, numberArray):
    #     print ('dec = {0}, bin = {1}, hex = {2}'.format(numberArray[0], numberArray[1], numberArray[2]))
    def printResult(self, number):
        decNumber = str(number)
        if number >= 0:
            binNumber = str(bin(number)[2:])
            hexNumber = str(hex(number)[2:]).upper().rstrip("L")
        else:
            binNumber = '-'+str(bin(number)[3:])
            hexNumber = '-'+str(hex(number)[3:]).upper()

        self.firstResultList = [decNumber, binNumber, hexNumber]
        self.checkThePipe(self.pipeToggle)
        if self.pipeToggle.state == 'normal':
            self.layTheSpace()

        # print(self.buttonPressed)
        self.resultTextOutput.text = self.firstResultList[self.buttonPressed]
        print ('dec = {0}, bin = {1}, hex = {2}'.format(decNumber, binNumber, hexNumber))

    def printError(self):
        self.firstResultList = ['Nie podales liczby', 'Nie podales liczby', 'Nie podales liczby']
        self.resultTextOutput.text = 'Nie podales liczby'

    def operiationOne(self):
        print (self.firstNumberspinner.choice)
        number = self.firstTextInput.text
        print (self.firstTextInput.text)
        if self.firstNumberspinner.choice == 'Dec':
            if self.checkDEC(number):
                number = int(number)
                # self.printResult(number)
            else:
                self.printError()
                return
        elif self.firstNumberspinner.choice == 'Bin':
            if self.checkBIN(number):
                number = int(number, 2)
                # self.printResult(number)
            else:
                self.printError()
                return
        elif self.firstNumberspinner.choice == 'Hex':
            if self.checkHEX(number):
                number = int(number, 16)
                # self.printResult(number)
            else:
                self.printError()
                return
        self.printResult(number)

    def operationTwo(self):
        if self.secondNumberspinner.choice == 'Wybierz' and self.secondTextInput.text == '' and self.mathSpinner.text == "brak":
            self.operiationOne()
            return
        if self.secondNumberspinner.choice == 'Wybierz':
            self.showPopup('Nie wybrales systemu liczbowego', 'Dolne okno')
            return
        if self.secondTextInput.text == '':
            self.showPopup('Nie podales liczby', 'Brak liczby')
            return
        if self.mathSpinner.text == "brak":
            self.showPopup('Nie wybrales dzialania')
            return

        print (self.firstNumberspinner.choice, self.firstTextInput.text)
        print (self.secondNumberspinner.choice, self.secondTextInput.text)

        firstNumber = self.firstTextInput.text
        secondNumber = self.secondTextInput.text
        if self.firstNumberspinner.choice == 'Dec':
            if self.checkDEC(firstNumber):
                firstNumber = int(firstNumber)
            else:
                self.printError()
                return
        elif self.firstNumberspinner.choice == 'Bin':
            if self.checkBIN(firstNumber):
                firstNumber = int(firstNumber, 2)
            else:
                self.printError()
                return
        elif self.firstNumberspinner.choice == 'Hex':
            if self.checkHEX(firstNumber):
                firstNumber = int(firstNumber, 16)
            else:
                self.printError()
                return
#---------------------------------------------------------------------------
        if self.secondNumberspinner.choice == 'Dec':
            if self.checkDEC(secondNumber):
                secondNumber = int(secondNumber)
            else:
                self.printError()
                return
        elif self.secondNumberspinner.choice == 'Bin':
            if self.checkBIN(secondNumber):
                secondNumber = int(secondNumber, 2)
            else:
                self.printError()
                return
        elif self.secondNumberspinner.choice == 'Hex':
            if self.checkHEX(secondNumber):
                secondNumber = int(secondNumber, 16)
            else:
                self.printError()
                return

        print (firstNumber,self.mathSpinner.text, secondNumber)

        try:
            number = eval(str(firstNumber) + str(self.mathSpinner.text) + str(secondNumber))
            self.printResult(number)
        except SyntaxError:
            self.showPopup('Nie poprawna liczba w dzialaniu')



    def showPopup(self, text, title=''):
        popup = Popup(title=title,
                      content=Label(text=text),
                      size_hint=(0.7, 0.3),
                      # size=(400, 200)
                      )
        popup.open()

    def manageFunctions(self, btn):
        firstNumberSystem = self.firstNumberspinner.choice
        # print (self.pipeToggle.state)
        # print(firstNumberSystem)
        if firstNumberSystem == 'Wybierz':
            self.showPopup('Nie wybrales systemu liczbowego', 'Gorne okno')
            self.playTutorial()
            return
        else:
            while len(self.tutorialLayout.children) != 0:
                self.tutorialLayout.remove_widget(self.tutorialLayout.children[0])

        if not self.firstTextInput.text:
            self.showPopup('Nie podales liczby', 'Brak liczby')
            return

        if len(self.twoOperationLayout.children) == 0:
            self.operiationOne()
        else:
            self.operationTwo()


class MySpinner(Spinner):
    def setChoice(self, instance, data, *largs):
        self.choice = self.text



if __name__=='__main__':
    MyApp().run()