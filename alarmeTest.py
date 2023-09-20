from mpython import *
import ntptime
from machine import Timer
import music

#Modulo de UI
ui = UI(oled)

#Dimensoes centrais da tela 128x64
centerX = 63
centerY = 31

#Tela inicial
opc = ["inicio", "Opcoes", "RGB", "Lanterna", "Piano", "CardPlay"]
tela = opc[0]
i = 0

#conexao WiFi
my_wifi = wifi()

try:
    oled.DispChar("Carregando...", 24, 16)
    for c in range(20):
        ui.ProgressBar(14, 32, 100, 16, c)
        oled.show()
        
    #Conectando ao wifi
    my_wifi.connectWiFi("Nome da rede", "Senha")
    for c in range(20, 60, 2):
        ui.ProgressBar(14, 32, 100, 16, c)
        oled.show()
    
    #Modulo de data/hora
    ntptime.settime(-4) #(p1 = fuso horario, p2 = servidor(ntp.ntsc.ac.cn))
    for c in range(60, 100):
        ui.ProgressBar(14, 32, 100, 16, c)
        oled.show()
except OSError :
    oled.fill(0)
    oled.DispChar("Erro de inicializacao", 0, 20)
    oled.show() 
else: 
    
    #Funcao para setar data e horario
    def getTime(_):
        oled.fill(0)
        t = time.localtime()
        oled.DispChar("{}/{}/{}".format(t[2], t[1], t[0]), 34, 0)
        oled.DispChar("{:02d}:{:02d}".format(t[3], t[4]), 50, 16)
        oled.show()
    
    def menu(i):
        print(i)
        oled.fill(0)
        oled.DispChar(opc[i], 0, 0, 2)
        try:
            oled.DispChar(opc[i+1], 0, 16)
        except:
            pass
        try:
            oled.DispChar(opc[i+2], 0, 32)
        except:
            pass
        oled.show()
        
        while True:
            if button_a.value() == 0:
                tela = opc[i]
                break
            elif button_b.value() == 0:
                print(len(opc))
                i = i+1 if i+1 <= (len(opc)-1) else 0
                return menu(i)
        
        return tela
    
    
    #Inicializando modulo Timer - Machine
    tim = Timer(1)
    
    while True:
        
        if tela == "inicio":
            
            #Inicializando horario, reseta a cada segundo periodicamente usando a funcao getTime()
            tim.init(period=1000, mode=Timer.PERIODIC, callback=getTime)
            while True:
                
                if button_b.value() == 0:
                    tela = "Opcoes"
                    break
        
        elif tela == "Opcoes":
            tim.deinit()
            
            tela = menu(0)
            print(tela)
        
        elif tela == "RGB":
            
            #Desligando a funcao de horario
            tim.deinit()
            oled.fill(0)
            oled.DispChar("Use os touch pads para acender os leds", 0, 0, 1, True)
            oled.show()
            while True:
                #Voltar para tela inicial
                if button_b.value() == 0:
                    tela = "Opcoes"
                    rgb[0] = (0, 0, 0)
                    rgb[1] = (0, 0, 0)
                    rgb[2] = (0, 0, 0)
                    rgb.write()
                    break
            
                #Brincadeira para usar os leds
                if(touchPad_P.read() < 100):
                    rgb[0] = (255,0,0)    
                    rgb[1] = (255,0,0) 
                    rgb[2] = (255,0,0) 
                    rgb.write()
                elif(touchPad_Y.read() < 100):
                    rgb[0] = (0,255,0) 
                    rgb[1] = (0,255,0)
                    rgb[2] = (0,255,0)
                    rgb.write()
                elif(touchPad_T.read() < 100):
                    rgb[0] = (0,0,255) 
                    rgb[1] = (0,0,255)
                    rgb[2] = (0,0,255)
                    rgb.write()
                elif(touchPad_H.read() < 100):
                    rgb[0] = (255,255,0) 
                    rgb[1] = (255,255,0)
                    rgb[2] = (255,255,0)
                    rgb.write()
                elif(touchPad_O.read() < 100):
                    rgb[0] = (255,0,255) 
                    rgb[1] = (255,0,255)
                    rgb[2] = (255,0,255)
                    rgb.write()
                elif(touchPad_N.read() < 100):
                    rgb[0] = (0,0,0) 
                    rgb[1] = (0,0,0)
                    rgb[2] = (0,0,0)
                    rgb.write()
        
        elif tela == "Lanterna":
            #Desligando a funcao de horario
            tim.deinit()
            oled.fill(0)
            oled.DispChar("Lanterna", 0, 0, 1, True)
            oled.show()
            
            #ligar led para representar uma lanterna
            rgb[0] = (255, 255, 255)
            rgb[1] = (255, 255, 255)
            rgb[2] = (255, 255, 255)
            rgb.write()
            while True:
                #Voltar para tela inicial
                if button_b.value() == 0:
                    tela = "Opcoes"
                    rgb[0] = (0, 0, 0)
                    rgb[1] = (0, 0, 0)
                    rgb[2] = (0, 0, 0)
                    rgb.write()
                    break
                
                
                
        elif tela == "Piano":
            #Desligando a funcao de horario
            tim.deinit()
            oled.fill(0)
            oled.DispChar("Piano", 0, 0)
            oled.show()
            
            while True:
                #Voltar para tela inicial
                if button_b.value() == 0:
                    tela = "Opcoes"
                    break
                
                #Se touchPad"_x" for tocado
                if(touchPad_P.read() < 100):
                    #Nota[Octavo][:Duracao]
                    music.play('C3:1')
                if(touchPad_Y.read() < 100):
                    music.play('D3:1')
                if(touchPad_T.read() < 100):
                    music.play('E3:1')
                if(touchPad_H.read() < 100):
                    music.play('F3:1')
                if(touchPad_O.read() < 100):
                    music.play('G3:1')
                if(touchPad_N.read() < 100):
                    music.play('A3:1')
        
        elif tela == "CardPlay":
            #Desligando a funcao de horario
            tim.deinit()
            oled.fill(0)
            oled.DispChar("CardPlay", 0, 0)
            oled.show()
            
            while True:
                #Voltar para tela inicial
                if button_b.value() == 0:
                    tela = "Opcoes"
                    break
                
                #Inicialmente foi pensado uma forma de ler o que foi falado e checar a palavra porem o microfone apensa le frequencia
                oled.DispChar(str(sound.read()), 0, 32)
                oled.show()
            
    