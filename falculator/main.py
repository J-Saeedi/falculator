import csv
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from math import sqrt

class FalculatorData():
    def __init__(self, data_path, has_header=True):
        self.file_name = data_path
        self.P_data = []
        self.Q_data = []
        self.data_count = 0
        self.has_header = has_header

        # read data to memory
        self.read_data()


    def read_data(self):
        with open(self.file_name, 'r') as filereader:
            csvreader = csv.reader(filereader)
            self.header = []
            if self.has_header:
                self.header = next(csvreader)
            for this_row in csvreader:
                self.Q_data.append(float(this_row[0]))
                self.P_data.append(float(this_row[1]))
                self.data_count += 1
            print("NOTICE", self.data_count, "rows has been loaded successfully!")
                
            

class FalculatorPlot():
    def __init__(self, title="Falculator!"):
        self.fig = plt.figure(title)
        self.ax = self.fig.add_subplot(1,1,1)
        self.call_id = self.fig.canvas.mpl_connect("button_press_event", self.onclick)
        self.clear_guide_lines()

    def draw_plot(self,x_data, y_data, current_rpm):
        self.x_data = x_data
        self.y_data = y_data
        self.current_rpm = current_rpm
        self.plot = self.ax.plot(self.x_data,self.y_data)

        self.ax.set_xscale('log')
        self.ax.set_yscale('log')

        self.x_range = 0.7*float(min(self.x_data)), 1.3*float(max(self.x_data))
        self.y_range = 0.9*float(min(self.y_data)), 2.5*float(max(self.y_data))

        self.ax.set_xlim(*self.x_range)
        self.ax.set_ylim(*self.y_range)

    
    def show(self):
        self.fig.show()
        
    def clear_guide_lines(self):
        if not hasattr(self, 'guide_lines'):
            # ^ check guide lines exist or not
            #print('no guide')
            # let`s create one!
            self.guide_lines = []    
        else:
            #print('you have guide')
            for this_guide in self.guide_lines:
                #print(this_guide[0])
                this_guide[0].remove()
            self.fig.canvas.draw()
            self.guide_lines = []
            

        

    # click handler
    def onclick(self, event):
        x,y = event.xdata, event.ydata      
        self.clear_guide_lines() # clear old guides


        #------------this part only used for finding intersecing point-------------------------------------
        first_line = LineString(zip(self.x_data,self.y_data))
        second_line = LineString(zip([x,x], [0,y]))
        intersection = first_line.intersection(second_line)
        if intersection.geom_type=='Point':
            clicked_rpm = sqrt(y/intersection.xy[1])*self.current_rpm
            self.guide_lines.append(self.ax.plot(*intersection.xy,'.', color='green', markersize=5))
            # ^ intersecting point

            rpm_ratio = clicked_rpm/self.current_rpm
            print(rpm_ratio)
            new_Q = [x*rpm_ratio for x in self.x_data]
            new_P = [x*rpm_ratio*rpm_ratio for x in self.y_data]
            #self.guide_lines.append(self.ax.plot(new_Q, new_P)) #, linewidth=1, linestyle=':', color='gray'))
            self.guide_lines.append(self.ax.plot(new_Q, new_P, linewidth=1, linestyle=':', color='gray'))
        else:
            clicked_rpm=-1
        #--------------------------------------------------------------------------------------------------
            

        self.guide_lines.append(self.ax.plot([x,x], [0,y], linestyle='--', color='gray', linewidth=1))
        # ^ vertical guide line
        
        
        self.guide_lines.append(self.ax.plot(x,y,'.', color='red', markersize=23))
        # ^ just point

 
        print('current rpm at clickd pos. =', clicked_rpm)
        self.ax.set_title(f'rpm at red point: {clicked_rpm:0.1f}')
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        
        




# defenitions
file_name = "../data/TDF22.csv"

TDF22_300RPM = FalculatorData(file_name)
testing_plot = FalculatorPlot()
testing_plot.draw_plot(TDF22_300RPM.Q_data, TDF22_300RPM.P_data, 300)
testing_plot.show()

