# Chess
My Chess Game. Made with Pygame it can be played with another person or a Chess bot powered by powerful algorithms and data.

About:
this chess game has 3 files 
Engine: the engine includes the board, rules, and moves a player can make including the bot
SmartMoveFinder: This is the AI bot that knows the best moves from board position, piece value and Current game state
Main: this runs the code checks for input and has all the UI

About BOT:
this bot is smart i have mapped each spot on the board and given it a value based on how good I think it is,
then I gave every piece a value based on how valuable it is, Then I have the game state this tells the bot 
what the board looks like its moves and its pieces under attack so it has all the knowledge it needs to make a move

This BOT uses Algiorithims Like MinMax recursion NegaMax Alphabeta Pruning, and Dictionaries to effectively Pick a move 
it will scan the board and look at every single move and every single state the board can be in as well as all the opponent moves. 
During each of those recursions, it will use its knowledge of the board and pieces to choose the highest value move.

One thing that makes this BOT fast and efficient is alpha-beta pruning. I said earlier the bot looks at every move and game state 
But what if there is a game state or move that has the highest value For Ex what if one move is to kill the queen with a pawn or kill a pawn with a pawn
the bot knows from the value of pieces the queen is the best thing it can get then why even bother searching for more moves and more game states
it already has the best move so the recursion stops and takes that move. 

If you want to play this download the folder and run the main file.
I will be uploading an EXE online soon. 
