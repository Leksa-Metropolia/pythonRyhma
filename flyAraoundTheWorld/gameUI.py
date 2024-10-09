from random import randint

#metodi nayttamaan pelin aloitus sivun
def gameMainMenu(game):
    print(f"Tervetuloa pelaamaan Fly Around the World -peliä!")
    print(f"Päävalikko:")
    print(f"1. Aloita uusi peli")
    print(f"2. Lopeta")
    query = f"Mitä tehdään?"
    exp = ['1', '2']
    input = inputCheck(query, exp)
    if input == 1:
        setName = input(f"Anna pelaajanimi: ")
        game.pelaaja.Name = setName
        query = f"Mikä reitti pelataan? (0-3, 0 on satunnainen)"
        exp = [0, 1, 2, 3]
        input = inputCheck(query, exp)
        if input == 0:
            input = randint(1, 3)
        game.route = game.routes[input]
        game.setStartLocation()
        gameActiveMenu(game)

    #nayta vaitoehdot pelaajalle: pelin aloitus, high score lista ja lopeta ohjelma

#metodi nayttamaan pelin kulun sivun
def gameActiveMenu(game):
    remaining = game.remainingCountries()
    choices = []
    if game.pelaaja.Funds < game.hintaY and not game.canFinish():
        gameEndFailure(game)
    if game.pelaaja.LastSlept < 17*60 and len(game.getValidAirports()) > 0 and game.airportOpen():
        a = "1. Lennä"
        choices.append(a)
    elif game.pelaaja.Funds > game.hintay and game.pelaaja.LastSlept > 0:
        a = "2. Yövy"
        choices.append(a)
    elif not game.airportOpen():
        a = "3. Odota"
        choices.append(a)



    print(f"Sijainti: {game.pelaaja.Airport[1]}, {game.pelaaja.Country}")
    print(f"Rahaa jäljellä: {game.pelaaja.Funds}")
    print(f"Reitillä vielä vierailtavat maat: {remaining}")
    print(f"Aika: {game.time}")
    print(f"Vaihtoehdot:")
    print(f"1. Lennä")
    print(f"2. Yövy hinta: {game.hintaY}")
    print(f"3. Odota lentokentän aukeamista")
    print(f"4. Lopeta peli kesken")
    query = "Mitä tehdään? "
    exp = [1, 2, 3, 4]
    input = inputCheck(query, exp)


    #nayta pelaajan tiedot
    #nayta vaihtoehdot pelaajalle:
    #lenna: avaa syoteenoton lentokohteen valinnaelle
    #yovy
    #odota
    #lopeta peli ja palaa paa valikkoon
    #ottaa vastaan kayttajasyotteen ja kutsuu oikeaa funktiota

#metodi nayttamaan pelin loppu sivun
def gameEndSuccess(game):
    DUMMY = 0
    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    #nayta pelaajan pistetulos
    #siirra pelaaja paavalikkoon ENTERia painamalla

def gameEndFailure(game):
    DUMMY = 0
    #nayta pelaajan kaymien valtioiden, mannerten ja lentokenttien maarat
    #siirra pelaaja paavalikkoon ENTERia painamalla

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