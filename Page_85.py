import turtle
import time
import random

# ------------------------------
# 1. CRÉER LA FENÊTRE ET LES MURS
# ------------------------------
fenetre = turtle.Screen()
fenetre.title("Snake amélioré")
fenetre.bgcolor("black")
fenetre.setup(width=600, height=600)
fenetre.tracer(0)

# Dessiner les murs autour de la zone de jeu
mur = turtle.Turtle()
mur.hideturtle()
mur.speed(0)
mur.color("orange")
mur.pensize(4)
mur.penup()
mur.goto(-280, -280)
mur.pendown()
for _ in range(4):
    mur.forward(560)
    mur.left(90)

# ------------------------------
# 2. CRÉER LE SERPENT
# ------------------------------
serpent = turtle.Turtle()
serpent.speed(0)
serpent.shape("square")
serpent.color("green")
serpent.penup()
serpent.goto(0, 0)
serpent.direction = "stop"

# Les nouveaux morceaux du corps seront rangés ici
corps = []

# ------------------------------
# 3. CRÉER LA NOURRITURE
# ------------------------------
nourriture = turtle.Turtle()
nourriture.speed(0)
nourriture.shape("circle")
nourriture.color("red")
nourriture.penup()
nourriture.goto(0, 100)

# ------------------------------
# 4. SCORE ET MESSAGES
# ------------------------------
score = 0
meilleur_score = 0
partie_terminee = False

stylo_score = turtle.Turtle()
stylo_score.hideturtle()
stylo_score.penup()
stylo_score.color("white")
stylo_score.goto(0, 250)

stylo_message = turtle.Turtle()
stylo_message.hideturtle()
stylo_message.penup()
stylo_message.color("yellow")
stylo_message.goto(0, -25)


def afficher_score():
    stylo_score.clear()
    stylo_score.write(
        f"Score : {score}   Meilleur score : {meilleur_score}",
        align="center",
        font=("Arial", 16, "bold")
    )


def afficher_message(texte):
    stylo_message.clear()
    stylo_message.write(
        texte,
        align="center",
        font=("Arial", 18, "bold")
    )


def terminer_partie(raison):
    global partie_terminee, meilleur_score
    partie_terminee = True
    serpent.direction = "stop"
    meilleur_score = max(meilleur_score, score)
    afficher_score()
    afficher_message(raison + "  Appuie sur ESPACE pour rejouer.")


def recommencer():
    global score, partie_terminee

    # Effacer tous les morceaux du corps
    for morceau in corps:
        morceau.goto(1000, 1000)
    corps.clear()

    serpent.goto(0, 0)
    serpent.direction = "stop"
    nourriture.goto(0, 100)
    score = 0
    partie_terminee = False
    stylo_message.clear()
    afficher_score()


# ------------------------------
# 5. CONTRÔLER LE SERPENT
# ------------------------------
def aller_haut():
    if not partie_terminee and serpent.direction != "bas":
        serpent.direction = "haut"


def aller_bas():
    if not partie_terminee and serpent.direction != "haut":
        serpent.direction = "bas"


def aller_gauche():
    if not partie_terminee and serpent.direction != "droite":
        serpent.direction = "gauche"


def aller_droite():
    if not partie_terminee and serpent.direction != "gauche":
        serpent.direction = "droite"


def mouvement():
    if serpent.direction == "haut":
        serpent.sety(serpent.ycor() + 20)
    elif serpent.direction == "bas":
        serpent.sety(serpent.ycor() - 20)
    elif serpent.direction == "gauche":
        serpent.setx(serpent.xcor() - 20)
    elif serpent.direction == "droite":
        serpent.setx(serpent.xcor() + 20)


fenetre.listen()
fenetre.onkey(aller_haut, "Up")
fenetre.onkey(aller_bas, "Down")
fenetre.onkey(aller_gauche, "Left")
fenetre.onkey(aller_droite, "Right")
fenetre.onkey(recommencer, "space")

# ------------------------------
# 6. BOUCLE PRINCIPALE DU JEU
# ------------------------------
afficher_score()
afficher_message("Attrape la boule rouge !")

while True:
    fenetre.update()

    if not partie_terminee:
        # Faire suivre chaque morceau du corps
        for index in range(len(corps) - 1, 0, -1):
            x = corps[index - 1].xcor()
            y = corps[index - 1].ycor()
            corps[index].goto(x, y)

        if len(corps) > 0:
            corps[0].goto(serpent.xcor(), serpent.ycor())

        mouvement()

        # Si le serpent mange la boule, il grandit
        if serpent.distance(nourriture) < 20:
            x = random.randrange(-240, 241, 20)
            y = random.randrange(-240, 241, 20)
            nourriture.goto(x, y)

            nouveau_morceau = turtle.Turtle()
            nouveau_morceau.speed(0)
            nouveau_morceau.shape("square")
            nouveau_morceau.color("lightgreen")
            nouveau_morceau.penup()
            corps.append(nouveau_morceau)

            score += 10
            meilleur_score = max(meilleur_score, score)
            afficher_score()
            afficher_message("Bravo ! Le serpent grandit : +10 points")

        # Échec si la tête touche un mur
        if (
            serpent.xcor() >= 280
            or serpent.xcor() <= -280
            or serpent.ycor() >= 280
            or serpent.ycor() <= -280
        ):
            terminer_partie("Mur touché ! Partie terminée.")

        # Échec si la tête touche son propre corps
        for morceau in corps:
            if serpent.distance(morceau) < 15:
                terminer_partie("Tu as touché le serpent ! Partie terminée.")
                break

    time.sleep(0.1)
