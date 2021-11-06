import csv
import os

def formatAllData(datapath,outpath):

    columns = ["Year","assist_percentage","assists","block_percentage","blocks","box_plus_minus","conference","defensive_box_plus_minus","defensive_rebound_percentage","defensive_rebounds","defensive_win_shares","effective_field_goal_percentage","field_goal_attempts","field_goal_percentage","field_goals","free_throw_attempt_rate","free_throw_attempts","free_throw_percentage","free_throws","games_played","games_started","height","minutes_played","offensive_box_plus_minus","offensive_rebound_percentage","offensive_rebounds","offensive_win_shares","personal_fouls","player_efficiency_rating","player_id","points","points_produced","position","steal_percentage","steals","team_abbreviation","three_point_attempt_rate","three_point_attempts","three_point_percentage","three_pointers","total_rebound_percentage","total_rebounds","true_shooting_percentage","turnover_percentage","turnovers","two_point_attempts","two_point_percentage","two_pointers","usage_percentage","weight","win_shares","win_shares_per_40_minutes"]

    strings = ["Year","conference","height","position","team_abbreviation","player_id"]

    floats = ["assist_percentage","block_percentage","box_plus_minus","defensive_win_shares","defensive_box_plus_minus", "defensive_rebound_percentage","effective_field_goal_percentage","free_throw_attempt_rate","free_throw_percentage",   "minutes_played","offensive_rebound_percentage","offensive_win_shares","field_goal_percentage", "player_efficiency_rating","three_point_attempt_rate","total_rebound_percentage","true_shooting_percentage",   "offensive_box_plus_minus","steal_percentage","usage_percentage","turnover_percentage","two_point_percentage","weight","win_shares","win_shares_per_40_minutes","three_point_percentage"]

    ints = ["assists","blocks","defensive_rebounds","field_goal_attempts","field_goals","free_throw_attempts","free_throws","games_played","games_started","offensive_rebounds","personal_fouls","points","points_produced","total_rebounds","three_point_attempts","two_pointers","steals","three_pointers","turnovers","two_point_attempts"]

    with open(datapath,"r") as csv_file, open(outpath,"w") as outfile:
        csv_reader = csv.reader(csv_file,delimiter=",")
        writer = csv.writer(outfile)
        header = 0
        for row in csv_reader:
            if header == 0:
                writer.writerow(row)
                header += 1
                continue
            idx = 0
            toWrite = True
            for col in row:
                formattedCol = col.strip().replace("'","")
                try:
                    colName = columns[idx]
                    #print(colName + " " + formattedCol)
                except IndexError:
                    continue
                if colName in ints:
                    try:
                        formattedCol = int(formattedCol)
                        row[idx] = formattedCol
                    except ValueError:
                        row[idx] = None
                elif colName in floats:
                    try:
                        formattedCol = float(formattedCol)
                        row[idx] = formattedCol
                    except ValueError:
                        row[idx] = None
                idx += 1
            if toWrite:
                writer.writerow(row)
                
if __name__ == "__main__":
    datapath = "/home/zaleskig8/dataWarehousing/basketball/getCBB/playerCSVs/"
    outpath = "/home/zaleskig8/dataWarehousing/basketball/getCBB/cleanCSVs/"
    for cc in os.listdir(datapath):
        print(cc)
        csvpath = datapath + cc
        writepath = outpath + cc
        formatAllData(csvpath,writepath)
