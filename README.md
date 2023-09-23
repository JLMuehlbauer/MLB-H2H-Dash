# MLB-H2H-Dash ⚾
--- 
## Background:
As an avid baseball fan and someone who's been very interested in data visualization, I've wanted to merge these passions. 

## Description:
This script creates a locally hosted HTML dashboard that displays a handful of popular stats from 2 user selected teams. The script also allows you to independently select the year for each team. The stats that this dashboard displays include the "batting average", "on base percentage", "slugging percentage", "runs scored", "ERA", "WHIP", "K/BB", and "runs allowed". 6 of the 8 subplots are bubble plots where each bubble is a player on the one of the selected teams and the size of the bubble is scaled by ABs and IPs for batters and pitchers respectively. The pitcher-based stats also break out the bubbles into 2 colors which correspond to starting pitchers (SP) and non-starting pitchers (RP).

## How:
This script uses the Python libraries "Dash" and "Plotly" to create the HTML dashboard. The dashboard has 4 user adjustable components which include 2 Dropdown menus to select the desired teams and 2 Input menus to select the desired years (see image below)
<img width="1433" alt="Screenshot 2023-09-23 at 4 53 29 PM" src="https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/2dd2db2f-8713-4bfc-8a3f-508984ae0714">


The script takes the user inputs and calls a function that utilizes the "BeautifulSoup" library to scrape data from baseball-reference team/year pages. This data is formatted into a "Pandas" dataframe that is then used to update the HTML figure. The image below shows the data between the 2023 LA Dodgers and the 2023 Atlanta Braves.

![newplot (4)](https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/37658636-c5cf-4ae3-aed2-40d733369f29)



## Running on Your Machine:
1. Download this repo to your machine.
2. Make sure that you have Anaconda or Miniconda installed on your machine
3. Use the .yaml file to create a virtual environment that has the required packages. This can be done by using the "Import" function in the "Environments" tab in the Anaconda Navigator. *Note: This has many extraneous packages that are not needed for this script. Feel free to individually install these packages.*
4. Make sure to activate the environment before running this script, this can be done using the anaconda prompt and running the script straight from the prompt.
5. Run the script and wait. It should open in the Web browser, otherwise copy and paste "http://localhost:8050/" into your browser. 

## Notes:
- This script updates very slowly. This is most likely a result of the slow webscraping step. The sports-reference API would be a much cleaner method of grabbing data for this dashboard, however, during testing I was not able to get this module to work. It's possible that it is out of date, so instead, I opted for the scraping method which also gave me the opportunity to learn.
- There is some cleaning that I implemented such that all the plots are informative. All players with less than 30 PAs and 10 IPs were dropped from this data. This mean that the Run bar plots are not truly accurate. That said, I put more emphasis on displaying the data from the players that were usual contributors.
- The bubble plots may be an odd choice, but I think with some practice the user can identify many key insights on how well the team is performing and which individuals are giving the most production. This is especially true with the hovertext info and the interactiveness of the plotly plots. Here is an example of of an interepretation one can make:

### Interpretation:
<img width="593" alt="Screenshot 2023-09-23 at 5 25 27 PM" src="https://github.com/JLMuehlbauer/MLB-H2H-Dash/assets/115378901/7d7fc22c-4940-4b38-aecb-9e6de0d0122f">

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
  

