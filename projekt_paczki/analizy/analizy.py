import pandas as pd

#funkcja która grupuje dane względem roku i parametru target (w analizach zazwyczaj jest to 'Country') oraz zwraca 5 najwyższych w każdym roku
#korzystamy z niej 2 razy - przy analizie emisji co2 oraz przychodzie na mieszkańca
def top_5_na_rok(dane,index,target,total):
    wynik = dane.set_index(index).groupby(['Year'])[target].nlargest(5)
    wynik = pd.DataFrame(wynik).reset_index()
    wynik = wynik.merge(dane[['Year',index,total]])
    return wynik

#Funcja która liczy różnicę wartości target w latach start-end
def diff(dane, start, end, by, target):
    if(end<=start):
        return(pd.DataFrame())
    else:
        pocz = dane[dane['Year'] == start][[by, target]]
        kon = dane[dane['Year'] == end][[by, target]]

        both = list(set(pocz[by]) & set(kon[by]))
        pocz = pocz[pocz[by].isin(both)].sort_values(by).reset_index()
        kon = kon[kon[by].isin(both)].sort_values(by).reset_index()

        roznica = pd.DataFrame()
        roznica[by] = pocz[by]
        roznica['Diff_'+target] = kon[target] - pocz[target]
        roznica = roznica.sort_values('Diff_'+target)

        print('Usunięto z powodu braku danych w podanych latach:')
        print(list(set(dane[by]).difference(set(roznica[by].dropna()))))
        roznica = roznica.dropna()

        return (roznica)