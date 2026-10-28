# -*- coding: utf-8 -*-
"""Arte ASCII e citacoes que preenchem o codigo-fonte visivel.

ATENCAO: nenhuma senha de fase pode aparecer aqui (inclusive a palavra que
nomeia o rosto). O rosto aparece so desenhado.
"""

FACE = r"""
                .:::::::::::::::::.
            .::'`'               '`'::.
          .:' ;  ,;;;;;;;;;;;;;,  ;  ':.
         ::  ;|  ;;'''       '''; |;  ::
        ::  ;;|  ;'   __     __  ': |;;  ::
       ::   ;;|  ;   /  \   /  \  ; |;;   ::
       ::   ;;|  ;   \()/   \()/  ; |;;   ::
       ::   ;;|  ;     '       '  ; |;;   ::
       ::   ;;|  ;        |       ; |;;   ::
       ::   ;;|  ;   .@@.  |  .@@.; |;;   ::
       ::   ;;|  ;  (@@@@)    (@@@@)|;;   ::
       ::   ;;|  ;   '@@'  ,_,  '@@' |;;   ::
       ::   ;;|  ;'.       ' '      .';|;;  ::
        ::  ;;|   ';   .________.   ;' |;;  ::
        ::  ;;|    ';  '-.____.-'  ;'  |;;  ::
         ':. ;|      ';;,      ,;;'    |; .:'
          ':.||        ';;;;;;;;'      ||.:'
            ||||                       ||||
            |||||                     |||||
            ||||||                   ||||||
"""

EYE = r"""
           .-'--------'-.
        .-'   .-""-.   '-.
       (     ( (@@) )     )
        '-.   '-..-'   .-'
           '-........-'
"""

WHEEL = r"""
              .-'-----'-.
            .'  \  |  /  '.
           /  '. \ | / .'  \
          |  --  -- (o) --  --  |
           \  .' / | \ '.  /
            '.  /  |  \  .'
              '-......-'
"""

WEB = r"""
      \   |   /
   .   \  |  /   .
     '. \ | / .'
  ----- (  *  ) -----
     .' / | \ '.
   '   /  |  \   '
      /   |   \
"""


HAIR = r"""
                   ..;;;;;;;;;;;..
               .;;;;;;;;;;;;;;;;;;;;.
             ;;;;;;;;||||||||||;;;;;;;;
            ;;;;;|||||||||||||||||||;;;;;
           ;;;;||||||||||||||||||||||;;;;
           ;;;|||||||||||||||||||||||||;;
           ;;||||||||||| . |||||||||||;;
           ;;|||||||||||   |||||||||||;;
           ;||||||||||| (@) ||||||||||;
            ||||||||||||   |||||||||||
            ||||||||||||||||||||||||||
            |||||||||||||||||||||||||
             ||||||||||||||||||||||||
             |||||||||||  |||||||||||
              |||||||||    |||||||||
              ||||||||      ||||||||
               ||||||        ||||||
                ||||          ||||
                 ||            ||
"""

HAND = r"""
                    _
                .-'| |'-.
               | | | | | |  _
               | | | | | | / )
               | | | | | |/ /
          _    | : : : : : /
         ( \   |          /
          \ \  |         /
           \ '-'        |
            \           |      .  :  .
             '.        /    .    :    .
               |      |   :  ..  :  ..  :
               |      |      .   :   .
  ___________________________________________
 |  .        .        .         .        .   |
"""

DOOR = r"""
         ______________________________
        |  __________________________  |
        | |                          | |
        | |                          | |
        | |           .--.           | |
        | |          (    )          | |
        | |           '..'           | |
        | |          /|  |\          | |
        | |         / |  | \         | |
        | |           |  |           | |
        | |           |  |           | |
        | |          _|  |_          | |
        | |__________________________| |
        |________________________() ___|
"""

PLANCHETTE = r"""
                      .
                     / \
                   .'   '.
                 .'  .-.  '.
               .'   (   )   '.
              /      '-'      \
             /                 \
            |   .           .   |
            |                   |
             \_________________/
               o             o
          A B C D E F G H I J K L M
       N O P Q R S T U V W X Y Z
          1 2 3 4 5 6 7 8 9 0
"""


def box(lines, w=66):
    out = ["┌" + "─" * (w - 2) + "┐"]
    for l in lines:
        out.append("│ " + l.ljust(w - 4) + " │")
    out.append("└" + "─" * (w - 2) + "┘")
    return "\n".join(out)


Q1 = box([
    "MAHABHARATA  ·  Yaksha Prashna",
    "",
    "  Qual é a coisa mais espantosa do mundo?",
    "  Dia após dia, incontáveis seres vão à casa da Morte,",
    "  e os que ficam desejam viver para sempre.",
    "",
    "  What is the most astonishing thing in the world?",
    "  Day after day countless beings go to the house of Death,",
    "  and those who remain wish to live forever.",
])

Q2 = box([
    "BHAGAVAD GITA 11.32",
    "",
    "    kalo 'smi loka-ksaya-krt pravrddho",
    "",
    "  Tempo sou eu, destruidor dos mundos, já crescido.",
    "  Time I am, destroyer of worlds, grown mighty.",
])

Q3 = box([
    "BHAGAVAD GITA 2.69",
    "",
    "  O que é noite para todos os seres,",
    "  nela vela aquele que se domina.",
    "",
    "  What is night for all beings,",
    "  in that the self-controlled one keeps awake.",
])

Q4 = box([
    "MAHABHARATA  ·  Santi Parva",
    "",
    "  O Tempo cozinha todos os seres. Ele vela enquanto os mundos dormem.",
    "  Time cooks all beings. It keeps watch while the worlds sleep.",
], w=74)

Q5 = box([
    "MAHABHARATA  ·  Vana Parva",
    "",
    "  O dharma é sutil. A porta do dharma está escondida numa caverna.",
    "  Dharma is subtle. Its door is hidden in a cave.",
], w=72)

Q6 = box([
    "GITA 4.7",
    "",
    "  yada yada hi dharmasya glanir bhavati bharata",
    "  Sempre que a ordem enfraquece, eu me manifesto.",
    "  Whenever order weakens, I manifest myself.",
])


# So citacoes no codigo-fonte. FACE fica apenas para o ritual final final (dentro do jogo).
BLOCKS = [Q1, Q2, Q3, Q4, Q5, Q6, Q2, Q4, Q1, Q3, Q5, Q6]
