#metodi nayttamaan pelin aloitus sivun
def gameMainMenu():
    DUMMY = 0
    #nayta vaitoehdot pelaajalle: pelin aloitus, high score lista ja lopeta ohjelma

#metodi nayttamaan pelin kulun sivun
def gameActiveMenu():
    DUMMY =0
    #nayta pelaajan tiedot
    #nayta vaihtoehdot pelaajalle:
    #lenna: avaa syoteenoton lentokohteen valinnaelle
    #yovy
    #odota
    #lopeta peli ja palaa paa valikkoon
    #ottaa vastaan kayttajasyotteen ja kutsuu oikeaa funktiota

#metodi nayttamaan pelin loppu sivun
def gameEndSuccess():
    DUMMY = 0
    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    #nayta pelaajan pistetulos
    #siirra pelaaja paavalikkoon ENTERia painamalla

def gameEndFailure():
    DUMMY = 0
    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    #siirra pelaaja paavalikkoon ENTERia painamalla

#metodi tarkistamaan pelaajan syotteen ja kutsumaan edellisen syote rivin uudelleen jos ei validi syote pelaajalta
def inputCheck(input, origin):
    DUMMY = 0
    #tarkistaa, etta syote on odotettu ja pyytaa syotteen udelleen jos ei ole

#metodit ottamaan vastaan pelaajansyotteet
def selectFlight(playerLocation):
    DUMMY = 0
    #nayttaa pelaajalle mantereet minne pystytaan lentamaan
    #ottaa vastaan mantereen minne pelaaja haluaa lentaa
    #nayttaa pelaajalle maat minne pystytaan lentamaan valitulla mantereella
    #ottaa vastaan maan minne pelaaja haluaa lentaa
    #nayttaa pelaajalle lentokentat joille pystytaan lentamaan
    #ottaa vastaan lentokentan jolle pelaaja haluaa lentaa
    #lentaa pelaaja valitulle kentalle
    #palaa pelin kulkuvalikkoon

#metodi nayttamaan high score listan
def showHS(origin):
    DUMMY = 0
    #kysyy pelaajalta minka reitin parhaat tulokset halutaan nahda
    #nayttaa pelaajalle reitin 10 parasta tulosta
    #palaa ENTERia painamalla edelliseen valikkoon

#metodi tyhjentamaan komentokehoteeen
def clearTerminal(menu):
    DUMMY = 0
    #tyhjentaa terminaalin tekstista ennen seuraavan valikon tulostamista