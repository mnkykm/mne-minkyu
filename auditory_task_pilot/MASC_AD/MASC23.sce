## MASC SCENARIO FILE ##

scenario = "MASC";
no_logfile = false;
default_font_size = 32;
response_matching = simple_matching;
active_buttons = 3;
default_background_color = 200,200,255;
default_font = "Arial";

# NOTE: Triggers:
# always a trigger on line 128, then ascends combined w/ other values
# so triggers accend in the following order:
# 129, 130, 132, 136, 144, 160, 192....

# triggers also also sent for:
# left button press: 1
# right button press: 2
# enter button: 3
# onset of question: 8

# send codes to Meglab
write_codes = true;
pulse_width = 5;

begin;

# load up all of the objects:


# set up the fixation cross

text { caption = "+"; font_size = 50; font_color = 0,0,0; background_color = 200,200,255; } asterisk;
text { caption = "+"; font_size = 50; font_color = 255,0,0; background_color = 200,200,255; } asterisk_red;
text { caption = "?"; font_size = 40; } question;
text { caption = " "; font_size = 40; } blank;

# and load up the sound files
wavefile {filename = "/easy_money_0.wav" ;}EM0;
wavefile {filename = "/easy_money_1.wav" ;}EM1;
wavefile {filename = "/easy_money_2.wav" ;}EM2;
wavefile {filename = "/easy_money_3.wav" ;}EM3;
wavefile {filename = "/easy_money_4.wav" ;}EM4;
wavefile {filename = "/easy_money_5.wav" ;}EM5;
wavefile {filename = "/easy_money_6.wav" ;}EM6;
wavefile {filename = "/easy_money_7.wav" ;}EM7;

wavefile {filename = "/lw1_0.wav" ;}LW0;
wavefile {filename = "/lw1_1.wav" ;}LW1;
wavefile {filename = "/lw1_2.wav" ;}LW2;
wavefile {filename = "/lw1_3.wav" ;}LW3;

wavefile {filename = "/cable_spool_fort_0.wav" ;}CSF0;
wavefile {filename = "/cable_spool_fort_1.wav" ;}CSF1;
wavefile {filename = "/cable_spool_fort_2.wav" ;}CSF2;
wavefile {filename = "/cable_spool_fort_3.wav" ;}CSF3;
wavefile {filename = "/cable_spool_fort_4.wav" ;}CSF4;
wavefile {filename = "/cable_spool_fort_5.wav" ;}CSF5;

wavefile {filename = "/The_Black_Willow_0.wav" ;}TBW0;
wavefile {filename = "/The_Black_Willow_1.wav" ;}TBW1;
wavefile {filename = "/The_Black_Willow_2.wav" ;}TBW2;
wavefile {filename = "/The_Black_Willow_3.wav" ;}TBW3;
wavefile {filename = "/The_Black_Willow_4.wav" ;}TBW4;
wavefile {filename = "/The_Black_Willow_5.wav" ;}TBW5;
wavefile {filename = "/The_Black_Willow_6.wav" ;}TBW6;
wavefile {filename = "/The_Black_Willow_7.wav" ;}TBW7;
wavefile {filename = "/The_Black_Willow_8.wav" ;}TBW8;
wavefile {filename = "/The_Black_Willow_9.wav" ;}TBW9;
wavefile {filename = "/The_Black_Willow_10.wav" ;}TBW10;
wavefile {filename = "/The_Black_Willow_11.wav" ;}TBW11;

wavefile {filename = "/intro0_samantha.wav" ;}intro0;
wavefile {filename = "/intro1_allison.wav" ;}intro1;
wavefile {filename = "/intro2_ava.wav" ;}intro2;


text { caption = "Please lay still.
We are setting up the recording for the next narrative."; font_size = 20; } nextNarrative_text;

picture {
   background_color = 200,200,255;

   text nextNarrative_text;
   x = 0; y = 100;

} next_narrative;


trial {
    trial_duration = 1000;
	 stimulus_event {

picture {
        text asterisk_red;
		  x = 0; y = 0;
    };

	time = 0;

};
} wrong_feedback;


# play synthesised voice intro
TEMPLATE "Intro.tem" {
soundName;
intro0;
intro1;
intro2;
};





# set up the instructions and information to be provided to subject #

text { caption = "Welcome to our experiment!

Please lay still while we set up the recording."; font_size = 20; } welcome_text;

picture {
   background_color = 200,200,255;

   text welcome_text;
   x = 0; y = 100;

} welcome_pic;


trial {
   trial_type = specific_response;
	terminator_button = 3;
   trial_duration = forever;

   picture welcome_pic;

};




#### ---- TBW ---- ####


# SUMMARY
text { caption = "
The Black Willow Summary:
=========================

Allan is a writer. At least, he wants to be. The story follows
his struggle in writing an interesting novel, while gaining
somewhat contradictory feedback from his two friends, Arthur
and Nathan."; font_size = 20; } BW0_summary;
picture {
   background_color = 200,200,255;
   text BW0_summary;
   x = 0; y = 100;
} BW0_summary_pic;
trial {
   trial_type = first_response;
   trial_duration = forever;
   picture BW0_summary_pic;
	time = 0;
};
# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW0	3	144	;
};
#QUESTION
text { caption = "
What was Allan writing?

A poem               A story"; font_size = 20; } TBW0_q;
picture {
   background_color = 200,200,255;
   text TBW0_q;
   x = 0; y = 100;
} TBW0_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW0_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};


# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW1	3	160	;
};
#QUESTION
text { caption = "
Who did the man leave with?

A woman               His son"; font_size = 20; } TBW1_q;
picture {
   background_color = 200,200,255;
   text TBW1_q;
   x = 0; y = 100;
} TBW1_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW1_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW2	3	192	;
};
#QUESTION
text { caption = "
What was Allan eating while he spoke?

A sandwich               A cake"; font_size = 20; } TBW2_q;
picture {
   background_color = 200,200,255;
   text TBW2_q;
   x = 0; y = 100;
} TBW2_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW2_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW3	3	129	;
};
#QUESTION
text { caption = "
The problem with Allan's stories was that they are too?

Happy               Morbid"; font_size = 20; } TBW3_q;
picture {
   background_color = 200,200,255;
   text TBW3_q;
   x = 0; y = 100;
} TBW3_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW3_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW4	3	130	;
};
#QUESTION
text { caption = "
Nathan was sat on a what?

Tree               Bench"; font_size = 20; } TBW4_q;
picture {
   background_color = 200,200,255;
   text TBW4_q;
   x = 0; y = 100;
} TBW4_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW4_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW5	3	132	;
};
#QUESTION
text { caption = "
Does Nathan think the stories are worth publishing?

No               Yes"; font_size = 20; } TBW5_q;
picture {
   background_color = 200,200,255;
   text TBW5_q;
   x = 0; y = 100;
} TBW5_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW5_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW6	3	136	;
};
#QUESTION
text { caption = "
Allan writes because it makes him?

Happy               Money"; font_size = 20; } TBW6_q;
picture {
   background_color = 200,200,255;
   text TBW6_q;
   x = 0; y = 100;
} TBW6_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW6_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW7	3	144	;
};
#QUESTION
text { caption = "
What does Allan blame for his Morbid story telling?

Willow               Raven"; font_size = 20; } TBW7_q;
picture {
   background_color = 200,200,255;
   text TBW7_q;
   x = 0; y = 100;
} TBW7_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW7_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW8	3	160	;
};
#QUESTION
text { caption = "
Who does Arthur tell Allan to talk to?

Mr. Clemm               Nathan"; font_size = 20; } TBW8_q;
picture {
   background_color = 200,200,255;
   text TBW8_q;
   x = 0; y = 100;
} TBW8_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW8_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW9	3	192	;
};
#QUESTION
text { caption = "
What does Allan see on his way home?

Fruit               Smoke"; font_size = 20; } TBW9_q;
picture {
   background_color = 200,200,255;
   text TBW9_q;
   x = 0; y = 100;
} TBW9_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW9_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW10	3	129	;
};
#QUESTION
text { caption = "
What had Arthur burned?

The tree               The house"; font_size = 20; } TBW10_q;
picture {
   background_color = 200,200,255;
   text TBW10_q;
   x = 0; y = 100;
} TBW10_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW10_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
TBW11	3	130	;
};
#QUESTION
text { caption = "
Allan walked into the woods and found what?

Willows               Streams"; font_size = 20; } TBW11_q;
picture {
   background_color = 200,200,255;
   text TBW11_q;
   x = 0; y = 100;
} TBW11_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture TBW11_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};



trial {
   trial_type = specific_response;
	terminator_button = 3;
	trial_duration = forever;

   picture next_narrative;
	time = 0;

};


#### ---- CSF ---- ####


# SUMMARY
text { caption = "
Cable Spool Fort Summary:
=========================

Two young brothers, Chad 6 years old and Roy 8 years old,
are playing together. Surprisingly, the younger brother Chad
makes all of the decisions, and is clearly the leader of the 
brotherhood. Indeed, since his brother Roy got brain surgery
after a terrible accident, Roy is slow and passive. His
handicap leads his friends to martyr him, sometimes up to a
dangerous point."; font_size = 20; } CSF0_summary;
picture {
   background_color = 200,200,255;
   text CSF0_summary;
   x = 0; y = 100;
} CSF0_summary_pic;
trial {
   trial_type = first_response;
   trial_duration = forever;
   picture CSF0_summary_pic;
	time = 0;
};
# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF0	1	144	;
};
#QUESTION
text { caption = "
Roy started acting differently since his?

Fall               8th Birthday"; font_size = 20; } CSF0_q;
picture {
   background_color = 200,200,255;
   text CSF0_q;
   x = 0; y = 100;
} CSF0_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF0_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF1	1	160	;
};
#QUESTION
text { caption = "
What month was it?

June               August"; font_size = 20; } CSF1_q;
picture {
   background_color = 200,200,255;
   text CSF1_q;
   x = 0; y = 100;
} CSF1_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF1_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF2	1	192	;
};
#QUESTION
text { caption = "
What did Chad call Roy?

Robot Boy               Remote Control Boy"; font_size = 20; } CSF2_q;
picture {
   background_color = 200,200,255;
   text CSF2_q;
   x = 0; y = 100;
} CSF2_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF2_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF3	1	129	;
};
#QUESTION
text { caption = "
What was Chad trying to keep the boys away from?

Flag               Treehouse"; font_size = 20; } CSF3_q;
picture {
   background_color = 200,200,255;
   text CSF3_q;
   x = 0; y = 100;
} CSF3_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF3_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF4	1	130	;
};
#QUESTION
text { caption = "
Where did the sharp rock hit Tucker?

Nose               Forehead"; font_size = 20; } CSF4_q;
picture {
   background_color = 200,200,255;
   text CSF4_q;
   x = 0; y = 100;
} CSF4_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF4_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
CSF5	1	132	;
};
#QUESTION
text { caption = "
What was Tucker doing?

Shouting               Crying"; font_size = 20; } CSF5_q;
picture {
   background_color = 200,200,255;
   text CSF5_q;
   x = 0; y = 100;
} CSF5_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture CSF5_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};


trial {
   trial_type = specific_response;
	terminator_button = 3;
	trial_duration = forever;

   picture next_narrative;
	time = 0;

};



#### ----- LW1 ----- #######


# SUMMARY
text { caption = "
LW1 Summary:
============

This is the first chapter of a science-fiction novel. A captain is
leading her spaceship to identify planets with life in order to save
the so-called Arallins species.
"; font_size = 20; } lw0_summary;
picture {
   background_color = 200,200,255;
   text lw0_summary;
   x = 0; y = 100;
} lw0_summary_pic;
trial {
   trial_type = first_response;
   trial_duration = forever;
   picture lw0_summary_pic;
	time = 0;
};
# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
LW0	0	129	;
};
#QUESTION
text { caption = "
What have the space explorers found?

Minerals               New Planet"; font_size = 20; } lw0_q;
picture {
   background_color = 200,200,255;
   text lw0_q;
   x = 0; y = 100;
} lw0_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture lw0_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;

};


# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
LW1	0	130	;
};
#QUESTION
text { caption = "
Who is the commander of the ship?

Tara               Harmon"; font_size = 20; } lw1_q;
picture {
   background_color = 200,200,255;
   text lw1_q;
   x = 0; y = 100;
} lw1_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture lw1_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
LW2	0	132	;
};
#QUESTION
text { caption = "
Rakal is what colour?

Yellow               Black"; font_size = 20; } lw2_q;
picture {
   background_color = 200,200,255;
   text lw2_q;
   x = 0; y = 100;
} lw2_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture lw2_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
LW3	0	136	;
};
#QUESTION
text { caption = "
How many previous attempts have been unsuccessful?

32               27"; font_size = 20; } lw3_q;
picture {
   background_color = 200,200,255;
   text lw3_q;
   x = 0; y = 100;
} lw3_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture lw3_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

trial {
   trial_type = specific_response;
	terminator_button = 3;
	trial_duration = forever;

   picture next_narrative;
	time = 0;

};


#### ---- EM ---- ####


# SUMMARY
text { caption = "
Easy Money Summary:
=========================

The narrator, Ed, gets contacted by an old friend from high-school:
Charles Acre. Charles has a secret that could make the two men
exremely rich... he has found a way to tele-transport himself
anywhere he wants. But this extraordinary ability entails
life-threatening risks."; font_size = 20; } EM0_summary;
picture {
   background_color = 200,200,255;
   text EM0_summary;
   x = 0; y = 100;
} EM0_summary_pic;
trial {
   trial_type = first_response;
   trial_duration = forever;
   picture EM0_summary_pic;
	time = 0;
};
# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM0	2	136	;
};
#QUESTION
text { caption = "
Where did Ed and Charles meet?

Cafe               Diner"; font_size = 20; } EM0_q;
picture {
   background_color = 200,200,255;
   text EM0_q;
   x = 0; y = 100;
} EM0_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM0_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM1	2	144	;
};
#QUESTION
text { caption = "
What is Charles asking help for?

Stealing               Selling"; font_size = 20; } EM1_q;
picture {
   background_color = 200,200,255;
   text EM1_q;
   x = 0; y = 100;
} EM1_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM1_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};

# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM2	2	160	;
};
#QUESTION
text { caption = "
Where was the stone tablet from?

Easter Island               Cuba"; font_size = 20; } EM2_q;
picture {
   background_color = 200,200,255;
   text EM2_q;
   x = 0; y = 100;
} EM2_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM2_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};


# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM3	2	192	;
};
#QUESTION
text { caption = "
What weapon did Ed take?

Gun               Knife"; font_size = 20; } EM3_q;
picture {
   background_color = 200,200,255;
   text EM3_q;
   x = 0; y = 100;
} EM3_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM3_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};


# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM4	2	129	;
};
#QUESTION
text { caption = "
What is the device?

Metal Gadget               Gestures"; font_size = 20; } EM4_q;
picture {
   background_color = 200,200,255;
   text EM4_q;
   x = 0; y = 100;
} EM4_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM4_q_pic;
	target_button = 2;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM5	2	130	;
};
#QUESTION
text { caption = "
What was the big statue wearing?

Hat               Scarf"; font_size = 20; } EM5_q;
picture {
   background_color = 200,200,255;
   text EM5_q;
   x = 0; y = 100;
} EM5_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM5_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};



# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM6	2	132	;
};
#QUESTION
text { caption = "
Where was the vault?

Fort Knox               Federal Bank"; font_size = 20; } EM6_q;
picture {
   background_color = 200,200,255;
   text EM6_q;
   x = 0; y = 100;
} EM6_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM6_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# SOUND
TEMPLATE "MASC.tem" {
soundName	block	trigger	;
EM7	2	136	;
};
#QUESTION
text { caption = "
What had Ed left on Charles?

His keys               His wallet"; font_size = 20; } EM7_q;
picture {
   background_color = 200,200,255;
   text EM7_q;
   x = 0; y = 100;
} EM7_q_pic;
trial {
   trial_type = first_response;
	incorrect_feedback = wrong_feedback;
   trial_duration = forever;
   picture EM7_q_pic;
	target_button = 1;
	time = 1000;
	port_code = 8;
};




# experiment over.

text { caption = "The experiment is now over.

Thank you for your participation!

Please lay still while we save the recording."; font_size = 20; } theEnd_text;

picture {
   background_color = 200,200,255;

   text theEnd_text;
   x = 0; y = 100;

} theEnd_pic;


trial {
   trial_type = specific_response;
	terminator_button = 3;
   trial_duration = forever;

   picture theEnd_pic;

};

