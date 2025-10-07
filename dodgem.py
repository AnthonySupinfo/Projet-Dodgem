neutre = 0 
pion1 = 1        
pion2 = 2       
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


# Création du plateau
def newBoard(n):
    board = []        
    i = 0                    
    while i < n:                
        ligne = []                
        j = 0                     
        while j < n:               
            ligne.append(neutre)    
            j = j + 1              
        board.append(ligne)        
        i = i + 1                
    return board                   



# Affichage du plateau
def displayBoard(board, n):
    print("Légende : . =vide | x =Joueur-1 | o =Joueur-2")        
    i = 0                                       
    while i < n:
        print(str(i + 1).rjust(2) + "|", end=" ")
        j = 0                                    
        while j < n:
            val = board[i][j]                    
            if val == neutre:                    
                ch = "."
            elif val == pion1:                     
                ch = "x"
            else:                               
                ch = "o"
            print(ch.rjust(2), end=" ")         
            j = j + 1                            
        print()                                  
        i = i + 1                                
    print("    " + "---" * n)
    print("   ", end=" ")
    j = 1
    while j <= n:
        print(str(j).rjust(2), end=" ")
        j = j + 1
    print()                                      
    print()                                      


# Vérifie si (i, j) est dans le plateau 
def in_bounds(n, i, j):   
    if i < 0:
        return False
    if i >= n:
        return False
    if j < 0:
        return False
    if j >= n:
        return False
    return True


# Place les pions au départ
def init_depart(board, n):
    i = 0
    while i < n - 1:         
        board[i][0] = pion1     
        i = i + 1
    j = 1
    while j < n:            
        board[n - 1][j] = pion2 
        j = j + 1


    # Indique si la direction m est une direction de sortie.
def is_exit_direction(player, m):
    if player == pion1 and m == 2:
        return True
    if player == pion2 and m == 1:
        return True
    return False


# Indique si un pion placé en (i, j) peut sortir en jouant la direction m.
def is_exit_move(n, player, i, j, m):
    if player == pion1 and m == 2 and j == n - 1:
        return True
    if player == pion2 and m == 1 and i == 0:
        return True
    return False


# Interdit le "retour en arrière"
def is_backward(player, m):
    if player == pion1 and m == 4:
        return True
    
    if player == pion2 and m == 3:
        return True
    return False


# Vérifie si le pion du 'player' en (i, j) peut jouer la direction m.
def possibleMove(board, n, directions, player, i, j, m):
    if m < 1 or m > 4:
        return False  
    
    if not in_bounds(n, i, j):
        return False
    
    if board[i][j] != player:
        return False
    
    if is_backward(player, m):
        return False

    if is_exit_move(n, player, i, j, m):
        return True

    di = directions[m - 1][0]  
    dj = directions[m - 1][1]  
    
    ni = i + di                 
    nj = j + dj                 
  
    if not in_bounds(n, ni, nj):
        return False
    
    if board[ni][nj] != neutre:
        return False

    return True


# Vrai si (i, j) contient un pion du joueur ET qu'il a au moins un coup possible.
def possiblePawn(board, n, directions, player, i, j):
    
    if not in_bounds(n, i, j):
        return False
    
    if board[i][j] != player:
        return False

    m = 1
    while m <= 4:
        if possibleMove(board, n, directions, player, i, j, m):
            return True
        m = m + 1
    return False


# Demande à l'utilisateur de choisir un pion du joueur 'player' qui peut bouger.
def selectPawn(board, n, directions, player):
    
    while True:
        raw = input("Joueur " + str(player) + " - pion à déplacer (ligne colonne) : ")
        try:
            morceaux = raw.strip().split()
            li = morceaux[0]
            lj = morceaux[1]
            i = int(li) - 1
            j = int(lj) - 1
        except:
            print("Entrée invalide. Exemple : 2 3")
            continue
        
        if not possiblePawn(board, n, directions, player, i, j):
            print("Ce pion ne peut pas bouger (ou n'est pas à vous).")
            continue
        return (i, j)


# Demande à l'utilisateur une direction m (1,2,3,4) pour le pion (i, j).
def selectMove(board, n, directions, player, i, j):
    
    while True:
        raw = input("Joueur " + str(player) + " - direction pour (" + str(i + 1) + "," + str(j + 1) + ") [1=Haut  2=Droite  3=Bas  4=Gauche] : ")
        try:
            m = int(raw)
        except:
            print("Veuillez saisir un entier entre 1 et 4.")
            continue
        
        if m < 1 or m > 4:
            print("Direction invalide. Choisir 1, 2, 3 ou 4.")
            continue
        
        if is_backward(player, m):
            print("Retour en arrière interdit pour ce joueur.")
            continue

        if not possibleMove(board, n, directions, player, i, j, m):
            if is_exit_direction(player, m):
                print("Sortie impossible depuis cette case.")
            else:
                print("Déplacement impossible (case occupée ou hors plateau).")
            continue
        return m


# Effectue le déplacement du pion (i, j) du joueur 'player'.
def move(board, n, directions, player, i, j, m):
 
    if is_exit_move(n, player, i, j, m):
        board[i][j] = neutre                  # Enlève le pion du plateau
        print("Joueur " + str(player) + " : pion sorti du plateau !")
        return

    di = directions[m - 1][0]               
    dj = directions[m - 1][1]              
    ni = i + di                            
    nj = j + dj                            

    board[i][j] = neutre
    board[ni][nj] = player


# Compte le nombre de pions du joueur encore sur le plateau.
def count_pieces(board, n, player):
    total = 0
    i = 0
    while i < n:
        j = 0
        while j < n:
            if board[i][j] == player:
                total = total + 1
            j = j + 1
        i = i + 1
    return total


# Le joueur a gagné s'il n'a plus de pion sur le plateau (tous sortis).
def win(board, n, directions, player):
    if count_pieces(board, n, player) == 0:
        return True
    return False


# On vérifie que n est au moins 2 pour éviter les placements impossibles
def dodgem(n):
    if n < 2:
        print("n doit être >= 2.")
        return

    board = newBoard(n)
    init_depart(board, n)

    current = pion1 #J1 commence

    while True:
        displayBoard(board, n)

        if win(board, n, directions, pion1):
            print("Joueur 1 a gagné (tous ses pions sont sortis) !")
            break
        if win(board, n, directions, pion2):
            print("Joueur 2 a gagné (tous ses pions sont sortis) !")
            break

        (i, j) = selectPawn(board, n, directions, current)

        m = selectMove(board, n, directions, current, i, j)

        move(board, n, directions, current, i, j, m)

        if win(board, n, directions, pion1):
            displayBoard(board, n)
            print("Joueur 1 a gagné (tous ses pions sont sortis) !")
            break
        if win(board, n, directions, pion2):
            displayBoard(board, n)
            print("Joueur 2 a gagné (tous ses pions sont sortis) !")
            break

        if current == pion1:
            current = pion2
        else:
            current = pion1


# Petit menu de départ pour demander la taille du plateau
def main():
    while True:
        raw = input("Taille du plateau (n × n) : ")
        try:
            n = int(raw)        
        except:
            print("Veuillez entrer un entier valide.")
            continue

        if n >= 2:
            break
        else:
            print("La taille doit être un entier ≥ 2.")

    # On lance la partie
    dodgem(n)

if __name__ == "__main__":
    main()
