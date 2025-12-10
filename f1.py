import os
import sys
import time
import random
import psutil
import platform
import shutil # Added for robust argument handling
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.align import Align
from datetime import datetime
import feedparser
import speedtest
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import subprocess

# --- WINDOWS TERMINAL FORCE LAUNCHER ---
if sys.platform == "win32":
    # Check if we are already in Windows Terminal
    if "WT_SESSION" not in os.environ:
        try:
            # Check if wt.exe is installed
            subprocess.run(["wt", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # THE FIX: Force the starting directory (-d) to be the App's Folder
            # This ensures VLC DLLs and Playlists are found immediately.
            app_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
            
            cmd = ["wt", "-w", "0", "nt", "-d", app_dir, sys.executable] + sys.argv[1:]
            
            subprocess.Popen(cmd)
            sys.exit(0)
        except (FileNotFoundError, Exception):
            pass # Fallback to CMD if WT is missing or fails

# --- CONFIGURATION ---
DRIVER_NAME = "JOE"   
TYRE_STRATEGY = ["SOFT", "MEDIUM", "HARD", "INTER"]

# Initialize Rich Console
console = Console()

class PitWallOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = DRIVER_NAME 
        self.tyre_compound = "SOFT"
        self.lap_count = 1
        self.platform_os = platform.system()

        self.calendar = [
            {"date": "2026-03-08", "event": "Australian Grand Prix", "circuit": "Albert Park"},
            {"date": "2026-03-15", "event": "Chinese Grand Prix", "circuit": "Shanghai"},
            {"date": "2026-03-29", "event": "Japanese Grand Prix", "circuit": "Suzuka"},
            {"date": "2026-04-12", "event": "Bahrain Grand Prix", "circuit": "Sakhir"},
            {"date": "2026-04-19", "event": "Saudi Arabian Grand Prix", "circuit": "Jeddah Corniche"},
            {"date": "2026-05-03", "event": "Miami Grand Prix", "circuit": "Miami Autodrome"},
            {"date": "2026-05-24", "event": "Canadian Grand Prix", "circuit": "Montreal"},
            {"date": "2026-06-07", "event": "Monaco Grand Prix", "circuit": "Monte Carlo"},
            {"date": "2026-06-14", "event": "Spanish Grand Prix", "circuit": "Barcelona-Catalunya"},
            {"date": "2026-06-28", "event": "Austrian Grand Prix", "circuit": "Red Bull Ring"},
            {"date": "2026-07-05", "event": "British Grand Prix", "circuit": "Silverstone"},
            {"date": "2026-07-19", "event": "Belgian Grand Prix", "circuit": "Spa-Francorchamps"},
            {"date": "2026-07-26", "event": "Hungarian Grand Prix", "circuit": "Hungaroring"},
            {"date": "2026-08-23", "event": "Dutch Grand Prix", "circuit": "Zandvoort"},
            {"date": "2026-09-06", "event": "Italian Grand Prix", "circuit": "Monza"},
            {"date": "2026-09-13", "event": "Spanish Grand Prix", "circuit": "Madrid"},
            {"date": "2026-09-26", "event": "Azerbaijan Grand Prix", "circuit": "Baku City"},
            {"date": "2026-10-11", "event": "Singapore Grand Prix", "circuit": "Marina Bay"},
            {"date": "2026-10-25", "event": "United States Grand Prix", "circuit": "COTA"},
            {"date": "2026-11-01", "event": "Mexico City Grand Prix", "circuit": "Hermanos Rodriguez"},
            {"date": "2026-11-08", "event": "São Paulo Grand Prix", "circuit": "Interlagos"},
            {"date": "2026-11-21", "event": "Las Vegas Grand Prix", "circuit": "Las Vegas Strip"},
            {"date": "2026-11-29", "event": "Qatar Grand Prix", "circuit": "Lusail"},
            {"date": "2026-12-06", "event": "Abu Dhabi Grand Prix", "circuit": "Yas Marina"},
        ]

        self.quotes = [
            ("Kimi Raikkonen", "Lotus", "Just leave me alone, I know what I'm doing."),
            ("Kimi Raikkonen", "Lotus", "Yes, yes, yes, I'm doing all the tyres. You don't have to remind me every 10 seconds."),
            ("Sebastian Vettel", "Ferrari", "Blue flag! Blue flag! Honestly, what are we doing here?"),
            ("Lewis Hamilton", "Mercedes", "Bono, my tyres are gone!"),
            ("Bono", "Mercedes", "Lewis, It's Hammer Time!"),
            ("Fernando Alonso", "McLaren", "GP2 Engine! GP2 Engine!"),
            ("Fernando Alonso", "McLaren", "The engine feels good, much slower than before. Amazing"),
            ("Max Verstappen", "Red Bull", "Mate, I have no power! No power!"),
            ("Charles Leclerc", "Ferrari", "I am stupid. I am stupid."),
            ("Charles Leclerc", "Ferrari", "I have the seat full of water, Team: must be the water.."),
            ("Max Verstappen", "Red Bull", "This is boring. I should have brought my pillow."),
            ("Carlos Sainz", "Ferrari", "Smooth Operator! Smooth Operator"),
            ("Lance Stroll", "Aston Martin", "\"You need to press the OK button Lance , OK button.\" \"I pressed it\" \"You are pressing the Pit confirm button,Lance.\" \"Pit confirm button is the OK button,Brad.\""),
            ("Valtteri Bottas", "Mercedes", "To whom it may concern, f**k you."),
            ("Toto Wolff", "Mercedes", "No Mikey, no no Mikey, that was so not right!"),
            ("Lando Norris", "McLaren", "It's Friday then... then Saturday, Sunday, WHAT?!"),
            ("Sebastian Vettel", "Red Bull", "There's Something Loose Between My Legs"),
            ("Yuki Tsunoda", "AlphaTauri", "Traffic paradise!"),
            ("Felipe Massa", "Ferrari", "Felipe baby, stay cool."),
            ("Jenson Button", "McLaren", "I'm going to pee in your seat."),
        ]

    def boot_sequence(self):
        """High-Intensity F1 Start Sequence."""
        console.clear()
        
        logo = """
                            BBGGGPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     PPPPPPPPPPPPPPG 
                        BGPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     BPPPPPPPPPPPPPP  
                      BPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     GPPPPPPPPPPPPPG    
                    BPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     BPPPPPPPPPPPPPP     
                   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     GPPPPPPPPPPPPPP       
                 GPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP     BPPPPPPPPPPPPPP        
                PPPPPPPPPPPPP                                                GPPPPPPPPPPPPPP          
              GPPPPPPPPPPPP     BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB      BPPPPPPPPPPPPPP           
             PPPPPPPPPPPPP    GPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP       GPPPPPPPPPPPPPP             
           BPPPPPPPPPPPP    GPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP       PPPPPPPPPPPPPPG              
          PPPPPPPPPPPPP    BPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP      PPPPPPPPPPPPPPG                
        BPPPPPPPPPPPP     GPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP      PPPPPPPPPPPPPPG                 
       GPPPPPPPPPPPP    BPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP       PPPPPPPPPPPPPPB                  
     BPPPPPPPPPPPP    GPPPPPPPPPPP                                    PPPPPPPPPPPPPPG            
    GPPPPPPPPPPPP    BPPPPPPPPPPP                                    BPPPPPPPPPPPPPP          
  BPPPPPPPPPPPP    GPPPPPPPPPPP                                     PPPPPPPPPPPPPPG           
 GPPPPPPPPPPPP    PPPPPPPPPPPP                                     BPPPPPPPPPPPPPP           
        """

        console.print(Align.center(logo), style="bold red")
        console.print(Align.center("[ ESTABLISHING CONNECTION TO PIT WALL ]", style="dim red"))
        console.print("\n\n")

        light_shape = """
            ███████
            ███████
            ███████  
        """ 
        
        def get_gantry(lit_count):
            gantry = Table.grid(padding=(0, 2)) 
            row_content = []
            for i in range(5):
                if i < lit_count:
                    row_content.append(Text(light_shape, style="bold red"))
                else:
                    row_content.append(Text(light_shape, style="dim grey"))
            gantry.add_row(*row_content)
            
            return Panel(
                Align.center(gantry), 
                title="[bold white]FIA START SEQUENCE[/]",
                border_style="grey30",
                padding=(1, 2),
                expand=False 
            )

        with Live(Align.center(get_gantry(0)), refresh_per_second=10) as live:
            time.sleep(1.0)
            for i in range(1, 6):
                live.update(Align.center(get_gantry(i)))
                time.sleep(0.9) 
            time.sleep(random.uniform(1.5, 3.5))
            
            gantry_out = Table.grid(padding=(0, 2))
            row_out = [Text(light_shape, style="black on black") for _ in range(5)]
            gantry_out.add_row(*row_out)
            
            final_panel = Panel(
                Align.center(gantry_out),
                title="[bold green]TRACK GREEN[/]", 
                border_style="green",
                padding=(1, 2),
                expand=False
            )
            live.update(Align.center(final_panel))
            time.sleep(0.5)

        console.print("\n")
        console.print(Align.center("[bold green on black]  LIGHTS OUT AND AWAY WE GO!  [/]"))
        time.sleep(1)
        console.clear()
        console.print("[bold red on black]Type in 'radio' to get started with the F1 commands !")

    def make_bar(self, percent, length=15):
        percent = max(0, min(100, percent))
        blocks = int((percent / 100) * length)
        spaces = length - blocks
        color = "green"
        if percent > 60: color = "yellow"
        if percent > 85: color = "red"
        return f"[{color}]{'█' * blocks}{'░' * spaces}[/]"
    

    def cmd_next(self):
        """Calculates and displays the next upcoming race."""
        
        now = datetime.now()
        upcoming_race = None
        
        # Logic: Find the first race in the future
        for race in self.calendar:
            race_date = datetime.strptime(race["date"], "%Y-%m-%d")
            
            # If this race is in the future
            if race_date > now:
                upcoming_race = race
                break
        
        # Display Logic
        if upcoming_race:
            race_date = datetime.strptime(upcoming_race["date"], "%Y-%m-%d")
            delta = race_date - now
            days_left = delta.days
            
            # Visual Panel
            grid = Table.grid(expand=True, padding=(0, 2))
            grid.add_column(style="bold white", justify="right")
            grid.add_column(style="bold cyan")
            
            grid.add_row("NEXT EVENT", f"[bold yellow]{upcoming_race['event'].upper()}[/]")
            grid.add_row("LOCATION", upcoming_race['circuit'])
            grid.add_row("DATE", race_date.strftime("%d %B %Y"))
            grid.add_row("COUNTDOWN", f"[bold red blink]{days_left} DAYS[/] until Lights Out")
            
            console.print(Panel(
                grid,
                title="[bold white]UPCOMING SESSION[/]",
                border_style="green",
                width=50
            ))
        else:
            # Fallback if season is over and next year isn't in list yet
            console.print(Panel(
                "[dim]No upcoming races scheduled in database.\nWaiting for FIA Season Calendar update...[/]",
                title="OFF SEASON",
                border_style="grey50"
            ))
    

    def get_track_ascii(self, track_name):
        """Returns ASCII art for famous circuits."""
        tracks = {
            "monza": """
    [bold red]AUTODROMO NAZIONALE MONZA[/]
    [dim]Italy | 5.793 km | 53 Laps[/]

 &#BBBBYGGGGGGGGG#                                                                                  
#GGGBBBPB####&&#GGB                                                                                 
PGG             #GGG                                                                                
GGG&             &PYP&                                                                              
&GGG              &GGG#                                                                             
 #P5G               BGG#                                                                            
  GPG&               BGGB                                                                           
   GGG                #GGB&                                                                         
   #GGB                &GGG#                                                                        
    BGGG#                #GGG#                                                                      
     &GGG                  #GGG#                                                                    
      GGG                    BGGB&                                                                  
      GGG                     &BGGB&                                                                
      BGG&                      &BGGB&                                                              
      BGG&                        #GGG#                                                             
      55B                          #GGGB                                                           
      &PPB                            #Y5G#                                                         
       GGG                             &#GGB&                                                       
       GGG                               &BGGBBGBB#&                                                
       #GGB                                &#####BGGB&&&&&                                          
        GGG#                                      &BGGGGGGGGJBBBBBBB####&&&&&&                      
         GGG#                                         &&&&&#B##BBBBBBGGGGGGGGGGGGGGBBBBBPB###&&&&   
          BGGB&                                                          &&&&&&####BBBBBYGGGGGGGGGB 
           &BGGG#&&               &&                                                         &&&#GGG
             &#BGGGGBBBBPG###BBBGGGGB&&&                                                         GGP
                 &###BBB5PBBBBBB##BGGGGG5YGGGGBBBBBBB#####&&&&&&                               &GGG#
                                   &&&&&#######BBBBBBBGGGGGGGGGGGGGGBBBBBPB#####&&&&&&&&&###BBGGGB& 
                                                          &&&&&&####BBBBBYGGGGGGGGGGGGGGGGGGGBB#&  
            """,

            "silverstone": """
    [bold blue]SILVERSTONE CIRCUIT[/]
    [dim]UK | 5.891 km | 52 Laps[/]

                                    &&&       &####&                                                
                        &&&&&&&&&#BGGGGGB####BGGBGGGB                                               
             &&##BBBGGGGG55GGGGGGGB#&&&#BBBBGB#&  &GGG&                                             
          #BGGGGBBB###&&&&&&&&&&     &######&       BGGB#&                                          
        &GGG#&&                    &BGGGBB55GGB#     &#BGYPB#&                                      
        #GG&                     &BGGB&  &#BGGGG&        ##BGGGB#&                                  
        #GG&                   &BGGB&   BGGGB##&             &#BGGGB#&                              
        &GG#                 &BGGB&     BGGB&                    &#BGGGB#&                          
         PPB               &BGGB&        &BGPG                       &#BGGGGB&                      
         PPG              #GGB&            #55G#                         &#PPGGB#&                  
         BGG            #GGB&                #GGB                            &#GGGB#&               
         #GG&         BPGB&                   BGG&                              &#BGGB              
         &GG#       #GPP#                     #GG&                                 &GGB             
          GGB     #GGG#                       GGG                                  #GGB             
          BGG&   BGG#                         GGB                              &BBGGG#              
           BGG#     ###&&                     GGG#                          #BGGGB#&                
            #GGGB     GGGG&                    #BGGB&                    &#GGG#&                    
              &BGGG    #GGB                      &#GGGB&               &BY5B#                       
                 &&G    GB&                         &BGGGB&          #GGGB#                         
                    &&&&                               &BGGG##       #GGG                           
                                                          #BY5B#&    &GGG#                          
                                                            &#BGGBBBYPGB&                           
                                                               &#BB#B#                              

            """,

            "spa": """
    [bold yellow]CIRCUIT DE SPA-FRANCORCHAMPS[/]
    [dim]Belgium | 7.004 km | 44 Laps[/]
    
                                                                      &&###&                        
                                                               &&BBBBGGGGGGG#&#GBBB#                
                                                       &&##BBGGGGYPB##&&  #GGGGYBBGGG&              
                                               &&&#BBGGGGGGBB##&&                  BPYG             
                                         &##BBGGGGGBB##&&                        && #PGG#           
                                      #BGGGGBB#&&                         &&##BBGGGGB&#GGB          
                                  &BGGGGB&&                    &&&##BBB55GGGGGBB#&&BPYB&GGG&        
                              &&BGG5P#&                      BGGGGGGBBBBB&&&        BPGB#GGG        
                         #BBGGGGGB#                         GGG#&                    &BGGBB&        
                       &GGGB#&&&                           &GGB                                     
                     &BGGB&                                &GGB                                     
                   BPGGB&                                   BGGB&                                   
                &BGG5B&                                      #BGGGB#&&                              
             &#GGGB&                        &#BBGGGGB#&&       &##BGGY5B##&                         
           &BGGG#       &#BBB#       &&##BGGGGBB####BGYYBB#&        &##BGGGGB#&                     
          #GGG#     &#BGGGGGGGBBGGG55GGGGB##&         &#BBGGG#            &#BGG#                    
        &PGG#   &#BY5GGB#& &B########&&                   &#GGG#            #GG#                    
       &G55& &BGGGGGG&                                       BGG#          #GGB                     
      &GGGGBGGGB#&                                            BGGB         #GGB&                    
     &GGGGGGB#&                                                #GGB         #BGGGB#                 
      #BB#&                                                     #GGG&          #BYPGB#              
                                                                 &BG5G&           &#GGB             
                                                                   #PGGB&          GGGB             
                                                                     &BGGGB#&    #G55&              
                                                                        #BGGGGBBGGG#                
                                                                           &&##B##&                 
            """,

            "monaco": """
    [bold red]CIRCUIT DE MONACO[/]
    [dim]Monaco | 3.337 km | 78 Laps[/]

                                                                #BBB&                               
                                                             &BGG##PG&#G##&                         
                                                           &BP5#  &5PGBPBGG                         
                                                         #GGB&     GGG  #GB                         
                                                        GG#&       &B#  PG&                         
                                                       &GG             BYB                          
                                                        &GG&          GG#                           
                                                         #GG        &GG#                            
                                               &&&&##&&#BGG#      &BGB&                             
                          &BGBBBBBBBBGPBBBBBBBGGBBBPGBBB#&    &#BGGB&                               
                         #GG                               BBGGB#&                                  
                        BGB  &BBBBBG5BBBBB###GGGBBBBBBBBPB##&&                                      
                       BGB  #PG&&&&&&&&&&######                                                     
                      #GG   G5#                                                                     
                      GG&  #GB                                                                      
                      55   &GG&                                                                     
                     &GG    G5#                                                                     
                     &GG    G5#                                                                     
                     &GG   #GG&                                                                     
                      GG   GG&                                                                      
                      BPB  BGB&                                                                     
                       BGB  &5PB&                                                                   
                        BP#   &BGGB                                                                 
                        #GGB    BGG&                                                                
                          &&&B####&                                                                 

            """,
            
            "abudhabi": """
    [bold cyan]YAS MARINA CIRCUIT[/]
    [dim]Abu Dhabi | 5.281 km | 58 Laps[/]

                                        ~^                                                          
                                       :PPYJ!^:                                                     
                                 ^~!77?JB!:~7JYJ7~:                                                 
                            ^77JYY?              JYYJ!^:                                            
                          :?5Y7^:   ~7JYYY?77P5^:  :~7JYY?!^:                                       
                        ^JP?^     :P57^: :  :5P         ^!?JYJ7~:                                   
                      ~Y57:       ~#^^:     :YY             :^7JYY?!^                               
           :        75Y~          ^#^   :   :55~:                ^!?YYJ!^:              :           
                 :7PJ~~77????~    ^#^   :   :PP~:            :       :~?YYJ7~:                      
               :?PJ^?PY?!~77PP    ^#~       :PP^:                        :~7JYY?~^                  
              7PJ:!PJ:::    5P    !#^       :PP                               ^!?YYJ!^              
            ^5P^ YG!:     :~7YYJJJPJ^       :PP               :~!!!~:             :~?YYJ7~:         
           ?G7  ~#^^^      :  ::^^::^       :PP       :     ~5YJY77JYYJ7~^::::::::    :~7JG!:       
         ^P5^   5P                          :PP      :^:^^^YG!  :    :~7YJJJJJJJJJJJJJJJJJ5~^       
        !G?    ^#!                          :P5          ^5G:           :          :::::::          
        #?     YP                           :YG~!!7??JJJY55^                                        
        7P?!~!JG^                           :^JJ??77!~~~^:^:                                        
         !77??!:                                                                                    

            """,


            "mexico": """
    [bold cyan]Autódromo Hermanos Rodríguez[/]
    [dim]Mexico City | 4.304 km | 71 Laps[/]

   :?5PBGGGGGGGGGBGPP5YJ?7!~^:                                                                      
  Y#P7^:         :^^~!7?JY55PPPPPPP55YYJ?77!~~^^:                                                   
^##^                            ::^^~!77?JJY55PPPPPPPPPPP55YYJ??7!!~^^:                             
B&:        :^                                        ::^^~~!!7?JJYY5PPPPPPPPP5YYJ?7!~~^::           
P#55YJ?7^~5# 5                                                            :^^~!7??JY5PPPGGPGP5Y?^   
  ^~!77YPPJ:P&:                                                                            :^~!Y J  
            ? !                                                                                ~ J  
            ^ Y                                                                                ? J  
             &G                                                                                 ?P#P
             5&5J??7!~^^:                                                                         G 
              ^!7??JY55PGPGGPP55YJ?7!~^:                                                          ##
                           ::^~!!7?JY5PPGGPJ~                                                    ? 7
                                         :~JPGGJ!:                                              ~ 5 
                                              ~?PGG7                                           ~&G  
                                                  ? 5                                         ! P   
                                                   ? J                                       J Y    
                                                    ?#GYJ?77!~^:                            5 7     
                                                      ~!7?JJY5PPGGY^                      :B&~      
                                                                 ^P 7                    ~&B:       
                                                                   Y J                  7 5         
                                                                    !GBY~              5 ?          
                                                                      ^JGB5^         :B&~           
                                                                         ^ G        !&G:            
                                                                         ^ Y       J Y              
                                                                         ? !     :G&7               
                                                                         5 ^    ~&B^                
                                                                         B#    ? 5                  
                                                                        : P   5&7                   
                                                                        ! ?  ^##7:                  
                                                                        J ~    ~5 P                 
                                                                        G :    7G#?                 
                                                                        ##  !5BP!                   
                                                                        7BBBG?:                     

            """,

            "imola": """
    [bold cyan] Autodromo Internazionale Enzo e Dino Ferrari[/]
    [dim]Imola | 4.909 km | 63 Laps[/]

                                                                :~!~^:                ::^^^:        
                                                               YBP55PPPP5YJJJYY5575PPPPPP5PG5:      
                                                             :PBJ    :^~!77777!!~:^^::  :!5B5       
                                                             5BJ                      ~?JGY~        
                                                            ^BG:                   ^?PG5~           
                                                            :GB~                 :5G57:             
                                                             ?5J                 ^GB~               
                                                             ~BG:                 5B?               
                                                              5B?                7BP:               
                                :^7J5PY!~~~~^^^^:^^^^:::::   ?GG~               7BG^                
                           :~?5P5?Y?!?555555555P7PPPPPPPPPP5PBY:               ~PG~                 
                        :75GPY7^:                         ^!7~                ~GP^                  
                      ~5GP?^                                                 ~GB!                   
                    7PBY~                                                   ^GB!                    
                 ^JGGJ^                                                    ^GB7                     
             :~?5GP7:                                                   :~?GG7                      
         !J5PP?Y7^                                                   ^JPGPY7:                       
        !#G7^       :~7J55PPPPPPPP55557Y5YJ7~^:                     ~GB7:                           
         J5?  :~7J5?5PY?!~^::^^^^^^~~~^~!7?Y5PPPP5YJ??????7!YYY555PPP57                             
          YGPPPPY?!^                           :~!7??JJJJ?7~77!!~~^:                                
           :^^                                                                             
            """,


            "interlagos": """
    [bold cyan]  Autódromo José Carlos Pace [/]
    [dim] Sao Paulo | 4.309 km | 71 Laps[/]

                                                :^!7??JJYYJJ?7!~^:                                  
                                        :^!?Y5GB#####BBGGGGGB##&##BGP5Y?7~^:                        
                                 ^~7J5PB####BP5?!~:       ::: :~!7JY5GBB##&##BGPYJ?!^:              
                         :^!?YPGB###BG5J7~^:    :~!?J5PGBBBBB5!         :^~!?JY5GBB###GY!:          
                  :~7J5PB##&#BPY?!^:        ^YG##&##GG5YJ?775&&J            :~!?YP5J7JP#&#5~        
          :^!?YPG##&#BG5J7!^:              J#&BJ!^:         5#&?       ^?PB##&#BGP##P  :7G&#Y       
    ^!J5GB####BPY?!~:                     5&#5:           !B&B7      !P#&BY7!^:  7#&B:    J#&G~     
 ^JG#&#G5J7~^                            7&#G            :##G:     !P&&P!     :JB&#Y:      !B&#7    
J#&G?^                                   5#&?            :#&B^   !P&&P!     ~5#&G?:         ^G##7   
B##!                                     J&#5             ^G##GG#&#P!     !P&&P!             ^B##~  
~G&#Y!                                   :G&#J:             ~?YYJ!:      J&&P~                !##B  
  7P#&B?                                  :Y#&#5!:                      ~&#P                   Y#&J 
    :B#&^                                   :7P#&#57:                   ?&&?                   :B##~
    ?#&P                                       :7P#&#P7:                ?&#J                    ?##P
   Y&#Y                                           :75#&#P?^             :B&B!                   :###
  7&#5                                               :!5B&#P?^           ^P&&5~                 ^###
  P##~                                                   !5B&#P?^          !P#&B57:             P##J
  B#B:                                                      !YB&#G?^         :75B&#GJ~         ?&#P 
  G##^                                                         !YB&#G?^          ~?P#&#P?^    ^###^ 
  7&#5                                                            ~YB&#P?           :!YG&&BY!7B&#7  
   J#&P^                                                             !5#&B7             ^75B##B5~   
    !G&#5~                                                             ^G&&Y                ::      
      7P#&B57~:                                                          G#&!                       
        ^?5B#&#BGPYJ7~^:                                                 J&&Y                       
            :~7JYPGB####BGPY?7~^:                                        J&&Y                       
                    :^~7JYPGB####BG5Y?!~:                                P#&?                       
                             :^!?J5PB#####BP5J7!^:                      :B##^                       
                                      :~!?Y5GB####BGPYJ7~^:             7&#P                        
                                              :^~7?YPGB####BGPY?7~^:   ^G#&7                        
                                                       :^~7JYPGB#&##BGB#&B?                         
                                                                :^!7JJJ?~                                                                                     
            """,


            "sakhir": """
    [bold cyan]  Bahrain International Circuit  [/]
    [dim]Sakhir | 3.543 km | 87 Laps[/]

                          &&&                                                                       
                        &GGGGGB&                                                                    
                        BGG##GGG#                         &#BB#&                                    
                        GGG   BG55#                     &BGGBBGGB                                   
                       #GGB    &GGGGB&                 &GGG&  #GGB&                                 
                       BGG&       #BGGGB#&            &PPG&    &GGG#                                
                       GGG          &&#BGGB           G55#       BGGB                               
                      #GGB              GGG          #GGB         #GGG&                             
                      BGG&              GGG          &GGG          &GGG#                            
                      GGG               BGGB&         #GGG#&         BGGB                           
                     #YYB                #BGGB#&       &BGGGP5B#&     #GGB&                         
                     BGG&                  &BBYYB#&       &&GGBGGGB    &GGG#                        
                     GGG                  #& &#BGGGB&           #GGG&    BGPG                       
                    #GGB                   GGGBBGGGGB            #GGB     BY5B&                     
                    BGG&                     BBBBBBB#&&&&&&&&&&&&#GGG      &GGG&                    
                    BGG&                     GGGGGGG?PGGGGGGGGGGGGGB&        BGG#                   
                    &GGG                     &&&&&&&&&&&&&&&&&&&&&&           #GGB                  
                     #GGB                                                      &GGG&                
                    #BGG#                                                        GGG#               
                   GGGGB################################GG#####################BBGGG#               
                   #BBBBGGGGGGGGGGGBBBBBBBBBBBBBBBBBBBBB55BBBBBBBBBBBBBBBBBBBBBBB#& 
                   #                                                                            
            """,



            "baku": """
    [bold cyan]  Azerbaijan Grand Prix  [/]
    [dim]Baku | 6.003 km | 51 Laps[/]

                   :^^^^^^^^^^:::                                                                                                 
               :?PP5555555555555PPPP5Y?:                                       !PPP55555YYJJ??77!!~~^^^::                         
             ^YB5~                 :^~&5                                      :&5 :::^^^~~!!77??JJYY5555PPPP555YJ??7!~~^^:        
           ~5BY:                     :&P^                                     7 ~                          ::^~~!7?JJY555PPP7     
         ^PB?:                        ^?BP^                                   P#                                           7 !    
        ~&5                              G&:                                  &5                                           ^ 7    
       ~ Y                               BG                 :7??JJJJJJJJJ???7Y ~                                           7 ~    
      ~&Y                               ~ 7                :&G777!!!!!!!!777??~                                            ? ^    
     ~&5                                5&      :^^~!7?JYY5PG^                                                             Y&:    
    ^&5                                 GB?Y5PPGGBBBBBBBGGGP55P555YJJ??77!~~^^::                                           PB     
    7 7                                 ~P#BBGPP55YJ?7!~~^^::::^^~~!!7??JJYY555PPPP5555YYYJ??77!~~^^::                     #P     
     ?&Y                               Y#Y!^::                                     ::^^~~!!77?JJYY555PPPP555YYJJ?77!!~^^^:? !     
      ^BB^                           7#P^                                                               ::^^~~!77?JJYY555PP7      
        5&7                   :^~7?YGG!                                                                                           
         7&5           :!?J55PP5YJ7~:                                                                                             
          ^GB~      ~JPPY?!~^                                                                                                     
            J#Y^^!YGP?^                                                                                                           
             ^Y55Y7:                                                                                                                                                                                                                                             
                                                                       
            """,


            "buddh": """
    [bold cyan]  Indian Grand Prix  [/]
    [dim]Greater Noida | 5.125 km | 60 Laps[/]

                            .^~!!~^                                                                     
                      ~5Y?7!!7JP~                                                                   
                     !B~       YG                                                                   
                     !#~       :B7                                                                  
                      !YYJ!:    !B7                                                                 
                        .~?YY?~. :PY.                                                               
                            :~?YY7~JG~                                                              
                                :!GJ~PY^.:^~!!:                                                     
                                  JB. !JJJ?7!7YY?~.                                                 
                                  :?5Y!:       :!J5J!:                                              
                                     ^7Y5?~!!:    .^7YY7.                                           
                                        .~7!?B~       .YG.                                          
                                             ?B.     ^?5J                                           
                                             ^#~ .~J5Y!.                                            
                                          .!J5J!J5J~.                                               
                                       :7Y5YYYY?^.                                                  
                                    ^7YY7?5J7:                                                      
                                 ^?5Y7:  ?G7~~~^^::..                                               
                             .~J5Y!.      :!!77??JJJJJJJJJ??77!!~^^::..                             
                          .~J5J!.                     ..::^^~~!77??JJJJJJJJJ?7:                     
                        ^JY?~                                          ...::~#7                     
                        YB7~~^:..                                           JG.                     
                         ^~!7?JJJJJJ?7!~^::.                                5P                      
                                 .::^~!7?JJJJJJ?7!~^^:.                     ^B?                     
                                            ..:^~!7??JJYJJ?7!~^:..           :5P!.                  
                                                       ..:^~!7?JJYJJ??7!~^:.   ^?YJ~.               
                                                                  .:^^~7??JJJJJ?77J5P5^             
                                                                            ..:^~!7?JY:             
                                                     
            """,



            "barcelona": """
    [bold cyan]  Circuit de Barcelona-Catalunya  [/]
    [dim]Barcelona | 4.66 km | 66 Laps[/]

                 &##BB##&&                                                                          
               &BGGGBBGPPGGBB##&&                                                                   
              &PGG&       #BBGGGGGGBB#&&                                                            
              GPP              &&##BGGGGGGBB##&&                                                    
             BGGG&   &GGGG#           &&##BBGGGGGBB##&&                                             
              #GGP&  BGPGGGG#                &&&#BBGGGGGGBB#&&&                                     
              BPGB   #PP# #GGG#                      &&##BBGGGGGBB##&&                              
             #GPB    &GGG&  #GGG#                           &&##BBGGGGPGBB#&&                       
             GGGB&    #BGGG&  #GGG#                                      GGGGGBB                    
              #BGGGB&   &GGG    #GGGB                    &GGG##BGGGG       &&BGGB                   
                &#GPGGB#BGGB      #PPG#                 #GGG&      &#BGG     BPP#                   
                   &#BGGBB#         #GGG#            &#GGGB&          &BGP   GGG#                   
                                      #GGG#&      &#BPPB#&              &GG    GGGB#                
                                        #GGGB&&&#BGGGB&    &#BGGGGBB##&&  &BG   #BPPG#              
                                          #BGGGGGGB&      BGGB       PPGGBBBGGG   &BGG#             
                                             &&&&        BGG#        &&&#BBBBB&     GGG             
                                                         #GGGB#&&                  #GGG             
                                                          &#BGGGGGGGG##&&       &#BGGB              
                                                               &&##BGGGGGGGBBBGGGGGB&               
                                                                      &&&##BBB##&&                                                                                                               
                                                      
            """,



            "montreal": """
    [bold cyan]  Canadian Grand Prix  [/]
    [dim]Montreal | 4.361 km | 70 Laps[/]

                                          ::::::::                                                  
                                     !JPGBBBBBBBBBBGPPYJ?!~:                                        
                                    J&&GJ????777???JY5PGB###BPY?!^                                  
                          :^!77!!~^^P&#^                :^~7J5G#&#G~                                
                        !5B&########&&P:                       :!&@P~^:                             
                     ^7P&&5!^:::^^~~!~:                          !5B&#BPY?!^:                       
              ~J5Y??P#&BY~                                         :^!J5GB###BG5YJJ??JY5PGGPY^      
           :!P&&GG##GJ~                                                  :^~7?Y5PGGGGGPP5YJ#@B:     
         ^?B&#Y~  ::                                                             :^~7YPGGGB&#?      
        J#@G?:                                                           :^~!?YPG####B5J???!:       
       5@&?                          ::^^:                 ::^^~~!77?JY5GB###BG5J7!~:               
      J&&7:7J?7!~^:::::^^~!!7?JY55PGBB####Y^^^~~!7?JJY5PPGBB#######BBGP5Y?!~::                      
      B@B?#@#B##############BBGGP5YJ?77~7B&#######BBGPP5YJ?77!~~^^::                                
      ~5GBG?: :^~!!777!!~^^:::           :!!!~^^:::                                                                                                                                                                
                                                      
            """,



            "miami": """
    [bold cyan]  Miami Grand Prix  [/]
    [dim]Miami | 5.41 km | 57 Laps[/]

                                    .:~7?JYY555YJ?7!^:                                              
                              .^7JPB&&&&#BGGPPPPGB##&#BPJ!:.                                        
                        .^7YP#&@&#PY7~:.    :~7JY5PPPGGB#&&#BGPGGGGGBBBBBBBBBBBGP5J7~::::^^:        
                   .~?5B&@&BPJ7^.        ~5#@&#BGPPGB#&&BPYJJYYYYYYYJJJJJJ????JY5GB&&&&&&&&&G~      
               ^7YB&@&B57~.             J@@P!:.      .^7P#@#P?^            .^!!~:  .^~~~~:^#@#      
           :75#@@B5?^.                  #@B              .~JG&@#57:     ^?G&@&#&@B7      :J@@Y      
          ~@@@P!:                      ^#@G                  :!YB@@B55P#@&GJ^..:J&@#Y??YB@@B7       
          .5#@#5~                   .7G&@B~                      ^7YPP5J!:       .75B##G5?^         
             ^P@@!                  J@@G~                                                           
        ~J555YB@#^                  ^P#&#GJ!:                                                       
      :P@&GPPP5?:                     .~?P#@@#PJ~:                                                  
      G@@J                                 :!YG#@&B5?~:                                             
      !&@G                                     .^7YG&@&B5?^.        .~JPB##BGY~.                    
      J@@?.:.......                                  ^7YG&&#G5YJJY5G#@&GJ??JP&@#Y^                  
      Y&@&&&&&&######BBBBGGGGPPPP555YYYJJJ???7777!!!~~^^^~?YGB###BGPJ!:      .!G@&P~                
       :^~~~!!!!777???JJJJYYY555PPPGGGGBBBB######&&&&&&&&&&##&&&&########BBBBGGG@@@B                
                                              ......:::::^^^^~~~~!!!777????JJJYYYY?:                
                                                     
            """,


            "qatar": """
    [bold cyan]  Qatar Grand Prix  [/]
    [dim]Lusail International Circuit | 5.41 km | 57 Laps[/]

                               :?PGBG57:                                                            
                              !#@P?7JB@G^                              :~7????????7!^               
                              G@P    :G@P                            ~5##BGGGGGGGGB#&P^             
          :^!?YPGG57:        ^#@?     ?@&~                          ?&&Y^:         ^5@#!            
        !5B##BPY?JG@#7       7@&~      5@B^                        7&&7              J&&7           
       Y@#?~:      ?@&!      5@G       :5@#7                      !&@?                7&@J          
      :B@Y          Y@#^    :B@Y         7B@BJ^                  ^#@Y                  ~B@P:        
       ?@#~         :G@P    !&&!          :!P&&Y:               :G@P:                   :B@Y        
        P@B:         ~&@?   Y@B:             ^P@B:             :P@G:                    ?&@?        
        ^B@Y          J@#^  G@5               ?@#^             5@B^                   !G@G!         
         !&&7         :G@G:~&@7              ~#@J            :5@B~                  ~P@#?:          
          Y@#^         ^P&##&P:              P@G            7B@P^                 ^5&&J:            
          :G@P           ^77~               7&&~         :7G@B?                 :J&&5^              
           ~#@J                            :B@5       :!Y#&G7:                :?#@P~                
            ?@&!                           ^#@Y^^^!?YG#&BY~                  !B@G!                  
             5@B:                           !G#####BPY7^                    ^#@Y                    
             :G@P^                            ^^~^:                         :B@5:                   
              ^5&&PJ~:                                                       ^P@B~                  
                ^75B&#PJ~:                                                     J&&?                 
                    ^?5B&#P?:                                                   !B@P:               
                       :^7G@G^                                                   ^P@B!              
                          ~&@7                                                     ?&&J             
                       :~JB@P:                                                      ~B@P^           
                   :~?P#&B5!                                                         :5@#7          
               :~JP#&B5?~:                                                             7#@5^        
              JB&B5?~:                                                                  ^5@#7       
             J@#!                                                                         7#@Y      
             J@#~                                                                          P@G      
             :Y#&GYYYYYYJJJJJJJJJJJJJJ????????????????????JJJJJJJJJJJJJJJYYYYYYYYYYYYYYYY5B&G~      
               ^7Y5PPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGGGGGGGGGGPPPPPPPPPPPPPPPPPPP55555555555J!:                                                                                                        
                                                     
            """,


            "lasvegas": """
    [bold cyan]  Las Vegas Grand Prix  [/]
    [dim]Las Vegas | 6.201 km | 60 Laps[/]

                                                          ?J!^                                      
                                                          ?@5J5J7:                                  
                                                           7G?^~7Y5J!:                              
                                                            :?Y5J^.~?55J~                           
                                                               .7#~   .!5P^                         
                                                                :&7      J#^                        
                                                              :7GJ        ?#^                       
                                                          :~?55J:          ?#~                      
                                                      :!J55J!:              7#~                     
                                                  :!J55J~:                   7#~                    
                 :!JYYYYY?^                   :!J55?~:                        !#!                   
               .YP?~:. .:7PP:             :!J5Y?~.                             !#!                  
              .G5.         YB:        ^7J5Y?~.                                  ~#7                 
              !&:           JB^  .^7Y5Y?~.                                       ~#7                
              :#J            7BJY5Y7^.                                            ~#?               
               ^#?            :~^.                                                 ^#?              
                ^#J                                                                 ^BJ             
                 ^#J                                                                 5G             
                  :BY                                                              .~BG.            
                   ^&~                                                         :~?Y5J!:             
                   ^&~                                                     :!J55J!:                 
                  ^BY                                                 .^7Y5Y?~.                     
                :YG!                                              .~?Y5Y7^.                         
               ?G?.                                           :~?Y5J7^.                             
             .5P:                                         :!J55J!:                                  
             ?#                                      .^7J55?~:                                      
             ~&~                                 .^7Y5Y7^.                                          
              PP.:::.                        :~?Y5Y7^.                                              
              ^5YJJYYYYYJJJ????77777!777??JYYYJ!:                                                   
                     ..::^^^~~~~!!!!!!!!~~^:.                                                                 
                                                     
            """,



            "suzuka": """
    [bold cyan]  Japanese Grand Prix  [/]
    [dim]Suzuka | 5.807 km | 53 Laps[/]

       ^7YPPPPY7:                                                                                   
      ?#@#GPPG&@B7                                                                                  
     :B@&!    ^B@&!                     ~!!^                                                        
      7#@#Y~   ~#@#7                  !G&&&#!                                                       
       :JB@&G?^ ^5&@G?^              7&@BB&@7                                                       
          !5#@&P?~!YB&&GJ!:        :Y&@GP&&Y             ^7?!~JPGGP5J!^                             
            :75B&&B5JYPB&&#G5J???JP#@#J^#&B:           ~5#@&&&&B55PB&@&P!                           
               :~?5B#&##BB#######BG57^ :B&#^        :7G&&G?75GY!^:  :7P@@P!                         
                    ^~?YPB#&&#G5J!^     5@&7      ^JB@#G5PB&&##&&#GY~  !G@&5^                       
                         :^!?YGB&&&#G5?~Y&@J  :^75#@B55#@#57~^^~7JG@&P:  7B@#J:                     
                               :^!?YPB&&&&&B5PB&&#P7?B@&J:         5@@?   :J#@B7                    
                                     :^~?#&&BG5J7^~P@@P^          ^B&&~     ^5&@G!                  
                                         J&@######&@B7            G@&7        !G@&5^                
                                          !JJ????77!:             P@&J^^^^:     ?B@#J:              
                                                                  :5#&&&&&#P7    :J&@B7             
                                                                    :~!777P@&J     ^5&@G!           
                                                                          :B@&~      !G@&5^         
                                                                           !#@#5YJ?~   ?B@#J:       
                                                                            ^JPBB#@&P~  :Y&@B~      
                                                                                 :!B@#?   !&@B:     
                                                                                   ^P@@5: ~&@B:     
                                                                                     J&@BP#@#!      
                                                                                      ~JPGPJ^       
                        
            """,



            "singapore": """
    [bold cyan]  Singapore Grand Prix  [/]
    [dim]Singapore | 4.927 km | 62 Laps[/]

                                                                          :!7~:                     
                                                                         !B&&@BYY?^                 
                                                                        :B@P^75GB&#!                
                                                                        ^&@Y     P@#:               
                                                                         5@#~    7&@?               
                                    ~!~^                                 :P@B~   :B@G               
                                  !G&&##B57^                              :P@B^   Y@&~              
                     !5GPJ~      !&@P^^!YG##GY!:                           :G@G:  ~&@J              
                   :5@@PP&&P!   !#@5      ^75B&#P?~:                        7&@7   G@B:             
                  ^P@#7  ^J#@BY5&@Y          :~JP#&#G5J77!!!!!!!!7777??????7P@&~   ?@&!             
                 ~B@G^                           :~7YPGBBBBBBBBBBBBB####&&##B5!    ^#@Y             
                7&@5:                                   ::::::::::::::::^^::        P@B:            
               J&&?          ?#@G5B&&GJ~                                            !&&7            
             :P@#!          7&@5:  ^?P&&BJ~:::              ::                       P@G            
            ^B@B~          ^#@G:      ^75B#BBBBG?         ~PBBBGGPY?~                Y@&^           
           :G@G^           J@&!           :~!7J@@7::::   ~#@P7?JY5G@&J             ~5&&J            
           ~&@Y           :B@G                 5&&##BBBBB#@B^     :5&&BBBBBBBBBBBGG&&P~             
           :P@&5~         ~&@J                  ~!??JJJJ?7!:        ^!7???????JJYYJ7^               
             !5&&5:       7&&!                                                                      
               ^#@P       J@#:                                                                      
                P@&J^     P@G                                                                       
                :?P&&P7: ^#@5                                                                       
                   ^?G@#55@@7                                                                       
                      !5B#B?     
            """,
        }
        return tracks.get(track_name.lower().replace(" ", ""), None)

    def cmd_map(self, track_name):
        """Displays track layout."""
        if not track_name:
            console.print("[yellow]Engineer:[/ yellow] Which track? Usage: map <name>")
            console.print("[dim]Available: [/]")
            console.print(""" 
                abudhabi
                monza
                silverstone
                spa
                monaco
                mexico
                imola
                interlagos
                sakhir
                baku
                buddh
                barcelona
                montreal
                miami
                qatar
                lasvegas
                suzuka
                singapore
            """)
            return

        # Get the art
        art = self.get_track_ascii(track_name)
        
        if art:
            # Display inside a panel
            console.print(Panel(
                Align.center(art),
                title=f"[bold]{track_name.upper()}[/]",
                border_style="green",
                padding=(1, 2)
            ))
        else:
            console.print(f"[bold red]NO DATA:[/] Track '{track_name}' not in simulation database.")


    def get_prompt(self):
        """Standard prompt string (No HTML/PromptToolkit)."""
        tyre_colors = {"SOFT": "red", "MEDIUM": "yellow", "HARD": "white", "INTER": "green"}
        t_col = tyre_colors.get(self.tyre_compound, "white")
        
        return f"[bold white on black] L{self.lap_count} [/][black on {t_col}] {self.tyre_compound} [/] [bold cyan]{self.user}[/] :: [bold green]{self.current_dir}[/] > "

    def cmd_grid(self, target_path=None):
        """Lists files. Can handle a specific target path."""
        # Determine which folder to look at
        search_dir = self.current_dir
        
        if target_path:
            # Handle quotes if user typed them
            clean_target = target_path.strip('"').strip("'")
            search_dir = os.path.join(self.current_dir, clean_target)

        try:
            files = os.listdir(search_dir)
        except FileNotFoundError:
            console.print(f"[bold red]SECTOR ERROR:[/] '{target_path}' not found on track map.")
            return
        except PermissionError:
            console.print("[bold red]RED FLAG:[/] Access Denied.")
            return

        display_name = os.path.basename(search_dir) or search_dir
        table = Table(title=f"TRACK LIMITS ({display_name})", show_header=True, header_style="bold magenta")
        table.add_column("Pos", style="dim", width=4)
        table.add_column("Driver (File)", min_width=25)
        table.add_column("Type", justify="right")
        table.add_column("Load (Size)", justify="right")

        for idx, file in enumerate(files):
            if idx > 19:
                table.add_row("...", f"+ {len(files) - 20} more", "", "")
                break
            
            full_path = os.path.join(search_dir, file)
            try:
                size = os.path.getsize(full_path)
                ftype = "DIR" if os.path.isdir(full_path) else "FILE"
                style = "bold blue" if ftype == "DIR" else "white"
                
                if size > 1024*1024: size_str = f"{round(size/(1024*1024), 1)} MB"
                elif size > 1024: size_str = f"{round(size/1024, 1)} KB"
                else: size_str = f"{size} B"

                table.add_row(str(idx + 1), file, ftype, size_str, style=style)
            except: continue
        console.print(table)

    def cmd_quote(self):
        """Plays a random famous team radio message."""
        if not hasattr(self, 'quotes'):
             # Fallback if init wasn't updated yet
             console.print("[red]No quotes database found. Please update __init__[/]")
             return

        driver, team, quote = random.choice(self.quotes)
        
        # Color coding based on team
        colors = {
            "Mercedes": "cyan", 
            "Red Bull": "blue", 
            "Ferrari": "red",
            "McLaren": "orange1",  # FIXED: 'keyword' -> 'orange1'
            "Lotus": "gold1", 
            "AlphaTauri": "white",
            "Alpine": "blue_violet",
            "Williams": "blue"
        }
        # Default to green if team not in list
        color = colors.get(team, "green")
        
        # Visual styling
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(style="bold white", width=20)
        grid.add_column(style=f"italic {color}")
        
        grid.add_row(f"{driver.upper()}", f"({team})")
        grid.add_row("", "") # Spacer
        grid.add_row("RADIO:", f'"{quote}"')
        
        console.print(Panel(
            grid,
            title="[bold white]TEAM RADIO TRANSCRIPT[/]",
            border_style=color,
            width=60
        ))

    def cmd_drs(self):
        """Runs a network speed test (DRS Speed Trap)."""
        
        console.print("\n[bold cyan]INITIATING DRS PERFORMANCE TEST...[/]")
        
        st = None
        try:
            # Phase 1: Finding Server (Reaction Time)
            with console.status("[bold yellow]CALIBRATING SENSORS (Finding Server)...[/]", spinner="dots"):
                st = speedtest.Speedtest()
                st.get_best_server()
                ping = st.results.ping
            
            console.print(f"[green]✓ REACTION TIME (Ping):[/] {ping:.1f} ms")

            # Phase 2: Top Speed Run (Download) & ERS (Upload)
            # We use a progress bar to simulate the test running
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=40, style="red", complete_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                
                # Download Test
                task1 = progress.add_task("MEASURING DOWNFORCE (Download)...", total=100)
                
                # We can't get real-time progress from the simple speedtest API easily, 
                # so we run it, but animate a 'fake' progress for the visual feel 
                # or just hold the spinner. For a TUI, a spinner is safer if we can't callback.
                # However, to keep it simple and blocking:
                
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                progress.update(task1, completed=100)
                
                # Upload Test
                task2 = progress.add_task("MEASURING THRUST (Upload)...", total=100)
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                progress.update(task2, completed=100)

            # Phase 3: The Telemetry Board
            console.print("\n")
            grid = Table.grid(expand=True, padding=(0, 2))
            grid.add_column(style="bold white", justify="right")
            grid.add_column(style="bold yellow")
            
            # Visualizing the speed as a 'Gear' or 'Speed'
            # < 50 Mbps = F2 Engine, > 500 Mbps = Rocket Ship
            engine_rating = "TRACTOR"
            if download_speed > 50: engine_rating = "V6 HYBRID"
            if download_speed > 200: engine_rating = "MERCEDES W11"
            if download_speed > 800: engine_rating = "JET ENGINE"

            grid.add_row("DOWNFORCE (Download)", f"{download_speed:.2f} Mbps")
            grid.add_row("THRUST (Upload)", f"{upload_speed:.2f} Mbps")
            grid.add_row("REACTION TIME (Ping)", f"{ping:.1f} ms")
            grid.add_row("POWER UNIT RATING", f"[italic red]{engine_rating}[/]")
            
            console.print(Panel(
                grid,
                title="[bold white]AERODYNAMICS REPORT[/]",
                border_style="magenta",
                width=50
            ))

        except Exception as e:
            console.print(f"[bold red]DRS FAILURE:[/] Could not connect to telemetry server.\n[dim]{e}[/]")

    def cmd_news(self):
        """Fetches latest F1 headlines via RSS."""
        rss_url = "https://news.google.com/rss/search?q=Formula+1+racing&hl=en-US&gl=US&ceid=US:en"
        
        # Show a loading spinner (Pit Crew working)
        with console.status("[bold yellow]ESTABLISHING UPLINK TO PADDOCK...[/]", spinner="dots"):
            try:
                feed = feedparser.parse(rss_url)
                
                if not feed.entries:
                    console.print("[bold red]CONNECTION LOST:[/] No news data received.")
                    return

                # Create the News Table
                table = Table(title="PADDOCK RUMORS & HEADLINES", border_style="bold red")
                table.add_column("Time", style="dim", width=12)
                table.add_column("Headline", style="bold white")
                table.add_column("Source", style="cyan")

                # Limit to top 10 stories to fit the terminal
                for entry in feed.entries[:10]:
                    # Clean up the date (published format usually usually lengthy)
                    try:
                        # Extract simple time if possible, or just ignore format
                        pub_date = entry.published_parsed
                        time_str = f"{pub_date.tm_mon}/{pub_date.tm_mday} {pub_date.tm_hour:02d}:{pub_date.tm_min:02d}"
                    except:
                        time_str = "LIVE"

                    # The source is usually in the title or source tag
                    title = entry.title
                    source = entry.source.get('title', 'Unknown')

                    # Make title clickable in supported terminals
                    headline_link = f"[link={entry.link}]{title}[/link]"
                    
                    table.add_row(time_str, headline_link, source)

                console.print(table)
                console.print("[dim italic]Tip: Click headlines to open in browser (if terminal supports it)[/]")

            except Exception as e:
                console.print(f"[bold red]COMMUNICATION FAILURE:[/] {e}")

    def cmd_champions(self):
        """Hall of Fame."""
        champs = [
            ("2025", "Lando Norris", "McLaren"),
            ("2024", "Max Verstappen", "Red Bull"),
            ("2023", "Max Verstappen", "Red Bull"),
            ("2022", "Max Verstappen", "Red Bull"),
            ("2021", "Max Verstappen", "Red Bull"),
            ("2020", "Lewis Hamilton", "Mercedes"),
            ("2019", "Lewis Hamilton", "Mercedes"),
            ("2018", "Lewis Hamilton", "Mercedes"),
            ("2017", "Lewis Hamilton", "Mercedes"),
            ("2016", "Nico Rosberg", "Mercedes"),
            ("2015", "Lewis Hamilton", "Mercedes"),
            ("2014", "Lewis Hamilton", "Mercedes"),
            ("2013", "Sebastian Vettel", "Red Bull"),
            ("2012", "Sebastian Vettel", "Red Bull"),
            ("2011", "Sebastian Vettel", "Red Bull"),
            ("2010", "Sebastian Vettel", "Red Bull"),
            ("2009", "Jenson Button", "Brawn"),
            ("2008", "Lewis Hamilton", "McLaren"),
            ("2007", "Kimi Raikkonen", "Ferrari"),
            ("2006", "Fernando Alonso", "Renault"),
            ("2005", "Fernando Alonso", "Renault"),
            ("2004", "Michael Schumacher", "Ferrari"),
            ("2003", "Michael Schumacher", "Ferrari"),
            ("2002", "Michael Schumacher", "Ferrari"),
            ("2001", "Michael Schumacher", "Ferrari"),
            ("2000", "Michael Schumacher", "Ferrari"),
            ("1999", "Mika Hakkinen", "McLaren"),
            ("1998", "Mika Hakkinen", "McLaren"),
            ("1997", "Jacques Villeneuve", "Williams"),
            ("1996", "Damon Hill", "Williams"),
            ("1995", "Michael Schumacher", "Benetton"),
            ("1994", "Michael Schumacher", "Benetton"),
            ("1993", "Alain Prost", "Williams"),
            ("1992", "Nigel Mansell", "Williams"),
            ("1991", "Ayrton Senna", "McLaren"),
            ("1990", "Ayrton Senna", "McLaren"),
            ("1989", "Alain Prost", "McLaren"),
            ("1988", "Ayrton Senna", "McLaren"),
            ("1987", "Nelson Piquet", "Williams"),
            ("1986", "Alain Prost", "McLaren"),
            ("1985", "Alain Prost", "McLaren"),
            ("1984", "Niki Lauda", "McLaren"),
            ("1983", "Nelson Piquet", "Brabham"),
            ("1982", "Keke Rosberg", "Williams"),
            ("1981", "Nelson Piquet", "Brabham"),
            ("1980", "Alan Jones", "Williams"),
            ("1979", "Jody Scheckter", "Ferrari"),
            ("1978", "Mario Andretti", "Lotus"),
            ("1977", "Niki Lauda", "Ferrari"),
            ("1976", "James Hunt", "McLaren"),
            ("1975", "Niki Lauda", "Ferrari"),
            ("1974", "Emerson Fittipaldi", "McLaren"),
            ("1973", "Jackie Stewart", "Tyrrell"),
            ("1972", "Emerson Fittipaldi", "Lotus"),
            ("1971", "Jackie Stewart", "Tyrrell"),
            ("1970", "Jochen Rindt", "Lotus"),
            ("1969", "Jackie Stewart", "Matra"),
            ("1968", "Graham Hill", "Lotus"),
            ("1967", "Denny Hulme", "Brabham"),
            ("1966", "Jack Brabham", "Brabham"),
            ("1965", "Jim Clark", "Lotus"),
            ("1964", "John Surtees", "Ferrari"),
            ("1963", "Jim Clark", "Lotus"),
            ("1962", "Graham Hill", "BRM"),
            ("1961", "Phil Hill", "Ferrari"),
            ("1960", "Jack Brabham", "Cooper"),
            ("1959", "Jack Brabham", "Cooper"),
            ("1958", "Mike Hawthorn", "Ferrari"),
            ("1957", "Juan Manuel Fangio", "Maserati"),
            ("1956", "Juan Manuel Fangio", "Ferrari"),
            ("1955", "Juan Manuel Fangio", "Mercedes"),
            ("1954", "Juan Manuel Fangio", "Mercedes"),
            ("1953", "Alberto Ascari", "Ferrari"),
            ("1952", "Alberto Ascari", "Ferrari"),
            ("1951", "Juan Manuel Fangio", "Alfa Romeo"),
            ("1950", "Giuseppe Farina", "Alfa Romeo"),
        ]
        
        table = Table(title="HALL OF FAME (World Drivers' Champions)", border_style="gold1")
        table.add_column("Season", style="bold white", justify="center")
        table.add_column("Driver", style="bold cyan")
        table.add_column("Constructor", style="italic white")
        
        for year, driver, team in champs:
            d_style = "bold cyan"
            if driver in ["Michael Schumacher"]: d_style = "bold magenta"
            elif driver in ["Lewis Hamilton"]: d_style = "bold red"
            elif driver in ["Juan Manuel Fangio"]: d_style = "bold green"
            elif driver in ["Max Verstappen", "Sebastian Vettel", "Ayrton Senna", "Niki Lauda"]: d_style = "bold yellow"  
            table.add_row(year, f"[{d_style}]{driver}[/]", team)

        console.print(table)


    def cmd_telemetry(self):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        
        battery = psutil.sensors_battery()
        fuel_level = battery.percent if battery else 100
        charging = "⚡" if battery and battery.power_plugged else ""
        
        temp_str = "NO SENSOR"
        if hasattr(psutil, "sensors_temperatures"):
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    first_key = next(iter(temps))
                    t = temps[first_key][0].current
                    temp_str = f"{t}°C"
            except: pass

        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(style="bold white")
        grid.add_column(justify="right")
        
        grid.add_row("Engine Map (CPU)", f"{self.make_bar(cpu_usage)} {cpu_usage}%")
        grid.add_row("ERS Store (RAM)", f"{self.make_bar(ram.percent)} {round(ram.used / (1024**3), 1)}GB")
        fuel_color = "green" if fuel_level > 20 else "red blink"
        grid.add_row("Fuel Cell (BAT)", f"[{fuel_color}]{fuel_level}% {charging}[/]")
        grid.add_row("Oil Temp", f"[cyan]{temp_str}[/]")

        panel = Panel(grid, title="[bold italic]VF-24 TELEMETRY[/]", subtitle=f"Chassis: {self.platform_os}", border_style="cyan", width=60)
        console.print(panel)

    def cmd_box(self, target_path):
        if not target_path:
            console.print("[yellow]Engineer:[/ yellow] Usage: box <directory>")
            return
        
        # Strip quotes just in case
        clean_path = target_path.strip('"').strip("'")
        
        if clean_path == "..": new_path = os.path.dirname(self.current_dir)
        else: new_path = os.path.join(self.current_dir, clean_path)

        try:
            os.chdir(new_path)
            self.current_dir = os.getcwd()
            console.print(f"[green]PIT STOP COMPLETE.[/] Joined sector {os.path.basename(self.current_dir)}")
            self.tyre_compound = random.choice(TYRE_STRATEGY)
            console.print(f"[dim italic]Fitted {self.tyre_compound} tyres.[/]")
            
        except FileNotFoundError:
            console.print("[bold red]GRAVEL TRAP![/] Directory not found.")
        except PermissionError:
            console.print("[bold red]BLACK FLAG![/] Permission denied.")

    def run(self):
        self.boot_sequence()
        
        while True:
            try:
                self.lap_count += 1
                
                # Standard Python Input
                user_input = console.input(self.get_prompt())
                
                if not user_input.strip():
                    continue

                # --- MANUAL PARSING FOR ROBUSTNESS ---
                # We strip the command, and take the rest as the raw argument string
                # This perfectly handles spaces: "box My Folder Name" -> "My Folder Name"
                parts = user_input.split(" ", 1)
                command = parts[0].lower()
                arg_string = parts[1] if len(parts) > 1 else None

                # --- COMMANDS ---
                if command in ["flag", "exit", "quit", "q"]:
                    console.print(Panel("[bold white]CHECKERED FLAG[/]\n[dim]P1. Great Drive. Session Ended.[/]", style="bold green"))
                    break
                
                elif command == "clear":
                    console.clear()
                    console.print("[yellow]SAFETY CAR DEPLOYED[/]")
                    
                elif command in ["grid","ls","dir"]: 
                    # Passes the raw argument string (e.g., "Folder Name")
                    self.cmd_grid(arg_string)
                    
                elif command in ["box","cd"]: 
                    self.cmd_box(arg_string)
                    
                elif command == "telemetry": 
                    self.cmd_telemetry()
                    
                elif command == "champions":
                    self.cmd_champions()

                elif command == "map":
                    self.cmd_map(arg_string)

                elif command == "next":
                    self.cmd_next()

                elif command == "news":
                    self.cmd_news()

                elif command == "drs":
                    self.cmd_drs()
                
                elif command == "quote":
                    self.cmd_quote()
                    
                elif command in ["radio","help"]: 
                    console.print(Panel(
                        """
                        [green]grid[/]         - List files (Current or Specific)
                        [green]box <dir>[/]    - Change directory
                        [green]telemetry[/]    - Status
                        [green]champions[/]    - Hall of Fame
                        [green]clear[/]        - Clear Screen
                        [green]flag[/]         - End Session (Exit)
                        [green]map <name>[/]   - Show Track Layout (eg: map monza)
                        [green]next[/]         - Next Race Countdown
                        [green]news[/]         - Latest Paddock Headlines
                        [green]drs[/]          - Network Speed Test
                        [green]quote[/]        - Iconic Radio Messages in F1
                        """,
                        title="RACE ENGINEER", border_style="green"
                    ))
                
                else:
                    # Pass through to system shell
                    console.print(f"[dim]Relaying to Race Control...[/]")
                    try: os.system(user_input)
                    except: console.print("[bold red]MECHANICAL FAILURE[/]")

            except KeyboardInterrupt:
                console.print("\n[bold red]RED FLAG![/] (Type 'flag' to exit)")
            except Exception as e:
                console.print(f"[bold red]CRITICAL FAILURE:[/] {e}")

if __name__ == "__main__":
    os_sim = PitWallOS()
    os_sim.run()