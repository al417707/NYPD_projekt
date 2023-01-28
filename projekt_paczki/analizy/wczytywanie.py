import pandas as pd

def wczytaj(GDP, pop, co2, poczatek, koniec, correction):
    GDP1 = pd.read_csv(GDP, skiprows=4)
    Pop1 = pd.read_csv(pop, skiprows=3)
    co2 = pd.read_csv(co2)

    # czyszczenie danych
    # usuwam niepotrzebne kolumny
    GDP1.drop('Unnamed: 66', axis=1, inplace=True)
    Pop1.drop('Unnamed: 66', axis=1, inplace=True)

    # zmieniam nazwy krajów na same wielkie litery - tak by format we wszystkich tabelkach był identyczny
    GDP1['Country Name'] = GDP1['Country Name'].str.upper()
    Pop1['Country Name'] = Pop1['Country Name'].str.upper()

    # Zauważmy, że nazwy w GDP1 i Pop1 są w takim samym formacie, ale już co2 ma inny format. Trzeba nanieść ręczne poprawki
    co2['Country'].replace(correction, inplace=True)

    # nazwy które wypadają z różnych powodów zapisuję do pliku:
    pd.DataFrame(set(GDP1['Country Name']).symmetric_difference(set(co2['Country']))).to_csv('odrzucone_kraje.csv',
                                                                                             index=False)

    # wybór lat:
    GDP_yrs = [int(x) for x in list(GDP1.columns[4:])]
    Pop_yrs = [int(x) for x in list(Pop1.columns[4:])]
    co2_yrs = [int(x) for x in list(co2['Year'])]

    # bierzemy tylko te lata które są we wszystkich tabelach
    yrs = list(set(GDP_yrs).intersection(set(Pop_yrs)).intersection(set(co2_yrs)))
    yrs = sorted(filter(lambda x: x >= poczatek and x <= koniec, yrs))

    if len(yrs) == 0: print('Dla takiego przedziału lat nie ma danych')

    co2 = co2[co2.Year.isin(yrs)].reset_index(drop=True)
    Pop1 = Pop1[list(Pop1.columns[:4]) + [str(x) for x in yrs]]
    GDP1 = GDP1[list(GDP1.columns[:4]) + [str(x) for x in yrs]]

    # merge tabel
    Pop1_melted = Pop1.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                            var_name='Year', value_name='Population')
    GDP1_melted = GDP1.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                            var_name='Year', value_name='GDP')

    Dane = Pop1_melted.merge(GDP1_melted, on=['Country Name', 'Country Code', 'Year'], suffixes=['_Pop', '_GDP'])
    Dane.rename(columns={'Country Name': 'Country'}, inplace=True)
    Dane = Dane.astype({'Year': 'int64'})
    Dane = Dane.merge(co2, on=['Country', 'Year'])

    return (Dane)
