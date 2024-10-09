from random import randint
import os
import numpy as np

#metodi nayttamaan pelin aloitus sivun
def gameMainMenu(game):
    clearTerminal() #Tyhjennetään terminaali ennenkuin jatketaan
    print(f"Tervetuloa pelaamaan Fly Around the World -peliä!")
    print(f"Päävalikko:")
    print(f"1. Aloita uusi peli")
    print(f"2. Lopeta")
    query = f"Mitä tehdään? "
    exp = ['1', '2']
    syote = inputCheck(query, exp)
    if syote == '1':
        setName = input("Anna pelaajanimi: ")
        game.pelaaja.Name = setName
        query = f"Mikä reitti pelataan? (0-3, 0 on satunnainen)"
        exp = ['0', '1', '2', '3']
        syote = inputCheck(query, exp)
        syote = int(syote)
        if syote == 0:
            syote = randint(1, 3)
        game.route = game.routes[syote - 1]
        game.setStartLocation()
        gameActiveMenu(game)

    #nayta vaitoehdot pelaajalle: pelin aloitus, high score lista ja lopeta ohjelma

#metodi nayttamaan pelin kulun sivun
def gameActiveMenu(game):
    clearTerminal()
    remaining = game.remainingCountries()
    choices = []
    exp = ['4']

    if len(remaining) == 0 and game.pelaaja.Airport == game.pelaaja.Start:
        gameEndSuccess(game)
    elif game.pelaaja.Funds < game.hintaY and not game.canFinish():
        gameEndFailure(game, 'varat')

    if game.pelaaja.LastSlept < 17*60 and len(game.getValidAirports()) > 0 and game.airportOpen():
        a = "1. Lennä"
        exp.append('1')
        choices.append(a)
    elif game.pelaaja.Funds > game.hintay and game.pelaaja.LastSlept > 0:
        a = "2. Yövy"
        exp.append('2')
        choices.append(a)
    elif not game.airportOpen():
        a = "3. Odota"
        exp.append('3')
        choices.append(a)

    print(f"Sijainti: {game.pelaaja.Airport['name']}, {game.pelaaja.Country}")
    print(f"Rahaa jäljellä: {game.pelaaja.Funds}")
    print(f"Reitillä vielä vierailtavat maat: {remaining}")
    print(f"Aika: {game.time}")
    print(f"Vaihtoehdot:")
    for choice in choices:
        print(choice)
    query = "Mitä tehdään? "
    syote = inputCheck(query, exp)
    if syote == '1':
        selectFlight(game)
    elif syote == '2':
        game.sleep()
        gameActiveMenu(game)
    elif syote == '3':
        game.wait()
        gameActiveMenu(game)

    #nayta pelaajan tiedot
    #nayta vaihtoehdot pelaajalle:
    #lenna: avaa syoteenoton lentokohteen valinnaelle
    #yovy
    #odota
    #lopeta peli ja palaa paa valikkoon
    #ottaa vastaan kayttajasyotteen ja kutsuu oikeaa funktiota

#metodi nayttamaan pelin loppu sivun
def gameEndSuccess(game):
    clearTerminal()
    print("Onnittelut! Voitit pelin.")
    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    print(f"Vierailit näillä lentokentillä: {len(game.pelaaja.Airports)}")
    print(f"Vierailit näissä maissa: {len(game.pelaaja.Countries)}")
    print(f"Vierailit näillä mantereilla: {len(game.pelaaja.Continents)}")
    #nayta pelaajan pistetulos
    final_score = game.finalScore()
    print(f"Lopullinen pistemääräsi on: {final_score}")
    #siirra pelaaja paavalikkoon ENTERia painamalla
    input("Paina ENTER siirtyäksesi takaisin päävalikkoon.")
    gameMainMenu(game)

def gameEndFailure(game, syy):
    clearTerminal()
    print("Voi ei, hävisit pelin.")

    if syy == "varat":
        print("Rahasi loppuivat kesken.")

    elif syy == "aika":
        print("Aikasi loppui kesken, et saavuttanut tavoitettasi ajoissa.")

    else:
        print("Tuntematon syy. Peli päättyi.")

    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    print(f"Vierailit näillä lentokentillä: {len(game.pelaaja.Airports)}")
    print(f"Vierailit näissä maissa: {len(game.pelaaja.Countries)}")
    print(f"Vierailit näillä mantereilla: {len(game.pelaaja.Continents)}")
    final_score = game.finalScore()
    print(f"Lopullinen pistemääräsi on: {final_score}")
    #siirra pelaaja paavalikkoon ENTERia painamalla
    input("Paina ENTER siirtyäksesi takaisin päävalikkoon.")
    gameMainMenu(game)

#metodi tarkistamaan pelaajan syotteen ja kutsumaan edellisen syote rivin uudelleen jos ei validi syote pelaajalta
def inputCheck(query, expected):
    syote = input(query)
    if not syote in expected:
        print(f"Odottamaton syöte. Yritä uudelleen.")
        inputCheck(query, expected)
    else:
        return syote

    #tarkistaa, etta syote on odotettu ja pyytaa syotteen udelleen jos ei ole

#metodit ottamaan vastaan pelaajansyotteet
def selectFlight(game):
    flights = game.getValidAirports()
    continents = []
    for airport in flights:
        continents.append(airport['continent'])
    continents = np.unique(continents)

    print(f"Mille mantereelle lennetään?")
    for continent in continents:
        print(f"{continent}")
    syote = inputCheck("Manner: ", continents)
    countries = []
    for airport in flights:
        if syote == airport['country']:
            countries.append(airport['country'])

    print(f"Mihin maahan lennetään?")
    for country in countries:
        print(f"{country}")
    syote = inputCheck("Maa: ", countries)
    kentat = []
    for airport in flights:
        if syote == airport['country']:
            kentat.append(airport)

    print(f"Mille kentälle lennetään?")
    exp = []
    for airport in kentat:
        exp.append(airport['icao'])
        print(f"{airport['icao']} {airport['name']}")
    syote = inputCheck("Anna kentän ICAO-koodi: ", exp)
    kohde = None
    for airport in kentat:
        if syote == airport['icao']:
            kohde = airport
    game.fly(kohde)
    gameActiveMenu(game)
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
def clearTerminal():
    #tyhjentaa terminaalin tekstista ennen seuraavan valikon tulostamista
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix-pohjaiset (Linux, macOS)
        os.system('clear')