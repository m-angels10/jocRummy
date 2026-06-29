import random
import os

def carregar_dades(ruta_fitxer):
    poblacions = []
    comarques_set = set()
    
    if not os.path.exists(ruta_fitxer):
        print(f"Error: No s'ha trobat el fitxer '{ruta_fitxer}'.")
        print("Assegura't de guardar el llistat en el mateix lloc amb el nom correcte.")
        return None, None

    with open(ruta_fitxer, 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia or ',' not in linia:
                continue
            # Separem per la coma i netegem espais
            poblacio, comarca = linia.split(',', 1)
            poblacio = poblacio.strip()
            comarca = comarca.strip()
            
            poblacions.append((poblacio, comarca))
            comarques_set.add(comarca)
            
    return poblacions, list(comarques_set)

def jugar():
    fitxer_dades = "poblacions.txt"
    poblacions, totes_comarques = carregar_dades(fitxer_dades)
    
    if not poblacions:
        return

    puntuacio = 0
    fetes = 0
    
    print("=========================================")
    print("      BENVINGUT AL JOC DE LES COMARQUES  ")
    print("=========================================\n")
    print(f"S'han carregat {len(poblacions)} poblacions correctament.\n")
    print("Escriu 'eixir' en qualsevol moment per a acabar.\n")

    # Barregem les preguntes per a que no siguen sempre iguals
    random.shuffle(poblacions)

    for poblacio, comarca_correcta in poblacions:
        print(f"Pregunta {fetes + 1}: De quina comarca és '{poblacio}'?")
        
        # Generem 3 respostes incorrectes falses
        altres_comarques = [c for c in totes_comarques if c != comarca_correcta]
        if len(altres_comarques) < 3:
            print("Error: Calen almenys 4 comarques diferents al fitxer de text.")
            break
            
        opcions_falses = random.sample(altres_comarques, 3)
        
        # Juntem la correcta amb les falses i les barregem
        opcions = opcions_falses + [comarca_correcta]
        random.shuffle(opcions)
        
        # Mostrem les opcions a l'usuari
        for i, opcio in enumerate(opcions, 1):
            print(f"  {i}. {opcio}")
            
        # Validació de la resposta de l'usuari
        while True:
            resposta = input("\nTria una opció (1-4): ").strip()
            
            if resposta.lower() == 'eixir':
                print(f"\nJoc acabat! Puntuació final: {puntuacio}/{fetes}")
                return
                
            if resposta in ['1', '2', '3', '4']:
                index_triat = int(resposta) - 1
                if opcions[index_triat] == comarca_correcta:
                    print("¡CORRECTE! 🌟\n")
                    puntuacio += 1
                else:
                    print(f"INCORRECTE... ❌ La resposta correcta era: {comarca_correcta}\n")
                fetes += 1
                break
            else:
                print("Per favor, introduïx un número de l'1 al 4 o 'eixir'.")
        
        print("-" * 40)

    print(f"Has completat totes les preguntes! Puntuació final: {puntuacio}/{fetes}")

if __name__ == "__main__":
    jugar()
