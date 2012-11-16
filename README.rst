###############################################################
Gothcal - A calendar generator for Gothic Events near Karlsruhe
###############################################################

I was tired of checking the websites of many clubs every time I wanted to know
where the next gothic parties in my area are. Usually, you miss a nice party
because you forget to check for a non-regular party, or simply because you mix
up the dates during checking it.

Because adding events to your calendar by hand is not an option (*srsly*, who is
not to lazy to do this?!), an automated method was required.

Obviously, Python is the perfect choise for this. The current impelementation
of Gothcal creates a single iCalendar from the dates gathered on several club
websites. To match the code quality of the data sources, the parsers I have
written so far are quite hacky, but *IMO* parsing HTML is **always** hacky.

A long distance feature would be adding CherryPy support and a database, so you
can get a nice history and more importantly may choose online which clubs and
events to include into your calendar. That way it could be more interessting
for friends to manage their club time with it, too. But that is far, far from
realisation, as it would require maintenance. And maintenance requires time.