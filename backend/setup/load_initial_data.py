#!/usr/bin/env python3
# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import SQLALCHEMY_DATABASE_URI

# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #
from backend.flaskr import print_exc_info

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

# ---------------------------------------------------------------------------- #
# Models.
# ---------------------------------------------------------------------------- #
from backend.flaskr.model import Category, Question

# script ids for categories
SID_SCIENCE = 1
SID_ART = 2
SID_GEOGRAPHY = 3
SID_HISTORY = 4
SID_ENTERTAINMENT = 5
SID_SPORTS = 6


def populate():
    # categories
    category_types = [
        # script id, category
        (SID_SCIENCE, "Science"),
        (SID_ART, "Art"),
        (SID_GEOGRAPHY, "Geography"),
        (SID_HISTORY, "History"),
        (SID_ENTERTAINMENT, "Entertainment"),
        (SID_SPORTS, "Sports"),
    ]
    categories = [Category(category_type=category_type[1]) for category_type in category_types]

    question_data = [
        # question, answer, difficulty, category_types[0]
        ("Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "Maya Angelou", 2, 4),
        ("What boxer's original name is Cassius Clay?", "Muhammad Ali", 1, 4),
        ("What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", "Apollo 13", 4, 5),
        ("What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", "Tom Cruise",
         4, 5),
        (
        "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
        "Edward Scissorhands", 3, 5),
        ("Which is the only team to play in every soccer World Cup tournament?", "Brazil", 3, 6),
        ("Which country won the first ever soccer World Cup in 1930?", "Uruguay", 4, 6),
        ("Who invented Peanut Butter?", "George Washington Carver", 2, 4),
        ("What is the largest lake in Africa?", "Lake Victoria", 2, 3),
        ("In which royal palace would you find the Hall of Mirrors?", "The Palace of Versailles", 3, 3),
        ("The Taj Mahal is located in which Indian city?", "Agra", 2, 3),
        ("Which Dutch graphic artist–initials M C was a creator of optical illusions?", "Escher", 1, 2),
        ("La Giaconda is better known as what?", "Mona Lisa", 3, 2),
        ("How many paintings did Van Gogh sell in his lifetime?", "One", 4, 2),
        ("Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
         "Jackson Pollock", 2, 2),
        ("What is the heaviest organ in the human body?", "The Liver", 4, 1),
        ("Who discovered penicillin?", "Alexander Fleming", 3, 1),
        ("Hematology is a branch of medicine involving the study of what?", "Blood", 4, 1),
        ("Which dung beetle was worshipped by the ancient Egyptians?", "Scarab", 4, 4),
    ]

    geography_data = [
        # question, answer
        ("What is the capital of Chile?", "Santiago"),
        ("What is the highest mountain in Britain?", "Ben Nevis"),
        ("What is the smallest country in the world?", "Vatican City"),
        ("Alberta is a province of which country?", "Canada"),
        ("How many countries still have the shilling as currency?", "Four"),
        # ("How many countries still have the shilling as currency?", "Four – Kenya, Uganda, Tanzania and Somalia"),
        ("Which is the only vowel not used as the first letter in a US State?", "E"),
        ("What is the largest country in the world?", "Russia"),
        ("Where would you find the River Thames?", "London, UK"),
        ("What is the hottest continent on Earth?", "Africa"),
        ("What is the longest river in the world?", "River Nile"),
    ]
    history_data = [
        # question, answer
        ("What did the Romans call Scotland?", "Caledonia"),
        ("Who was made Lord Mayor of London in 1397, 1398, 1406 and 1419?", "Dick Whittington"),
        # ("Who was made Lord Mayor of London in 1397, 1398, 1406 and 1419?", "Richard (Dick) Whittington"),
        ("Who was Henry VIIIs last wife?", "Catherine Parr"),
        ("Who was the youngest British Prime Minister?", "William Pitt"),
        # ("Who was the youngest British Prime Minister?", "William Pitt (The Younger)"),
        ("In which year was Joan of Arc burned at the stake?", "1431"),
        ("Which nationality was the polar explorer Roald Amundsen?", "Norwegian"),
        ("Who was the first female Prime Minister of Australia?", "Julia Gillard"),
        # ("Who was the first female Prime Minister of Australia?", "Julia Gillard (2010-2013)"),
        ("Which English explorer was executed in 1618, fifteen year after being found guilty of conspiracy against "
         "King James I of England and VI of Scotland?", "Sir Walter Raleigh"),
        ("Which English city was once known as Duroliponte?", "Cambridge"),
        ("The first successful vaccine was introduced by Edward Jenner in 1796. Which disease did it guard against?",
         "Smallpox"),
    ]
    sport_data = [
        # question, answer
        ("What are the five colours of the Olympic rings?", "Blue, yellow, black, green and red"),
        ("In football, which team has won the Champions League (formerly the European Cup) the most?", "Real Madrid"),
        ("How many players are there in a rugby league team?", "13"),
        ("Which horse is the only three-time winner of the Grand National?", "Red Rum"),
        ("Since 1977, where has snooker's World Championship taken place?", "Crucible Theatre"),
        ("In tennis, what piece of fruit is found at the top of the men's Wimbledon trophy?", "Pineapple"),
        ("Who won the FIFA Women's World Cup in 2019?", "USA"),
        ("In bowling, what is the term given for three consecutive strikes?", "A turkey"),
        ("How many world titles has Phil Talyor won in darts?", "16"),
        ("In golf, where does the Masters take place?", "Augusta National"),
        ("What is Usain Bolt’s 100m world record time?", "9.58 seconds"),
        ("Which England footballer was famously never given a yellow card?", "Gary Lineker"),
        ("Who is the only player to have scored in the Premier League, Championship, League 1, League 2, Conference, "
         "FA Cup, League Cup, Football League Trophy, FA Trophy, Champions League, Europa League, Scottish Premier "
         "League, Scottish Cup and Scottish League Cup?", "Gary Hooper"),
        ("The LA Lakers and New York Knicks play which sport?", "Basketball"),
        ("Katarina Johnson-Thompson is world champion in which sport?", "Heptathlon"),
        ("Which country did F1 legend Ayrton Senna come from?", "Brazil"),
        ("A penalty in football is taken how many yards away from the goal?", "12 yards"),
        ("Who holds the women's record for the 100m sprint?", "Florence Griffith-Joyner"),
        # ("Who holds the women's record for the 100m sprint?", "Florence Griffith-Joyner (10.49s)"),
        ("What club were West Ham United founded as?", "Thames Ironworks"),
        ("Who has scored the most Premier League hat-tricks?", "Sergio Aguero"),
        ("Who were Man Utd playing when Eric Cantona leaped into the crowd and kicked a fan?", "Crystal Palace"),
        ("In which sport do you wear a plastron?", "Fencing"),
        ("Which sport involves tucks and pikes?", "Diving"),
        ("Who is the Premier League’s all-time top scorer?", "Alan Shearer"),
        # ("Who is the Premier League’s all-time top scorer?", "Alan Shearer (260 goals)"),
        ("Jessica Ennis-Hill competed for Great Britain in which sport?", "Heptathlon"),
        ("England won the 2003 Rugby World Cup thanks to an iconic, last-gasp drop goal from Jonny Wilkinson. How "
         "many points did England score in that famous match?", "20"),
        ("Which famous football manager once said: “I wouldn’t say I was the best manager in the business. But I was "
         "in the top one”?", "Bryan Clough"),
        ("How many F1 championships has Lewis Hamilton won?", "Six"),
        ("Chris Wilder helped guide Sheffield United from League One to the Premier League. In the Blades' League One "
         "title-winning season, how many points did they accumulate?", "100"),
        ("What colours are the five Olympic rings?", "Blue, yellow, black, green and red"),
        ("How many Olympic gold medals did rower Steve Redgrave win?", "Five"),
        ("In what year did Andy Murray win Wimbledon for the first time?", "2013"),
        ("At which course is The Masters golf tournament held?", "Augusta"),
        ("Who did Cristiano Ronaldo make his Premier League debut against in 2003?", "Bolton Wanderers"),
        ("Who has won more Grand Slams, Roger Federer or Serena Williams?", "Serena Williams"),
        ("The Pittsburgh Penguins play which sport?", "Ice hockey"),
        ("Which WWE superstar did Tyson Fury wrestle in 2019?", "Braun Strowman"),
        ("Who did England beat in the 2019 cricket World Cup final?", "New Zealand"),
        ("Who is the top-ranked female golfer in the world?", "Jin Young Ko"),
        ("Which rugby team play their home games at The Stoop?", "Harlequins"),
        ("Who was the first woman to train the winner of the Grand National?", "Jennifer Susan Pitman"),
        # ("Who was the first woman to train the winner of the Grand National?", "Jennifer Susan Pitman OBE"),
        ("Who did Manchester City beat to win the Premier League on the final day of the 2011/12 season?", "QPR"),
        ("The term ‘albatross’ in golf means what?", "Three under par"),
        ("Which snooker player is nicknamed The Rocket?", "Ronnie O'Sullivan"),
        ("Who are the owners of Liverpool FC?", "Fenway Sports Group"),
        ("Wayne Rooney scored his Premier League first goal against which team?", "Arsenal"),
        ("What was Wladimir Klitschko's boxing nickname?", "Dr. Steelhammer"),
        ("Name the four Grand Slam events in tennis", "Australian Open, French Open, Wimbledon, US Open"),
        ("At which Olympics did Dame Kelly Holmes win two gold medals?", "2004"),
        ("Who is the current manager of Crystal Palace?", "Roy Hodgson"),
        ("Name the only two positions who can score in netball.", "Goal shooter and goal attack"),
        ("Where were the Olympics held in 1980?", "Russia"),
        ("How many Super Bowls has American Football star Tom Brady won?", "Six"),
        ("How many clubs did David Beckham play for during his career?", "Six"),
        # ("How many clubs did David Beckham play for during his career?", "Six (Manchester United, Preston North
        # End, Real Madrid, LA Galaxy, AC Milan, Paris Saint-Germain)"),
        ("In which sport do competitors refer to ‘catching a crab’?", "Rowing"),
        ("Which Scottish footballer was the first to command a six-figure transfer fee when he moved from Torino to "
         "Manchester United?", "Denis Law"),
        ("What colour medal did diver Tom Daley win at London 2012?", "Bronze"),
    ]
    science_data = [
        # question, answer
        ("At what temperature are Fahrenheit and Celsius equal to each other?", "-40"),
        ("Which planet has the most moons?", "Jupiter"),
        ("In the periodic table, what's the symbol for zinc?", "Zn"),
        ("What type of animal is a barramundi", "A fish"),
        ("What is a pomelo? Is it a) A hat b) A fruit c) A musical instrument?",
         "b) A fruit - a pomelo is the largest fruit in the citrus family%%%b"),
        ("What's the material called that won't carry an electric charge?", "An insulator"),
        ("Where on the human body would you find the papillae?", "The tongue"),
        ("Who was the ancient Greek god of medicine?", "Ascepius"),
        ("What  kitchen appliance that saves us time did Percy Spencer invent?", "The Microwave cooker"),
        ("Umami is the name of one of the five basic what?", "Tastes"),
        ("If you get scurvy, what vitamin are you deficient in?", "Vitamin C"),
        ("What is equal to mass times acceleration?", "Force"),
        ("Who wrote A Brief History of Time?", "Stephen Hawking"),
        ("Which frozen gas forms dry ice?", "Carbon Dioxide"),
        ("What does a chronometer measure", "Time"),
        ("What is the part of the eye called that's coloured and surrounds the pupil?", "The iris"),
        ("For which animal is the Latin word lupine used?", "Wolf"),
        ("What is the lightest metal?", "Lithium"),
        ("What type of sugar does the brain need for energy?", "Glucose"),
        ("Alopecia causes what to be lost from the body?", "Hair"),
        ("Who discovered radio waves?", "Heinrich Hertz"),
        ("What disease can you get from ticks?", "Lyme disease"),
        ("Out of the seven colours of the rainbow, which one is in the middle?", "Green"),
        ("What makes up between 0.5 per cent and three per cent of the dry weight of tobacco?", "Nicotine"),
        ("In computer science, what does USB stand for?", "Universal Serial Bus"),
    ]
    art_data = [
        # question, answer
        ("Which two cities provide the setting for Charles Dickens’ ‘A Tale of Two Cities’?", "London and Paris"),
        ("The Mona Lisa by Leonardo da Vinci is on display in which Paris museum?", "Louvre"),
        ("Which artist painted the Poppy Field in 1873?", "Claude Monet"),
        ("What is the name of the fourth book in the Harry Potter series?", "Harry Potter and the Goblet of Fire"),
        ("The Creation of Adam is one of nine scenes featured on the ceiling of which Rome landmark?",
         "The Sistine Chapel"),
        ("Which Shakespeare play is the following quote from? \"The course of true love never did run smooth\"",
         "A Midsummer Night's Dream"),
        ("Who wrote the Curious Incident of the Dog in the Night Time?", "Mark Haddon"),
        ("In which century did Leonardo da Vinci paint The Last Supper?", "Fifteenth century"),
        ("The Tate is a network of four art museums; two are based in London, give the other two English locations?",
         "Liverpool, and St. Ives, Cornwall"),
        ("What are the names of the three ‘Darling’ children in J.M. Barrie’s ‘Peter Pan’?", "Wendy, John and Michael"),
        ("Who created the famous sculpture 'The Thinker'?", "Auguste Rodin"),
        ("Which Emily Brontë novel is the inspiration for a Kate Bush song?", "Wuthering Heights"),
        ("Sir Quentin Saxby Blake is an English cartoonist, illustrator and children's writer best known for "
         "illustrating books by which author?", "Roald Dahl"),
        ("Which Shakespearean play features the characters of Goneril, Regan and Cordelia?", "King Lear"),
        ("In which city would you find The Van Gogh Museum?", "Amsterdam"),
        ("Which two primary colours could you mix together to make purple when painting?", "Red and blue"),
        ("The Hunger Games young adult series was written by which author?", "Suzanne Collins"),
        ("Who created the Angel of the North?", "Antony Gormley"),
        ("Which famous work of literature opens with these lines? “Two households, both alike in dignity, "
         "in fair Verona, where we lay our scene…”", "Romeo and Juliet"),
        ("‘Guernica’, ‘The Weeping Woman’ and ‘Le Rêve’ are all works by the same artist. Can you name them?",
         "Pablo Picasso"),
        ("What is the name of the pig in E.B. White’s Charlotte’s Web?", "Wilbur"),
        ("Which book has the following opening line been taken from? “These two very old people are the father and "
         "mother of Mr. Bucket.”", "Charlie and the Chocolate Factory"),
        ("Which artist cut off the lobe of his own ear and later shot himself?", "Vincent van Gogh"),
        ("How many lines are there in a sonnet?", "14"),
        ("What artist sold a balloon dog for $58.4 million?", "Jeff Koons"),
    ]
    entertainment_data = [
        # question, answer
        ("John Singleton is the youngest person to be nominated for Best Director at the Oscars. For which film was "
         "he nominated?", "Boyz n the Hood"),
        ("What is the name of the opening number from 2016 musical La La Land", "Another Day of Sun"),
        ("What was the highest grossing film of 2019?", "Avengers: Endgame"),
        ("Which three films did James Dean star in?", "East of Eden, Rebel Without a Cause and Giant"),
        ("Who wrote the score for 1994 Disney film The Lion King?", "Hans Zimmer"),
        ("When was the National Television Awards’ Most Popular Entertainment/TV Presenter category won by someone "
         "other than Ant and Dec?", "2000"),
        ("What is the name of the Christmas hit written by Will Brewis’ (Hugh Grant) father in comedy About a Boy?",
         "Santa’s Super Sleigh"),
        ("Which American comedy series has won a record 37 Emmy Awards?", "Frasier"),
        ("What is the title of the first ever Game of Throne episode?", "Winter is Coming"),
        ("What is the name of the pub featured in UK soap Emmerdale", "The Woolpack"),
        ("What are the names of the two winners of Love Island series 1", "Jess and Max"),
        ("What was the most watched Netflix original TV series of 2019?", "Stranger Things"),
        ("The Wire is set in which US city?", "Baltimore"),
        ("What is the population of David Lynch’s idiosyncratic town Twin Peaks?", "52,101"),
        ("Which key Breaking Bad character was famously meant to die in series one?", "Jesse Pinkman"),
        ("What are the dying words of Charles Foster Kane in Citizen Kane?", "Rosebud"),
        ("In The Matrix, does Neo take the blue pill or the red pill?", "Red"),
        ("For what movie did Steven Spielberg win his first Oscar for Best Director?", "Schindler’s List"),
        ("Which is the only foreign film to wine Best Picture at the Oscars?", "Parasite"),
        ("Which veteran actors starred in the lead roles of True Detective, season one.",
         "Matthew McConaughey and Woody Harrelson"),
        ("What is the first name of Zoolander’s title character?", "Derek"),
        ("Mary Poppins is nanny to which family?", "The Banks family"),
        ("Which actor chipped a tooth making Fight Club?", "Brad Pitt"),
        ("What is the name of Batman’s butler?", "Alfred Pennyworth"),
        ("\"After all, tomorrow is another day!\" was the last line in which Oscar-winning Best Picture?",
         "Gone With The Wind"),
    ]

    try:
        # add categories
        session.add_all(categories)
        session.commit()

        # retrieve categories
        categories = [
            (category_type[0], session.query(Category).filter(Category.type == category_type[1]).first())
            for category_type in category_types
        ]

        # populate questions
        questions = [
            Question(question=q[0], answer=q[1], difficulty=q[2],
                     category=next(x[1].id for x in categories if q[3] == x[0]))
            for q in question_data
        ]
        session.add_all(questions)

        # populate geography_data
        for sid, array in [
            (SID_SCIENCE, science_data),
            (SID_ART, art_data),
            (SID_GEOGRAPHY, geography_data),
            (SID_HISTORY, history_data),
            (SID_ENTERTAINMENT, entertainment_data),
            (SID_SPORTS, sport_data),
        ]:
            category = next(x[1].id for x in categories if sid == x[0])
            questions = [
                Question(question=q[0], answer=q[1], difficulty=random.randint(1, 5), category=category)
                for q in array
            ]
            session.add_all(questions)

        session.commit()
    except:
        print_exc_info()
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    populate()
