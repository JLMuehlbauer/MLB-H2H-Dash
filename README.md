# MLB-H2H-Dash ⚾
--- 
## Background:
As an avid baseball fan and someone who's been very interested in data visualization, I've wanted to merge these passions. 

## Description:
This script creates a locally hosted HTML dashboard that displays a handful of popular stats from 2 user selected teams. The script also allows you to independently select the year for each team. The stats that this dashboard displays include the "batting average", "on base percentage", "slugging percentage", "runs scored", "ERA", "WHIP", "K/BB", and "runs allowed". 6 of the 8 subplots are bubble plots where each bubble is a player on the one of the selected teams and the size of the bubble is scaled by ABs and IPs for batters and pitchers respectively. The pitcher-based stats also break out the bubbles into 2 colors which correspond to starting pitchers (SP) and non-starting pitchers (RP).

## How:
This script uses the Python libraries "Dash" and "Plotly" to create the HTML dashboard. The dashboard has 4 user adjustable components which include 2 Dropdown menus to select the desired teams and 2 Input menus to select the desired years (see image below)
![image](https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/e2eaafaa-4ec2-49cf-b3bd-3ae67478eea8)

The script takes the user inputs and calls a function that utilizes the "BeautifulSoup" library to scrape data from baseball-reference team/year pages. This data is formatted into a "Pandas" dataframe that is then used to update the HTML figure. The image below shows the data between the 2023 LA Dodgers and the 2023 Atlanta Braves.

![image](https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/b651d6b4-ddcb-471c-b242-7c9480ab8e31)



## Notes:
- This script updates very slowly. This is most likely a result of the slow webscraping step. The sports-reference API would be a much cleaner method of grabbing data for this dashboard, however, during testing I was not able to get this module to work. It's possible that it is out of date, so instead, I opted for the scraping method which also gave me the opportunity to learn.
- There is some cleaning that I implemented such that all the plots are informative. All players with less than 30 PAs and 10 IPs were dropped from this data. This mean that the Run bar plots are not truly accurate. That said, I put more emphasis on displaying the data from the players that were usual contributors.
- The bubble plots may be an odd choice, but I think with some practice the user can identify many key insights on how well the team is performing and which individuals are giving the most production. This is especially true with the hovertext info and the interactiveness of the plotly plots. Here is an example of of an interepretation one can make:

### Interpretation:
![image](https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/b1c2eca6-df1a-4e87-991c-f0eb0fd3ca2d)

- The Braves have counted on steady and robust performances by 3 starting pitchers (seen by the 3 large blue bubbles in the high 3 ERAs). These pitchers are pitching many innings to a low ERA. On the flip side, the Dodgers starting picthers have struggled with staying on the field (seen by the smaller diameter bubbles) and many of them have had weak performances (seen the blue bubbles at higher ERAs and WHIPs).
- The Dodgers have made up for the shortfall in their starting pitchers with half a dozen relief pitchers (and possibly non-listed starters). These pitchers have given many innings with and ERA around 3 or lower. The Braves have not had very reliable relief pitchers, many of them are performing about as well as their starters.
- In a 5-7 game match up between the Dodgers and Braves, we should assume that the Braves will have the edge with their starting pitchers, however, the Dodger should make back some ground with their top performing relief pitchers.

This interpetation takes a little longer that plots that might display more aggregated data but I think it lends itself to interesting findings.


## Next Steps:
- It would be valuable to add horizontal lines on all the plots with the league averages and +/-1 stdevs. This would help the user determine if a team truly excels in a given category. 
- The time of updating this dashboard could be greatly improved.

---

Thanks for reading. Please feel free to give insights and thoughts about what I've done here.

**Author: Jackson Muehlbauer**

**Contact: jlmuehlbauer@gmail.com**

**Date : 09/23/2023**
  

