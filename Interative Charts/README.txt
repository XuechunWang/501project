{\rtf1\ansi\ansicpg1252\cocoartf1671\cocoasubrtf100
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww13360\viewh16000\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 README.txt\
cleaned_data.csv: cleaned data used to create visualizations\
\
treemap - interactive.py: plots tree map of movie gross of 1987, 1997, 2007, 2017.\
4 output tree maps:\
squarify-treemap-interactive-1.png, squarify-treemap-interactive-2.png, \
squarify-treemap-interactive-3.png, squarify-treemap-interactive-4.png \
1 html: squarify-treemap-interactive.html\
\
slider - interactive.py: plots bubble chart of movie rating as x-axis, movie runtime as y-axis,\
			   movie gross as the size of bubble, movie year as the slider and \
			   movie genre as the color of the bubble. It should run in the Jupyter \
			   notebook in order to see the output animation. This python script will \
			   not show the animation but runs well.\
Slider.ipynb: the slider Jupyter notebook that runs and directly outputs the animation.\
Slider.html: Jupyter notebook in the html format\
Slider Screen Recording: The video of the animation.\
\
valence line chart - interactive.py: selects four Harry Potter movies and plot the valence, the level of \
					positiveness or negativeness of a track, change\
					 in the order of the soundtracks in the album (which happen \
					to follow the order of when they are used in the movie, thus \
					a good indicator of movie plots). The name of the track could \
					serve as a short summary of the plot of the whole story.\
4 output valence line charts: valence line interactive-1.png, valence line interactive-2.png,\
				 valence line interactive-3.png, valence line interactive-4.png\
1 html: valence line interactive.html\
\
radar chart- interactive.py: plots radar chart comparing two sound tracks\'92 six musical attributes \
				in a single movie based on users\'92 choice. It\'92s actually an Dash app \
				supported by poorly. The code running result is a domain where the \
				result is showed. Must open the domain manually and then select \
				anything you want.\
1 output example: radar chart.png\
 \
\
movie genre network - interactive.py: plots a giant network where movies and genres are nodes and \
					      the edges represents \'91belong to\'92. Note a movie may have more\
					      than one genres. The size of the nodes represents the degrees.\
					      Allow for selected different color scale for both nodes and edges.\
\
1 output graph: movie genre network - interactive.png\
1 html: movie genre network - interactive.html\
\
horizontal bar.py: plots grouped bar chart of genre counts across 10-year gap of 1987, 1997, 2007, 2017\
1 output graph: Horizontal Group Bar.png\
1 html: Horizontal Group Bar.html\
\
\
\
}