currenttemp = 3

cold = 0
warm = 10

# The purpose of temp_colour is to return a RGB colour which best represents the temp. Ideally this would use s
# See: http://en.wikipedia.org/wiki/Color_temperature AND http://en.wikipedia.org/wiki/CIE_1960_color_space

def colour_limit(colour):
    return ( 0 if colour < 0 else ( 255 if colour > 255 else colour))

def temp_colour(temp):
    colourratio = (float(temp - cold) / float(warm - cold)) # returns ratio as float between cold and warm
    #print colourratio
    red = colour_limit(int(255 * (colourratio)*2))
    blue = colour_limit(int(255 * (0.7 - colourratio)*2))
    green = colour_limit(int((1-((4*colourratio**2)-4*colourratio+1))*255))
    return str(red) + "," + str(green) + "," + str(blue)

print '<table width="400" align="center">'
print '<tbody>'
print '<tr>'
print '<th>Count Down/RGB</th>'
print '<th>Background Color: RGB</th>'
print '</tr>'

x = 0
while x < 10:
    colour = temp_colour(x)
    print '<tr>'
    print '<td align="left">', str(x), ' | ', colour, '</td>'
    print '<td style="background: rgb(', colour, ');" align="center">', colour,'</td>'
    print '</tr>'
    x += 0.1

print '</tbody>'
print '</table>'